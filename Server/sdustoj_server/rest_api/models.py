from django.db.models import Model, CASCADE, SET_NULL

from django.db.models import BigAutoField, IntegerField, FloatField
from django.db.models import BooleanField
from django.db.models import CharField, TextField
from django.db.models import DateTimeField
from django.db.models import BinaryField
from django.db.models import ForeignKey, ManyToManyField, OneToOneField
from django.db.models import GenericIPAddressField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField, ArrayField

from config import OJ_SETTINGS, OJ_STATUS_SCORE, OJ_SCORE_SETTING, OJ_FINAL_STATUS
from math import floor

_INPUT_MAX = OJ_SETTINGS['test_data_input_max_size']


# -- Resource ----------------------------------------------------------------------------------------------------------

class Resource(Model):
    """
    SDUSTOJ资源表共有字段。
    """
    # 创建者
    creator = CharField(max_length=150, null=True)
    # 创建时间
    create_time = DateTimeField(auto_now_add=True)
    # 最后一次更新者
    updater = CharField(max_length=150, null=True)
    # 最后一次更新时间
    update_time = DateTimeField(auto_now=True)

    # 是否可用（当前并没什么用……）
    available = BooleanField(default=True)
    # 是否废弃（被废弃将不能被非管理者的任何用户、用户端或评测机发现）
    deleted = BooleanField(default=False)

    class Meta:
        abstract = True


class TitleMixin(Model):
    """
    某些需要由标题和简介的资源的共有字段。
    """
    # 题目
    title = CharField(max_length=128)
    # 简介
    introduction = CharField(max_length=512, null=True)

    class Meta:
        abstract = True


class SourceMixin(Model):
    """
    某些需要记录来源的资源的共有字段。
    """
    # 来源
    source = CharField(max_length=256, null=True)
    # 作者
    author = CharField(max_length=64, null=True)

    class Meta:
        abstract = True


# == Meta Problem ======================================================================================================

class MetaProblem(Resource, TitleMixin, SourceMixin):
    """
    题元表。
    题元是描述、样例、测试数据以及题目的集合。
    出题目时，从题元里选择一个描述、一个样例、以及需要的测试数据。
    """
    # 编号
    id = BigAutoField(primary_key=True)

    # 包含的描述的数量
    number_description = IntegerField(default=0)
    # 包含的样例的数量
    number_sample = IntegerField(default=0)
    # 包含的测试数据的数量
    number_test_data = IntegerField(default=0)
    # 包含的题目的数量
    number_problem = IntegerField(default=0)

    def __str__(self):
        return '<MetaProblem ' + str(self.id) + ': ' + str(self.title) + '>'


# -- Components --------------------------------------------------------------------------------------------------------

class Description(Resource, TitleMixin):
    """
    描述，对于题意和输入输出要求的描述性文字。
    对应一般OJ的Description、Input、和Output。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 所属的题元
    meta_problem = ForeignKey(MetaProblem, related_name='descriptions', to_field='id')

    # 描述正文（建议使用Markdown格式书写）
    content = TextField(null=True)

    # 有多少题目使用了此描述
    number_problem = IntegerField(default=0)

    def __str__(self):
        return '<Description ' + str(self.id) + ' in MetaProblem ' + str(self.meta_problem_id) + '>'


class Sample(Resource, TitleMixin):
    """
    一套样例，对于程序可能的输入以及对应应当输出内容举的例子。
    样例仅为描述性文字，并不参与题目评测。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 所属题元
    meta_problem = ForeignKey(MetaProblem, related_name='samples', to_field='id')

    # 样例正文（建议使用Markdown格式书写）
    content = TextField(null=True)

    # 有多少题目使用了此样例
    number_problem = IntegerField(default=0)

    def __str__(self):
        return '<Sample ' + str(self.id) + ' in MetaProblem ' + str(self.meta_problem_id) + '>'


