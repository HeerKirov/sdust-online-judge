from rest_framework.serializers import ModelSerializer, SlugRelatedField, CharField, PrimaryKeyRelatedField, FloatField
from rest_framework.serializers import ListField
from rest_framework.serializers import FileField
from rest_framework.serializers import ValidationError

from .models import MetaProblem, Description, Sample, TestData
from .models import Problem, ProblemTestData, Limit, InvalidWord, SpecialJudge, ProblemLimitJudge
from .models import Submission, CompileInfo, TestDataStatus, SubmissionCode
from .models import Category, CategoryProblem
from .models import Environment, Judge
from .models import Client, ClientCategory

from .permissions import GROUP_NAME_CLIENT

from django.contrib.auth.models import Group

from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from config import OJ_SETTINGS


_RESOURCE_READONLY = ('creator', 'updater', 'create_time', 'update_time')
_RESOURCE_KWARGS = {
    'available': {'required': False, 'default': True},
    'deleted': {'required': False, 'default': False}
}
_RESOURCE_TITLE_KWARGS = {
    'available': {'required': False, 'default': True},
    'deleted': {'required': False, 'default': False},
    'introduction': {'required': False},
    'source': {'required': False},
    'author': {'required': False}
}

_INPUT_MAX = OJ_SETTINGS['test_data_input_max_size']


class Utils:
    @staticmethod
    def check_in_meta(obj_name, validated_data, instance=None):
        obj = validated_data.get(obj_name)
        if instance is None:
            meta_problem = validated_data['meta_problem']
        else:
            meta_problem = instance.meta_problem

        if obj is not None and obj.meta_problem != meta_problem:
            raise ValidationError('Cannot choose components from other meta problem.')


class EnvironmentSerializers:
    class EnvironmentAdminSerializer(ModelSerializer):
        class Meta:
            model = Environment
            fields = '__all__'
            read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                     'number_limit',
                                                     'number_judge')

            extra_kwargs = _RESOURCE_KWARGS

        def update(self, instance, validated_data):
            instance = super().update(instance, validated_data)
            instance.limits.update(env_name=instance.name)
            return instance

    class EnvironmentSerializer(ModelSerializer):
        class Meta:
            model = Environment
            fields = ('id', 'name', 'create_time', 'update_time')

    class JudgeAdminSerializer(ModelSerializer):
        class Meta:
            model = Judge
            fields = '__all__'
            read_only_fields = _RESOURCE_READONLY + ('last_update', )
            extra_kwargs = {
                'environment': {
                    'required': False,
                    'allow_null': True
                }
            }


