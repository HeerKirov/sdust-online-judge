# 数据库的设定
PG_SETTINGS = {
    'host': 'localhost',
    'port': '5432',
    'db': 'sdustoj_server',
    'user': 'heer',
    'password': '262144'
}

REDIS_SETTINGS = {
    'host': '120.25.229.109',
    'port': '6379',
    'password': '262144',
    'db': 10  # 这儿用一个大的数字进行测试
}

# 系统初始根用户信息，密码仅在首次创建用户时设定
# 当日后无需检查时，可将此项设为None，则每次同步数据库时不会检查
INIT_USER_SETTINGS = {
    'username': 'admin',
    'password': 'admin262144',
    'first_name': 'Administrator',
    'last_name': 'Mr.',
}

# OJ相关设置
OJ_SETTINGS = {
    'test_data_input_max_size': 131072
}

# 完成度有关设置
OJ_SCORE_SETTING = {
    'threshold_score': 30  # 有效分数的临界点，只有不小于这个分数的分数才会被判定为非零
}

# OJ中从status状态到score完成度的转换，不在该表中的项记为0，取值范围为0~100.
OJ_STATUS_SCORE = {
    'AC': 100,    # Accepted
    'PE': 50,    # 格式错误
    'WA': 0,    # 结果错误
    'TLE': 0,   # 超时
    'MLE': 0,   # 超内存
    'OLE': 0,   # 超输出
    'RE': 0,   # 运行错误
    'CE': 0,   # 编译错误
    'UE': 25,  # 标点符号错误
    '': 0,
}

# 代表结束的状态
OJ_FINAL_STATUS = [
    'AC', 'PE', 'WA', 'TLE', 'MLE', 'OLE', 'RE', 'CE', 'UE'
]
