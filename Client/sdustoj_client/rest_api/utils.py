from rest_framework import viewsets, mixins, status, exceptions, serializers
from django.utils import timezone
from rest_framework.filters import FilterSet
import django_filters
from .models import IdentityChoices, Organization
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404


# -- Tools ----

def dict_sub(dictionary, *args):
    """
    根据参数列表，返回一个字典结构的一部分。
    :param dictionary: 
    :param args: 
    :return: 
    """
    ans = {}
    for a in args:
        ans[a] = dictionary[a]
    return ans


def is_parent_organization(base=None, goal=None):
    """
    判断base是否是goal的一个子机构。
    :param base: 基org。可以为id(int)或org。
    :param goal: 目标org。可以为id(int)或org。
    :return: 
    """
    if base is None or goal is None:
        return False
    if not isinstance(base, Organization):
        if isinstance(base, str):
            base = Organization.objects.filter(name=base).first()
        else:
            base = Organization.objects.filter(id=base).first()
    if not isinstance(goal, Organization):
        if isinstance(goal, str):
            goal = Organization.objects.filter(name=goal).first()
        else:
            goal = Organization.objects.filter(id=goal).first()

    root = Organization.objects.filter(name='ROOT').first()
    checked = set()
    cur = base
    while cur is not None and (goal.id == root.id or cur.id != root.id) and cur.id not in checked:
        if cur.id == goal.id:
            return True
        checked.add(cur.id)
        cur = cur.parent
    return False


def is_parent_organizations(base, goal=None):
    """
    判断base列表是否存在goal的子机构。
    :param base: 一个机构列表
    :param goal: 一个机构
    :return: 
    """
    if base is None or goal is None:
        return False
    for i in base:
        if is_parent_organization(i, goal):
            return True
    return False


# -- Functions --------------------------------------------------------------------------

def is_root(user):
    return IdentityChoices.root in user.identities


def is_user_admin(user):
    return IdentityChoices.user_admin in user.identities


def is_org_admin(user):
    return IdentityChoices.org_admin in user.identities


def has_org_identity(user_identities, identity_str, organization_id):
    return identity_str in user_identities and organization_id in user_identities[identity_str]


def is_edu_admin(user, organization_id):
    edu_admin = IdentityChoices.edu_admin
    return has_org_identity(user.identities, edu_admin, organization_id)


def is_teacher(user, organization_id):
    teacher = IdentityChoices.teacher
    return has_org_identity(user.identities, teacher, organization_id)


# -- Exception --------------------------------------------------------------------------

class UserDisabled(exceptions.AuthenticationFailed):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('User disabled.')


class AlreadyLogin(exceptions.PermissionDenied):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Already login.')


# -- Filters ----------------------------------------------------------------------------

class ResourceFilter(FilterSet):
    create_time_gte = django_filters.DateTimeFilter(name='create_time', lookup_expr='gte')
    create_time_lte = django_filters.DateTimeFilter(name='create_time', lookup_expr='lte')
    update_time_gte = django_filters.DateTimeFilter(name='update_time', lookup_expr='gte')
    update_time_lte = django_filters.DateTimeFilter(name='update_time', lookup_expr='lte')
    creator = django_filters.CharFilter(name='creator')
    updater = django_filters.CharFilter(name='updater')


# -- Mixin ------------------------------------------------------------------------------

class ExtraDataMixin(object):
    def __init__(self, *args, **kwargs):
        self.extra_data = {}
        init = getattr(super(), '__init__')
        init(*args, **kwargs)


class CreateResourceMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        extra_data = getattr(self, 'extra_data')
        extra_data['creator'] = request.user.username
        extra_data['updater'] = request.user.username
        extra_data['let_creator'] = request.user.username
        extra_data['let_updater'] = request.user.username
        extra_data['update_time'] = timezone.now()
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        extra_data = getattr(self, 'extra_data')
        instance = serializer.save(**extra_data)
        return instance


class UpdateResourceMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        extra_data = getattr(self, 'extra_data')
        extra_data['updater'] = request.user.username
        extra_data['update_time'] = timezone.now()
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        extra_data = getattr(self, 'extra_data')
        instance = serializer.save(**extra_data)
        return instance


class NestedMixin(object):
    parent_queryset = None
    parent_lookup = None
    parent_pk = None
    parent_related_name = None

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