class MetaProblemSerializers:
    # -- Meta Problems ----------------------------------------------------------------------------
    class MetaProblemAdminSerializer(ModelSerializer):
        class Meta:
            model = MetaProblem
            fields = '__all__'
            read_only_fields = _RESOURCE_READONLY + ('number_description',
                                                     'number_sample',
                                                     'number_test_date',
                                                     'number_problem',
                                                     'number_test_data')

            extra_kwargs = _RESOURCE_TITLE_KWARGS

    # -- Components -------------------------------------------------------------------------------
    class Description:
        class DescriptionAdminListSerializer(ModelSerializer):
            class Meta:
                model = Description
                exclude = ('meta_problem', )

                read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                         'meta_problem')
                extra_kwargs = {
                    'content': {'write_only': True}
                }

        class DescriptionAdminInstanceSerializer(ModelSerializer):
            class Meta:
                model = Description
                exclude = ('meta_problem', )

                read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                         'meta_problem')

    class Sample:
        class SampleAdminListSerializer(ModelSerializer):
            class Meta:
                model = Sample
                fields = '__all__'

                read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                         'meta_problem')
                extra_kwargs = {
                    'content': {'write_only': True}
                }

        class SampleAdminInstanceSerializer(ModelSerializer):
            class Meta:
                model = Sample
                fields = '__all__'

                read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                         'meta_problem')

    class TestData:
        class TestDataAdminListSerializer(ModelSerializer):
            test_in = CharField(write_only=True, allow_null=True, max_length=_INPUT_MAX,
                                style={'base_template': 'textarea.html'})
            test_out = CharField(write_only=True, allow_null=True, max_length=_INPUT_MAX,
                                 style={'base_template': 'textarea.html'})

            test_in_file = FileField(write_only=True, allow_null=True, required=False)
            test_out_file = FileField(write_only=True, allow_null=True, required=False)

            class Meta:
                model = TestData
                fields = '__all__'
                read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                         'meta_problem',
                                                         'in_size', 'out_size')

            def create(self, validated_data):
                test_in = validated_data.pop('test_in', None)
                test_out = validated_data.pop('test_out', None)
                in_size = 0
                out_size = 0
                test_in_file = validated_data.pop('test_in_file', None)
                test_out_file = validated_data.pop('test_out_file', None)

                if test_in_file is not None:
                    test_in = b''
                    for b in test_in_file.chunks():
                        test_in += b
                    in_size = test_in_file.size
                elif test_in is not None:
                    test_in = test_in.encode('utf-8')
                    in_size = len(test_in)
                else:
                    test_in = None

                if test_out_file is not None:
                    test_out = b''
                    for b in test_out_file.chunks():
                        test_out += b
                    out_size = test_out_file.size
                elif test_out is not None:
                    test_out = test_out.encode('utf-8')
                    out_size = len(test_out)
                else:
                    test_out = None

                print(test_in)

                validated_data['test_in'] = test_in
                validated_data['in_size'] = in_size
                validated_data['test_out'] = test_out
                validated_data['out_size'] = out_size

                return super().create(validated_data)

        class TestDataAdminInstanceSerializer(ModelSerializer):
            test_in = CharField(allow_null=True, max_length=_INPUT_MAX, source='get_test_in',
                                style={'base_template': 'textarea.html'})
            test_out = CharField(allow_null=True, max_length=_INPUT_MAX, source='get_test_out',
                                 style={'base_template': 'textarea.html'})
            test_in_file = FileField(write_only=True, allow_null=True, required=False)
            test_out_file = FileField(write_only=True, allow_null=True, required=False)

            class Meta:
                model = TestData
                fields = '__all__'
                read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                         'meta_problem',
                                                         'in_size', 'out_size')

            def update(self, instance, validated_data):
                if 'get_test_in' in validated_data or 'test_in_file' in validated_data:
                    test_in = validated_data.pop('get_test_in', None)
                    test_in_file = validated_data.pop('test_in_file', None)
                    if test_in_file is not None:
                        test_in = b''
                        for b in test_in_file.chunks():
                            test_in += b
                        in_size = test_in_file.size
                    elif test_in is not None:
                        test_in = test_in.encode('utf-8')
                        in_size = len(test_in)
                    else:
                        test_in = None
                        in_size = 0
                    validated_data['test_in'] = test_in
                    validated_data['in_size'] = in_size
                if 'get_test_out' in validated_data or 'test_out_file' in validated_data:
                    test_out = validated_data.pop('get_test_out', None)
                    test_out_file = validated_data.pop('test_out_file', None)
                    if test_out_file is not None:
                        test_out = b''
                        for b in test_out_file.chunks():
                            test_out += b
                        out_size = test_out_file.size
                    elif test_out is not None:
                        test_out = test_out.encode('utf-8')
                        out_size = len(test_out)
                    else:
                        test_out = None
                        out_size = 0
                    validated_data['test_out'] = test_out
                    validated_data['out_size'] = out_size

                return super().update(instance, validated_data)

    class Problem:
        # -- Problem ----------------------------------------------------------
        class ProblemAdminListSerializer(ModelSerializer):
            description_id = PrimaryKeyRelatedField(
                queryset=Description.objects.all(), source='description', many=False, allow_null=True
            )
            sample_id = PrimaryKeyRelatedField(
                queryset=Sample.objects.all(), source='sample', many=False, allow_null=True
            )

            class Meta:
                model = Problem
                exclude = ('test_data', 'environments', 'description', 'sample', 'meta_problem', 'judge')
                read_only_fields = _RESOURCE_READONLY + ('is_special_judge',
                                                         'number_test_data',
                                                         'number_limit',
                                                         'number_category',
                                                         'number_node',
                                                         'number_invalid_word')

            def create(self, validated_data):
                Utils.check_in_meta(obj_name='description', validated_data=validated_data)
                Utils.check_in_meta(obj_name='sample', validated_data=validated_data)
                return super().create(validated_data)

        class ProblemAdminInstanceSerializer(ModelSerializer):
            class LimitField(ModelSerializer):
                class Meta:
                    model = Limit
                    exclude = ('problem', 'judge')
                    read_only_fields = _RESOURCE_READONLY + ('env_name',)

            class DescriptionField(ModelSerializer):
                class Meta:
                    model = Description
                    exclude = ('meta_problem', 'number_problem')

                    read_only_fields = _RESOURCE_READONLY

            class SampleField(ModelSerializer):
                class Meta:
                    model = Sample
                    exclude = ('meta_problem', 'number_problem')

                    read_only_fields = _RESOURCE_READONLY

            # test_data = MetaTestDataAdminListSerializer(many=True, read_only=True)
            limits = LimitField(many=True, read_only=True)
            description = DescriptionField(many=False, read_only=True)
            sample = SampleField(many=False, read_only=True)
            description_id = PrimaryKeyRelatedField(
                queryset=Description.objects.all(), many=False, required=False, allow_null=True
            )
            sample_id = PrimaryKeyRelatedField(
                queryset=Sample.objects.all(), many=False, required=False, allow_null=True
            )

            class Meta:
                model = Problem
                exclude = ('environments', 'test_data', 'meta_problem', 'judge')
                read_only_fields = _RESOURCE_READONLY + ('is_special_judge',
                                                         'number_test_data',
                                                         'number_limit',
                                                         'number_category',
                                                         'number_node',
                                                         'number_invalid_word')

            def update(self, instance, validated_data):
                validated_data['description'] = validated_data.get('description_id')
                validated_data['sample'] = validated_data.get('sample_id')

                Utils.check_in_meta(obj_name='description', validated_data=validated_data, instance=instance)
                Utils.check_in_meta(obj_name='sample', validated_data=validated_data, instance=instance)

                return super().update(instance, validated_data)

        # -- Components -------------------------------------------------------
        class Limit:
            class LimitAdminListSerializer(ModelSerializer):
                class Meta:
                    model = Limit
                    exclude = ('problem', 'judge')
                    read_only_fields = _RESOURCE_READONLY + ('problem', 'env_name')

                def create(self, validated_data):
                    environment = validated_data['environment']
                    problem = validated_data['problem']
                    if problem.limits.filter(environment=environment).exists():
                        raise ValidationError('Environment exists.')
                    validated_data['env_name'] = environment.name
                    return super().create(validated_data)

            class LimitAdminInstanceSerializer(ModelSerializer):
                class Meta:
                    model = Limit
                    exclude = ('problem', 'judge')
                    read_only_fields = _RESOURCE_READONLY + ('problem', 'environment', 'env_name',)

        class TestData:
            class TestDataRelAdminListSerializer(ModelSerializer):
                class TestDataField(ModelSerializer):
                    class Meta:
                        model = TestData
                        exclude = ('meta_problem', 'test_in', 'test_out')
                        read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                                 'in_size', 'out_size')

                class Meta:
                    model = ProblemTestData
                    exclude = ('problem',)
                    read_only_fields = _RESOURCE_READONLY

                def create(self, validated_data):
                    test_data = validated_data['test_data']
                    problem = validated_data['problem']
                    if ProblemTestData.objects.filter(problem=problem, test_data=test_data).exists():
                        raise ValidationError('Test data exists.')
                    Utils.check_in_meta('test_data', validated_data, problem)
                    return super().create(validated_data)

            class TestDataRelAdminInstanceSerializer(ModelSerializer):
                class TestDataField(ModelSerializer):
                    class Meta:
                        model = TestData
                        exclude = ('meta_problem', 'test_in', 'test_out')
                        read_only_fields = _RESOURCE_READONLY + ('number_problem',
                                                                 'in_size', 'out_size')

                # problem = MetaProblemAdminListSerializer(many=False, read_only=True)
                test_data = TestDataField(many=False, read_only=True)

                class Meta:
                    model = ProblemTestData
                    exclude = ('problem',)
                    read_only_fields = _RESOURCE_READONLY + ('test_data',)

        class InvalidWord:
            class InvalidWordAdminSerializer(ModelSerializer):
                class Meta:
                    model = InvalidWord
                    exclude = ('problem',)
                    read_only_fields = _RESOURCE_READONLY

        class SpecialJudge:
            class SpecialJudgeAdminListSerializer(ModelSerializer):
                code = CharField(write_only=True, max_length=_INPUT_MAX,
                                 style={'base_template': 'textarea.html'})

                class Meta:
                    model = SpecialJudge
                    exclude = ('problem',)
                    read_only_fields = _RESOURCE_READONLY

                def create(self, validated_data):
                    code = validated_data.pop('code')
                    validated_data['code'] = code.encode('utf-8')
                    return super().create(validated_data)

            class SpecialJudgeAdminInstanceSerializer(ModelSerializer):
                code = CharField(source='get_code',
                                 style={'base_template': 'textarea.html'})

                class Meta:
                    model = SpecialJudge
                    exclude = ('problem',)
                    read_only_fields = _RESOURCE_READONLY

                def update(self, instance, validated_data):
                    code = validated_data.pop('get_code')
                    validated_data['code'] = code.encode('utf-8')
                    return super().update(instance, validated_data)


