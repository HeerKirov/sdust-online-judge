from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from .permissions import IsUserAdmin, IsProblemAdmin, IsCategoryAdmin, IsJudgeAdmin, IsClientAdmin
from .permissions import ClientReadOnly, ClientWriteable
from .permissions import IsSelf
from .permissions import GROUP_NAME_CLIENT

from .utils import ExtraDataMixin, FilterViewSet, UserMixin
from .utils import UserModelViewSet, UserModelListViewSet
from .utils import ReadOnlyListViewSet, ReadOnlyDetailViewSet
from .utils import NestedUserModelListViewSet, NestedUserModelDetailViewSet, NestedUserModelViewSet
from .utils import AlreadyLogin, UserDisabled, PasswordConfirmationField

from .models import MetaProblem, Description, Sample, TestData
from .models import Problem, Limit, InvalidWord, SpecialJudge, ProblemTestData, ProblemLimitJudge
from .models import Environment, Judge
from .models import Category, CategoryProblem
from .models import Submission, CompileInfo, TestDataStatus, SubmissionCode
from .models import Client, ClientCategory

from .serializers import MetaProblemSerializers, ProblemSerializers, CategorySerializers, SubmissionSerializers
from .serializers import EnvironmentSerializers, UserSerializers
from .serializers import ClientSerializers

from .filters import MetaProblemFilters
from .filters import EnvironmentAdminFilter, EnvironmentFilter
from .filters import UserAdminFilter
from .filters import SubmissionFilters

from .judge import update_problem, update_meta, update_all, publish_submission

from json import loads


