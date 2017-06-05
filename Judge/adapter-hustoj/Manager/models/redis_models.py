# -*- coding: utf-8 -*-
from json import loads, dumps

import redis
import time

from conf import queue, subscribe, local_queue, default_status
from conf import redis_db, local_redis_db

pool = redis.ConnectionPool(
    host=redis_db['host'],
    port=int(redis_db['port']),
    db=int(redis_db['db']),
    password=redis_db['password']
)
r = redis.Redis(connection_pool=pool)

local_pool = redis.ConnectionPool(
    host=local_redis_db['host'],
    port=int(local_redis_db['port']),
    db=int(local_redis_db['db']),
    password=local_redis_db['password']
)
lr = redis.Redis(connection_pool=local_pool)

sub_analyse_key = local_queue['submission-analyse']  # 提交解析队列？


class TestData(object):  # 看起来处理测试数据相关。与Client对接将测试数据写入本地文件系统。
    @staticmethod
    def write(problem_id, test_in, test_out):
        """
        将数据发送到HUSTOJ本地的写入器，写入测试数据。
        :param problem_id: HUSTOJ题目的ID。
        :param test_in: bytes类型，测试输入。
        :param test_out: bytes类型，测试输出。
        :return: 无返回值。
        """

        if test_in is None:
            test_in = b''
        if test_out is None:
            test_out = b''
        # 填空，不重要。
        test_data = {
            'problem_id': str(problem_id),
            'test_in': test_in.decode('utf-8'),
            'test_out': test_out.decode('utf-8')
        }  # 构造一个测试数据的集
        lr.rpush(local_queue['test-data'], dumps(test_data))
        # 在本地消息队列追加命令TEST-DATA，内容是测试数据集的json。
        # 看起来这个本地消息队列就是hustoj的写入器？遵循的是hustoj的命令规范的样子。
        # 好像是跟Client端对接的。


class SpecialJudge(object):  # 特殊评测相关
    @staticmethod
    def write(problem_id, code):
        """
        将数据发送到HUSTOJ本地的写入器，写入特殊评测数据。
        :param problem_id: HUSTOJ题目的ID。
        :param code: 特殊评测代码。
        :return: 无返回值。
        """
        special_judge = {
            'problem_id': str(problem_id),
            'code': code.decode('utf-8')
        }  # 同样构造一个特殊评测的数据集
        lr.rpush(local_queue['special-judge'], dumps(special_judge))
        # 同样写入本地消息队列。写入的指令是SPECIAL-JUDGE.