class ProblemSerializers:
    class ProblemListSerializer(ModelSerializer):
        class Meta:
            model = Problem
            exclude = ('test_data', 'environments', 'description', 'sample', 'meta_problem', 'judge',
                       'creator', 'updater', 'available', 'deleted')

    class ProblemInstanceSerializer(ModelSerializer):
        class LimitField(ModelSerializer):
            class Meta:
                model = Limit
                fields = ('environment', 'env_name', 'time_limit', 'memory_limit', 'length_limit')

        limits = LimitField(many=True, read_only=True)
        description = SlugRelatedField(many=False, read_only=True, slug_field='content')
        sample = SlugRelatedField(many=False, read_only=True, slug_field='content')

        class Meta:
            model = Problem
            exclude = ('test_data', 'environments', 'meta_problem', 'judge', 'creator', 'updater',
                       'available', 'deleted')

    class ProblemAdminListSerializer(ModelSerializer):
        class Meta:
            model = Problem
            exclude = ('test_data', 'environments', 'description', 'sample', 'meta_problem', 'judge')

    class ProblemAdminInstanceSerializer(ModelSerializer):
        class LimitField(ModelSerializer):
            class Meta:
                model = Limit
                fields = ('environment', 'env_name', 'time_limit', 'memory_limit', 'length_limit')

        limits = LimitField(many=True, read_only=True)
        description = SlugRelatedField(many=False, read_only=True, slug_field='content')
        sample = SlugRelatedField(many=False, read_only=True, slug_field='content')

        class Meta:
            model = Problem
            exclude = ('test_data', 'environments', 'meta_problem', 'judge')

    class Admin:
        class ProblemAdminListSerializer(ModelSerializer):
            class LimitField(ModelSerializer):
                class Meta:
                    model = Limit
                    fields = ('environment', 'time_limit', 'memory_limit', 'length_limit')

            class TestDataField(ModelSerializer):
                test_in = CharField(write_only=True, allow_null=True, max_length=_INPUT_MAX, default="",
                                    required=False,
                                    style={'base_template': 'textarea.html'})
                test_out = CharField(write_only=True, allow_null=True, max_length=_INPUT_MAX, default="",
                                     style={'base_template': 'textarea.html'})

                weight = FloatField(write_only=True, allow_null=True, default=1, required=False)

                class Meta:
                    model = TestData
                    fields = ('test_in', 'test_out', 'title', 'introduction', 'weight')

            class SpecialJudgeField(ModelSerializer):
                code = CharField(write_only=True, allow_null=True, max_length=_INPUT_MAX, default="",
                                 style={'base_template': 'textarea.html'})
                environment = PrimaryKeyRelatedField(queryset=Environment.objects.all(), many=False, write_only=True)

                class Meta:
                    model = SpecialJudge
                    fields = ('environment', 'code')

            class InvalidWordField(ListField):
                child = CharField(max_length=128, write_only=True)

            description = CharField(write_only=True, allow_null=True, max_length=_INPUT_MAX,
                                    required=False,
                                    style={'base_template': 'textarea.html'})
            sample = CharField(write_only=True, allow_null=True, max_length=_INPUT_MAX,
                               required=False,
                               style={'base_template': 'textarea.html'})
            limits = LimitField(many=True, write_only=True)
            test_data = TestDataField(many=True, write_only=True)
            special_judge = SpecialJudgeField(many=False, write_only=False, required=False)
            invalid_words = InvalidWordField(required=False, write_only=True)

            class Meta:
                model = Problem
                exclude = ('environments', 'judge')
                read_only_fields = _RESOURCE_READONLY + (
                    'number_test_data', 'number_limit', 'number_category', 'number_node', 'number_invalid_word',
                    'meta_problem'
                )

            def create(self, validated_data):
                """
                创建独立题目。
                :param validated_data: Serializer传入的合法数据。
                :return: 创建后的题目实例。
                """
                # 获取用户信息
                creator = validated_data.pop('creator')
                updater = validated_data.pop('updater')
                title = validated_data.pop('title')
                introduction = validated_data.pop('introduction', None)
                source = validated_data.pop('source', None)
                author = validated_data.pop('author', None)
                available = validated_data.pop('available', True)
                deleted = validated_data.pop('deleted', False)

                # == 创建题元及组件 ==============================
                # 创建题元
                meta_problem = MetaProblem(
                    creator=creator,
                    updater=updater,
                    available=available,
                    deleted=deleted,
                    title=str(title) + ' Meta',
                    introduction=introduction,
                    source=source,
                    author=author,
                    number_description=1,
                    number_sample=1,
                    number_problem=1,
                    number_test_data=len(validated_data['test_data'])
                )
                meta_problem.save()
                # 创建描述
                d_content = validated_data.pop('description', None)
                if d_content is not None:
                    description = Description(
                        creator=creator,
                        updater=updater,
                        available=available,
                        deleted=deleted,
                        title=str(title) + ' Description',
                        introduction='Auto-generated description.',
                        meta_problem=meta_problem,
                        content=d_content
                    )
                    description.save()
                else:
                    description = None
                # 创建样例
                s_content = validated_data.pop('sample', None)
                if s_content is not None:
                    sample = Sample(
                        creator=creator,
                        updater=updater,
                        available=available,
                        deleted=deleted,
                        title=str(title) + ' Sample',
                        introduction='Auto-generated sample.',
                        meta_problem=meta_problem,
                        content=s_content
                    )
                    sample.save()
                else:
                    sample = None
                # 创建测试数据
                test_data = validated_data.pop('test_data')
                test_data_bulk_create = []
                for td in test_data:
                    t_title = td.get('title')
                    t_introduction = td.get('introduction')
                    test_in = td.get('test_in')
                    test_out = td.get('test_out')
                    weight = td.get('weight')
                    data = TestData(
                        creator=creator,
                        updater=updater,
                        available=available,
                        deleted=deleted,
                        title=t_title,
                        introduction=t_introduction,
                        in_size=len(test_in),
                        out_size=len(test_out),
                        test_in=test_in.encode('utf-8'),
                        test_out=test_out.encode('utf-8'),
                        meta_problem=meta_problem
                    )
                    test_data_bulk_create.append((data, weight))
                TestData.objects.bulk_create((d for d, _ in test_data_bulk_create))
                # == 创建题目及组件 ==============================
                # 创建题目
                is_special_judge = validated_data.pop('is_special_judge', False)
                if is_special_judge and \
                        ('special_judge' not in validated_data or validated_data['special_judge'] is None):
                    is_special_judge = False
                problem = Problem(
                    creator=creator,
                    updater=updater,
                    available=available,
                    deleted=deleted,
                    title=str(title),
                    introduction=introduction,
                    source=source,
                    author=author,
                    description=description,
                    sample=sample,
                    is_special_judge=is_special_judge,
                    meta_problem=meta_problem,
                    number_limit=len(validated_data['limits']),
                    number_test_data=len(test_data_bulk_create)
                )
                problem.save()
                # 创建题目限制
                limits = validated_data.get('limits')
                limit_bulk_create = []
                for limit in limits:
                    environment = limit.get('environment')
                    time_limit = limit.get('time_limit', -1)
                    memory_limit = limit.get('memory_limit', -1)
                    length_limit = limit.get('length_limit', -1)
                    limit = Limit(
                        creator=creator,
                        updater=updater,
                        available=available,
                        deleted=deleted,
                        problem=problem,
                        environment=environment,
                        env_name=environment.name,
                        time_limit=time_limit,
                        memory_limit=memory_limit,
                        length_limit=length_limit
                    )
                    limit_bulk_create.append(limit)
                Limit.objects.bulk_create(limit_bulk_create)
                # 创建特殊评测
                if is_special_judge:
                    special_judge_code = validated_data.pop('special_judge')
                    special_judge = SpecialJudge(
                        creator=creator,
                        updater=updater,
                        available=available,
                        deleted=deleted,
                        title=str(title) + ' Special Judge',
                        introduction='Auto-generated special judge.',
                        problem=problem,
                        environment=special_judge_code['environment'],
                        code=special_judge_code['code'].encode('utf-8')
                    )
                    special_judge.save()
                # 创建禁用单词
                invalid_words = validated_data.pop('invalid_words', None)
                if invalid_words is not None:
                    iw_bulk_create = []
                    for word in invalid_words:
                        iw_bulk_create.append(InvalidWord(
                            creator=creator,
                            updater=updater,
                            available=available,
                            deleted=deleted,
                            problem=problem,
                            word=word
                        ))
                    InvalidWord.objects.bulk_create(iw_bulk_create)
                    problem.number_invalid_word = len(iw_bulk_create)
                    problem.save()
                # 建立题目与测试数据的关系
                pt_relation = []
                for test_data, test_data_weight in test_data_bulk_create:
                    pt_relation.append(ProblemTestData(
                        creator=creator,
                        updater=updater,
                        available=available,
                        deleted=deleted,
                        problem=problem,
                        test_data=test_data,
                        weight=test_data_weight
                    ))
                ProblemTestData.objects.bulk_create(pt_relation)
                # 建立题目、限制和评测机之间的关系（哪些评测机能评测这道题）
                ptl_bulk_create = []
                for limit in limit_bulk_create:
                    judges = limit.environment.judge.all()
                    for judge in judges:
                        ptl_bulk_create.append(ProblemLimitJudge(
                            problem=problem,
                            limit=limit,
                            judge=judge
                        ))
                ProblemLimitJudge.objects.bulk_create(ptl_bulk_create)
                return problem

        class ProblemAdminInstanceSerializer(ModelSerializer):
            class LimitField(ModelSerializer):
                class Meta:
                    model = Limit
                    fields = ('environment', 'env_name', 'time_limit', 'memory_limit', 'length_limit')

            limits = LimitField(many=True, read_only=True)
            description = SlugRelatedField(many=False, read_only=True, slug_field='content')
            sample = SlugRelatedField(many=False, read_only=True, slug_field='content')

            class Meta:
                model = Problem
                exclude = ('test_data', 'environments', 'judge')


