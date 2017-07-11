from rest_framework import routers

from .views import PersonalViewSets, UserViewSets
from .views import OrganizationViewSets


admin_router = routers.DefaultRouter()

admin_router.register(
    r'roots', UserViewSets.RootList.RootAdminViewSet, base_name='admin-root')
admin_router.register(
    r'roots', UserViewSets.RootInstance.RootAdminViewSet, base_name='admin-root')
admin_router.register(
    r'admins', UserViewSets.AdminList.AdminAdminViewSet, base_name='admin-admin')
admin_router.register(
    r'admins', UserViewSets.AdminInstance.AdminAdminViewSet, base_name='admin-admin')
admin_router.register(
    r'user-admins', UserViewSets.AdminList.UserAdminAdminViewSet, base_name='admin-user-admin')
admin_router.register(
    r'user-admins', UserViewSets.AdminInstance.UserAdminAdminViewSet, base_name='admin-user-admin')
admin_router.register(
    r'org-admins', UserViewSets.AdminList.OrgAdminAdminViewSet, base_name='admin-org-admin')
admin_router.register(
    r'org-admins', UserViewSets.AdminInstance.OrgAdminAdminViewSet, base_name='admin-org-admin')
admin_router.register(
    r'users', UserViewSets.UserList.UserAdminViewSet, base_name='admin-user')
admin_router.register(
    r'users', UserViewSets.UserInstance.UserAdminViewSet, base_name='admin-user')

admin_router.register(
    r'organizations', OrganizationViewSets.OrganizationList.OrganizationAdminViewSet, base_name='admin-organization')
admin_router.register(
    r'organizations', OrganizationViewSets.OrganizationInstance.OrganizationAdminViewSet, base_name='admin-organization')


admin_patterns = []
admin_patterns += admin_router.urls


api_router = routers.DefaultRouter()

api_router.register(
    r'login', PersonalViewSets.Login.LoginViewSet, base_name='api-login')
api_router.register(
    r'logout', PersonalViewSets.Logout.LogoutViewSet, base_name='api-logout')
api_router.register(
    r'personal-info', PersonalViewSets.Personal.PersonalViewSet, base_name='api-personal-info')
api_router.register(
    r'personal-password', PersonalViewSets.Personal.PasswordViewSet, base_name='api-personal-password')

api_patterns = []
api_patterns += api_router.urls