class TestData(Resource, TitleMixin):
    """
    测试数据。
    评测机在评测提交时将使用此表中的数据。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 所属题元
    meta_problem = ForeignKey(MetaProblem, related_name='test_data', to_field='id')

    # 测试输入的大小
    in_size = IntegerField()
    # 测试输出的大小
    out_size = IntegerField()

    # 测试输入（二进制数据）
    test_in = BinaryField(null=True)
    # 测试输出（二进制数据）
    test_out = BinaryField(null=True)

    # 有多少题目使用了此测试数据
    number_problem = IntegerField(default=0)

    def __str__(self):
        return '<TestData ' + str(self.id) + ' in MetaProblem ' + str(self.meta_problem_id) + '>'

    def get_test_in(self):
        """
        读取测试输入，将二进制数据转换为字符串。
        :return: 字符串，测试输入。
        """
        if self.test_in is None:
            return None
        else:
            return bytes(self.test_in).decode('utf-8', 'ignore')[:_INPUT_MAX]

    def get_test_out(self):
        """
        读取测试输出，将二进制数据转换为字符串。
        :return: 字符串，测试输出。
        """
        if self.test_out is None:
            return None
        else:
            return bytes(self.test_out).decode('utf-8', 'ignore')[: _INPUT_MAX]


# == Problem ===========================================================================================================

class Problem(Resource, TitleMixin, SourceMixin):
    """
    题目。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 所属的题元
    meta_problem = ForeignKey(MetaProblem, related_name='problems', to_field='id')

    # 所选的描述，可为空
    description = ForeignKey(Description, related_name='problems', to_field='id', null=True, on_delete=SET_NULL)
    # 所选的样例，可为空
    sample = ForeignKey(Sample, related_name='problems', to_field='id', null=True, on_delete=SET_NULL)

    # 这道题支持哪几种编程环境的评测
    environments = ManyToManyField('Environment', related_name='problems',
                                   through='Limit', through_fields=('problem', 'environment'))
    # 这道题使用了题元里的哪些测试数据
    test_data = ManyToManyField('TestData', related_name='problems',
                                through='ProblemTestData', through_fields=('problem', 'test_data'))

    # 这道题是否是特殊评测
    is_special_judge = BooleanField(default=False)

    # 这道题的提交有哪些评测机可以评测
    judge = ManyToManyField('Judge', related_name='problem',
                            through='ProblemLimitJudge', through_fields=('problem', 'judge'))

    # 这道题选用的测试数据的数量
    number_test_data = IntegerField(default=0)
    # 这道题的编程限制的数量
    number_limit = IntegerField(default=0)
    # 这道题被哪些目录收录
    number_category = IntegerField(default=0)
    # 这道题被哪些结点收录
    number_node = IntegerField(default=0)
    # 这道题包含多少非法单词
    number_invalid_word = IntegerField(default=0)

    def __str__(self):
        return '<Problem ' + str(self.id) + ': ' + str(self.title) + '>'


# -- Components --------------------------------------------------------------------------------------------------------

class Limit(Resource):
    """
    题目的编程限制。
    提交应在满足相应编程环境对应的编程限制的条件下才能正常运行或获得正确结果，否则将被判为相应的错误。
    不同于大部分OJ，SDUSTOJ的限制是加在具体编程环境上的，不同的环境可能有不同的限制，以满足不同语言的特性。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 所属的题目
    problem = ForeignKey(Problem, related_name='limits', to_field='id')
    # 该编程限制是哪个编程环境的限制
    environment = ForeignKey('Environment', related_name='limits', to_field='id')
    # 编程环境的名称
    env_name = CharField(max_length=128)

    # 被该编程限制作用的提交有哪些评测机可以进行评测
    judge = ManyToManyField('Judge', related_name='limit',
                            through='ProblemLimitJudge', through_fields=('limit', 'judge'))

    # 时间限制
    time_limit = IntegerField(default=-1)
    # 内存限制
    memory_limit = IntegerField(default=-1)
    # 代码长度限制
    length_limit = IntegerField(default=-1)

    def __str__(self):
        return '<Limit %s of Problem %s>' % (self.id, self.problem.id)


class InvalidWord(Resource):
    """
    禁用单词。
    提交的代码中不得出现非法单词，否则将被判为对应错误。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 所属题目
    problem = ForeignKey(Problem, related_name='invalid_words', to_field='id')
    # 单词
    word = CharField(max_length=128)

    def __str__(self):
        return '<InvalidWord %s: %s of Problem %s>' % (self.id, self.word, self.problem.id)


class SpecialJudge(Resource, TitleMixin):
    """
    特殊评测。
    由于废弃字段等原因，一道题目下可以出现多个特殊评测代码，未被废弃的编号最大的特殊评测将作为题目的特殊评测，
    若题目下无特殊评测或特殊评测均未废弃状态，则题目被设定为不存在特殊评测。
    """
    # 所属题目
    problem = ForeignKey(Problem, related_name='special_judge', to_field='id')
    # 特殊评测代码是属于哪个编程环境的（HUSTOJ仅支持C/C++的代码）
    environment = ForeignKey('Environment', related_name='special_judge', to_field='id')

    # 特殊评测代码（二进制数据）
    code = BinaryField()

    def __str__(self):
        return '<Special Judge %s of Problem %s>' % (self.id, self.problem.id)

    def get_code(self):
        """
        获取特殊评测代码，将二进制数据转换为字符串。
        :return: 字符串，特殊评测代码。
        """
        return bytes(self.code).decode('utf-8', 'ignore')