class UserSerializers:
    class LoginSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'password')
            extra_kwargs = {
                'username': {'write_only': True,
                             'validators': [RegexValidator()]},
                'password': {'write_only': True,
                             'style': {'input_type': 'password'}}
            }

    class UserAdminSerializer(ModelSerializer):
        groups = SlugRelatedField(
            queryset=Group.objects.all(),
            many=True,
            slug_field='name'
        )

        class Meta:
            model = User
            fields = ('username', 'password',
                      'first_name', 'last_name', 'email',
                      'is_active', 'groups', 'date_joined', 'last_login')
            read_only_fields = ('date_joined', 'last_login')
            extra_kwargs = {
                'password': {'write_only': True,
                             'style': {'input_type': 'password'}}
            }

        def create(self, validated_data):
            instance = super().create(validated_data)
            instance.set_password(instance.password)
            instance.save()
            return instance

        def update(self, instance, validated_data):
            instance = super().update(instance, validated_data)
            instance.set_password(instance.password)
            instance.save()
            return instance

    class UserInfoSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name', 'email')
            read_only_fields = ('username', )

    class UserPasswordSerializer(ModelSerializer):
        old_password = CharField(write_only=True, style={'input_type': 'password'})
        new_password = CharField(write_only=True, style={'input_type': 'password'})
        confirmation = CharField(write_only=True, style={'input_type': 'password'})

        class Meta:
            model = User
            fields = ('username', 'old_password', 'new_password', 'confirmation')
            read_only_fields = ('username', )


