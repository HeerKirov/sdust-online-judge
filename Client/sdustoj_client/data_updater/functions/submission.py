import requests
from requests.auth import HTTPBasicAuth

from sqlalchemy.orm import sessionmaker
from data_updater.models import server as server_models

from datetime import datetime
from time import mktime

from .cache import update_cache
from config import CLIENT_SETTINGS

from .utils import request_data, updated_request, timestamp_cur, str_to_datetime

url = CLIENT_SETTINGS['root_url'].rstrip('/') + '/' + CLIENT_SETTINGS['submission_url'].lstrip('/')
username = CLIENT_SETTINGS['username']
password = CLIENT_SETTINGS['password']
auth = HTTPBasicAuth(username, password)
cache_name = 'submission_updater_cache'


Session = sessionmaker(bind=server_models.engine)
session = Session()


def request_submit(submission_json):
    request_url = '%s/' % (url.rstrip('/'),)
    r = requests.post(url, submission_json, auth=auth)
    if r.status_code == 201:
        return r.json()
    else:
        return None


def submit(submission_json):
    """
    发起一次提交，将submission提交到Server端。该函数会返回Server端的请求回执信息。
    :param submission_json: 
    :return: 
    """
    chance_left = 3
    result = None
    while result is None and chance_left > 0:
        print('submitting submission, tried %s ......' % (3 - chance_left,))
        result = request_submit(submission_json)
        chance_left -= 1
    if result is None:
        print('submitting submissio failed')
    return result


def request_submission_list(request_url):
    return request_data(url=request_url, auth=auth)


def request_submission_detail(sid):
    request_url = '%s/%s/' % (url.rstrip('/'), str(sid))
    return request_data(url=request_url, auth=auth)


def write_submission_compile_info(local_id, submission_json):
    info = session.query(server_models.CompileInfo).filter_by(submission_id=local_id).first()
    if info is not None:
        info.info = submission_json['compile_info']


def write_submission_test_data_status(local_id, submission_json):
    test_data = session.query(server_models.TestDataStatus).filter_by(submission_id=local_id).first()
    if test_data is not None:
        test_data.status = submission_json['test_data_status']


def write_submission_code(local_id, submission_json):
    code = session.query(server_models.SubmissionCode).filter_by(submission_id=local_id).first()
    if code is not None:
        code.code = submission_json['code']


def write_rank(local_submission, submission_json):
    """
    根据提交，将提交的信息更新到Rank上去。
    :param local_submission: 
    :param submission_json: 
    :return: 
    """
    if local_submission.finished is False:  # 仅当提交已完成，才会做累计。
        return
    rank = session.query(server_models.Rank).filter_by(mission_id=local_submission.mission_id).first()
    mission = session.query(server_models.Mission).filter_by(id=local_submission.mission_id).first()

    if rank is None:
        # 创建新的model
        rank = server_models.Rank(
            mission_id=local_submission.mission_id,
            user_id=local_submission.user_id,
            organization_id=local_submission.organization_id,
            sub_count=0,
            solved=0,
            penalty=0,
            sum_score=0,
            result={}
        )
        session.add(rank)
    problem_id = local_submission.problem_id  # 获得了题目的ID。
    rank.sub_count += 1
    if str(problem_id) not in rank.result:  # 这个题目还没有被提交过的痕迹，那么就创建。
        rank.result[str(problem_id)] = {
            'sub_count': 0,
            'ac_time': None,
            'wrong_count': 0,
            'status': '',
            'average_score': 0,
            'max_score': 0,
            'latest_score': 0
        }
    # 下面对该题目的信息进行更新
    p_result = rank.result[str(problem_id)]

    if p_result['ac_time'] is None:  # 这表明该题目仍未AC
        if local_submission.status == 'AC':  # 这次AC了
            now_time = datetime.now()
            p_result['ac_time'] = now_time
            p_result['status'] = 'AC'
            rank.solved += 1
            # 这里的罚时计算规则是每一次错误20分钟。
            this_penalty = mktime(now_time - mission.start_time) + p_result['wrong_count'] * 20 * 60
            rank.penalty += this_penalty
        else:  # 这次还是没有AC……
            p_result['wrong_count'] += 1
            p_result['status'] = local_submission.status
        # 而如果该题目AC了，那么后续的提交是不会有影响的。
    now_score = local_submission.score
    old_latest_score = p_result['latest_score']
    old_max_score = p_result['max_score']
    old_average_score = p_result['average_score']
    p_result['latest_score'] = now_score
    if now_score > p_result['max_score']:
        p_result['max_score'] = now_score
    p_result['average_score'] = \
        (p_result['average_score'] * p_result['sub_count'] + now_score) / (p_result['sub_count'] + 1)
    # 更新提交次数必须放在后面，因为前面有个平均数依赖
    p_result['sub_count'] += 1
    # 更新在总集中的sum_score
    if mission.config['type'] == 'oi':
        if mission.config['type_config']['valid_submission'] == 'latest':
            rank.sum_score += p_result['latest_score'] - old_latest_score
        elif mission.config['type_config']['valid_submission'] == 'highest':
            rank.sum_score += p_result['max_score'] - old_max_score
    rank.result = p_result


def write_submission(submission_json):
    submission = session.query(server_models.Submission).filter_by(sid=submission_json['id']).first()
    if submission is not None:
        print("Update submission %s" % (submission_json['id'],))
        submission.time = submission_json['time']
        submission.memory = submission_json['memory']
        submission.length = submission_json['length']
        submission.status = submission_json['status']
        submission.score = submission_json['score'] if 'score' in submission_json else None
        submission.finished = submission_json['finished']
        submission.update_time = submission_json['update_time']
        # 由于查询附带信息需要本地提交的id，所以需要手动加入。
        write_submission_compile_info(submission.id, submission_json)
        write_submission_test_data_status(submission.id, submission_json)
        write_submission_code(submission.id, submission_json)
        session.commit()


def update_submission(sid):
    chance_left = 3
    submission_detail = None
    while submission_detail is None and chance_left > 0:
        submission_detail = request_submission_detail(sid)
        chance_left -= 1
    if submission_detail is not None:
        write_submission(submission_detail)


def update_submissions(update_all=False):
    time = timestamp_cur()
    request_url = url if update_all else updated_request(url, cache_name)
    while request_url is not None:
        chance_left = 3
        submission_list = None
        while submission_list is None and chance_left > 0:
            # 我觉得在请求列表的时候可以把user也作为过滤筛选项。
            submission_list = request_submission_list(request_url)
            chance_left -= 1
        if submission_list is None:
            request_url = None
        else:
            for s in submission_list['results']:
                update_submission(s['id'])
            request_url = submission_list['next']
    update_cache(cache_name, time)