class ProblemTestData(Resource):
    """
    题目和测试数据的关系表。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 题目
    problem = ForeignKey(Problem, related_name='test_data_rel', to_field='id')
    # 测试数据
    test_data = ForeignKey(TestData, related_name='problems_rel', to_field='id')
    # 测试数据在该题目中的分数权重
    weight = FloatField(default=1)

    def __str__(self):
        return 'ProblemTestData relation %s of Problem %s, Test Data %s' % (
            self.id, self.problem.id, self.test_data.id
        )


class ProblemLimitJudge(Model):
    """
    题目、编程限制、评测机之间的关系表。
    """
    # 题目
    problem = ForeignKey(Problem, to_field='id', on_delete=CASCADE)
    # 编程限制
    limit = ForeignKey(Limit, to_field='id', on_delete=CASCADE)
    # 评测机
    judge = ForeignKey('Judge', related_name='p_l_relation', to_field='id', on_delete=CASCADE)


# == Submission ========================================================================================================

class Submission(Model):
    """
    提交记录。
    """
    # 提交记录状态码和对应的状态的映射
    STATUS_CHOICES = (
        ('PD', 'Pending'),
        ('PDR', 'Pending Rejudge'),
        ('CP', 'Compiling'),
        ('CE', 'Compile Error'),
        ('CD', 'Compile Done'),
        ('RJ', 'Running & Judging'),
        ('RN', 'Running'),
        ('RE', 'Runtime Error'),
        ('TLE', 'Time Limit Exceed'),
        ('MLE', 'Memory Limit Exceed'),
        ('OLE', 'Output Limit Exceed'),

        ('IW', 'Invalid Word'),
        ('LLE', 'Length Limit Exceed'),

        ('RD', 'Running Done'),
        ('JD', 'Judging'),
        ('WA', 'Wrong Answer'),
        ('PE', 'Presentation Error'),
        ('UE', 'Punctuation Error'),
        ('AC', 'Accepted'),
    )

    # 编号
    id = BigAutoField(primary_key=True)
    # 所属题目
    problem = ForeignKey(Problem, related_name='submissions', to_field='id')
    # 所属编程环境
    environment = ForeignKey('Environment', related_name='submissions', to_field='id')

    # 运行花费的时间
    time = IntegerField(default=-1)
    # 运行花费的内存
    memory = IntegerField(default=-1)
    # 代码长度
    length = IntegerField(default=-1)

    # 提交的用户
    user = CharField(max_length=150, null=True)
    # 提交所属的竞赛
    contest = CharField(max_length=150, null=True)
    # 来自哪个用户端
    client = ForeignKey('Client', related_name='submissions', to_field='id', null=True, on_delete=SET_NULL)

    # 状态，由各组测试数据的状态合成的总状态
    status = CharField(max_length=4, default='PD', choices=STATUS_CHOICES)
    # 完成度信息
    score_info = FloatField(default=None, null=True)
    # 是否完成了评测
    finished = BooleanField(default=False)

    # 提交时间
    submit_time = DateTimeField(auto_now_add=True)
    # 状态更新时间
    update_time = DateTimeField(auto_now=True)
    # 提交的ip
    ip = GenericIPAddressField()

    # 哪一个评测机评测了这条提交
    judge = ForeignKey('Judge', related_name='submissions', to_field='id', null=True)

    # 提交完成度
    @property
    def score(self):
        if self.score_info is None:
            return self.refresh_score()
        else:
            return self.score_info

    # 刷新提交完成度。数值会自动刷新到数据库并保存。如果刷新失败则不会保存且返回0。
    def refresh_score(self):
        if hasattr(self, 'test_data_status'):
            test_data_weight = {}  # 记录每一条关联测试数据的权重信息([t_id] = weight)
            problem_test_data_relation = self.problem.test_data_rel  # 全部的题目-测试数据关系
            test_data_count = problem_test_data_relation.count()  # 测试数据数目
            for relation in problem_test_data_relation.all():  # 惰性查询：性能损耗点
                test_data_weight[int(relation.test_data.id)] = relation.weight  # 添加新记录

            weight_sum = 0
            score_sum = 0
            final_sum = 0
            for s_id, status in self.test_data_status.status.items():  # 遍历：性能损耗点
                status_name = status['status']
                if status_name in OJ_FINAL_STATUS:
                    final_sum += 1
                score = OJ_STATUS_SCORE[status_name]  # 获取完成度(0~100)
                weight = abs(test_data_weight[int(s_id)])  # 获取权重值(Number)的绝对值
                score_sum += score * weight
                weight_sum += weight
            if test_data_count != final_sum:  # 在测试数据的实际数目不等的状态下，判定该题目还没有判完，退出判定。
                return 0
            final_score = floor(score_sum / weight_sum) if weight_sum != 0 else 0
            self.score_info = final_score if final_score >= OJ_SCORE_SETTING['threshold_score'] else 0
            self.save()
            return self.score_info
        else:
            return 0


# -- Components --------------------------------------------------------------------------------------------------------

class CompileInfo(Model):
    """
    编译信息。
    """
    # 所属的提交
    submission = OneToOneField(Submission, related_name='compile_info', to_field='id', primary_key=True)
    # 编译信息
    info = TextField(null=True)


class TestDataStatus(Model):
    """
    测试数据评测信息，即提交的每组测试数据的评测状态。
    """
    # 所属的提交
    submission = OneToOneField(Submission, related_name='test_data_status', to_field='id', primary_key=True)
    # 状态
    status = JSONField()


class SubmissionCode(Model):
    """
    提交代码。
    """
    # 所属的提交
    submission = OneToOneField(Submission, related_name='code', to_field='id', primary_key=True)
    # 代码
    code = JSONField()


# == Category ==========================================================================================================

class Category(Resource, TitleMixin, SourceMixin):
    """
    题库。
    """
    # 编号
    id = BigAutoField(primary_key=True)

    # 包含的题目数量
    number_problem = IntegerField(default=0)

    # 题库下包含的题目
    problems = ManyToManyField(Problem, related_name='categories',
                               through='CategoryProblem', through_fields=('category', 'problem'))

    def __str__(self):
        return '<Category %s: %s>' % (self.id, self.title)


class CategoryProblem(Resource):
    """
    题库、题目的关系。
    """
    # 题库
    category = ForeignKey(Category, related_name='problem_relations', on_delete=CASCADE)
    # 题目
    problem = ForeignKey(Problem, related_name='category_relations', on_delete=CASCADE)
    # 所在目录
    directory = ArrayField(CharField(max_length=128))


# == Environment =======================================================================================================

class Environment(Resource):
    """
    编程环境
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 供评测机识别用的标识符
    judge_id = CharField(max_length=16, unique=True)
    # 对外显示的名称
    name = CharField(max_length=128)

    # 有多少题目支持此编程环境的评测
    number_problem = IntegerField(default=0)
    # 有多少编程限制属于此编程环境
    number_limit = IntegerField(default=0)
    # 有多少评测机能够评测此编程环境的提交
    number_judge = IntegerField(default=0)

    def __str__(self):
        return '<Environment ' + str(self.id) + ': ' + str(self.name) + '>'


