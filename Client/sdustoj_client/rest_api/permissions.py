# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import IdentityChoices, SITE_IDENTITY_CHOICES


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated():
            return False
        return user == obj or user == obj.user


class SitePermission(BasePermission):
    read_identities = []
    write_identities = []

    @staticmethod
    def _has_site_identity(expected_identities, user_identities, request):
        if request:
            pass
        for identity in expected_identities:
            if identity in SITE_IDENTITY_CHOICES and identity in user_identities:
                return True
        return False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        identities = user.profile.identities
        if request.method in SAFE_METHODS:
            return self._has_site_identity(self.read_identities, identities, request)
        else:
            return self._has_site_identity(self.write_identities, identities, request)


class OrgPermission(BasePermission):
    read_identities = []
    write_identities = []

    @staticmethod
    def _has_site_identity(expected_identities, user_identities, request):
        if request:
            pass
        for identity in expected_identities:
            if identity in SITE_IDENTITY_CHOICES and identity in user_identities:
                return True
        return False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        identities = user.profile.identities
        if request.method in SAFE_METHODS:
            return self._has_site_identity(self.read_identities, identities, request)
        else:
            return self._has_site_identity(self.write_identities, identities, request)


class IsRoot(SitePermission):
    read_identities = [IdentityChoices.root]
    write_identities = [IdentityChoices.root]


class IsUserAdmin(SitePermission):
    read_identities = [IdentityChoices.user_admin, IdentityChoices.root]
    write_identities = [IdentityChoices.user_admin, IdentityChoices.root]


class IsOrgAdmin(SitePermission):
    read_identities = [IdentityChoices.org_admin, IdentityChoices.root]
    write_identities = [IdentityChoices.org_admin, IdentityChoices.root]


