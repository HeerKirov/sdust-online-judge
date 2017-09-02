# -*- coding: utf-8 -*-
# == SDUSTOJ 通信相关设置 ==============================================================================================

# SDUSTOJ数据库的参数
pg_db = {
    'user': 'heer',
    'password': '262144',
    'host': 'localhost',
    'port': '5432',
    'database': 'sdustoj_server'
}

# 用于监听SDUSTOJ消息的Redis的参数
redis_db = {
    'host': '120.25.229.109',
    'port': '6379',
    'password': '262144',
    'db': 10
}

# 接受SDUSTOJ命令的队列
queue = 'hustoj'

# 订阅SDUSTOJ哪些编程环境的提交消息
subscribe = [
    'gcc',
    'g++',
    'java',
    'python',
]

# 该评测机在SDUSTOJ中的ID
judger_id = 2


# == HUSTOJ 通信相关设置 ===============================================================================================

# HUSTOJ数据库的参数
mysql_db = {
    'user': 'heer',
    'password': '262144',
    'host': 'localhost',
    'database': 'jol'
}

# 用于HUSTOJ服务器接受消息的Redis的参数
local_redis_db = {
    'host': '120.25.229.109',
    'port': '6379',
    'password': '262144',
    'db': 9
}

# 向HUSTOJ发送命令的队列
local_queue = {
    'test-data': 'test-data',
    'special-judge': 'special-judge',
    'submission-analyse': 'sa',
    'makefile': 'makefile',
    'template': 'template'
}

# 向HUSTOJ更新提交时将提交挂在哪一HUSTOJ用户下
user = {
    'user_id': 'admin'
}


# == 评测相关 ==========================================================================================================

# SDUSTOJ编程环境ID到HUSTOJ语言编号的映射
language = {
    'gcc': 0,
    'g++': 1,
    'java': 3,
    'python': 6,
}

# HUSTOJ的结果编号到SDUSTOJ提交状态/得分的映射
status = {
    0: ('PD', 0),    # 提交中
    1: ('PDR', 0),   # 提交Rejudge中
    2: ('CP', 0),    # 编译中
    3: ('RJ', 0),    # 运行 & 评测
    4: ('AC', 100),  # Accepted
    5: ('PE', 50),   # 格式错误
    6: ('WA', 0),    # 结果错误
    7: ('TLE', 0),   # 超时
    8: ('MLE', 0),   # 超内存
    9: ('OLE', 0),   # 超输出
    10: ('RE', 0),   # 运行错误
    11: ('CE', 0),   # 编译错误
    12: ('CD', 0),   # 编译完成
    13: ('RD', 0),   # 运行完成
    14: ('UE', 25),  # 标点符号错误
}

# 结果的优先级，用于合成提交的总状态
priority = {
    0: 2000,
    1: 1000,
    2: 900,
    3: 700,
    4: 0,
    5: 10,
    6: 20,
    7: 40,
    8: 30,
    9: 50,
    10: 60,
    11: 899,
    12: 800,
    13: 600,
    14: 15,
}

# 提交的默认状态
default_status = 0

# HUSTOJ中哪些结果表示评测已结束，检测到评测结束后分析器将不再追踪相应提交
final_status = {
    4, 5, 6, 7, 8, 9, 10, 11, 14
}

# 更新提交时未找到题目更新题目重新提交尝试次数
try_max = 3

# 使用HUSTOJ的哪一个评测机
judger = 'admin'
