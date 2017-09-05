# -*- encoding=utf-8 -*

# 数据库的设定
PG_SETTINGS = {
    'host': 'localhost',
    'port': '5432',
    'db': 'sdustoj_client',
    'user': 'heer',
    'password': '1234'
}

REDIS_SETTINGS = {
    'host': 'localhost',
    'port': '6379',
    'password': '1234',
    'db': 0
}

# 系统初始根用户信息，密码仅在首次创建用户时设定
# 当日后无需检查时，可将此项设为None，则每次同步数据库时不会检查
INIT_USER_SETTINGS = {
    'username': 'admin',
    'password': 'admin262144',
    'name': 'Administrator',
    'sex': 'MALE'
}

# 用户端信息
CLIENT_SETTINGS = {
    'root_url': 'http://localhost:8002/',
    'submission_url': '/JudgeAdmin/api/submissions/',
    'problem_url': '/JudgeAdmin/api/problems/',
    'environment_url': '/JudgeAdmin/api/environments/',
    'category_url': '/JudgeAdmin/api/categories/',
    'category_problem_url': 'problem-relations',
    'username': 'kawaiiClient',
    'password': '1234'
}