class MetaProblemViewSets:
    # -- Meta Problem -----------------------------------------------------------------------------
    class MetaAdminViewSet(UserModelViewSet):
        queryset = MetaProblem.objects.all().order_by('id')
        serializer_class = MetaProblemSerializers.MetaProblemAdminSerializer
        lookup_field = 'id'
        permission_classes = (IsProblemAdmin, )
        filter_class = MetaProblemFilters.MetaProblemAdminFilter
        search_fields = ('title', 'introduction')
        ordering_fields = ('id', 'create_time', 'update_time',
                           'title',
                           'number_description', 'number_sample', 'number_test_data', 'number_problem')

    # -- Components -------------------------------------------------------------------------------
    class Description:
        class List:
            class DescriptionAdminViewSet(NestedUserModelListViewSet):
                queryset = Description.objects.all().order_by('id')
                serializer_class = MetaProblemSerializers.Description.DescriptionAdminListSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)
                filter_class = MetaProblemFilters.DescriptionAdminFilter
                search_fields = ('id', 'introduction')
                ordering_fields = ('id', 'create_time', 'update_time', 'number_problem')

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_create(self, serializer):
                    instance = super().perform_create(serializer)
                    meta_problem = instance.meta_problem
                    meta_problem.number_description += 1
                    meta_problem.save()
                    return instance

        class Instance:
            class DescriptionAdminViewSet(NestedUserModelDetailViewSet):
                queryset = Description.objects.all()
                serializer_class = MetaProblemSerializers.Description.DescriptionAdminInstanceSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin, )

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_destroy(self, instance):
                    instance.meta_problem.number_description -= 1
                    instance.meta_problem.save()
                    instance.delete()

    class Sample:
        class List:
            class SampleAdminViewSet(NestedUserModelListViewSet):
                queryset = Sample.objects.all().order_by('id')
                serializer_class = MetaProblemSerializers.Sample.SampleAdminListSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)
                filter_class = MetaProblemFilters.SampleAdminFilter
                search_fields = ('id', 'introduction')
                ordering_fields = ('id', 'create_time', 'update_time', 'number_problem')

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_create(self, serializer):
                    instance = super().perform_create(serializer)
                    meta_problem = instance.meta_problem
                    meta_problem.number_sample += 1
                    meta_problem.save()
                    return instance

        class Instance:
            class SampleAdminViewSet(NestedUserModelDetailViewSet):
                queryset = Sample.objects.all()
                serializer_class = MetaProblemSerializers.Sample.SampleAdminInstanceSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_destroy(self, instance):
                    instance.meta_problem.number_sample -= 1
                    instance.meta_problem.save()
                    instance.delete()

    class TestData:
        class List:
            class TestDataAdminViewSet(NestedUserModelListViewSet):
                queryset = TestData.objects.all().order_by('id')
                serializer_class = MetaProblemSerializers.TestData.TestDataAdminListSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)
                filter_class = MetaProblemFilters.TestDataAdminFilter
                search_fields = ('id', 'introduction')
                ordering_fields = ('id', 'create_time', 'update_time', 'number_problem')

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_create(self, serializer):
                    instance = super().perform_create(serializer)
                    meta_problem = instance.meta_problem
                    meta_problem.number_test_data += 1
                    meta_problem.save()
                    return instance

        class Instance:
            class TestDataAdminViewSet(NestedUserModelDetailViewSet):
                queryset = TestData.objects.all()
                serializer_class = MetaProblemSerializers.TestData.TestDataAdminInstanceSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_update(self, serializer):
                    instance = super().perform_update(serializer)
                    update_meta(instance.meta_problem)
                    return instance

                def perform_destroy(self, instance):
                    meta_problem = instance.meta_problem
                    instance.meta_problem.number_test_data -= 1
                    instance.meta_problem.save()
                    instance.delete()
                    update_meta(meta_problem)

    class Problem:
        # -- Problem in MetaProblem -------------------------------------------
        class List:
            class ProblemAdminViewSet(NestedUserModelListViewSet):
                queryset = Problem.objects.all().order_by('id')
                serializer_class = MetaProblemSerializers.Problem.ProblemAdminListSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)
                filter_class = MetaProblemFilters.Problem.ProblemAdminFilter
                search_fields = ('id', 'introduction')
                ordering_fields = ('id', 'create_time', 'update_time',
                                   'number_test_data', 'number_limit', 'number_category', 'number_node')

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_create(self, serializer):
                    instance = super().perform_create(serializer)
                    meta_problem = instance.meta_problem
                    meta_problem.number_problem += 1
                    meta_problem.save()
                    update_problem(instance)
                    return instance

        class Instance:
            class ProblemAdminViewSet(NestedUserModelDetailViewSet):
                queryset = Problem.objects.all().order_by('id')
                serializer_class = MetaProblemSerializers.Problem.ProblemAdminInstanceSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)

                parent_queryset = MetaProblem.objects.all()
                parent_lookup = 'meta_problem_id'
                parent_related_name = 'meta_problem'
                parent_pk_field = 'id'

                def perform_destroy(self, instance):
                    instance.meta_problem.number_problem -= 1
                    instance.meta_problem.save()
                    instance.delete()

        # -- Components -------------------------------------------------------

        class Description:
            class DescriptionViewSet(GenericViewSet):
                permission_classes = (IsProblemAdmin,)

                @staticmethod
                def list(*args, **kwargs):
                    if args:
                        pass
                    problem = get_object_or_404(Problem.objects, id=kwargs['problem_id'])
                    description = problem.description
                    if description is None:
                        serializer = MetaProblemSerializers.Description.DescriptionAdminInstanceSerializer()
                    else:
                        serializer = MetaProblemSerializers.Description.DescriptionAdminInstanceSerializer(description)
                    return Response(serializer.data)

        class Sample:
            class SampleViewSet(GenericViewSet):
                permission_classes = (IsProblemAdmin,)

                @staticmethod
                def list(*args, **kwargs):
                    if args:
                        pass
                    problem = get_object_or_404(Problem.objects, id=kwargs['problem_id'])
                    sample = problem.sample
                    if sample is None:
                        serializer = MetaProblemSerializers.Sample.SampleAdminInstanceSerializer()
                    else:
                        serializer = MetaProblemSerializers.Sample.SampleAdminInstanceSerializer(sample)
                    return Response(serializer.data)

        class Limit:
            class List:
                class LimitAdminViewSet(NestedUserModelListViewSet):
                    queryset = Limit.objects.all().order_by('id')
                    serializer_class = MetaProblemSerializers.Problem.Limit.LimitAdminListSerializer
                    lookup_field = 'id'
                    permission_classes = (IsProblemAdmin,)
                    filter_class = MetaProblemFilters.Problem.LimitAdminFilter
                    search_fields = ('id', 'title', 'env_name')
                    ordering_fields = ('id', 'create_time', 'update_time', 'environment', 'env_name',
                                       'time_limit', 'memory_limit', 'length_limit')

                    parent_queryset = Problem.objects.all()
                    parent_lookup = 'problem_id'
                    parent_related_name = 'problem'
                    parent_pk_field = 'id'

                    def perform_create(self, serializer):
                        instance = super().perform_create(serializer)
                        instance.problem.number_limit += 1
                        instance.problem.save()
                        instance.environment.number_limit += 1
                        instance.environment.save()
                        through_model = Limit.judge.through
                        bulk_create = []
                        for judge in instance.environment.judge.filter(deleted=False):
                            bulk_create.append(through_model(limit=instance, judge=judge, problem=instance.problem))
                        through_model.objects.bulk_create(bulk_create)
                        update_problem(instance.problem)
                        return instance

            class Instance:
                class LimitAdminViewSet(NestedUserModelDetailViewSet):
                    queryset = Limit.objects.all()
                    serializer_class = MetaProblemSerializers.Problem.Limit.LimitAdminInstanceSerializer
                    lookup_field = 'id'
                    permission_classes = (IsProblemAdmin,)

                    parent_queryset = Problem.objects.all()
                    parent_lookup = 'problem_id'
                    parent_related_name = 'problem'
                    parent_pk_field = 'id'

                    def perform_update(self, serializer):
                        instance = super().perform_update(serializer)
                        update_problem(instance.problem)
                        return instance

                    def perform_destroy(self, instance):
                        problem = instance.problem
                        instance.problem.number_limit -= 1
                        instance.problem.save()
                        instance.environment.number_limit -= 1
                        instance.environment.save()
                        instance.delete()
                        update_problem(problem)

        class TestDataRelation:
            class List:
                class TestDataRelationAdminViewSet(NestedUserModelListViewSet):
                    queryset = ProblemTestData.objects.all().order_by('id')
                    serializer_class = MetaProblemSerializers.Problem.TestData.TestDataRelAdminListSerializer
                    lookup_field = 'id'
                    permission_classes = (IsProblemAdmin,)

                    filter_class = MetaProblemFilters.Problem.TestDataRelAdminFilter
                    search_fields = ('id',)

                    parent_queryset = Problem.objects.all()
                    parent_lookup = 'problem_id'
                    parent_related_name = 'problem'
                    parent_pk_field = 'id'

                    def perform_create(self, serializer):
                        instance = super().perform_create(serializer)
                        instance.problem.number_test_data += 1
                        instance.problem.save()
                        instance.test_data.number_problem += 1
                        instance.test_data.save()
                        update_problem(instance.problem)
                        return instance

            class Instance:
                class TestDataRelationAdminViewSet(NestedUserModelDetailViewSet):
                    queryset = ProblemTestData.objects.all()
                    serializer_class = MetaProblemSerializers.Problem.TestData.TestDataRelAdminInstanceSerializer
                    lookup_field = 'id'
                    permission_classes = (IsProblemAdmin,)

                    parent_queryset = Problem.objects.all()
                    parent_lookup = 'problem_id'
                    parent_related_name = 'problem'
                    parent_pk_field = 'id'

                    def perform_update(self, serializer):
                        instance = super().perform_update(serializer)
                        update_problem(instance.problem)
                        return instance

                    def perform_destroy(self, instance):
                        problem = instance.problem
                        instance.problem.number_test_data -= 1
                        instance.problem.save()
                        instance.test_data.number_problem -= 1
                        instance.test_data.save()
                        instance.delete()
                        update_problem(problem)

        class InvalidWord:
            class InvalidWordViewSet(NestedUserModelViewSet):
                queryset = InvalidWord.objects.all().order_by('id')
                serializer_class = MetaProblemSerializers.Problem.InvalidWord.InvalidWordAdminSerializer
                lookup_field = 'id'
                permission_classes = (IsProblemAdmin,)
                filter_class = MetaProblemFilters.Problem.InvalidWordAdminFilter
                search_fields = ('id', 'word')

                parent_queryset = Problem.objects.all()
                parent_lookup = 'problem_id'
                parent_related_name = 'problem'
                parent_pk_field = 'id'

                def perform_create(self, serializer):
                    instance = super().perform_create(serializer)
                    instance.problem.number_invalid_word += 1
                    instance.problem.save()

                def perform_destroy(self, instance):
                    instance.problem.number_invalid_word -= 1
                    instance.problem.save()
                    instance.delete()

        class SpecialJudge:
            class List:
                class SpecialJudgeAdminViewSet(NestedUserModelListViewSet):
                    queryset = SpecialJudge.objects.all().order_by('id')
                    serializer_class = MetaProblemSerializers.Problem.SpecialJudge.SpecialJudgeAdminListSerializer
                    lookup_field = 'id'
                    permission_classes = (IsProblemAdmin,)
                    filter_class = MetaProblemFilters.Problem.SpecialJudgeAdminFilter
                    search_fields = ('id',)
                    ordering_fields = ('id', 'create_time', 'update_time')

                    parent_queryset = Problem.objects.all()
                    parent_lookup = 'problem_id'
                    parent_related_name = 'problem'
                    parent_pk_field = 'id'

                    def perform_create(self, serializer):
                        instance = super().perform_create(serializer)
                        problem = instance.problem
                        number = problem.special_judge.filter(available=True, deleted=False).count()
                        if number > 0:
                            problem.is_special_judge = True
                        else:
                            problem.is_special_judge = False
                        problem.save()
                        update_problem(problem)
                        return instance

            class Instance:
                class SpecialJudgeAdminViewSet(NestedUserModelDetailViewSet):
                    queryset = SpecialJudge.objects.all()
                    serializer_class = MetaProblemSerializers.Problem.SpecialJudge.SpecialJudgeAdminInstanceSerializer
                    lookup_field = 'id'
                    permission_classes = (IsProblemAdmin,)

                    parent_queryset = Problem.objects.all()
                    parent_lookup = 'problem_id'
                    parent_related_name = 'problem'
                    parent_pk_field = 'id'

                    def perform_update(self, serializer):
                        instance = super().perform_update(serializer)
                        problem = instance.problem
                        number = problem.special_judge.filter(available=True, deleted=False).count()
                        if number > 0:
                            problem.is_special_judge = True
                        else:
                            problem.is_special_judge = False
                        problem.save()
                        update_problem(problem)
                        return instance

                    def perform_destroy(self, instance):
                        problem = instance.problem
                        instance.delete()
                        number = problem.special_judge.filter(available=True, deleted=False).count()
                        if number > 0:
                            problem.is_special_judge = True
                        else:
                            problem.is_special_judge = False
                        problem.save()
                        update_problem(problem)