class SubmissionSerializers:
    # -- Submission -------------------------------------------------------------------------------
    class SubmissionListSerializer(ModelSerializer):
        problem_id = PrimaryKeyRelatedField(
            queryset=Problem.objects.all(), source='problem', many=False, allow_null=False
        )
        env_id = PrimaryKeyRelatedField(
            queryset=Environment.objects.all(), source='environment', many=False, allow_null=False
        )
        environment = SlugRelatedField(many=False, read_only=True, slug_field='name')
        code = CharField(allow_null=False, max_length=_INPUT_MAX, write_only=True,
                         style={'base_template': 'textarea.html'})
        status_word = CharField(source='get_status_display', read_only=True)
        score = FloatField(read_only=True)

        class Meta:
            model = Submission
            exclude = ('problem', 'client', 'judge', 'score_info')
            read_only_fields = ('time', 'memory', 'length',
                                'status', 'finished',
                                'submit_time', 'update_time', 'ip', 'score')

        def create(self, validated_data):
            code = validated_data.pop('code')
            validated_data['length'] = len(code)

            instance = super().create(validated_data)
            # 创建编译信息
            instance.compile_info = CompileInfo()
            instance.compile_info.save()
            # 创建测试数据评测信息
            instance.test_data_status = TestDataStatus()
            status = {}
            for test_data in instance.problem.test_data.all():
                status[test_data.id] = {
                    'time': -1,
                    'memory': -1,
                    'status': ''
                }
            instance.test_data_status.status = status
            instance.test_data_status.save()
            # 录入提交代码
            instance.code = SubmissionCode()
            instance.code.code = {
                'code': code
            }
            instance.code.save()
            return instance

    class SubmissionAdminListSerializer(ModelSerializer):
        problem_id = PrimaryKeyRelatedField(
            queryset=Problem.objects.all(), source='problem', many=False, allow_null=False
        )
        env_id = PrimaryKeyRelatedField(
            queryset=Environment.objects.all(), source='environment', many=False, allow_null=False
        )
        environment = SlugRelatedField(many=False, read_only=True, slug_field='name')
        code = CharField(allow_null=False, max_length=_INPUT_MAX, write_only=True,
                         style={'base_template': 'textarea.html'})
        status_word = CharField(source='get_status_display', read_only=True)

        score = FloatField(read_only=True)

        class Meta:
            model = Submission
            exclude = ('problem', 'score_info')
            read_only_fields = ('time', 'memory', 'length',
                                'user', 'status', 'finished',
                                'submit_time', 'update_time', 'ip', 'judge', 'score')

        def create(self, validated_data):
            code = validated_data.pop('code')
            validated_data['length'] = len(code)

            instance = super().create(validated_data)
            # 创建编译信息
            instance.compile_info = CompileInfo()
            instance.compile_info.save()
            # 创建测试数据评测信息
            instance.test_data_status = TestDataStatus()
            status = {}
            for test_data in instance.problem.test_data.all():
                status[test_data.id] = {
                    'time': -1,
                    'memory': -1,
                    'status': ''
                }
            instance.test_data_status.status = status
            instance.test_data_status.save()
            # 录入提交代码
            instance.code = SubmissionCode()
            instance.code.code = {
                'code': code
            }
            instance.code.save()
            return instance

    class SubmissionInstanceSerializer(ModelSerializer):
        problem_id = PrimaryKeyRelatedField(source='problem', many=False, allow_null=False, read_only=True)
        environment = SlugRelatedField(many=False, read_only=True, slug_field='name')
        compile_info = SlugRelatedField(many=False, read_only=True, slug_field='info')
        test_data_status = SlugRelatedField(many=False, read_only=True, slug_field='status')
        code = SlugRelatedField(many=False, read_only=True, slug_field='code')
        score = FloatField(read_only=True)

        class Meta:
            model = Submission
            exclude = ('problem', 'judge', 'client', 'score_info')
            read_only_fields = ('time', 'memory', 'length',
                                'user', 'contest', 'status', 'finished',
                                'submit_time', 'update_time', 'ip', 'score')

        def update(self, instance, validated_data):
            ret = super().update(instance, validated_data)
            ret.compile_info.info = ''
            ret.compile_info.save()
            status = {}
            for test_data in instance.problem.test_data.all():
                status[test_data.id] = {
                    'time': -1,
                    'memory': -1,
                    'status': ''
                }
            instance.test_data_status.status = status
            instance.test_data_status.save()
            return ret

    class SubmissionAdminInstanceSerializer(ModelSerializer):
        problem_id = PrimaryKeyRelatedField(source='problem', many=False, allow_null=False, read_only=True)
        environment = SlugRelatedField(many=False, read_only=True, slug_field='name')
        score = FloatField(read_only=True)

        class Meta:
            model = Submission
            exclude = ('problem', 'score_info')
            read_only_fields = ('time', 'memory', 'length',
                                'user', 'contest', 'status', 'finished',
                                'submit_time', 'update_time', 'ip', 'judge', 'client', 'score')

        def update(self, instance, validated_data):
            ret = super().update(instance, validated_data)
            ret.compile_info.info = ''
            ret.compile_info.save()
            status = {}
            for test_data in instance.problem.test_data.all():
                status[test_data.id] = {
                    'time': -1,
                    'memory': -1,
                    'status': ''
                }
            instance.test_data_status.status = status
            instance.test_data_status.save()
            return ret

    # -- Components -------------------------------------------------------------------------------
    class CompileInfo:
        class CompileInfoSerializer(ModelSerializer):
            class Meta:
                model = CompileInfo
                exclude = ('submission', )

    class TestDataStatus:
        class TestDataStatusSerializer(ModelSerializer):
            class Meta:
                model = TestDataStatus
                exclude = ('submission', )

    class SubmissionCode:
        class SubmissionCodeSerializer(ModelSerializer):
            class Meta:
                model = SubmissionCode
                exclude = ('submission', )


