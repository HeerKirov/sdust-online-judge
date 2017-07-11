# 数据库的设定
PG_SETTINGS = {
    'host': '120.25.229.109',
    'port': '5432',
    'db': 'sdustoj_server',
    'user': 'ojuser',
    'password': '262144'
}

REDIS_SETTINGS = {
    'host': '120.25.229.109',
    'port': '6379',
    'password': '262144',
    'db': 0
}

# 系统初始根用户信息，密码仅在首次创建用户时设定
# 当日后无需检查时，可将此项设为None，则每次同步数据库时不会检查
INIT_USER_SETTINGS = {
    'username': 'korosensei',
    'password': 'big_boss',
    'first_name': 'せんせー',
    'last_name': '殺',
}

# OJ相关设置
OJ_SETTINGS = {
    'test_data_input_max_size': 131072
}

# OJ中从status状态到score完成度的转换，不在该表中的项记为0，取值范围为0~100.
OJ_STATUS_SCORE = {
    'AC': 100,    # Accepted
    'PE': 50,    # 格式错误
    'WA': 0,    # 结果错误
    'TLE': 10,   # 超时
    'MLE': 10,   # 超内存
    'OLE': 0,   # 超输出
    'RE': 0,   # 运行错误
    'CE': 0,   # 编译错误
}
