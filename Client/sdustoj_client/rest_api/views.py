from rest_framework import viewsets, status, exceptions, response, settings, permissions as permissions_
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse

from .models import *
from . import permissions
from .serializers import PersonalSerializers, UserSerializers, OrgUserSerializers
from .serializers import CourseUserSerializers, CourseGroupUserSerializer
from .serializers import OrganizationSerializers, CategorySerializers, SubmissionSerializers, RankSerializers
from .serializers import CourseSerializers, MissionSerializers, ProblemSerializers, ProblemRelationSerializers
from .utils import UserDisabled, AlreadyLogin, OrgNestedMixin
from .utils import ListResourceViewSet, InstanceResourceViewSet
from .utils import ListReadonlyResourceViewSet, InstanceReadonlyResourceViewSet, ListReadonlyNestedResourceViewSet
from .utils import ListNestedResourceViewSet, InstanceNestedResourceViewSet, InstanceReadonlyNestedResourceViewSet
from .utils import ListNestedViewSet, ListReadonlyNestedViewSet, InstanceDeleteNestedViewSet
from .utils import InstanceReadonlyNestedViewSet, CreateNestedViewSet
from .permissions import *


# 个人api
class PersonalViewSets(object):
    class Login(object):
        class LoginViewSet(viewsets.ViewSet):
            @staticmethod
            def create(request):
                if request.user.is_authenticated():
                    raise AlreadyLogin()

                data = request.data
                serializer = PersonalSerializers.LoginSerializer(data=data)
                serializer.is_valid(raise_exception=True)

                username = data['username']
                password = data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.profile.available and not user.profile.deleted:
                        login(request, user)
                        user.profile.last_login = timezone.now()
                        if 'HTTP_X_FORWARDED_FOR' in request.META:
                            ip = request.META['HTTP_X_FORWARDED_FOR']
                        else:
                            ip = request.META['REMOTE_ADDR']
                        user.profile.ip = ip
                        user.profile.save()
                    else:
                        raise UserDisabled()
                else:
                    raise exceptions.AuthenticationFailed

                try:
                    headers = {'Location': serializer.data[settings.api_settings.URL_FIELD_NAME]}
                except (TypeError, KeyError):
                    headers = {}
                return response.Response(status=status.HTTP_200_OK, headers=headers)

    class Logout(object):
        class LogoutViewSet(viewsets.GenericViewSet):
            permission_classes = (permissions_.IsAuthenticated, )

            @staticmethod
            def list(request):
                logout(request)
                return response.Response(status=status.HTTP_200_OK)

    class Personal(object):
        class PersonalViewSet(viewsets.mixins.RetrieveModelMixin,
                              viewsets.mixins.UpdateModelMixin,
                              viewsets.GenericViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = PersonalSerializers.PersonalInfoSerializer
            permission_classes = (permissions.IsSelf, )
            lookup_field = 'username'

        class PasswordViewSet(viewsets.mixins.RetrieveModelMixin,
                              viewsets.mixins.UpdateModelMixin,
                              viewsets.GenericViewSet):
            queryset = getattr(User, 'objects')
            serializer_class = PersonalSerializers.UserPasswordSerializer
            permission_classes = (permissions.IsSelf, )
            lookup_field = 'username'


# 用户api
class UserViewSets(object):
    class RootList(object):
        # admin - 超级管理员
        class RootAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(
                is_staff=True, identities__ROOT=True).order_by('username')
            serializer_class = UserSerializers.ListRoot
            permission_classes = (IsRoot,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

    class RootInstance(object):
        # admin - 超级管理员
        class RootAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(
                is_staff=True, identities__ROOT=True).order_by('username')
            serializer_class = UserSerializers.InstanceRoot
            permission_classes = (IsRoot,)
            lookup_field = 'username'

            def perform_destroy(self, instance):
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()

    class AdminList(object):
        # admin - 所有管理员
        class AdminAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).order_by('username')
            serializer_class = UserSerializers.ListAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

        # admin - 机构管理员
        class OrgAdminAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').\
                filter(is_staff=True).filter(identities__ORG_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.ListOrgAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

        # admin - 用户管理员
        class UserAdminAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).\
                filter(identities__USER_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.ListUserAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

    class AdminInstance(object):
        # admin - 所有管理员
        class AdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

            def perform_destroy(self, instance):
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()

        # admin - 机构管理员
        class OrgAdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').\
                filter(is_staff=True).filter(identities__ORG_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.InstanceOrgAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

            def perform_destroy(self, instance):
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()

        # admin - 用户管理员
        class UserAdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).\
                filter(identities__USER_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.InstanceUserAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

            def perform_destroy(self, instance):
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()

    # admin用户管理部分的用户
    class UserList(object):
        # admin - 所有用户
        class UserAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.ListAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

        # admin - 教务管理员 - deep2
        class EduAdminViewSet(ListNestedResourceViewSet):
            queryset = getattr(EduAdmin, 'objects').order_by('username')
            serializer_class = UserSerializers.ListEduAdmin
            permission_classes = (IsOrgAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            # parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            # parent_related_name = 'identities__%s__contains' % (IdentityChoices.edu_admin,)  # 在当前models中，上级model的关联名
            parent_queryset = Organization.objects.all()
            parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得UserProfile
                instance.organization.update_numbers()
                return instance

    # admin用户管理部分的用户
    class UserInstance(object):
        # admin - 所有用户
        class UserAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

            def perform_destroy(self, instance):
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()

        # admin - 教务管理员 - deep2
        class EduAdminViewSet(InstanceNestedResourceViewSet):
            queryset = getattr(EduAdmin, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceEduAdmin
            permission_classes = (IsOrgAdmin,)
            lookup_field = 'username'

            parent_queryset = Organization.objects.all()
            parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def perform_update(self, serializer):
                instance = super().perform_update(serializer)  # 获得UserProfile
                instance.organization.update_numbers()
                return instance

            def perform_destroy(self, instance):
                organization = instance.organization
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()
                organization.update_numbers()

    # org部分下属的用户
    class OrgUserList(object):
        # 教务管理员 - deep2
        class EduAdminViewSet(ListReadonlyNestedResourceViewSet):
            queryset = getattr(EduAdmin, 'objects').exclude(deleted=True).order_by('username')
            serializer_class = OrgUserSerializers.ListEduAdmin
            permission_classes = (IsEduAdminReadonly,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            parent_queryset = Organization.objects.all()
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

        # 教师 - deep2
        class TeacherViewSet(ListNestedResourceViewSet):
            queryset = getattr(Teacher, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.ListTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            parent_queryset = Organization.objects.all()
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_org_manager():  # 这段代码确保筛选掉deleted的内容，使它们只能被机构的一般管理者看见。
                    return self.queryset.exclude(deleted=True)
                return self.queryset

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得UserProfile
                instance.organization.update_numbers()
                return instance

        # 学生 - deep2
        class StudentViewSet(ListNestedResourceViewSet):
            queryset = getattr(Student, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.ListStudent
            permission_classes = (IsStudentReadonlyOrEduAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            parent_queryset = Organization.objects.all()
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_org_manager():
                    return self.queryset.exclude(deleted=True)
                return self.queryset

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得UserProfile
                instance.organization.update_numbers()
                return instance

    # org部分下属的用户
    class OrgUserInstance(object):
        # 教务管理员 - deep2
        class EduAdminViewSet(InstanceReadonlyNestedResourceViewSet):
            queryset = getattr(EduAdmin, 'objects').exclude(deleted=True).order_by('username')
            serializer_class = UserSerializers.InstanceEduAdmin
            permission_classes = (IsEduAdminReadonly,)
            lookup_field = 'username'

            parent_queryset = Organization.objects.all()
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

        # 教师 - deep2
        class TeacherViewSet(InstanceNestedResourceViewSet):
            queryset = getattr(Teacher, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.InstanceTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            lookup_field = 'username'

            parent_queryset = Organization.objects.all()
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_org_manager():
                    return self.queryset.exclude(deleted=True)
                return self.queryset

            def perform_update(self, serializer):
                instance = super().perform_update(serializer)  # 获得UserProfile
                instance.organization.update_numbers()
                return instance

            def perform_destroy(self, instance):
                organization = instance.organization
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()
                organization.update_numbers()

        # 学生 - deep2
        class StudentViewSet(InstanceNestedResourceViewSet):
            queryset = getattr(Student, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.InstanceStudent
            permission_classes = (IsStudentReadonlyOrEduAdmin,)
            lookup_field = 'username'

            parent_queryset = Organization.objects.all()
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_org_manager():
                    return self.queryset.exclude(deleted=True)
                return self.queryset

            def perform_update(self, serializer):
                instance = super().perform_update(serializer)  # 获得UserProfile
                instance.organization.update_numbers()
                return instance

            def perform_destroy(self, instance):
                organization = instance.organization
                if hasattr(instance, 'user'):
                    user = instance.user
                    user.delete()
                organization.update_numbers()

    # course下属的用户
    class CourseUserList(object):
        # 课程拥有的教师 - deep2 - relation
        class TeacherViewSet(ListNestedResourceViewSet):
            queryset = CourseTeacherRelation.objects.all()
            serializer_class = CourseUserSerializers.ListTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('id',)

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course'  # 在当前models中，上级model的关联名
            parent_pk = 'cid'  # 上级model的主键名

        # 课程拥有的学生 - deep2 - relation
        class StudentViewSet(ListNestedResourceViewSet):
            queryset = CourseStudentRelation.objects.all()
            serializer_class = CourseUserSerializers.ListStudent
            permission_classes = (IsAnyOrgReadonlyOrEduAdmin,)
            ordering_fields = ('id',)

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course'  # 在当前models中，上级model的关联名
            parent_pk = 'cid'  # 上级model的主键名

        # 课程可以添加的教师 - deep2
        class TeacherAvailableViewSet(ListReadonlyNestedResourceViewSet):
            queryset = Teacher.objects.all()
            serializer_class = CourseUserSerializers.ListAvailableTeacher
            permission_classes = (IsEduAdminReadonly,)
            ordering_fields = ('id',)

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'
            parent_pk = 'cid'
            parent_related_name = 'course'

            def _set_queryset(self, **kwargs):
                # 有关可以使用的题库的选定规则：
                # 机构使用的题库，仅显示与该机构有直接关联的题库；
                # 机构可以使用的题库，仅显示该机构还没添加、但是(上级机构添加了的题库|上级机构是root时的所有题库).
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到上级course的cid
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该course
                self.queryset = parent.available_teachers(filter_exists=True)

                return parent_related_name, parent

        # 课程可以添加的学生 - deep2
        class StudentAvailableViewSet(ListReadonlyNestedResourceViewSet):
            queryset = Student.objects.all()
            serializer_class = CourseUserSerializers.ListAvailableStudent
            permission_classes = (IsEduAdminReadonly,)
            ordering_fields = ('id',)

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'
            parent_pk = 'cid'
            parent_related_name = 'course'

            def _set_queryset(self, **kwargs):
                # 有关可以使用的题库的选定规则：
                # 机构使用的题库，仅显示与该机构有直接关联的题库；
                # 机构可以使用的题库，仅显示该机构还没添加、但是(上级机构添加了的题库|上级机构是root时的所有题库).
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到上级course的cid
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该course
                self.queryset = parent.available_students(filter_exists=True)

                return parent_related_name, parent

    # course下属的用户
    class CourseUserInstance(object):
        # 课程拥有的教师 - deep2 - relation
        class TeacherViewSet(InstanceNestedResourceViewSet):
            queryset = CourseTeacherRelation.objects.all()
            serializer_class = CourseUserSerializers.InstanceTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            lookup_field = 'id'

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course'  # 在当前models中，上级model的关联名
            parent_pk = 'cid'  # 上级model的主键名

        # 课程拥有的学生 - deep2 - relation
        class StudentViewSet(InstanceNestedResourceViewSet):
            queryset = CourseStudentRelation.objects.all()
            serializer_class = CourseUserSerializers.InstanceStudent
            permission_classes = (IsAnyOrgReadonlyOrEduAdmin,)
            lookup_field = 'id'

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course'  # 在当前models中，上级model的关联名
            parent_pk = 'cid'  # 上级model的主键名

    # course group下属的用户
    class CourseGroupUserList(object):
        # 课程组拥有的教师 - deep2 - relation
        class TeacherViewSet(ListNestedResourceViewSet):
            queryset = CourseGroupTeacherRelation.objects.all()
            serializer_class = CourseGroupUserSerializer.ListTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('id',)

            parent_queryset = CourseGroup.objects.all()
            parent_lookup = 'course_group_gid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_group'  # 在当前models中，上级model的关联名
            parent_pk = 'gid'  # 上级model的主键名

        # 课程组可以添加的教师 - deep2
        class TeacherAvailableViewSet(ListReadonlyNestedResourceViewSet):
            queryset = Teacher.objects.all()
            serializer_class = CourseGroupUserSerializer.ListAvailableTeacher
            permission_classes = (IsEduAdminReadonly,)
            ordering_fields = ('id',)

            parent_queryset = CourseGroup.objects.all()
            parent_lookup = 'course_group_gid'
            parent_pk = 'gid'
            parent_related_name = 'course_group'

            def _set_queryset(self, **kwargs):
                # 有关可以使用的题库的选定规则：
                # 机构使用的题库，仅显示与该机构有直接关联的题库；
                # 机构可以使用的题库，仅显示该机构还没添加、但是(上级机构添加了的题库|上级机构是root时的所有题库).
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到上级course_group的gid
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该course
                self.queryset = parent.available_teachers(filter_exists=True)

                return parent_related_name, parent

    # course group下属的用户
    class CourseGroupUserInstance(object):
        # 课程组拥有的教师 - deep2 - relation
        class TeacherViewSet(InstanceNestedResourceViewSet):
            queryset = CourseGroupTeacherRelation.objects.all()
            serializer_class = CourseGroupUserSerializer.InstanceTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            lookup_field = 'id'

            parent_queryset = CourseGroup.objects.all()
            parent_lookup = 'course_group_gid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_group'  # 在当前models中，上级model的关联名
            parent_pk = 'gid'  # 上级model的主键名


# 机构api
class OrganizationViewSets(object):
    class OrganizationList(object):
        # admin - 所有机构
        class OrganizationAdminViewSet(ListResourceViewSet):
            queryset = getattr(Organization, 'objects').exclude(name='ROOT').order_by('id')
            serializer_class = OrganizationSerializers.Organization.ListAdmin
            permission_classes = (IsOrgAdmin,)
            search_fields = ('name', 'caption')
            ordering_fields = ('name', 'caption', 'parent',
                               'number_organizations',
                               'number_students',
                               'number_teachers',
                               'number_admins')

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                instance.parent.update_numbers()
                return instance

        # 所有相关机构
        class OrganizationViewSet(ListReadonlyResourceViewSet):
            queryset = getattr(Organization, 'objects').exclude(name='ROOT').exclude(deleted=True).order_by('id')
            serializer_class = OrganizationSerializers.Organization.List
            permission_classes = (IsAnyOrgReadonly,)
            search_fields = ('name', 'caption')
            ordering_fields = ('name', 'caption', 'parent',
                               'number_organizations',
                               'number_students',
                               'number_teachers',
                               'number_admins')

            def get_queryset(self):
                user = self.request.user
                profile = getattr(user, 'profile')
                if profile is not None:
                    organizations = profile.get_organizations()
                    return organizations
                else:
                    return self.queryset.none()

    class OrganizationInstance(object):
        # admin - 所有机构
        class OrganizationAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(Organization, 'objects').exclude(name='ROOT').order_by('id')
            serializer_class = OrganizationSerializers.Organization.InstanceAdmin
            permission_classes = (IsOrgAdmin,)
            lookup_field = 'name'

            def perform_update(self, serializer):
                parent = serializer.instance.parent
                instance = super().perform_update(serializer)
                if parent != instance.parent:
                    parent.update_numbers()
                    instance.parent.update_numbers()
                return instance

            def perform_destroy(self, instance):
                parent = instance.parent
                parent.update_numbers()
                super().perform_destroy(instance)

        # 所有相关机构
        class OrganizationViewSet(InstanceReadonlyResourceViewSet):
            queryset = getattr(Organization, 'objects').exclude(name='ROOT').exclude(deleted=True).order_by('id')
            serializer_class = OrganizationSerializers.Organization.Instance
            permission_classes = (IsAnyOrgReadonly,)
            lookup_field = 'name'

            def get_queryset(self):
                user = self.request.user
                profile = getattr(user, 'profile')
                if profile is not None:
                    organizations = profile.get_organizations()
                    return organizations
                else:
                    return self.queryset.none()


# 题库api
class CategoryViewSet(object):
    class CategoryList(object):
        # admin - 机构使用的题库 - deep2 - relation
        class CategoryOrgAdminViewSet(ListNestedViewSet):
            queryset = OrganizationCategoryRelation.objects.all()
            serializer_class = CategorySerializers.Category.ListOrgAdmin
            permission_classes = (IsOrgAdmin,)
            ordering_fields = ('id',)

            parent_queryset = Organization.objects.all()
            parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得Relation
                organization = instance.organization
                organization.update_numbers()
                return instance

        # admin - 可以使用的题库 - deep2
        class CategoryAvailableOrgAdminViewSet(ListReadonlyNestedViewSet):
            queryset = Category.objects.all()
            serializer_class = CategorySerializers.Category.ListAvailableOrgAdmin
            permission_classes = (IsOrgAdmin,)
            ordering_fields = ('id',)

            parent_queryset = Organization.objects.all()
            parent_lookup = 'admin_organization_pk'
            parent_pk = 'name'
            parent_related_name = 'organization'

            def _set_queryset(self, **kwargs):
                # 有关可以使用的题库的选定规则：
                # 机构使用的题库，仅显示与该机构有直接关联的题库；
                # 机构可以使用的题库，仅显示该机构还没添加、但是(上级机构添加了的题库|上级机构是root时的所有题库).
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到隶属org的name
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该org
                exist_id = [i.id for i in parent.categories.all()]  # 获得该org旗下的所有的已用题库的id-list

                self.queryset = parent.available_categories()
                # 然后，从圈定的范围内筛选出所有可用的题库。
                self.queryset = self.queryset.exclude(id__in=exist_id).all()

                return parent_related_name, parent

        # 课程基类使用的题库 - deep2 - relation
        class CategoryMetaViewSet(ListNestedViewSet):
            queryset = CourseMetaCategoryRelation.objects.all()
            serializer_class = CategorySerializers.CourseMetaCategory.List
            permission_classes = (IsEduAdmin,)
            ordering_fields = ('id',)

            parent_queryset = CourseMeta.objects.all()
            parent_lookup = 'course_meta_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_meta'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得Relation
                course_meta = instance.course_meta
                course_meta.update_numbers()
                return instance

        # 课程基类可以使用的题库 - deep2
        class CategoryAvailableMetaViewSet(ListReadonlyNestedViewSet):
            queryset = Course.objects.all()
            serializer_class = CategorySerializers.CourseMetaCategory.ListAvailable
            permission_classes = (IsEduAdmin,)
            ordering_fields = ('id',)

            parent_queryset = CourseMeta.objects.all()
            parent_lookup = 'course_meta_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_meta'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def _set_queryset(self, **kwargs):
                # 可使用的题库的规则：
                # 1.该meta的所属org拥有的题库
                # 2.且过滤掉所有已经添加了的题库
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # meta model
                exist_id = [i.id for i in parent.categories.all()]  # 获得该meta旗下的所有的已用题库的id-list

                self.queryset = parent.available_categories()
                self.queryset = self.queryset.exclude(id__in=exist_id).all()
                return parent_related_name, parent

    class CategoryInstance(object):
        # admin - 机构使用的题库 - deep2 - relation
        class CategoryOrgAdminViewSet(InstanceDeleteNestedViewSet):
            queryset = OrganizationCategoryRelation.objects.all()
            serializer_class = CategorySerializers.Category.InstanceOrgAdmin
            permission_classes = (IsOrgAdmin,)
            lookup_field = 'id'

            parent_queryset = Organization.objects.all()
            parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'organization'  # 在当前models中，上级model的关联名
            parent_pk = 'name'  # 上级model的主键名

            def perform_destroy(self, instance):
                organization = instance.organization
                super().perform_destroy(instance)
                organization.update_numbers()

        # 课程基类使用的题库 - deep2 - relation
        class CategoryMetaViewSet(InstanceDeleteNestedViewSet):
            queryset = CourseMetaCategoryRelation.objects.all()
            serializer_class = CategorySerializers.CourseMetaCategory.List
            permission_classes = (IsEduAdmin,)
            lookup_field = 'id'

            parent_queryset = CourseMeta.objects.all()
            parent_lookup = 'course_meta_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_meta'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def perform_destroy(self, instance):
                course_meta = instance.course_meta
                super().perform_destroy(instance)
                course_meta.update_numbers()


# 课程基类与课程api
class CourseViewSets(object):
    class CourseMetaList(object):
        # 机构下的课程基类 - deep2
        class CourseMetaOrgViewSet(ListNestedResourceViewSet):
            queryset = CourseMeta.objects.all()
            serializer_class = CourseSerializers.CourseMeta.ListOrg
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_field = ('id', 'caption',
                              'number_courses',
                              'number_course_groups',
                              'number_categories',
                              'number_problems')
            search_fields = ('caption',)

            parent_queryset = Organization.objects.all()
            parent_lookup = 'organization_pk'
            parent_pk = 'name'
            parent_related_name = 'organization'

            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_org_manager():
                    return self.queryset.exclude(deleted=True)
                return self.queryset

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                organization = instance.organization
                organization.update_numbers()
                return instance

    class CourseMetaInstance(object):
        # 课程基类
        class CourseMetaViewSet(InstanceResourceViewSet):
            queryset = CourseMeta.objects.all()
            serializer_class = CourseSerializers.CourseMeta.InstanceOrg
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            lookup_field = 'id'

            def perform_destroy(self, instance):
                organization = instance.organization
                super().destroy(instance)
                organization.update_numbers()

            def set_queryset(self):
                # 该api虽然不是二级api 但是仍然限制访问范围在[ORG]关联范围[SITE]全部范围
                user = self.request.user
                profile = user.profile
                identities = profile.identities  # 权限列表
                org_set = set()
                for identity, value in identities.items():
                    if identity in SITE_IDENTITY_CHOICES and value is True:  # 该账户拥有site管理员权限
                        return self.queryset
                    elif identity in ORG_IDENTITY_CHOICES and len(value) > 0:  # 该账户是机构内账户
                        # 逻辑：从identities的列表中，题目每一个org权限的所有org名称组成集合，
                        # 然后去提取所有与这些名称相关的Organization
                        for org in value:
                            org_set.add(org)
                queryset = CourseMeta.objects.none()
                for org in org_set:
                    queryset = queryset | self.queryset.filter(organization__id=org)
                if not profile.is_org_manager():
                    queryset = queryset.exclude(deleted=True)
                return queryset.distinct()

    class CourseList(object):
        # 课程基类下的课程
        class CourseViewSet(ListNestedResourceViewSet):
            queryset = Course.objects.all()
            serializer_class = CourseSerializers.Course.List
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('caption', 'start_time', 'end_time')
            search_fields = ('caption',)

            parent_queryset = CourseMeta.objects.all()
            parent_lookup = 'course_meta_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'meta'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            # def _set_queryset(self, **kwargs):
            #     lookup = kwargs[self.parent_lookup]  # parent的id名
            #     parent = get_object_or_404(self.parent_queryset, **{self.parent_pk: lookup})
            #     org_id = parent.id
            #     profile = self.request.user.profile
            #     if not profile.is_org_manager():
            #         self.queryset = profile.get_courses().filter(**{self.parent_related_name: org_id}).\
            #             exclude(deleted=True).all()
            #     else:
            #         self.queryset = profile.get_courses().filter(**{self.parent_related_name: org_id}).all()
            #
            #     return self.parent_related_name, parent
            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_org_manager():
                    return profile.get_courses().exlcude(deleted=True)
                else:
                    return profile.get_courses()

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                instance.organization.update_numbers()
                return instance

        # 我教的课程
        class CourseTeachingViewSet(ListReadonlyResourceViewSet):
            queryset = Course.objects.all()
            serializer_class = CourseSerializers.Course.List
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('caption', 'start_time', 'end_time')
            search_fields = ('caption',)

            def get_queryset(self):
                profile = self.request.user.profile
                return profile.get_courses(teaching=True).exclude(deleted=True)

        # 我学习的课程
        class CourseLearningViewSet(ListReadonlyResourceViewSet):
            queryset = Course.objects.all()
            serializer_class = CourseSerializers.Course.List
            permission_classes = (IsStudentReadonlyOrEduAdmin,)
            ordering_fields = ('caption', 'start_time', 'end_time')
            search_fields = ('caption',)

            def get_queryset(self):
                profile = self.request.user.profile
                return profile.get_courses(learning=True).exclude(deleted=True)

        # 课程组所拥有的课程 - deep2 - relation
        class CourseCourseGroupViewSet(ListNestedResourceViewSet):
            queryset = CourseGroupRelation.objects.all()
            serializer_class = CourseSerializers.CourseGroupCourse.List
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('id',)

            parent_queryset = CourseGroup.objects.all()
            parent_lookup = 'course_group_gid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_group'  # 在当前models中，上级model的关联名
            parent_pk = 'gid'  # 上级model的主键名

        # 课程组可以添加的课程 - deep2
        class CourseAvailableCourseGroupViewSet(ListReadonlyNestedResourceViewSet):
            queryset = Course.objects.all()
            serializer_class = CourseSerializers.CourseGroupCourse.ListAvailable
            permission_classes = (IsEduAdminReadonly,)
            ordering_fields = ('id',)

            parent_queryset = CourseGroup.objects.all()
            parent_lookup = 'course_group_gid'
            parent_pk = 'gid'
            parent_related_name = 'course_group'

            def _set_queryset(self, **kwargs):
                # 有关可以使用的题库的选定规则：
                # 机构使用的题库，仅显示与该机构有直接关联的题库；
                # 机构可以使用的题库，仅显示该机构还没添加、但是(上级机构添加了的题库|上级机构是root时的所有题库).
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到上级course_group的gid
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该course
                self.queryset = parent.available_courses(filter_exists=True)

                return parent_related_name, parent

    class CourseInstance(object):
        # 课程
        class CourseViewSet(InstanceResourceViewSet):
            queryset = Course.objects.all()
            serializer_class = CourseSerializers.Course.Instance
            permission_classes = (IsAnyOrgReadonlyOrEduAdmin,)
            lookup_field = 'cid'

            def perform_destroy(self, instance):
                organization = instance.organization
                super().perform_destroy(instance)
                organization.update_numbers()

            def get_queryset(self):
                # 限定访问列表。对于SITE权限，访问列表为全部;对于EDUADMIN，访问列表为ORG管辖下所有course。对于S/T，仅可以访问关联course
                user = self.request.user
                profile = user.profile
                identities = profile.identities
                for identity, value in identities.items():
                    if identity in SITE_IDENTITY_CHOICES and value is True:
                        return self.queryset
                if not profile.is_org_manager():
                    return profile.get_courses().exclude(deleted=True)
                return profile.get_courses()

        # 课程组所拥有的课程 - deep2 - relation
        class CourseCourseGroupViewSet(InstanceNestedResourceViewSet):
            queryset = CourseGroupRelation.objects.all()
            serializer_class = CourseSerializers.CourseGroupCourse.Instance
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            lookup_field = 'id'

            parent_queryset = CourseGroup.objects.all()
            parent_lookup = 'course_group_gid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_group'  # 在当前models中，上级model的关联名
            parent_pk = 'gid'  # 上级model的主键名

    class CourseGroupList(object):
        # 课程组
        class CourseGroupViewSet(ListNestedResourceViewSet):
            queryset = CourseGroup.objects.all()
            serializer_class = CourseSerializers.CourseGroup.List
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('caption',)
            search_fields = ('caption',)

            parent_queryset = CourseMeta.objects.all()
            parent_lookup = 'course_meta_id'
            parent_related_name = 'meta'
            parent_pk = 'id'

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                instance.organization.update_numbers()
                return instance

            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_org_manager():
                    return profile.get_course_groups().exclude(deleted=True)
                return profile.get_course_groups()

        # 我所教的课程组
        class CourseGroupTeachingViewSet(ListReadonlyResourceViewSet):
            queryset = CourseGroup.objects.all()
            serializer_class = CourseSerializers.CourseGroup.List
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('caption',)
            search_fields = ('caption',)

            def get_queryset(self):
                profile = self.request.user.profile
                return profile.get_course_groups(teaching=True).exclude(deleted=True)

        # 课程所隶属的课程组 - deep2 - relation
        class CourseGroupCourseViewSet(ListNestedResourceViewSet):
            queryset = CourseGroupRelation.objects.all()
            serializer_class = CourseSerializers.CourseCourseGroup.List
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            ordering_fields = ('id',)

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course'  # 在当前models中，上级model的关联名
            parent_pk = 'cid'  # 上级model的主键名

        # 课程可以加入的课程组 - deep2
        class CourseGroupAvailableCourseViewSet(ListReadonlyNestedResourceViewSet):
            queryset = CourseGroup.objects.all()
            serializer_class = CourseSerializers.CourseCourseGroup.ListAvailable
            permission_classes = (IsEduAdminReadonly,)
            ordering_fields = ('id',)

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'
            parent_pk = 'cid'
            parent_related_name = 'course'

            def _set_queryset(self, **kwargs):
                # 有关可以使用的题库的选定规则：
                # 机构使用的题库，仅显示与该机构有直接关联的题库；
                # 机构可以使用的题库，仅显示该机构还没添加、但是(上级机构添加了的题库|上级机构是root时的所有题库).
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到上级course的cid
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该course
                self.queryset = parent.available_course_groups(filter_exists=True)

                return parent_related_name, parent

    class CourseGroupInstance(object):
        # 课程组
        class CourseGroupViewSet(InstanceResourceViewSet):
            queryset = CourseGroup.objects.all()
            serializer_class = CourseSerializers.CourseGroup.Instance
            permission_classes = (IsAnyOrgReadonlyOrEduAdmin,)
            lookup_field = 'gid'

            def perform_destroy(self, instance):
                organization = instance.organization
                super().perform_destroy(instance)
                organization.update_numbers()

            def get_queryset(self):
                # 限定访问列表。
                # 对于site权限，全部可访问.对于EDU_ADMIN，可访问全部org相关;对于Teacher，可访问关联项
                profile = self.request.user.profile
                identities = profile.identities
                course_groups_queryset = self.queryset.none()
                for identity, value in identities.items():
                    if identity in SITE_IDENTITY_CHOICES and value is True:
                        return self.queryset
                    elif identity in ORG_IDENTITY_CHOICES and identity == IdentityChoices.edu_admin and len(value) > 0:
                        for oid in value:
                            organization = Organization.objects.filter(id=oid).first()
                            org_course_groups = CourseGroup.objects.filter(organization_id=organization.name)
                            course_groups_queryset = course_groups_queryset | org_course_groups
                for teacher in profile.teacher_identities.all():
                    course_groups_queryset = course_groups_queryset | teacher.course_groups
                if not profile.is_org_manager():
                    return course_groups_queryset.exclude(deleted=True).distinct()
                return course_groups_queryset.distinct()

        # 课程所隶属的课程组 - deep2 - relation
        class CourseGroupCourseViewSet(InstanceNestedResourceViewSet):
            queryset = CourseGroupRelation.objects.all()
            serializer_class = CourseSerializers.CourseCourseGroup.Instance
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            lookup_field = 'id'

            parent_queryset = Course.objects.all()
            parent_lookup = 'course_cid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course'  # 在当前models中，上级model的关联名
            parent_pk = 'cid'  # 上级model的主键名


# 任务及任务组相关api
class MissionViewSets(object):
    class MissionList(object):
        # 课程基类下的任务 - deep2
        class MissionMetaViewSet(ListNestedResourceViewSet):
            queryset = Mission.objects.all()
            serializer_class = MissionSerializers.Mission.List
            permission_classes = (IsTeacherOrEduAdmin,)
            ordering_fields = ('caption', 'start_time', 'end_time')
            search_fields = ('caption',)

            parent_queryset = CourseMeta.objects.all()
            parent_lookup = 'course_meta_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_meta'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def set_queryset(self):
                profile = self.request.user.profile
                if not profile.is_mission_manager():
                    return self.queryset.exclude(deleted=True)
                return self.queryset

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                instance.organization.update_numbers()
                return instance

        # 任务组下的任务 - deep2 - relation
        class MissionMissionGroupViewSet(ListNestedResourceViewSet):
            queryset = MissionGroupRelation.objects.all()
            serializer_class = MissionSerializers.MissionMissionGroup.List
            permission_classes = (IsStudentReadonlyOrAnyOrg,)
            ordering_fields = ('id',)

            parent_queryset = MissionGroup.objects.all()
            parent_lookup = 'mission_group_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission_group'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

        # 任务组下可以添加的任务 - deep2
        class MissionAvailableMissionGroupViewSet(ListReadonlyNestedResourceViewSet):
            queryset = Mission.objects.all()
            serializer_class = MissionSerializers.MissionMissionGroup.ListAvailable
            permission_classes = (IsTeacherOrEduAdminReadonly,)
            ordering_fields = ('id',)

            parent_queryset = MissionGroup.objects.all()
            parent_lookup = 'mission_group_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission_group'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def _set_queryset(self, **kwargs):
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到上级course的cid
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该course
                self.queryset = parent.available_missions(filter_exists=True)

                return parent_related_name, parent

    class MissionInstance(object):
        # 任务
        class MissionViewSet(InstanceResourceViewSet):
            queryset = Mission.objects.all()
            serializer_class = MissionSerializers.Mission.Instance
            permission_classes = (IsStudentReadonlyOrAnyOrg,)
            lookup_field = 'id'

            def perform_destroy(self, instance):
                organization = instance.organization
                super().perform_destroy(instance)
                organization.update_numbers()

            def get_queryset(self):
                # 限定访问列表。对于T/edu_admin/site，公开机构内全部/全部公开;对于S，仅包含关联部分
                # 关联判定：mission隶属于mission_group.而mission_group又属于course_unit.
                profile = self.request.user.profile
                queryset = self.queryset.none()
                course_units = CourseUnit.objects.none()
                for identity, value in profile.identities.items():
                    if identity in SITE_IDENTITY_CHOICES and value is True:
                        return self.queryset
                    elif identity == IdentityChoices.edu_admin \
                            or identity == IdentityChoices.teacher and len(value) > 0:
                        for oid in value:
                            queryset = queryset | self.queryset.filter(organization_id=oid)
                units = (v['course_unit'] for v in profile.get_courses().values('course_unit'))
                course_units = course_units | CourseUnit.objects.filter(id__in=units)
                # 从课程单元查任务组，再查任务
                mission_groups = MissionGroup.objects.none()
                for course_unit in course_units:
                    if hasattr(course_unit, 'mission_groups'):
                        mission_groups = mission_groups | course_unit.mission_groups.all()
                for mission_group in mission_groups:
                    queryset = queryset | mission_group.missions.all()
                if not profile.is_mission_manager():
                    return queryset.exclude(deleted=True).distinct()
                return queryset.distinct()

        # 任务组下的任务 - deep2 - relation
        class MissionMissionGroupViewSet(InstanceNestedResourceViewSet):
            queryset = MissionGroupRelation.objects.all()
            serializer_class = MissionSerializers.MissionMissionGroup.List
            permission_classes = (IsStudentReadonlyOrAnyOrg,)
            lookup_field = 'id'

            parent_queryset = MissionGroup.objects.all()
            parent_lookup = 'mission_group_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission_group'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

    class MissionGroupList(object):
        # 课程下的任务组
        class MissionGroupCourseViewSet(ListNestedResourceViewSet):
            queryset = MissionGroup.objects.all()
            serializer_class = MissionSerializers.MissionGroup.ListCourse
            permission_classes = (IsStudentReadonlyOrAnyOrg,)
            ordering_fields = ('caption', 'weight')
            search_fields = ('caption',)

            parent_queryset = CourseUnit.objects.all()
            parent_lookup = 'course_cid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_unit'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def _set_queryset(self, **kwargs):
                # 需要特别对待。
                # 学生将需要从这里访问到该课程隶属的课程组的任务组。
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]

                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 课程单元

                self.queryset = self.queryset.filter(**{parent_related_name: parent})  # 这里做了初步筛选。

                profile = self.request.user.profile
                if profile.has_identities(IdentityChoices.student):
                    now_course = getattr(parent, 'course')
                    if hasattr(now_course, 'course_groups'):
                        course_groups = now_course.course_groups.all()
                        for g in course_groups:
                            unit = g.course_unit
                            if hasattr(unit, 'mission_groups'):
                                self.queryset = self.queryset | unit.mission_groups.all()
                        self.queryset = self.queryset.distinct()
                if not profile.is_mission_manager():
                    self.queryset = self.queryset.exclude(deleted=True)
                return parent_related_name, parent

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                instance.organization.update_numbers()
                return instance

        # 课程组下的任务组
        class MissionGroupCourseGroupViewSet(ListNestedResourceViewSet):
            queryset = MissionGroup.objects.all()
            serializer_class = MissionSerializers.MissionGroup.ListCourseGroup
            permission_classes = (IsTeacherOrEduAdmin,)
            ordering_fields = ('caption', 'weight')
            search_fields = ('caption',)

            parent_queryset = CourseUnit.objects.all()
            parent_lookup = 'course_group_gid'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'course_unit'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                instance.organization.update_numbers()
                return instance

    class MissionGroupInstance(object):
        # 任务组
        class MissionGroupViewSet(InstanceResourceViewSet):
            queryset = MissionGroup.objects.all()
            serializer_class = MissionSerializers.MissionGroup.Instance
            permission_classes = (IsStudentReadonlyOrAnyOrg,)
            lookup_field = 'id'

            def perform_destroy(self, instance):
                organization = instance.organization
                super().perform_destroy(instance)
                organization.update_numbers()

            def get_queryset(self):
                # 限定访问列表。对于edu_admin/site,公开全部
                # 对于T,包含关联部分。
                profile = self.request.user.profile
                queryset = self.queryset.none()
                course_units = CourseUnit.objects.none()
                for identity, value in profile.identities.items():
                    if identity in SITE_IDENTITY_CHOICES and value is True:
                        return self.queryset
                    elif identity == IdentityChoices.edu_admin and len(value) > 0:
                        for oid in value:
                            queryset = queryset | self.queryset.filter(organization_id=oid)
                units = (v['course_unit'] for v in profile.get_courses().values('course_unit'))
                g_units = (v['course_unit'] for v in profile.get_course_groups().values('course_unit'))
                course_units = course_units | CourseUnit.objects.filter(id__in=units)
                course_units = course_units | CourseUnit.objects.filter(id__in=g_units)
                # 从课程单元查任务组，再查任务
                mission_groups = MissionGroup.objects.none()
                for course_unit in course_units:
                    if hasattr(course_unit, 'mission_groups'):
                        mission_groups = mission_groups | course_unit.mission_groups.all()
                if not profile.is_mission_manager():
                    return mission_groups.exclude(deleted=True).distinct()
                return mission_groups.distinct()

    class ProblemList(object):
        # 任务下的题目 - deep2 - relation
        class ProblemViewSet(ListNestedResourceViewSet):
            queryset = MissionProblemRelation.objects.all()
            serializer_class = ProblemRelationSerializers.List
            permission_classes = (IsStudentReadonlyOrAnyOrg,)
            ordering_fields = ('id', 'weight')
            search_fields = ('id',)

            parent_queryset = Mission.objects.all()
            parent_lookup = 'mission_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def list(self, request, *args, **kwargs):
                # 对学生而言，无法在任务开始之前查看题目列表
                profile = self.request.user.profile

                if profile.has_identities(IdentityChoices.student):
                    # 学生权限下需要做时间验证.
                    parent_id = kwargs[self.parent_lookup]
                    parent_mission = get_object_or_404(Mission.objects.all(), id=parent_id)
                    if parent_mission.get_state() == MissionState.not_started:
                        data = {
                            'message': 'The mission is not started.'
                        }
                        return Response(data, 406)
                result = super().list(request, *args, **kwargs)

                return result

            def create(self, request, *args, **kwargs):
                # 对学生而言，不能在任务开始之前做提交
                profile = self.request.user.profile
                if profile.has_identities(IdentityChoices.student):
                    # 学生权限下需要做时间验证.
                    parent_id = kwargs[self.parent_lookup]
                    parent_mission = get_object_or_404(Mission.objects.all(), id=parent_id)
                    if parent_mission.get_state() == MissionState.not_started:
                        data = {
                            'message': 'The mission is not started.'
                        }
                        return Response(data, 406)
                result = super().create(request, *args, **kwargs)
                return result

        # 任务可以使用的全部题目 - deep2 - relation
        class ProblemAvailableViewSet(ListReadonlyNestedResourceViewSet):
            queryset = CategoryProblemRelation.objects.all()
            serializer_class = ProblemRelationSerializers.ListAvailable
            permission_classes = (IsTeacherOrEduAdminReadonly,)
            ordering_fields = ('id',)
            search_fields = ('id',)

            parent_queryset = Mission.objects.all()
            parent_lookup = 'mission_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def _set_queryset(self, **kwargs):
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]  # 查询得到上级course的cid
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 查询得到该course
                self.queryset = parent.available_problem_relations()

                return parent_related_name, parent

    class ProblemInstance(object):
        # 任务下的题目 - deep2 - relation
        class ProblemViewSet(InstanceNestedResourceViewSet):
            queryset = MissionProblemRelation.objects.all()
            serializer_class = ProblemRelationSerializers.Instance
            permission_classes = (IsStudentReadonlyOrAnyOrg,)
            lookup_field = 'id'

            parent_queryset = Mission.objects.all()
            parent_lookup = 'mission_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

    class SubmissionList(object):
        # 任务下的提交 - deep2
        class SubmissionViewSet(ListNestedViewSet):
            queryset = Submission.objects.order_by('-update_time')
            serializer_class = SubmissionSerializers.List
            permission_classes = (IsAnyOrg,)
            ordering_fields = ('id', 'sid', 'status', 'submit_time', 'update_time', 'user', 'environment')
            search_fields = ('status', 'user', 'environment')

            parent_queryset = Mission.objects.all()
            parent_lookup = 'mission_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def _set_queryset(self, **kwargs):
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]

                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # 获得了任务的model
                # 由于存在配置，需要限制学生的访问范围。
                profile = self.request.user.profile
                if not profile.is_mission_manager():  # 这表示是学生。需要作出限制。
                    submission_display = parent.config['submission_display']
                    if submission_display == 'no':
                        self.queryset = Submission.objects.none()
                    elif submission_display == 'self':
                        self.queryset = Submission.objects.\
                            filter(**{parent_related_name: parent}).filter(user=profile).order_by('-update_time')
                else:
                    self.queryset = Submission.objects.filter(**{parent_related_name: parent}).order_by('-update_time')
                return parent_related_name, parent

            def create(self, request, *args, **kwargs):
                profile = self.request.user.profile

                if profile.has_identities(IdentityChoices.student):
                    # 学生权限下需要做时间验证.
                    parent_id = kwargs[self.parent_lookup]
                    parent_mission = get_object_or_404(Mission.objects.all(), id=parent_id)
                    if parent_mission.get_state() == MissionState.not_started:
                        data = {
                            'message': 'The mission is not started.'
                        }
                        return Response(data, 406)

                return super().create(request, *args, **kwargs)

            def perform_create(self, serializer):

                extra_data = getattr(self, 'extra_data')
                extra_data['profile'] = self.request.user.profile
                return super().perform_create(serializer)

    class SubmissionInstance(object):
        # 任务下的提交
        class SubmissionViewSet(InstanceReadonlyNestedViewSet):
            queryset = Submission.objects.all()
            serializer_class = SubmissionSerializers.Instance
            permission_classes = (IsAnyOrg,)
            lookup_field = 'id'

            parent_queryset = Mission.objects.all()
            parent_lookup = 'mission_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def retrieve(self, request, *args, **kwargs):
                profile = self.request.user.profile

                if profile.has_identities(IdentityChoices.student):
                    # 学生权限下需要做隶属验证.
                    obj = self.get_object()
                    if obj is None or getattr(obj, 'user') != profile:
                        data = {
                            'message': 'You cannot see others\' submissions.'
                        }
                        return Response(data, 406)
                instance = super().retrieve(request, *args, **kwargs)
                return instance

    class RankInstance(object):
        # 任务下的成绩信息
        class RankViewSet(InstanceReadonlyNestedResourceViewSet):
            queryset = Rank.objects.all()
            serializer_class = RankSerializers.Instance
            permission_classes = (IsAnyOrgReadonly,)
            lookup_field = 'user__username'

            parent_queryset = Mission.objects.all()
            parent_lookup = 'mission_id'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'mission'  # 在当前models中，上级model的关联名
            parent_pk = 'id'  # 上级model的主键名

            def _set_queryset(self, **kwargs):
                parent_queryset = getattr(self, 'parent_queryset')
                parent_lookup = getattr(self, 'parent_lookup')
                parent_pk = getattr(self, 'parent_pk')
                parent_related_name = getattr(self, 'parent_related_name')

                lookup = kwargs[parent_lookup]

                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})

                setattr(self, 'queryset',
                        getattr(self, 'queryset').filter(**{parent_related_name: parent}))

                return parent_related_name, parent

            def retrieve(self, request, *args, **kwargs):
                self._set_queryset(**kwargs)
                profile = self.request.user.profile
                parent = Mission.objects.filter(id=kwargs['mission_id']).first()
                if not profile.is_mission_manager():
                    self.queryset = self.queryset.filter(user=profile)
                    if parent.config['score_display'] == 'yes':  # 显示成绩，不作处理
                        pass
                    elif parent.config['score_display'] == 'close':  # 临时封闭成绩，检测时间段，如果在缎内不显示
                        if parent.get_state() != MissionState.ended:
                            data = {
                                'message': 'Score is not available now.'
                            }
                            return Response(data, 406)
                    elif parent.config['score_display'] == 'no':  # 就是不给你看
                        data = {
                            'message': 'Score is not available.'
                        }
                        return Response(data, 406)
                instance = super().retrieve(request, *args, **kwargs)
                return instance