class CategorySerializers:
    class CategorySerializer(ModelSerializer):
        class Meta:
            model = Category
            exclude = ('problems', 'creator', 'updater', 'available', 'deleted')
            read_only_fields = _RESOURCE_READONLY + ('number_problem', 'number_node')

    class CategoryAdminSerializer(ModelSerializer):
        class Meta:
            model = Category
            exclude = ('problems', )
            read_only_fields = _RESOURCE_READONLY + ('number_problem', 'number_node')

    class ProblemSerializer(ModelSerializer):
        class ProblemField(ModelSerializer):
            class Meta:
                model = Problem
                fields = ('id', 'title', 'introduction', 'source', 'author',
                          'create_time', 'update_time', 'is_special_judge',
                          'number_test_data', 'number_limit', 'number_category', 'number_invalid_word')

        problem = ProblemField(many=False, read_only=True)

        class Meta:
            model = CategoryProblem
            exclude = ('category', 'creator', 'updater', 'available', 'deleted')
            read_only_fields = _RESOURCE_READONLY

    class ProblemAdminSerializer(ModelSerializer):
        class ProblemField(ModelSerializer):
            class Meta:
                model = Problem
                fields = ('id', 'title', 'introduction', 'source', 'author',
                          'create_time', 'update_time', 'is_special_judge',
                          'number_test_data', 'number_limit', 'number_category', 'number_invalid_word')

        problem_id = PrimaryKeyRelatedField(
            queryset=Problem.objects.all(), source='problem', many=False, allow_null=False, write_only=True
        )
        problem = ProblemField(many=False, read_only=True)

        class Meta:
            model = CategoryProblem
            exclude = ('category', )
            read_only_fields = _RESOURCE_READONLY


