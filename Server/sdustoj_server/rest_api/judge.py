import redis
from json import dumps
from .models import Judge
from config import REDIS_SETTINGS

pool = redis.ConnectionPool(
    host=REDIS_SETTINGS['host'],
    port=int(REDIS_SETTINGS['port']),
    db=int(REDIS_SETTINGS['db']),
    password=REDIS_SETTINGS['password']
)
r = redis.Redis(connection_pool=pool)


# -- 更新题元及题目相关 ------------------------------------------------------------------------------------------------

def inform_machine(machine, info):
    r.rpush(machine, info)


def update_problem(problem, judge=None):
    """
    通知评测机更新题目。
    :param problem: 题目的Model对象。
    :param judge: 需要通知更新的评测机Model对象，若为None则表示更新包含此题目的全部评测机。
    :return: 无返回值。
    """
    if judge is None:
        for j in problem.judge.all().distinct():
            inform_machine(j.cmd_queue, dumps({
                'cmd': 'update',
                'type': 'problem',
                'pid': problem.id
            }))
    else:
        inform_machine(judge.cmd_queue, dumps({
            'cmd': 'update',
            'type': 'problem',
            'pid': problem.id
        }))


def update_meta(meta_problem, judge=None):
    """
    通知评测机更新题元。
    :param meta_problem: 题元的Model对象。
    :param judge: 需要通知更新的评测机Model对象，若为None则表示更新包含此题目的全部评测机。
    :return: 无返回值。
    """
    if judge is None:
        for j in Judge.objects.all():
            inform_machine(j.cmd_queue, dumps({
                'cmd': 'update',
                'type': 'meta',
                'mid': meta_problem.id
            }))
    else:
        inform_machine(judge.cmd_queue, dumps({
            'cmd': 'update',
            'type': 'meta',
            'mid': meta_problem.id
        }))


def update_all(judge=None):
    """
    通知评测机更新全部数据。
    :param judge: 需要通知更新的评测机Model对象，若为None则表示更新包含此题目的全部评测机。
    :return: 无返回值。
    """
    if judge is None:
        for j in Judge.objects.all():
            inform_machine(j.cmd_queue, dumps({
                'cmd': 'update',
                'type': 'all'
            }))
    else:
        inform_machine(judge.cmd_queue, dumps({
            'cmd': 'update',
            'type': 'all'
        }))


# -- 发布提交相关 ------------------------------------------------------------------------------------------------------

def push_submission(submission_id):
    r.rpush(str(submission_id), '_')


def publish_submission(submission):
    judge_id = submission.environment.judge_id
    push_submission(submission.id)
    r.publish(judge_id, str(submission.id))
