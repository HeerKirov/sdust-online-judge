from rest_framework import viewsets, status, exceptions, response, settings, permissions as permissions_
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import *
from . import permissions
from .serializers import PersonalSerializers, UserSerializers
from .serializers import OrganizationSerializers, CategorySerializers
from .utils import UserDisabled, AlreadyLogin
from .utils import ListResourceViewSet, InstanceResourceViewSet
from .utils import ListNestedResourceViewSet, InstanceNestedResourceViewSet
from .utils import ListNestedViewSet, ListReadonlyNestedViewSet, InstanceNestedViewSet, InstanceDeleteNestedViewSet
from .permissions import IsRoot, IsUserAdmin, IsOrgAdmin


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


class UserViewSets(object):
    class RootList(object):
        # admin - 超级管理员
        class RootAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(
                is_staff=True, identities__ROOT=True).order_by('username')
            serializer_class = UserSerializers.ListAdmin
            permission_classes = (IsRoot,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

    class RootInstance(object):
        # admin - 超级管理员
        class RootAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(
                is_staff=True, identities__ROOT=True).order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
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

    class UserList(object):
        # admin - 所有用户
        class UserAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.ListAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

        # admin - 教务管理员
        class EduAdminViewSet(ListNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.ListEduAdmin
            permission_classes = (IsOrgAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

            def _set_queryset(self, **kwargs):
                parent_queryset = Organization.objects.all()
                parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
                parent_related_name = 'identities__EDU_ADMIN__contains'  # 在当前models中，上级model的关联名
                parent_pk = 'name'  # 上级model的主键名

                lookup = kwargs[parent_lookup]  # parent的id名,即org的name
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})  # parent Org 的model
                org_id = parent.id
                self.queryset = self.queryset.filter(**{parent_related_name: org_id}).all()

                return 'organization', parent  # 返回的元组将在下级的serializer等地方被应用。

    class UserInstance(object):
        # admin - 所有用户
        class UserAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

        # admin - 教务管理员
        class EduAdminViewSet(InstanceNestedResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceEduAdmin
            permission_classes = (IsOrgAdmin,)
            lookup_field = 'username'

            def _set_queryset(self, **kwargs):
                parent_queryset = Organization.objects.all()
                parent_lookup = 'admin_organization_pk'  # url传入的资源参数代号，按照drf-nested规则定义在urls中
                parent_related_name = 'identities__EDU_ADMIN__contains'  # 在当前models中，上级model的关联名
                parent_pk = 'name'  # 上级model的主键名

                lookup = kwargs[parent_lookup]  # parent的id名
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})
                self.queryset = self.queryset.filter(**{parent_related_name: lookup}).all()

                return 'organization', parent


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

            def _set_queryset(self, **kwargs):
                parent_queryset = Organization.objects.all()
                parent_lookup = 'admin_organization_pk'
                parent_pk = 'name'
                parent_related_name = 'organization'

                lookup = kwargs[parent_lookup]
                parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})
                exist_id = [i.id for i in parent.categories.all()]
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

