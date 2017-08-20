class VirtualException(Exception):
    pass


class VirtualProblem(object):
    oj = None  # 题目的来源oj
    pid = None  # 题目的pid
    title = None  # 标题
    introduction = None  # 简介
    description = None  # 包括描述与输入输出说明，采用md语法
    sample = None  # 包括输入输出样例，采用md语法
    author = None  # 作者
    source = None  # 来源
    limits = {}

    def __init__(self, oj, pid, title, introduction, description, sample, time={}, memory={}, author=None, source=None):
        self.oj = oj
        self.pid = pid
        self.title = title
        self.introduction = introduction
        self.description = description
        self.sample = sample
        self.author = author
        self.source = source
        for k, v in time.items():
            if k not in self.limits or self.limits[k] is None:
                self.limits[k] = {}
            self.limits[k]['time'] = v
        for k, v in memory.items():
            if k not in self.limits or self.limits[k] is None:
                self.limits[k] = {}
            self.limits[k]['memory'] = v
