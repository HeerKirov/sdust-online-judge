from rest_framework import viewsets, status, exceptions, response, settings, permissions as permissions_
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from .models import *
from . import permissions
from .serializers import PersonalSerializers, UserSerializers
from .serializers import OrganizationSerializers
from .utils import UserDisabled, AlreadyLogin
from .utils import ListResourceViewSet, InstanceResourceViewSet
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
        class RootAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(
                is_staff=True, identities__ROOT=True).order_by('username')
            serializer_class = UserSerializers.ListAdmin
            permission_classes = (IsRoot,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

    class RootInstance(object):
        class RootAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(
                is_staff=True, identities__ROOT=True).order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
            permission_classes = (IsRoot,)
            lookup_field = 'username'

    class AdminList(object):
        class AdminAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).order_by('username')
            serializer_class = UserSerializers.ListAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

        class OrgAdminAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).filter(identities__ORG_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.ListOrgAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

        class UserAdminAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).\
                filter(identities__USER_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.ListUserAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

    class AdminInstance(object):
        class AdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

        class OrgAdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).filter(identities__ORG_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.InstanceOrgAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

        class UserAdminAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').filter(is_staff=True).\
                filter(identities__USER_ADMIN=True).order_by('username')
            serializer_class = UserSerializers.InstanceUserAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'

    class UserList(object):
        class UserAdminViewSet(ListResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.ListAdmin
            permission_classes = (IsUserAdmin,)
            search_fields = ('username', 'name')
            ordering_fields = ('username', 'name', 'sex', 'last_login',
                               'creator', 'updater', 'create_time', 'update_time')

    class UserInstance(object):
        class UserAdminViewSet(InstanceResourceViewSet):
            queryset = getattr(UserProfile, 'objects').order_by('username')
            serializer_class = UserSerializers.InstanceAdmin
            permission_classes = (IsUserAdmin,)
            lookup_field = 'username'


class OrganizationViewSets(object):
    class OrganizationList(object):
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