class ProblemViewSets:
    class List:
        class ProblemViewSet(ReadOnlyListViewSet):
            queryset = Problem.objects.filter(available=True, deleted=False).order_by('id')
            serializer_class = ProblemSerializers.ProblemListSerializer
            lookup_field = 'id'
            permission_classes = (ClientReadOnly,)
            search_fields = ('title', 'introduction')
            ordering_fields = ('id', 'create_time', 'update_time',
                               'number_test_data', 'number_limit', 'number_category', 'number_node')

            def list(self, request, *args, **kwargs):
                user = request.user
                if user.groups.filter(name='Client').exists():
                    client = user.client
                    self.queryset = self.queryset.filter(categories__clients=client).distinct()
                return super().list(request, *args, **kwargs)

        class ProblemAdminViewSet(ReadOnlyListViewSet):
            queryset = Problem.objects.filter(deleted=False).order_by('id')
            serializer_class = ProblemSerializers.ProblemAdminListSerializer
            lookup_field = 'id'
            permission_classes = (IsCategoryAdmin, )
            search_fields = ('title', 'introduction')
            ordering_fields = ('id', 'create_time', 'update_time',
                               'number_test_data', 'number_limit', 'number_category', 'number_node')

    class Instance:
        class ProblemViewSet(ReadOnlyDetailViewSet):
            queryset = Problem.objects.filter(available=True, deleted=False)
            serializer_class = ProblemSerializers.ProblemInstanceSerializer
            lookup_field = 'id'
            permission_classes = (ClientReadOnly, )

            def retrieve(self, request, *args, **kwargs):
                user = request.user
                if user.groups.filter(name='Client').exists():
                    client = user.client
                    self.queryset = self.queryset.filter(categories__clients=client).distinct()
                return super().retrieve(request, *args, **kwargs)

        class ProblemAdminViewSet(ReadOnlyDetailViewSet):
            queryset = Problem.objects.filter(deleted=False)
            serializer_class = ProblemSerializers.ProblemAdminInstanceSerializer
            lookup_field = 'id'
            permission_classes = (IsCategoryAdmin,)

    class Admin:
        class List:
            class ProblemAdminViewSet(UserModelListViewSet):
                queryset = Problem.objects.filter(deleted=False).order_by('id')
                serializer_class = ProblemSerializers.Admin.ProblemAdminListSerializer
                lookup_field = 'id'
                permission_classes = (IsCategoryAdmin, )
                search_fields = ('title', 'introduction')
                ordering_fields = ('id', 'create_time', 'update_time',
                                   'number_test_data', 'number_limit', 'number_category', 'number_node',
                                   'origin_oj')

                def create(self, request, *args, **kwargs):
                    if 'dataStr' in request.data:
                        get_username = getattr(self, 'get_username')
                        get_username(request)
                        extra_data = getattr(self, 'extra_data')
                        username = getattr(self, 'username')
                        extra_data['creator'] = username
                        extra_data['updater'] = username
                        data = loads(request.data['dataStr'])
                        serializer = self.get_serializer(data=data)
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)
                        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
                    else:
                        return super().create(request, *args, **kwargs)

                def perform_create(self, serializer):
                    instance = super().perform_create(serializer)
                    update_meta(instance.meta_problem)
                    update_problem(instance)
                    return instance

            class VirtualProblemAdminViewSet(UserModelListViewSet):
                queryset = Problem.objects.filter(deleted=False).filter(is_virtual_judge=True).order_by('id')
                serializer_class = ProblemSerializers.Admin.VirtualProblemAdminListSerializer
                lookup_field = 'id'
                permission_classes = (IsCategoryAdmin,)
                search_fields = ('title', 'introduction')
                ordering_fields = ('id', 'create_time', 'update_time',
                                   'number_test_data', 'number_limit', 'number_category', 'number_node',
                                   'origin_oj')

                def create(self, request, *args, **kwargs):
                    if 'dataStr' in request.data:
                        get_username = getattr(self, 'get_username')
                        get_username(request)
                        extra_data = getattr(self, 'extra_data')
                        username = getattr(self, 'username')
                        extra_data['creator'] = username
                        extra_data['updater'] = username
                        data = loads(request.data['dataStr'])
                        serializer = self.get_serializer(data=data)
                        serializer.is_valid(raise_exception=True)
                        self.perform_create(serializer)
                        headers = self.get_success_headers(serializer.data)
                        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
                    else:
                        return super().create(request, *args, **kwargs)

                def perform_create(self, serializer):
                    instance = super().perform_create(serializer)
                    update_meta(instance.meta_problem)
                    update_problem(instance)
                    return instance

        class Instance:
            class ProblemAdminViewSet(ReadOnlyDetailViewSet):
                queryset = Problem.objects.filter(deleted=False)
                serializer_class = ProblemSerializers.Admin.ProblemAdminInstanceSerializer
                lookup_field = 'id'
                permission_classes = (IsCategoryAdmin,)

            class VirtualProblemAdminViewSet(ReadOnlyDetailViewSet):
                queryset = Problem.objects.filter(deleted=False).filter(is_virtual_judge=True)
                serializer_class = ProblemSerializers.Admin.VirtualProblemAdminInstanceSerializer
                lookup_field = 'id'
                permission_classes = (IsCategoryAdmin,)