class Submission(object):  # 看起来跟提交代码有关。

    @staticmethod
    def _get_key(submission_id):  # 一个getkey方法，暂且不知道有什么特别含义。
        return str(submission_id)

    @staticmethod
    def mark(submission_id, submission_info):  # (提交ID，标记数据(测试数据ID,提交submission的ID)).
        """
        标记提交，之后分析器将持续追踪此提交的动态直至评测完成。
        :param submission_id: SDUSTOJ提交的ID。
        :param submission_info: 列表，SDUSTOJ提交对应的HUSTOJ提交信息。
        :return: 无返回值。
        """
        key = Submission._get_key(submission_id)  # 获得key，在这里是sdustoj的提交ID。
        for test_id, solution_id in submission_info:
            lr.hset(key, test_id, solution_id)
        # 这里的代码是将info里的信息写入本地消息队列的提交ID的hash表。
        # 信息组织的方式是将每个sdustoj上的提交作为一个hash表，集中管理隶属于这个提交的N个测试数据问题的信息。
        # hash表内的k-v为sdustoj上的测试数据ID-hustoj上提交的submission的ID。
        lr.rpush(sub_analyse_key, key)  # 向本地消息队列的提交解析队列push当前sdustoj提交的ID。

    @staticmethod
    def unmark(submission_id):
        """
        删除提交的标记，之后分析器将不再追踪此提交。
        :param submission_id: SDUSTOJ提交的ID。
        :return: 无返回值。
        """
        key = Submission._get_key(submission_id)
        if lr.exists(key):
            lr.delete(key)  # 从本地消息队列中删掉这个提交的ID的info。

    @staticmethod
    def remove_status(submission_id, test_data_id):
        """
        从标记的一条提交的标记信息中删除某条测试数据的评测信息。
        :param submission_id: SDUSTOJ提交的ID。
        :param test_data_id: SDUSTOJ测试数据ID。
        :return: 无返回值。
        """
        key = Submission._get_key(submission_id)
        lr.hdel(key, test_data_id)  # 删除该提交ID的该条测试数据。从此提交的hash表中删掉。

    @staticmethod
    def get_status(submission_id):
        """
        获取被标记提交的状态信息。
        :param submission_id: SDUSTOJ提交的ID。
        :return: 若提交被标记，返回含有状态信息的字典，键为测试数据ID，值为HUSTOJ提交ID，否则返回None。
        """
        key = Submission._get_key(submission_id)
        if lr.exists(key):  # 本地消息中存在这个提交的info时
            ret = dict()  # 构造一个字典。
            for k, v in lr.hgetall(key).items():  # 该部分提取此提交的ID的所有的hash表中的信息并以k-v的形式遍历。
                ret[int(k.decode('utf-8'))] = int(v.decode('utf-8'))  # 这里按照utf-8格式转码然后转换为int。数据已知。
            return ret  # 返回这个dict<int,int>的字典。
        else:
            return None

    @staticmethod
    def push(submission_id):
        """
        将标记提交放回分析队列，继续下一轮分析。
        :param submission_id:  SDUSTOJ提交的ID。
        :return: 无返回值。
        """
        lr.rpush(sub_analyse_key, submission_id)  # 如描述。将这个ID再放到分析队列末尾。

    @staticmethod
    def analyse_mark_submissions(handler):
        """
        分析处理标记的提交。
        :param handler: 处理函数。
        :return: 无返回值。
        """
        # 这个函数说白了就是封装了从提交解析队列提取下一个待处理项的命令。
        while True:
            info = lr.blpop(sub_analyse_key, timeout=1)
            # blpop：阻塞tmeout秒等待获取list中的第一个值。用于阻塞等待消息。
            # 这里是获得了分析队列中的第一个提交的ID。
            if info is not None:  # 如果阻塞时间过长就只能返回None。
                sid = int(info[1].decode('utf-8'))  # 所以说info不是一个ID吗……为什么要获得[1]？难道是基于blpop的返回值？
                handler(sid)  # 调用回调数对这个信息进行处理
            time.sleep(0.5)  # 线程睡眠0.5s？


def get_command(handler):  # 看起来是用来……接受执行sdustoj的命令的？
    while True:
        info = r.blpop(queue, timeout=1)  # 获得用于接收从sdustoj来的消息队列。然后从里面提取第一个信息。
        if info is not None:
            command = loads(info[1].decode('utf-8'))  # 构造一个json对象？
            handler(command)  # 回调，调用这个json对象。


def get_queue_info(name):  # 看功能是从任意一个list类型的消息队列中pop出来首位的内容返回。提取的地方是sdustoj的消息队列。
    info = r.lpop(name)
    return info


def get_subscribe(handler):  # 看起来是用来产生一个阻塞的编程环境消息订阅器，从sdustoj订阅获得编程语言消息。
    ps = r.pubsub()  # 看功能描述，是产生一个订阅器？
    ps.subscribe(*subscribe)   # 使这个订阅器订阅列表里的编程语言频道。
    while True:
        message = ps.get_message(ignore_subscribe_messages=True)  # 死循环获取下一个订阅频道中的消息。
        if message:
            handler(message)  # 然后将得到的信息处理。
        time.sleep(0.5)  # 睡眠0.5s
