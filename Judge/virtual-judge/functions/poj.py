import requests
import datetime
import re
from conf import oj_user_info
from models.local_pg_models import engine as local_engine, PojSubmission
from models.utils import SessionBuilder, RemainList, local_psql as lpsql
import base64

SETTING = {
    'host': 'http://poj.org/',
    'login': 'login',
    'submit': 'submit',
    'submissions': 'status',
}

CONFIG = {
    'max_record_count': 20,  # 每一页的记录条数上限
    'code_min_bytes': 10,
    'code_max_bytes': 65536
}

STATUS = {  # poj -> sdustoj 的(状态, 得分)代换
    'Accepted': ('AC', 100),
    'Wrong Answer': ('WA', 0),
    'Presentation Error': ('PE', 50),
    'Compilation Error': ('CE', 0),
    'Runtime Error': ('RE', 0),
    'Time Limit Exceeded': ('TLE', 0),
    'Memory Limit Exceeded': ('MLE', 0),
    'Output Limit Exceeded': ('OLE', 0),
    'Waiting': ('PD', 0),
    'Compiling': ('CP', 0),
    'Running & Judging': ('RJ', 0),
    '': ('PD', 0)  # 防出错
}

FINISHED_STATUS = [  # 表示已完成的状态
    'Accepted',
    'Wrong Answer',
    'Presentation Error',
    'Compilation Error',
    'Runtime Error',
    'Time Limit Exceeded',
    'Memory Limit Exceeded',
    'Output Limit Exceeded'
]

auth_user, auth_pass = oj_user_info['poj']
session = requests.session()


def get_url(url, *args):
    return SETTING['host'] + SETTING[url] % args


def do_login():
    data = {
        'user_id1': auth_user,
        'password1': auth_pass,
        'B1': 'login',
        'url': '/'
    }
    res = session.post(get_url('login'), data=data)
    print("POJ Login: %s" % (res.status_code,))
    return res.status_code == 302 or res.status_code == 200


def do_submit(pid, lang, code):
    data = {
        'encoded': 1,
        'submit': 'Submit',
        'problem_id': pid,
        'language': lang,
        'source': base64.b64encode(code.encode('utf-8')).decode('utf-8'),
    }
    res = session.post(get_url('submit'), data=data)
    if re.search("""Error Occurred""", res.text) is not None:  # poj的这个状态很万能。
        return False
    if res.status_code != 200:
        return False
    return res.url == get_url('submissions')


def get_submissions(top=None, bottom=None):
    def get_language(lang_html):
        regs = re.search('<a[^>]*>([\\s\\S]*?)</a>', lang_html)
        if regs.groups() is not None and len(regs.groups()) > 0:
            return regs.group(1)
        else:
            return lang_html

    data = {'user_id': auth_user}
    if top is not None:
        data['top'] = top
    elif bottom is not None:
        data['bottom'] = bottom
    res = session.get(get_url('submissions'), params=data)
    f = open('show.html', 'w')
    f.write(res.text)
    f.close()
    regex = """<tr align=center>""" + \
            """<td>(\\d*)</td>""" + \
            """<td><a href=userstatus\\?user_id=[\\s\\S]*?>([\\s\\S]*?)</a></td>""" + \
            """<td><a href=problem\\?id=\\d*>(\\d*)</a></td>""" + \
            """<td><font color=\\w*>([\\s\\S]*?)</font></td>""" + \
            """<td>(\\d*)K?</td>""" + \
            """<td>(\\d*)M?S?</td>""" + \
            """<td>([\\s\\S]*?)</td>""" + \
            """<td>(\\d*)B?</td>""" + \
            """<td>([-:\\d ]*)</td></tr>"""
    reg = re.findall(regex, res.text)
    li = [{
        'run_id': it[0],
        'pid': it[2],
        'status': it[3],
        'memory': it[4],
        'time': it[5],
        'language': get_language(it[6]),
        'length': it[7],
        'submit_time': it[8]
    } for it in reg]
    return li


