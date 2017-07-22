from rest_framework import viewsets, status, exceptions, response, settings, permissions as permissions_
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import *
from . import permissions
from .serializers import PersonalSerializers, UserSerializers, OrgUserSerializers
from .serializers import OrganizationSerializers, CategorySerializers
from .utils import UserDisabled, AlreadyLogin, OrgNestedMixin
from .utils import ListResourceViewSet, InstanceResourceViewSet
from .utils import ListReadonlyResourceViewSet, InstanceReadonlyResourceViewSet, ListReadonlyNestedResourceViewSet
from .utils import ListNestedResourceViewSet, InstanceNestedResourceViewSet, InstanceReadonlyNestedResourceViewSet
from .utils import ListNestedViewSet, ListReadonlyNestedViewSet, InstanceNestedViewSet, InstanceDeleteNestedViewSet
from .permissions import IsRoot, IsUserAdmin, IsOrgAdmin, IsStudent, IsTeacher, IsEduAdmin, IsAnyOrg, IsAnyOrgReadonly
from .permissions import IsStudentReadonly, IsTeacherReadonly, IsEduAdminReadonly, IsTeacherReadonlyOrEduAdmin
from .permissions import IsStudentReadonlyOrEduAdmin


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
                    if user.profile.available:
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
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).filter(identities__ORG_ADMIN=True).order_by('username')
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

        # admin - 机构管理员
        class OrgAdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).filter(identities__ORG_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.InstanceOrgAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

        # admin - 用户管理员
        class UserAdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).\
                filter(identities__USER_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.InstanceUserAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

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
        class EduAdminViewSet(OrgNestedMixin, ListNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.ListEduAdmin
            permission_classes = (IsOrgAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.edu_admin,)  # 在当前models中，上级model的关联名

    # admin用户管理部分的用户
    class UserInstance(object):
        # admin - 所有用户
        class UserAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

        # admin - 教务管理员 - deep2
        class EduAdminViewSet(OrgNestedMixin, InstanceNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceEduAdmin
            permission_classes = (IsOrgAdmin,)
            lookup_field = 'username'

            parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.edu_admin,)  # 在当前models中，上级model的关联名

    # org部分下属的用户
    class OrgUserList(object):
        # 教务管理员 - deep2
        class EduAdminViewSet(OrgNestedMixin, ListReadonlyNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.ListEduAdmin
            permission_classes = (IsEduAdminReadonly,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.edu_admin,)  # 在当前models中，上级model的关联名

        # 教师 - deep2
        class TeacherViewSet(OrgNestedMixin, ListNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.ListTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.teacher,)  # 在当前models中，上级model的关联名

        # 学生 - deep2
        class StudentViewSet(OrgNestedMixin, ListNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.ListStudent
            permission_classes = (IsStudentReadonlyOrEduAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.student,)  # 在当前models中，上级model的关联名

    # org部分下属的用户
    class OrgUserInstance(object):
        # 教务管理员 - deep2
        class EduAdminViewSet(OrgNestedMixin, InstanceReadonlyNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceEduAdmin
            permission_classes = (IsEduAdminReadonly,)
            lookup_field = 'username'

            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.edu_admin,)  # 在当前models中，上级model的关联名

        # 教师 - deep2
        class TeacherViewSet(OrgNestedMixin, InstanceNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.InstanceTeacher
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)
            lookup_field = 'username'

            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.teacher,)  # 在当前models中，上级model的关联名

        # 学生 - deep2
        class StudentViewSet(OrgNestedMixin, InstanceNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.InstanceStudent
            permission_classes = (IsStudentReadonlyOrEduAdmin,)
            lookup_field = 'username'
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.student,)  # 在当前models中，上级model的关联名


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
            queryset = getattr(Organization, 'objects').exclude(name='ROOT').order_by('id')
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
                    return self.queryset

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
                super().perform_destroy(instance)
                parent.update_numbers()

        # 所有相关机构
        class OrganizationViewSet(InstanceReadonlyResourceViewSet):
            queryset = getattr(Organization, 'objects').exclude(name='ROOT').order_by('id')
            serializer_class = OrganizationSerializers.Organization.Instance
            permission_classes = (IsAnyOrgReadonly,)
            lookup_field = 'name'


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

        # admin - 可以使用的题库 - deep2
        class CategoryAvailableOrgAdminViewSet(ListReadonlyNestedViewSet):
            queryset = Category.objects.all()
            serializer_class = CategorySerializers.Category.ListAvailableOrgAdmin
            permission_classes = (IsOrgAdmin,)
            ordering_fields = ('name', 'number_problem')
            search_fields = ('name',)

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

