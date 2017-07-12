# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import IdentityChoices, SITE_IDENTITY_CHOICES, ORG_IDENTITY_CHOICES, Organization


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated():
            return False
        return user == obj or user == obj.user


class SitePermission(BasePermission):  # 网站管理型permission的基类。
    read_identities = []
    write_identities = []

    @staticmethod
    def _has_site_identity(expected_identities, user_identities, request):
        if request:  # 这是什么……
            pass
        for identity in expected_identities:
            if identity in SITE_IDENTITY_CHOICES and identity in user_identities:
                return True
        return False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        identities = user.profile.identities  # 取得权限的json数据
        if request.method in SAFE_METHODS:
            return self._has_site_identity(self.read_identities, identities, request)
        else:
            return self._has_site_identity(self.write_identities, identities, request)


class OrgPermission(BasePermission):  # 机构内的permission的基类。
    read_identities = []
    write_identities = []

    @staticmethod
    def _has_org_identity(expected_identities, user_identities, request):
        if request:
            pass
        for identity in expected_identities:
            if identity in user_identities:
                return True
        return False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        identities = user.profile.identities
        if request.method in SAFE_METHODS:
            id_check = self.read_identities
        else:
            id_check = self.write_identities
        return self._has_org_identity(id_check, identities, request)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        identities = user.profile.identities
        if request.method in SAFE_METHODS:
            id_check = self.read_identities
        else:
            id_check = self.write_identities
        for identity in id_check:
            if identity in identities:  # 这表示用户有这个权限的登记
                if identity in ORG_IDENTITY_CHOICES:
                    org_id = identities[identity]  # 获得权限所在的org的id
                    if isinstance(obj, Organization):  # 如果要查看的目标是机构的一个实例
                        # todo:需要顺着org向上查找。
                        if obj.id in org_id:  # 判断是否要查看的目标机构在认证信息的值之中。
                            return True
                    elif obj.organization_id in org_id:
                        # todo:需要顺着org向上查找
                        # todo:最好加一个异常判断，万一obj没有org_id这个东西
                        # 不是一个实例，要查看的目标时其他的目标，那么判断是否该目标的组织所属是不是在user所属组织中
                        return True
                else:  # 如果是一个不是org权限的权限类型，那么不进行org判断直接True。
                    return True


class IsRoot(SitePermission):
    read_identities = [IdentityChoices.root]
    write_identities = [IdentityChoices.root]


class IsUserAdmin(SitePermission):
    read_identities = [IdentityChoices.user_admin, IdentityChoices.root]
    write_identities = [IdentityChoices.user_admin, IdentityChoices.root]


class IsOrgAdmin(SitePermission):
    read_identities = [IdentityChoices.org_admin, IdentityChoices.root]
    write_identities = [IdentityChoices.org_admin, IdentityChoices.root]


class IsEduAdmin(OrgPermission):
    read_identities = [IdentityChoices.edu_admin, IdentityChoices.org_admin, IdentityChoices.root]
    write_identities = [IdentityChoices.edu_admin, IdentityChoices.org_admin, IdentityChoices.root]


class IsEduAdminReadonly(OrgPermission):
    read_identities = [IdentityChoices.edu_admin, IdentityChoices.org_admin, IdentityChoices.root]
    write_identities = [IdentityChoices.org_admin, IdentityChoices.root]


class IsTeacher(OrgPermission):
    read_identities = [IdentityChoices.teacher, IdentityChoices.root]
    write_identities = [IdentityChoices.teacher, IdentityChoices.root]


class IsTeacherReadonly(OrgPermission):
    read_identities = [IdentityChoices.teacher, IdentityChoices.root]
    write_identities = [IdentityChoices.root]


class IsStudent(OrgPermission):
    read_identities = [IdentityChoices.student, IdentityChoices.root]
    write_identities = [IdentityChoices.student, IdentityChoices.root]


class IsStudentReadonly(OrgPermission):
    read_identities = [IdentityChoices.student, IdentityChoices.root]
    write_identities = [IdentityChoices.root]