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
    'db': 0
}

# 接受SDUSTOJ命令的队列
queue = 'virtualjudge1'

# 订阅SDUSTOJ哪些编程环境的提交消息
subscribe = [
    'hdu-c',
    'hdu-cpp',
    'hdu-java'
]

# 该评测机在SDUSTOJ中的ID
judger_id = 1


# 本地数据库参数
local_pg_db = {
    'user': 'heer',
    'password': '262144',
    'host': 'localhost',
    'port': '5432',
    'database': 'virtual_judge'
}

# 本地进行通信的队列参数
local_redis_db = {
    'host': '120.25.229.109',
    'port': '6379',
    'password': '262144',
    'db': 8
}

# 本地进行消息通信的队列
local_queue = {
    'submission-analyse': 'sa'
}

# == 爬虫相关 ====================================================================================

# 保存所有可用oj的登陆账户信息
oj_user_info = {
    'hdu': ('HeerKirov', 'furandouru')
}

oj_env_message = {
    'hdu-c': ('hdu', '3'),
    'hdu-cpp': ('hdu', '2'),
    'hdu-java': ('hdu', '5')
}
