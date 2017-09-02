from sqlalchemy.orm import sessionmaker
from data_updater.models import server as server_models
from datetime import datetime, timedelta
import json
from time import mktime

# 该部分function的作用是定时更新rank。
# 只会选择未完成的rank进行更新（严格来说，有一定的时间差）。

Session = sessionmaker(bind=server_models.engine)
session = Session()


def get_submissions_group(submissions):
    """
    将所有的提交按照user进行分组
    :param submissions: 查询集。必须已经进行排序。
    :return: 返回一个字典，字典的键是user_id,值是一个submission的列表。
    """
    ret = dict()
    user_id = None
    group = []
    for submission in submissions:
        if user_id is None:  # 第一个
            user_id = submission.user_id
        elif user_id != submission.user_id:  # 碰到了分组边界
            ret[user_id] = group
            group = []
            user_id = submission.user_id
        group.append(submission)
    if len(group) > 0 and user_id is not None:
        ret[user_id] = group
    return ret


def get_organization_id(submissions):
    """
    只是从提交列表里面弄出来一个organization的id而已。
    :param submissions: 
    :return: 
    """
    for s in submissions:
        if hasattr(s, 'organization_id'):
            return s.organization_id
    return None


def update_rank_by_user(user_id, mission, submissions, **kwargs):
    """
    按照user_id来更新rank。
    :param user_id: 传入user_id
    :param mission: 传入mission
    :param submissions: 传入该用户所有提交的列表。
    :return: 没有返回值。
    """
    print("Update user :%s" % (user_id,))
    title_map = kwargs['title_map'] if 'title_map' in kwargs else None
    rank = session.query(server_models.Rank).filter_by(user_id=user_id).first()
    organization_id = get_organization_id(submissions)
    if rank is None:  # 还没有碰过。给这个人创建新的rank模型。
        # 创建新的model
        rank = server_models.Rank(
            mission_id=mission.id,
            user_id=user_id,
            organization_id=organization_id,
            sub_count=0,
            solved=0,
            penalty=0,
            sum_score=0,
            result={}
        )
        session.add(rank)
    else:  # 不是第一次，那么还需要首先清空之前的关键数据。
        rank.sub_count = 0
        rank.solved = 0
        rank.penalty = 0
        rank.sum_score = 0
    result = {}
    # 然后开始处理所有的submission信息。
    for s in submissions:  # 遍历所有的提交。
        rank.sub_count += 1
        p_id = str(s.problem_id)  # 获得题目的id。
        if p_id not in result:  # 该题目还没有被提交过，首先创建它
            result[p_id] = {
                'title': title_map[p_id] if title_map is not None and p_id in title_map else None,
                'sub_count': 0,
                'ac_time': None,
                'wrong_count': 0,
                'status': '',
                'average_score': 0,
                'max_score': 0,
                'latest_score': 0
            }
        # 然后对该题目的题目数据组进行更新。
        p_res = result[p_id]
        p_res['sub_count'] += 1
        # 更新ACM部分数据
        if p_res['ac_time'] is None:  # 该题目还没有被AC
            if s.status == 'AC':  # 这次对了
                now_time = s.submit_time  # todo 通过时间计算为第一次AC题目的提交时间。

                p_res['ac_time'] = str(now_time)
                p_res['status'] = 'AC'
                rank.solved += 1
                rank.penalty += (now_time - mission.start_time).total_seconds() + p_res['wrong_count'] * 20 * 60
            else:  # 仍未AC
                p_res['wrong_count'] += 1
                p_res['status'] = s.status
        # 下面处理OI部分数据
        now_score = s.score if s.score is not None else 0

        if now_score > p_res['max_score']:
            p_res['max_score'] = now_score
        p_res['latest_score'] = now_score
        p_res['average_score'] += now_score  # 后面平均一次
    # 下面处理一下总数据
    # 处理一下平均数，处理一下总成绩，回写rank
    mission_type = mission.config['type']
    if 'type_config' in mission.config and 'valid_submission' in mission.config['type_config']:
        mission_valid_submission = mission.config['type_config']['valid_submission']
    else:
        mission_valid_submission = None
    for p, v in result.items():  # 遍历一遍所有题目的数据
        if v['sub_count'] > 0:
            v['average_score'] /= v['sub_count']
        else:
            v['average_score'] = 0
        if mission_type == 'oi':
            if mission_valid_submission == 'latest':
                rank.sum_score += v['latest_score']
            elif mission_valid_submission == 'highest':
                rank.sum_score += v['max_score']
    rank.result = result


def update_rank_of_mission(mission):
    """
    更新指定的mission下属的所有rank。
    :param mission: 
    :return: 
    """
    print("Update rank of mission %s" % (mission.id,))
    submissions = session.query(server_models.Submission).\
        filter_by(mission_id=mission.id). \
        filter(server_models.Submission.submit_time >= mission.start_time). \
        filter(server_models.Submission.submit_time <= mission.end_time). \
        order_by(server_models.Submission.submit_time).\
        order_by(server_models.Submission.user_id).\
        all()
    problems = session.query(server_models.MissionProblemRelation).filter_by(mission_id=mission.id).all()
    problem_map = {}
    for u in problems:
        problem = session.query(server_models.Problem).filter_by(id=u.problem_id).first()
        if problem is not None:
            problem_map[str(problem.id)] = problem.title
    # 更新策略：
    # 以提交为基点进行操作。将提交按照user_id分组，然后分别查询rank.
    groups = get_submissions_group(submissions)
    for k, v in groups.items():
        update_rank_by_user(k, mission, v, title_map=problem_map)
    print("Update completed.")


def update_ranks(update_all=False):
    """
    更新rank的数据。
    :param update_all:如果选择了True，那么会更新所有的rank;否则只会更新还没结束的rank。 
    :return: 
    """
    if update_all:
        missions = session.query(server_models.Mission).filter_by(deleted=False).all()
    else:
        now = datetime.now()
        missions = session.query(server_models.Mission).\
            filter_by(deleted=False).filter(server_models.Mission.end_time >= now - timedelta(minutes=2)).\
            filter(server_models.Mission.start_time <= now) .all()
    for mission in missions:
        update_rank_of_mission(mission)
    session.commit()


if __name__ == '__main__':
    # test
    update_ranks(True)
