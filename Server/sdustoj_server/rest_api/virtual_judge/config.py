class OjMessage(object):
    name = None
    environments = {}  # 编程环境映射。字典规则为：(创建的编程环境名称:发送消息的名称)

    def __init__(self, name=None, environments=None):
        self.name = name
        self.environments = environments

    def get_env(self, name):
        return self.environments[name] if name in self.environments else None

    def has_env(self, name):
        return name in self.environments

OJ_LIST = {
    'hdu': OjMessage(name='hdu', environments={
        'G++': '0',
        'GCC': '1',
        'C++': '2',
        'C': '3',
        'Pascal': '4',
        'Java': '5',
        'C#': '6'
    }),
    'poj': OjMessage(name='poj', environments={
        'G++': '0',
        'GCC': '1',
        'Java': '2',
        'Pascal': '3',
        'C++': '4',
        'C': '5',
        'Fortran': '6'
    })
}