class EnvironmentViewSets:
    class EnvironmentAdminViewSet(UserModelViewSet):
        queryset = Environment.objects.all().order_by('id')
        serializer_class = EnvironmentSerializers.EnvironmentAdminSerializer
        lookup_field = 'id'
        permission_classes = (IsJudgeAdmin, )
        filter_class = EnvironmentAdminFilter
        search_fields = ('name', 'judge_id')
        ordering_fields = ('id', 'create_time', 'update_time',
                           'name', 'judge_id')

    class EnvironmentViewSet(ReadOnlyModelViewSet):
        queryset = Environment.objects.all().filter(available=True, deleted=False).order_by('id')
        serializer_class = EnvironmentSerializers.EnvironmentSerializer
        lookup_field = 'id'
        permission_classes = (IsAuthenticated, )
        filter_class = EnvironmentFilter
        search_fields = ('name', )
        ordering_fields = ('id', 'name', 'create_time', 'update_time')

    class JudgeAdminViewSet(UserModelViewSet):
        queryset = Judge.objects.all().order_by('id')
        serializer_class = EnvironmentSerializers.JudgeAdminSerializer
        lookup_field = 'id'
        permission_classes = (IsJudgeAdmin, )
        search_fields = ('id', 'name')
        ordering_fields = ('id', 'name')

        def perform_create(self, serializer):
            instance = super().perform_create(serializer)
            bulk_create = []
            for env in instance.environment.filter(deleted=False).all():
                env.number_judge += 1
                env.save()
                limits = env.limits.filter(deleted=False)
                for limit in limits:
                    bulk_create.append(ProblemLimitJudge(limit=limit, problem=limit.problem, judge=instance))
            ProblemLimitJudge.objects.bulk_create(bulk_create)
            update_all(instance)
            return instance

        def perform_update(self, serializer):
            instance = self.get_object()
            instance.p_l_relation.all().delete()
            for env in instance.environment.filter(deleted=False).all():
                env.number_judge -= 1
                env.save()
            instance = super().perform_update(serializer)
            bulk_create = []
            for env in instance.environment.filter(deleted=False).all():
                env.number_judge += 1
                env.save()
                limits = env.limits.filter(deleted=False)
                for limit in limits:
                    bulk_create.append(ProblemLimitJudge(limit=limit, problem=limit.problem, judge=instance))
            ProblemLimitJudge.objects.bulk_create(bulk_create)
            update_all(instance)
            return instance

        def perform_destroy(self, instance):
            for env in instance.environment.all():
                env.number_judge -= 1
                env.save()
            instance.delete()


