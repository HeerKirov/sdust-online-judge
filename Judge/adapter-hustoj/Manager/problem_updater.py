# -*- coding: utf-8 -*-
from datetime import datetime

from models import mysql_models
from models import pg_models
from models.redis_models import get_command
from sqlalchemy.orm import sessionmaker

from functions import problem

MysqlSession = sessionmaker(bind=mysql_models.engine)
mysql_session = MysqlSession()

PgSession = sessionmaker(bind=pg_models.engine)
pg_session = PgSession()


# 接收题目题元更新消息，将SDUSTOJ中的题目按测试数据分拆为一至多个HUSTOJ中的题目写入HUSTOJ的数据库，
# 将测试数据或特殊评测代码发送至Client写入评测机文件系统。
# SDUSTOJ中的题目将依照测试数据生成HUSTOJ题目，一组数据一个题目。
# 接收消息与向Client发送消息均通过Redis的队列实现。


class Function(object):
    @staticmethod
    def func(cmd):
        pass


class Update(Function):
    update_func = {
        'all': problem.update_all,
        'meta': problem.update_meta,
        'problem': problem.update
    }

    @staticmethod
    def func(cmd):
        Update.update_func[cmd['type']](**cmd)


func_classes = {
    'update': Update
}


def handler(command):
    print('[' + str(datetime.now()) + ']' + 'Get Command: ' + str(command))
    func_class = func_classes[command['cmd']]
    func_class.func(command)


# 启动一项服务，轮询从sdustoj来的指令队列。
get_command(handler)