class OrgNestedMixin(object):
    """
    专供parent为org的user使用的混入类。仅重写了set_queryset函数以契合通用的identity查询模式。
    """
    parent_queryset = Organization.objects.all()
    parent_lookup = None
    parent_pk = 'name'
    parent_related_name = None
    parent_resource_name = 'organization'

    def _set_queryset(self, **kwargs):
        parent_queryset = getattr(self, 'parent_queryset')  # Organization的查询集
        parent_lookup = getattr(self, 'parent_lookup')  # 在url中的资源代号
        parent_pk = getattr(self, 'parent_pk')  # 在Organization中的查询键
        parent_related_name = getattr(self, 'parent_related_name')  # 与上级model的关联名称
        parent_resource_name = getattr(self, 'parent_resource_name')  # 导入到下级资源的名称

        lookup = kwargs[parent_lookup]  # parent的id名
        parent = get_object_or_404(parent_queryset, **{parent_pk: lookup})
        org_id = parent.id
        self.queryset = self.queryset.filter(**{parent_related_name: org_id}).all()

        return parent_resource_name, parent


class ListNestedMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        getattr(self, '_set_queryset')(**kwargs)
        return super().list(request, *args, **kwargs)


class CreateNestedMixin(CreateResourceMixin):
    def create(self, request, *args, **kwargs):
        related_name, parent = getattr(self, '_set_queryset')(**kwargs)
        extra_data = getattr(self, 'extra_data')
        extra_data[related_name] = parent
        return super().create(request, *args, **kwargs)


class RetrieveNestedMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        getattr(self, '_set_queryset')(**kwargs)
        return super().retrieve(request, *args, **kwargs)


class UpdateNestedMixin(UpdateResourceMixin):
    def update(self, request, *args, **kwargs):
        getattr(self, '_set_queryset')(**kwargs)
        return super().update(request, *args, **kwargs)


class DestroyNestedMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        getattr(self, '_set_queryset')(**kwargs)
        return super().destroy(request, *args, **kwargs)


# -- View Set ---------------------------------------------------------------------------

class ListResourceViewSet(mixins.ListModelMixin,
                          CreateResourceMixin,
                          ExtraDataMixin,
                          viewsets.GenericViewSet):
    pass


class ListReadonlyResourceViewSet(mixins.ListModelMixin,
                                  ExtraDataMixin,
                                  viewsets.GenericViewSet):
    pass


class InstanceResourceViewSet(mixins.RetrieveModelMixin,
                              UpdateResourceMixin,
                              mixins.DestroyModelMixin,
                              ExtraDataMixin,
                              viewsets.GenericViewSet):
    pass


class InstanceReadonlyResourceViewSet(mixins.RetrieveModelMixin,
                                      ExtraDataMixin,
                                      viewsets.GenericViewSet):
    pass


class ResourceViewSet(mixins.ListModelMixin,
                      CreateResourceMixin,
                      mixins.RetrieveModelMixin,
                      UpdateResourceMixin,
                      mixins.DestroyModelMixin,
                      ExtraDataMixin,
                      viewsets.GenericViewSet):
    pass


class ListReadonlyNestedResourceViewSet(ListNestedMixin,
                                        ExtraDataMixin,
                                        NestedMixin,
                                        viewsets.GenericViewSet):
    pass


class ListNestedResourceViewSet(ListNestedMixin,
                                CreateNestedMixin,
                                ExtraDataMixin,
                                NestedMixin,
                                viewsets.GenericViewSet):
    pass


class InstanceNestedResourceViewSet(RetrieveNestedMixin,
                                    UpdateResourceMixin,
                                    DestroyNestedMixin,
                                    ExtraDataMixin,
                                    NestedMixin,
                                    viewsets.GenericViewSet):
    pass


class InstanceReadonlyNestedResourceViewSet(RetrieveNestedMixin,
                                            ExtraDataMixin,
                                            NestedMixin,
                                            viewsets.GenericViewSet):
    pass


class InstanceDeleteNestedResourceViewSet(RetrieveNestedMixin,
                                          DestroyNestedMixin,
                                          ExtraDataMixin,
                                          NestedMixin,
                                          viewsets.GenericViewSet):
    pass


class NestedResourceViewSet(ListNestedMixin,
                            CreateNestedMixin,
                            RetrieveNestedMixin,
                            UpdateResourceMixin,
                            DestroyNestedMixin,
                            ExtraDataMixin,
                            NestedMixin,
                            viewsets.GenericViewSet):
    pass


class ListReadonlyNestedViewSet(ListNestedMixin,
                                ExtraDataMixin,
                                NestedMixin,
                                viewsets.GenericViewSet):
    pass


class ListNestedViewSet(ListNestedMixin,
                        CreateNestedMixin,
                        ExtraDataMixin,
                        NestedMixin,
                        viewsets.GenericViewSet):
    pass


class InstanceNestedViewSet(RetrieveNestedMixin,
                            UpdateResourceMixin,
                            DestroyNestedMixin,
                            ExtraDataMixin,
                            NestedMixin,
                            viewsets.GenericViewSet):
    pass


class InstanceDeleteNestedViewSet(RetrieveNestedMixin,
                                  DestroyNestedMixin,
                                  ExtraDataMixin,
                                  NestedMixin,
                                  viewsets.GenericViewSet):
    pass
