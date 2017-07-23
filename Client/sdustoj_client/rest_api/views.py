from rest_framework import viewsets, status, exceptions, response, settings, permissions as permissions_
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import *
from . import permissions
from .serializers import PersonalSerializers, UserSerializers, OrgUserSerializers
from .serializers import OrganizationSerializers, CategorySerializers
from .serializers import CourseSerializers
from .utils import UserDisabled, AlreadyLogin, OrgNestedMixin
from .utils import ListResourceViewSet, InstanceResourceViewSet
from .utils import ListReadonlyResourceViewSet, InstanceReadonlyResourceViewSet, ListReadonlyNestedResourceViewSet
from .utils import ListNestedResourceViewSet, InstanceNestedResourceViewSet, InstanceReadonlyNestedResourceViewSet
from .utils import ListNestedViewSet, ListReadonlyNestedViewSet, InstanceNestedViewSet, InstanceDeleteNestedViewSet
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

        # admin - 机构管理员
        class OrgAdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').\
                filter(is_staff=True).filter(identities__ORG_ADMIN=True).order_by('username')
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

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得UserProfile
                edu_admin = instance.edu_admin_identities
                for i in edu_admin.all():
                    i.organization.update_numbers()
                return instance

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

            def perform_update(self, serializer):
                instance = super().perform_update(serializer)  # 获得UserProfile
                edu_admin = instance.edu_admin_identities
                for i in edu_admin.all():
                    i.organization.update_numbers()
                return instance

            def perform_destroy(self, instance):
                edu_admin = instance.edu_admin_identities
                super().perform_destroy(instance)
                for i in edu_admin.all():
                    i.organization.update_numbers()

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

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得UserProfile
                identities = instance.teacher_identities
                for i in identities.all():
                    i.organization.update_numbers()
                return instance

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

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)  # 获得UserProfile
                identities = instance.student_identities
                for i in identities.all():
                    i.organization.update_numbers()
                return instance

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

            def perform_update(self, serializer):
                instance = super().perform_update(serializer)  # 获得UserProfile
                identities = instance.teacher_identities
                for i in identities.all():
                    i.organization.update_numbers()
                return instance

            def perform_destroy(self, instance):
                identities = instance.teacher_identities
                super().perform_destroy(instance)
                for i in identities.all():
                    i.organization.update_numbers()

        # 学生 - deep2
        class StudentViewSet(OrgNestedMixin, InstanceNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = OrgUserSerializers.InstanceStudent
            permission_classes = (IsStudentReadonlyOrEduAdmin,)
            lookup_field = 'username'
            parent_lookup = 'organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
            parent_related_name = 'identities__%s__contains' % (IdentityChoices.student,)  # 在当前models中，上级model的关联名

            def perform_update(self, serializer):
                instance = super().perform_update(serializer)  # 获得UserProfile
                identities = instance.student_identities
                for i in identities.all():
                    i.organization.update_numbers()
                return instance

            def perform_destroy(self, instance):
                identities = instance.student_identities
                super().perform_destroy(instance)
                for i in identities.all():
                    i.organization.update_numbers()


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
            queryset = getattr(Organization, 'objects').exclude(name='ROOT').order_by('id')
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

            def perform_destroy(self, instance):
                organization = instance.organization
                super().perform_destroy(instance)
                organization.update_numbers()


# 课程基类与课程api
class CourseViewSets(object):
    class CourseMetaList(object):
        # 机构下的课程基类 - deep2
        class CourseMetaOrgViewSet(ListNestedResourceViewSet):
            queryset = CourseMeta.objects.all()
            serializer_class = CourseSerializers.CourseMeta.ListOrg
            permission_classes = (IsTeacherReadonlyOrEduAdmin,)  # todo 课程基类列表的查看权限待定
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

            def get_queryset(self):
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
                queryset = None
                for org in org_set:
                    if queryset is None:
                        queryset = self.queryset.filter(organization__id=org)
                    else:
                        queryset = queryset | self.queryset.filter(organization__id=org)
                if queryset is None:
                    return CourseMeta.objects.none()
                else:
                    return queryset

    class CourseList(object):
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

            def perform_create(self, serializer):
                instance = super().perform_create(serializer)
                instance.organization.update_numbers()
                return instance

    class CourseInstance(object):
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
                return profile.get_courses()

    class CourseGroupList(object):
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

    class CourseGroupInstance(object):
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
                # 对于site权限，全部可访问.对于EDUADMIN，可访问全部org相关;对于Teacher，可访问关联项
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
                return course_groups_queryset
