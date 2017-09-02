# -*- coding: utf-8 -*-
from requests.auth import HTTPBasicAuth

from sqlalchemy.orm import sessionmaker
from data_updater.models import server as server_models

from .cache import update_cache

from config import CLIENT_SETTINGS

from .utils import request_data, updated_request, timestamp_cur, str_to_datetime

url = CLIENT_SETTINGS['root_url'].rstrip('/') + '/' + CLIENT_SETTINGS['problem_url'].lstrip('/')
username = CLIENT_SETTINGS['username']
password = CLIENT_SETTINGS['password']
auth = HTTPBasicAuth(username, password)
cache_name = 'problem_updater_cache'


Session = sessionmaker(bind=server_models.engine)
session = Session()

env_cache = set()


def request_problem_list(request_url):
    return request_data(url=request_url, auth=auth)


def request_problem_detail(problem_id):
    request_url = '%s/%s/' % (url.rstrip('/'), str(problem_id))
    return request_data(url=request_url, auth=auth)


def flush_environment_cache():
    environments = session.query(server_models.Environment.id).all()
    env_cache.clear()
    for env_tuple in environments:
        env_cache.add(env_tuple[0])


def write_problem_limits(problem_json):
    limits_json = problem_json['limits']
    problem_id = problem_json['id']
    # 删除已经不存在对应编程环境的编程限制
    cur_limits = session.query(server_models.Limit).filter_by(problem_id=problem_id)
    for limit in cur_limits:
        if int(limit.environment_id) not in env_cache:
            session.delete(limit)
    session.commit()
    # 更新或创建编程环境
    for limit_json in limits_json:
        environment_id = limit_json['environment']
        limit = session.query(server_models.Limit).filter_by(problem_id=problem_id,
                                                             environment_id=environment_id).first()
        if limit is None and int(environment_id) in env_cache:
            limit_model = server_models.Limit(problem_id=problem_id,
                                              environment_id=environment_id,
                                              env_name=limit_json['env_name'],
                                              time_limit=limit_json['time_limit'],
                                              memory_limit=limit_json['memory_limit'],
                                              length_limit=limit_json['length_limit'],
                                              is_temp=limit_json['is_temp'],
                                              template_list=limit_json['template'] if limit_json['is_temp'] else None)
            session.add(limit_model)
            session.commit()
        elif limit is not None:
            limit.env_name = limit_json['env_name']
            limit.time_limit = limit_json['time_limit']
            limit.memory_limit = limit_json['memory_limit']
            limit.length_limit = limit_json['length_limit']
            limit.is_temp = limit_json['is_temp']
            limit.template = limit_json['template'] if limit_json['is_temp'] else None
            session.commit()


def write_problem(problem_json):
    problem = session.query(server_models.Problem).filter_by(id=problem_json['id']).first()
    if problem is None:
        problem_model = server_models.Problem(id=problem_json['id'],
                                              description=problem_json['description'],
                                              sample=problem_json['sample'],
                                              create_time=str_to_datetime(problem_json['create_time']),
                                              update_time=str_to_datetime(problem_json['update_time']),
                                              title=problem_json['title'],
                                              introduction=problem_json['introduction'],
                                              source=problem_json['source'],
                                              author=problem_json['author'],
                                              is_special_judge=problem_json['is_special_judge'],
                                              number_test_data=problem_json['number_test_data'],
                                              number_limit=problem_json['number_test_data'],
                                              number_category=problem_json['number_test_data'],
                                              number_invalid_word=problem_json['number_test_data'])
        session.add(problem_model)
        print('created problem %s: %s' % (problem_model.id, problem_model.title))
    else:
        problem.description = problem_json['description']
        problem.sample = problem_json['sample']
        problem.create_time = problem_json['create_time']
        problem.update_time = problem_json['update_time']
        problem.title = problem_json['title']
        problem.introduction = problem_json['introduction']
        problem.source = problem_json['source']
        problem.author = problem_json['author']
        problem.is_special_judge = problem_json['is_special_judge']
        problem.number_test_data = problem_json['number_test_data']
        problem.number_limit = problem_json['number_limit']
        problem.number_category = problem_json['number_category']
        problem.number_invalid_word = problem_json['number_invalid_word']
        print('updated problem %s: %s' % (problem.id, problem.title))
    session.commit()
    write_problem_limits(problem_json)


def update_problem(problem_id):
    chance_left = 3
    problem_detail = None
    while problem_detail is None and chance_left > 0:
        print('requesting problem %s, tried %s ......' % (problem_id, 3 - chance_left))
        problem_detail = request_problem_detail(problem_id)
        chance_left -= 1
    if problem_detail is not None:
        write_problem(problem_detail)
    else:
        print('updating problem %s failed' % (problem_id,))


def update_problems(update_all=False):
    print('updating problems ......')
    time = timestamp_cur()
    flush_environment_cache()
    request_url = url if update_all else updated_request(url, cache_name)
    while request_url is not None:
        chance_left = 3
        problem_list = None
        while problem_list is None and chance_left > 0:
            print('requesting %s, tried %s ......' % (request_url, 3-chance_left))
            problem_list = request_problem_list(request_url)
            chance_left -= 1
        if problem_list is None:
            request_url = None
        else:
            for p in problem_list['results']:
                update_problem(p['id'])
            request_url = problem_list['next']
    update_cache(cache_name, time)