class SubmissionViewSets:
    # -- Submission -------------------------------------------------------------------------------
    class List:
        class SubmissionViewSet(CreateModelMixin, ListModelMixin,
                                ExtraDataMixin, FilterViewSet, UserMixin):
            queryset = Submission.objects.all().order_by('-submit_time')
            serializer_class = SubmissionSerializers.SubmissionListSerializer
            lookup_field = 'id'
            permission_classes = (ClientWriteable,)
            filter_class = SubmissionFilters.SubmissioinAdminFilter
            search_fields = ('user', 'contest',)
            ordering_fields = ('id', 'problem', 'environment',
                               'time', 'memory', 'length',
                               'user', 'contest', 'status', 'finished',
                               'submit_time', 'update_time',
                               'ip',)

            def create(self, request, *args, **kwargs):
                user = request.user
                extra_data = self.extra_data
                if user.groups.filter(name=GROUP_NAME_CLIENT).exists():
                    client = user.client
                    extra_data['client'] = client
                else:
                    self.get_username(request)
                    username = self.username
                    extra_data['user'] = username
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                extra_data['ip'] = ip
                return super().create(request, *args, **kwargs)

            def perform_create(self, serializer):
                extra_data = getattr(self, 'extra_data')
                instance = serializer.save(**extra_data)
                publish_submission(instance)
                return instance

        class SubmissionAdminViewSet(CreateModelMixin, ListModelMixin,
                                     ExtraDataMixin, FilterViewSet, UserMixin):
            queryset = Submission.objects.all().order_by('-submit_time')
            serializer_class = SubmissionSerializers.SubmissionAdminListSerializer
            lookup_field = 'id'
            permission_classes = (IsCategoryAdmin,)
            filter_class = SubmissionFilters.SubmissioinAdminFilter
            search_fields = ('user', 'contest',)
            ordering_fields = ('id', 'problem', 'environment',
                               'time', 'memory', 'length',
                               'user', 'contest', 'status', 'finished',
                               'submit_time', 'update_time',
                               'ip', 'judge')

            def create(self, request, *args, **kwargs):
                self.get_username(request)
                extra_data = self.extra_data
                username = self.username
                extra_data['user'] = username
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                extra_data['ip'] = ip
                return super().create(request, *args, **kwargs)

            def perform_create(self, serializer):
                extra_data = getattr(self, 'extra_data')
                instance = serializer.save(**extra_data)
                publish_submission(instance)
                return instance

    class Instance:
        class SubmissionViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                                ExtraDataMixin, FilterViewSet, UserMixin):
            queryset = Submission.objects.all()
            serializer_class = SubmissionSerializers.SubmissionInstanceSerializer
            lookup_field = 'id'
            permission_classes = (ClientWriteable, )

            def perform_update(self, serializer):
                extra_data = getattr(self, 'extra_data')
                instance = serializer.save(**extra_data)
                publish_submission(instance)
                return instance

        class SubmissionAdminViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                                     ExtraDataMixin, FilterViewSet, UserMixin):
            queryset = Submission.objects.all()
            serializer_class = SubmissionSerializers.SubmissionAdminInstanceSerializer
            lookup_field = 'id'
            permission_classes = (IsCategoryAdmin,)

            def perform_update(self, serializer):
                extra_data = getattr(self, 'extra_data')
                instance = serializer.save(**extra_data)
                publish_submission(instance)
                return instance

    # -- Components -------------------------------------------------------------------------------

    class CompileInfo:
        class CompileInfoAdminViewSet(GenericViewSet):
            permission_classes = (IsCategoryAdmin, )

            @staticmethod
            def list(*args, **kwargs):
                if args:
                    pass
                compile_info = get_object_or_404(CompileInfo.objects, submission_id=kwargs['submission_id'])
                serializer = SubmissionSerializers.CompileInfo.CompileInfoSerializer(compile_info)
                return Response(serializer.data)

    class TestDataStatus:
        class TestDataStatusAdminViewSet(GenericViewSet):
            permission_classes = (IsCategoryAdmin, )

            @staticmethod
            def list(*args, **kwargs):
                if args:
                    pass
                compile_info = get_object_or_404(TestDataStatus.objects, submission_id=kwargs['submission_id'])
                serializer = SubmissionSerializers.TestDataStatus.TestDataStatusSerializer(compile_info)
                return Response(serializer.data)

    class SubmissionCode:
        class SubmissionCodeAdminViewSet(GenericViewSet):
            permission_classes = (IsCategoryAdmin, )

            @staticmethod
            def list(*args, **kwargs):
                if args:
                    pass
                compile_info = get_object_or_404(SubmissionCode.objects, submission_id=kwargs['submission_id'])
                serializer = SubmissionSerializers.SubmissionCode.SubmissionCodeSerializer(compile_info)
                return Response(serializer.data)


