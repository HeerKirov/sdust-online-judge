# -*- coding: utf-8 -*-
from models.redis_models import get_subscribe, get_queue_info

from models import pg_models, mysql_models
from sqlalchemy.orm import sessionmaker

from functions.submission import update

PgSession = sessionmaker(bind=pg_models.engine)
pg_session = PgSession()

MysqlSession = sessionmaker(bind=mysql_models.engine)
mysql_session = MysqlSession()

# 维护标记提交，根据标记的未完成提交轮询HUSTOJ数据库，将HUSTOJ提交状态转换为SDUSTOJ提交状态回填SDUSTOJ数据库。

# Manager将从未完成提交队列中轮流获取提交ID，根据此ID查询到对应的HUSTOJ提交，
# 并根据提交状态生成SDUSTOJ提交的每组测试数据的状态及当前总状态。根据各状态信息决定当前评测是否完成，
# 若未完成，则提交将被重新加入未完成提交队列继续下一轮处理。


def handler(message):
    if message['type'] == 'message':
        sid = message['data'].decode('utf-8')
        language_str = message['channel'].decode('utf-8')
        info = get_queue_info(sid)
        if info is not None:
            update(sid=sid, language=language_str)

# 启动一项订阅服务，订阅sdustoj的消息，从sdustoj晶振提交并在上面的handler函数中进行sdustoj->hustoj的转换。
get_subscribe(handler)
