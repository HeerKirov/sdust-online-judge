# -*- coding: utf-8 -*-
from models.redis_models import get_subscribe, get_queue_info

from models import pg_models, mysql_models
from sqlalchemy.orm import sessionmaker

from functions.submission import update

PgSession = sessionmaker(bind=pg_models.engine)
pg_session = PgSession()

MysqlSession = sessionmaker(bind=mysql_models.engine)
mysql_session = MysqlSession()


def handler(message):
    if message['type'] == 'message':
        sid = message['data'].decode('utf-8')
        language_str = message['channel'].decode('utf-8')
        info = get_queue_info(sid)
        if info is not None:
            update(sid=sid, language=language_str)

# 启动一项订阅服务，订阅sdustoj的消息，从sdustoj提交并在上面的handler函数中进行sdustoj->hustoj的转换。
get_subscribe(handler)
