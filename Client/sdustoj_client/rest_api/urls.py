from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from .views import PersonalViewSets, UserViewSets
from .views import OrganizationViewSets, CategoryViewSet, CourseViewSets


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

# --------
admin_organization_router = NestedSimpleRouter(admin_router, r'organizations', lookup='admin_organization')
admin_organization_router.register(
    r'categories', CategoryViewSet.CategoryList.CategoryOrgAdminViewSet, base_name='admin-organization-categories')
admin_organization_router.register(
    r'categories', CategoryViewSet.CategoryInstance.CategoryOrgAdminViewSet, base_name='admin-organization-categories')
admin_organization_router.register(
    r'available-categories', CategoryViewSet.CategoryList.CategoryAvailableOrgAdminViewSet,
    base_name='admin-organization-available-categories')
admin_organization_router.register(
    r'admins', UserViewSets.UserList.EduAdminViewSet, base_name='admin-organization-edu-admins')
admin_organization_router.register(
    r'admins', UserViewSets.UserInstance.EduAdminViewSet, base_name='admin-organization-edu-admins')
# --------

admin_patterns = []
admin_patterns += admin_router.urls
admin_patterns += admin_organization_router.urls


api_router = routers.DefaultRouter()

api_router.register(
    r'login', PersonalViewSets.Login.LoginViewSet, base_name='api-login')
api_router.register(
    r'logout', PersonalViewSets.Logout.LogoutViewSet, base_name='api-logout')
api_router.register(
    r'personal-info', PersonalViewSets.Personal.PersonalViewSet, base_name='api-personal-info')
api_router.register(
    r'personal-password', PersonalViewSets.Personal.PasswordViewSet, base_name='api-personal-password')
api_router.register(
    r'organizations', OrganizationViewSets.OrganizationList.OrganizationViewSet, base_name='api-organization')
api_router.register(
    r'organizations', OrganizationViewSets.OrganizationInstance.OrganizationViewSet, base_name='api-organization')
api_router.register(
    r'course-metas', CourseViewSets.CourseMetaInstance.CourseMetaViewSet, base_name='api-course-meta')
api_router.register(
    r'courses', CourseViewSets.CourseInstance.CourseViewSet, base_name='api-course')
api_router.register(
    r'course-groups', CourseViewSets.CourseGroupInstance.CourseGroupViewSet, base_name='api-course-group')

# --------
api_organization_router = NestedSimpleRouter(api_router, r'organizations', lookup='organization')
api_organization_router.register(
    r'admins', UserViewSets.OrgUserList.EduAdminViewSet, base_name='api-organization-edu-admins')
api_organization_router.register(
    r'admins', UserViewSets.OrgUserInstance.EduAdminViewSet, base_name='api-organization-edu-admins')
api_organization_router.register(
    r'teachers', UserViewSets.OrgUserList.TeacherViewSet, base_name='api-organization-teacher')
api_organization_router.register(
    r'teachers', UserViewSets.OrgUserInstance.TeacherViewSet, base_name='api-organization-teacher')
api_organization_router.register(
    r'students', UserViewSets.OrgUserList.StudentViewSet, base_name='api-organization-student')
api_organization_router.register(
    r'students', UserViewSets.OrgUserInstance.StudentViewSet, base_name='api-organization-student')
api_organization_router.register(
    r'course-metas', CourseViewSets.CourseMetaList.CourseMetaOrgViewSet, base_name='api-organization-course-meta')
# --------
api_course_meta_router = NestedSimpleRouter(api_router, r'course-metas', lookup='course_meta')
api_course_meta_router.register(
    r'courses', CourseViewSets.CourseList.CourseViewSet, base_name='api-course-meta-course')
api_course_meta_router.register(
    r'course-groups', CourseViewSets.CourseGroupList.CourseGroupViewSet, base_name='api-course-meta-course-group')


api_patterns = []
api_patterns += api_router.urls
api_patterns += api_organization_router.urls
api_patterns += api_course_meta_router.urls