class ClientSerializers:
    class UserAdminSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'password',
                      'first_name', 'last_name', 'email',
                      'is_active', 'date_joined', 'last_login')
            read_only_fields = ('date_joined', 'last_login')
            extra_kwargs = {
                'password': {'write_only': True,
                             'style': {'input_type': 'password'}}
            }

        def create(self, validated_data):
            instance = super().create(validated_data)
            instance.set_password(instance.password)
            instance.save()
            group = Group.objects.filter(name=GROUP_NAME_CLIENT).first()
            instance.groups.add(group)
            return instance

        def update(self, instance, validated_data):
            instance = super().update(instance, validated_data)
            instance.set_password(instance.password)
            instance.save()
            return instance

    class ClientAdminSerializer(ModelSerializer):
        user = SlugRelatedField(queryset=User.objects.all(), slug_field='username')

        class Meta:
            model = Client
            exclude = ('categories', )
            read_only_fields = _RESOURCE_READONLY + ('number_problem', 'number_category')

        def create(self, validated_data):
            user = validated_data['user']
            if not user.groups.filter(name=GROUP_NAME_CLIENT).exists():
                raise ValidationError('user not exists')
            if Client.objects.filter(user=user).exists():
                raise ValidationError('user already attached to other client.')
            return super().create(validated_data)

        def update(self, instance, validated_data):
            user = validated_data.get('user', None)
            if (user is not None) and (not user.groups.filter(name=GROUP_NAME_CLIENT).exists()):
                raise ValidationError('user not exists')
            if user != instance.user and Client.objects.filter(user=user).exists():
                raise ValidationError('user already attached to other client.')
            return super().update(instance, validated_data)

    class ClientCategoryAdminSerializer(ModelSerializer):
        class CategoryField(ModelSerializer):
            class Meta:
                model = Category
                exclude = ('problems', )

        category = CategoryField(many=False, read_only=True)
        category_id = PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')

        class Meta:
            model = ClientCategory
            exclude = ('client', )
            read_only_fields = _RESOURCE_READONLY

        def create(self, validated_data):
            client = validated_data['client']
            if client.categories.filter(id=validated_data['category'].id).exists():
                raise ValidationError('category exists.')
            instance = super().create(validated_data)
            return instance

        def update(self, instance, validated_data):
            category = validated_data.get('category', None)
            if category is not None:
                client = instance.client
                category_cur = instance.category
                if category != category_cur and client.categories.filter(id=category.id).exists():
                    raise ValidationError('category exists.')
            return super().update(instance, validated_data)
