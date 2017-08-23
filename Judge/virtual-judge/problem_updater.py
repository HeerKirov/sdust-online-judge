from models.redis_models import get_command


def update_problems(**cmd):
    pass


class Function(object):
    @staticmethod
    def func(cmd):
        pass


class Update(Function):
    update_func = {
        'all': update_problems,
        'meta': update_problems,
        'problem': update_problems
    }

    @staticmethod
    def func(cmd):
        Update.update_func[cmd['type']](**cmd)


func_classes = {
    'update': Update
}


def handler(command):
    func_class = func_classes[command['cmd']]
    func_class.func(command)


# 启动一项服务，轮询从sdustoj来的指令队列。
get_command(handler)