def request_submit(sid, pid, lang, code):
    """
    向POJ提交。
    :param sid:sdustoj的提交id 
    :param pid: poj的题目id
    :param lang: poj的语言代号
    :param code: 代码
    :return: 
    """
    # 首先检查代码长度限制。
    byte_length = len(code.encode('gb2312'))
    if not CONFIG['code_min_bytes'] <= byte_length <= CONFIG['code_max_bytes']:
        return None, {
            'status': 'LLE',
            'score': 0,
            'finished': True
        }
    # 长时间不用之后，登录状态可能会掉。需要注意修复。
    retry_count = 1
    while retry_count >= 0:
        do_result = do_submit(pid, lang, code)
        if do_result:
            # 提交成功。由于poj没有runid的返回机制，因此只能选择使用数据库全时刻轮询，并且在提交时立刻查询。
            psql = lpsql.session()

            submission_messages = get_submissions()  # 直接抓取一次status表的第一页的数据
            if submission_messages is None or len(submission_messages) <= 0:  # 这意味着出错了
                return None, {
                    'status': 'SF',
                    'score': 0,
                    'finished': True
                }
            new_submission = submission_messages[0]  # 获得第一条数据

            # 构造新的提交缓存到中间数据库
            submission = PojSubmission(
                run_id=new_submission['run_id'],
                pid=new_submission['pid'],
                time=new_submission['time'],
                memory=new_submission['memory'],
                length=new_submission['length'],
                language=new_submission['language'],
                status=new_submission['status'],
                submission_id=sid,
                submit_time=datetime.datetime.now(),
                update_time=datetime.datetime.now(),
                finished=False
            )
            psql.add(submission)
            psql.commit()
            print("-- Poj Update: run_id=%s" % (new_submission['run_id'],))
            return {
                'run_id': new_submission['run_id']
            }, None
        else:
            retry_count -= 1
            do_login()  # 针对可能的错误，试图进行一次重新登陆。
    return None, {
        'status': 'SF',
        'score': 0,
        'finished': True
    }


def update_submit(sid, status):
    """
    更新提交信息。
    :param sid: sdustoj的提交id
    :param status: 更新状态内容
    :return: (isOk, status, update)
    """
    # 根据协定，status的内容包括run_id
    run_id = status['run_id']
    psql = lpsql.session()
    submission = psql.query(PojSubmission).filter_by(run_id=run_id).first()
    if submission is not None:
        finished = submission.finished
        ret_status = None if finished else status
        status, score = STATUS[submission.status]
        ret_update = {
            'status': status,
            'score': score,
            'time': submission.time,
            'memory': submission.memory,
            'finished': finished
        }
        return finished, ret_status, ret_update
    else:  # 找不到相关记录。这表示出错了，返回提交失败的状态。
        return True, None, {
            'status': 'SF',
            'score': 0,
            'time': '-1',
            'memory': '-1',
            'finished': True
        }


def reptile_submit():
    """
    爬取所有的提交并刷新到中间数据库。
    :return: 
    """
    psql = lpsql.session()
    submissions = psql.query(PojSubmission).filter_by(finished=False).order_by(PojSubmission.id).all()
    if len(submissions) > 0:  # 有未完成的内容，确认进行查询。
        print("Poj analyse submissions count %s @ %s" % (len(submissions), datetime.datetime.now()))
        remain = RemainList(submissions)  # 构成一个剩余列表，以便排查
        top = None
        while True:
            records = get_submissions(top=top)  # 获取该页的所有记录
            for record in records:
                run_id = int(record['run_id'])
                submission = remain.pop(lambda s: s.run_id == run_id)
                if submission is not None:  # 找到了与当前网页记录匹配的数据库项目
                    # 从记录更新数据库
                    submission.time = record['time']
                    submission.memory = record['memory']
                    submission.status = record['status']
                    submission.finished = record['status'] in FINISHED_STATUS
                    print("Poj Reptile Submission: run_id=%s" % (run_id,))
            if len(records) < CONFIG['max_record_count'] or remain.is_empty():  # 满足了退出条件
                break
            top = records[-1]['id']
        psql.commit()


def init():
    if not do_login():
        raise Exception('Login failed. Please check your authentication or network.')

init()