class Judge(Resource):
    """
    评测机。
    """
    # 编号
    id = BigAutoField(primary_key=True)

    # 评测机的名称
    name = CharField(max_length=128)
    # 评测机的说明信息
    info = TextField(null=True)

    # 最后一次更新题目的时间
    last_update = DateTimeField(null=True)
    # 用于接收命令的Redis队列名称
    cmd_queue = CharField(max_length=64)
    # 支持评测哪些评测编程环境
    environment = ManyToManyField(to=Environment, related_name='judge')


# == Client ============================================================================================================

class Client(Resource):
    """
    使用此评测端的用户端。
    """
    # 编号
    id = BigAutoField(primary_key=True)
    # 绑定的用户（用于进行身份识别）
    user = OneToOneField(User, related_name='client')

    # 名称
    name = CharField(max_length=128)
    # 简介
    introduction = TextField()
    # 是否允许使用本端全部题库及题目
    allow_all = BooleanField(default=False)

    # 可用的题库数量
    number_category = IntegerField(default=0)
    # 可用的题目数量
    number_problem = IntegerField(default=0)

    # 允许此用户端使用的题库
    categories = ManyToManyField(Category, related_name='clients',
                                 through='ClientCategory', through_fields=('client', 'category'))


class ClientCategory(Resource):
    """
    用户端与题库的关系。
    """
    # 编号
    id = BigAutoField(primary_key=True)

    # 用户端
    client = ForeignKey(Client, related_name='category_relation', on_delete=CASCADE)
    # 题库
    category = ForeignKey(Category, related_name='client_relation', on_delete=CASCADE)
