from models.redis_models import get_subscribe, get_queue_info, Submission
from models.utils import AlchemyUtils
from models import pg_models
from sqlalchemy.orm import sessionmaker
from conf import oj_env_message

from functions import hdu, poj
# 竞争提交并向原oj提交
PgSession = sessionmaker(bind=pg_models.engine)
pg_session = PgSession()

updater_functions = {
    'hdu': hdu.request_submit,
    'poj': poj.request_submit
}


def update(sid, language):
    global pg_session
    # 首先抓取提交的必要信息
    print("Update a submission: sid=%s, lang=%s" % (sid, language))
    submission = pg_session.query(pg_models.Submission).filter_by(id=sid).first()  # 获得submission模型
    code = pg_session.query(pg_models.SubmissionCode).filter_by(submission_id=sid).first().code['code']  # 获得code内容
    problem = pg_session.query(pg_models.Problem).filter_by(id=submission.problem_id).first()  # 获得problem模型

    oj, lang_id = oj_env_message[language]  # 获得oj名称和发送的语言代号
    pid = problem.origin_pid  # 获得题目编号
    ret, update_msg = updater_functions[oj](submission.id, pid, lang_id, code)
    # 返回值为(status, update).status为空表示不存在轮询数据。update不为空表示需要对提交做一些初始化(也可能是直接finish)
    # 取得回执信息。拥有回执信息的提交，需要放入轮询队列。
    # 回执的信息根据oj自己决定。但是至少需要包括如下数据:
    # oj:oj的名称
    # 下面也会自动补全一些数据。
    if ret is not None:
        if 'oj' not in ret:
            ret['oj'] = oj
        Submission.mark(submission.id, ret)
    if update_msg is not None:
        AlchemyUtils.update_submission(submission, update_msg)
        pg_session.commit()


def handler(message):
    if message['type'] == 'message':
        sid = message['data'].decode('utf-8')
        language_str = message['channel'].decode('utf-8')
        info = get_queue_info(sid)
        if info is not None:
            update(sid, language_str)

# 启动一项订阅服务，订阅sdustoj的消息，从sdustoj提交并在上面的handler函数中进行sdustoj->vj的转换。
get_subscribe(handler)