class CategoryViewSets:
    class CategoryViewSet(ReadOnlyModelViewSet):
        queryset = Category.objects.filter(available=True, deleted=False).order_by('id')
        serializer_class = CategorySerializers.CategorySerializer
        lookup_field = 'id'
        permission_classes = (ClientReadOnly, )
        search_fields = ('title', 'introduction')
        ordering_fields = ('id', 'create_time', 'update_time',
                           'title',
                           'number_problem')

        def list(self, request, *args, **kwargs):
            user = request.user
            if user.groups.filter(name='Client').exists():
                client = user.client
                self.queryset = self.queryset.filter(clients=client).distinct()
            return super().list(request, *args, **kwargs)

        def retrieve(self, request, *args, **kwargs):
            user = request.user
            if user.groups.filter(name='Client').exists():
                client = user.client
                self.queryset = self.queryset.filter(clients=client).distinct()
            return super().retrieve(request, *args, **kwargs)

    class CategoryAdminViewSet(UserModelViewSet):
        queryset = Category.objects.all().order_by('id')
        serializer_class = CategorySerializers.CategoryAdminSerializer
        lookup_field = 'id'
        permission_classes = (IsCategoryAdmin, )
        search_fields = ('title', 'introduction')
        ordering_fields = ('id', 'create_time', 'update_time',
                           'title',
                           'number_problem')

    class ProblemViewSet(ReadOnlyModelViewSet):
        queryset = CategoryProblem.objects.filter(available=True, deleted=False).order_by('id')
        serializer_class = CategorySerializers.ProblemSerializer
        lookup_field = 'id'
        permission_classes = (ClientReadOnly, )
        ordering_fields = ('id', 'create_time', 'update_time')

        def list(self, request, *args, **kwargs):
            user = request.user
            if user.groups.filter(name='Client').exists():
                client = user.client
                category = get_object_or_404(Category.objects.filter(available=True, deleted=False),
                                             clients=client, id=int(kwargs['category_id']))
                self.queryset = self.queryset.filter(category=category)
            else:
                category = get_object_or_404(Category.objects.filter(available=True, deleted=False),
                                             id=int(kwargs['category_id']))
                self.queryset = self.queryset.filter(category=category)
            return super().list(request, *args, **kwargs)

        def retrieve(self, request, *args, **kwargs):
            user = request.user
            if user.groups.filter(name='Client').exists():
                client = user.client
                category = get_object_or_404(Category.objects.filter(available=True, deleted=False),
                                             clients=client, id=int(kwargs['category_id']))
                self.queryset = self.queryset.filter(category=category)
            else:
                category = get_object_or_404(Category.objects.filter(available=True, deleted=False),
                                             id=int(kwargs['category_id']))
                self.queryset = self.queryset.filter(category=category)
            return super().retrieve(request, *args, **kwargs)

    class ProblemAdminViewSet(NestedUserModelViewSet):
        queryset = CategoryProblem.objects.all().order_by('id')
        serializer_class = CategorySerializers.ProblemAdminSerializer
        lookup_field = 'id'
        permission_classes = (IsCategoryAdmin, )
        ordering_fields = ('id', 'create_time', 'update_time')

        parent_queryset = Category.objects.all()
        parent_lookup = 'category_id'
        parent_related_name = 'category'
        parent_pk_field = 'id'

        def perform_create(self, serializer):
            instance = super().perform_create(serializer)
            client = instance.category
            client.number_problem = client.problems.filter(
                deleted=False, category_relations__deleted=False
            ).distinct().count()
            client.save()
            return instance

        def perform_update(self, serializer):
            instance = super().perform_update(serializer)
            client = instance.category
            client.number_problem = client.problems.filter(
                deleted=False, category_relations__deleted=False
            ).distinct().count()
            client.save()
            return instance

        def perform_destroy(self, instance):
            client = instance.category
            instance.delete()
            client.number_problem = client.problems.distinct().count()
            client.save()


class UserViewSets:
    class LoginViewSet(ViewSet):
        @staticmethod
        def create(request):
            if request.user.is_authenticated():
                raise AlreadyLogin()

            serializer = UserSerializers.LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = request.data['username']
            password = request.data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    raise UserDisabled()
            else:
                raise AuthenticationFailed

            try:
                headers = {'Location': serializer.data[api_settings.URL_FIELD_NAME]}
            except (TypeError, KeyError):
                headers = {}
            return Response(status=HTTP_200_OK, headers=headers)

    class LogoutViewSet(GenericViewSet):
        permission_classes = (IsAuthenticated,)

        @staticmethod
        def list(request):
            logout(request)
            return Response(status=HTTP_200_OK)

    class UserAdminViewSet(ModelViewSet):
        queryset = User.objects.exclude(groups__name='Client').order_by('id')
        serializer_class = UserSerializers.UserAdminSerializer
        lookup_field = 'username'
        permission_classes = (IsUserAdmin, )
        filter_class = UserAdminFilter
        search_fields = ('username', 'first_name', 'last_name',  'email')
        ordering_fields = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')

    class UserInfoViewSet(UpdateModelMixin, GenericViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializers.UserInfoSerializer
        lookup_field = 'username'
        permission_classes = (IsSelf, )

    class UserPasswordViewSet(UpdateModelMixin, GenericViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializers.UserPasswordSerializer
        lookup_field = 'username'
        permission_classes = (IsSelf,)

        def update(self, request, *args, **kwargs):
            kwargs.pop('partial', None)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            username = serializer.data['username']
            old_password = validated_data['old_password']
            new_password = validated_data['new_password']
            confirmation = validated_data['confirmation']

            if new_password != confirmation:
                raise PasswordConfirmationField

            user = authenticate(username=username, password=old_password)
            if user is not None:
                if not user.is_active:
                    raise UserDisabled()
            else:
                raise AuthenticationFailed

            user.set_password(new_password)

            return Response(serializer.data)


class ClientViewSets:
    class UserAdminViewSet(ModelViewSet):
        queryset = User.objects.filter(groups__name=GROUP_NAME_CLIENT).order_by('id')
        serializer_class = ClientSerializers.UserAdminSerializer
        lookup_field = 'username'
        permission_classes = (IsClientAdmin, )
        filter_class = UserAdminFilter
        search_fields = ('username', 'first_name', 'last_name',  'email')
        ordering_fields = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')

    class ClientAdminViewSet(UserModelViewSet):
        queryset = Client.objects.all().order_by('id')
        serializer_class = ClientSerializers.ClientAdminSerializer
        lookup_field = 'id'
        permission_classes = (IsClientAdmin, )
        search_fields = ('name', 'introduction')
        ordering_fields = ('id', 'name', 'number_category', 'number_problem')

    class ClientCategoryViewSet(NestedUserModelViewSet):
        queryset = ClientCategory.objects.all().order_by('id')
        serializer_class = ClientSerializers.ClientCategoryAdminSerializer
        lookup_field = 'id'
        permission_classes = (IsClientAdmin, )
        ordering_fields = ('id',)

        parent_queryset = Client.objects.all()
        parent_lookup = 'client_id'
        parent_related_name = 'client'
        parent_pk_field = 'id'

        def perform_create(self, serializer):
            instance = super().perform_create(serializer)
            instance.client.number_category += 1
            instance.client.save()
            return instance

        def perform_destroy(self, instance):
            instance.client.number_category -= 1
            instance.client.save()
            instance.delete()
