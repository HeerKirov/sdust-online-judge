from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from .views import PersonalViewSets, UserViewSets
from .views import OrganizationViewSets, CategoryViewSet, CourseViewSets, MissionViewSets


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
    r'organizations', OrganizationViewSets.OrganizationInstance.OrganizationAdminViewSet,
    base_name='admin-organization')
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
    r'teaching-course-groups', CourseViewSets.CourseGroupList.CourseGroupTeachingViewSet,
    base_name='api-teaching-course-groups')
api_router.register(
    r'teaching-courses', CourseViewSets.CourseList.CourseTeachingViewSet, base_name='api-teaching-course')
api_router.register(
    r'learning-courses', CourseViewSets.CourseList.CourseLearningViewSet, base_name='api-learning-course')
api_router.register(
    r'courses', CourseViewSets.CourseInstance.CourseViewSet, base_name='api-course')
api_router.register(
    r'course-groups', CourseViewSets.CourseGroupInstance.CourseGroupViewSet, base_name='api-course-group')
api_router.register(
    r'missions', MissionViewSets.MissionInstance.MissionViewSet, base_name='api-mission')
api_router.register(
    r'mission-groups', MissionViewSets.MissionGroupInstance.MissionGroupViewSet, base_name='api-mission-group')
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
api_course_meta_router.register(
    r'missions', MissionViewSets.MissionList.MissionMetaViewSet, base_name='api-course-meta-mission')
api_course_meta_router.register(
    r'categories', CategoryViewSet.CategoryList.CategoryMetaViewSet, base_name='api-course-meta-category')
api_course_meta_router.register(
    r'categories', CategoryViewSet.CategoryInstance.CategoryMetaViewSet, base_name='api-course-meta-category')
api_course_meta_router.register(
    r'available-categories', CategoryViewSet.CategoryList.CategoryAvailableMetaViewSet,
    base_name='api-course-meta-available-categories')
# --------
api_course_router = NestedSimpleRouter(api_router, r'courses', lookup='course')
api_course_router.register(
    r'teachers', UserViewSets.CourseUserList.TeacherViewSet, base_name='api-course-teacher')
api_course_router.register(
    r'teachers', UserViewSets.CourseUserInstance.TeacherViewSet, base_name='api-course-teacher')
api_course_router.register(
    r'available-teachers', UserViewSets.CourseUserList.TeacherAvailableViewSet,
    base_name='api-course-available-teacher')
api_course_router.register(
    r'students', UserViewSets.CourseUserList.StudentViewSet, base_name='api-course-student')
api_course_router.register(
    r'students', UserViewSets.CourseUserInstance.StudentViewSet, base_name='api-course-student')
api_course_router.register(
    r'available-students', UserViewSets.CourseUserList.StudentAvailableViewSet,
    base_name='api-course-available-student')
api_course_router.register(
    r'groups', CourseViewSets.CourseGroupList.CourseGroupCourseViewSet, base_name='api-course-course-group')
api_course_router.register(
    r'groups', CourseViewSets.CourseGroupInstance.CourseGroupCourseViewSet, base_name='api-course-course-group')
api_course_router.register(
    r'available-groups', CourseViewSets.CourseGroupList.CourseGroupAvailableCourseViewSet,
    base_name='api-course-available-course-group')
api_course_router.register(
    r'mission-groups', MissionViewSets.MissionGroupList.MissionGroupCourseViewSet, base_name='api-course-mission-group')
# --------
api_course_group_router = NestedSimpleRouter(api_router, r'course-groups', lookup='course_group')
api_course_group_router.register(
    r'teachers', UserViewSets.CourseGroupUserList.TeacherViewSet, base_name='api-course-group-teacher')
api_course_group_router.register(
    r'teachers', UserViewSets.CourseGroupUserInstance.TeacherViewSet, base_name='api-course-group-teacher')
api_course_group_router.register(
    r'available-teachers', UserViewSets.CourseGroupUserList.TeacherAvailableViewSet,
    base_name='api-course-group-available-teacher')
api_course_group_router.register(
    'courses', CourseViewSets.CourseList.CourseCourseGroupViewSet, base_name='api-course-group-course')
api_course_group_router.register(
    r'courses', CourseViewSets.CourseInstance.CourseCourseGroupViewSet, base_name='api-course-group-course')
api_course_group_router.register(
    r'available-courses', CourseViewSets.CourseList.CourseAvailableCourseGroupViewSet,
    base_name='api-course-group-available-course')
api_course_group_router.register(
    r'mission-groups', MissionViewSets.MissionGroupList.MissionGroupCourseGroupViewSet,
    base_name='api-course-group-mission-group')
# --------
api_mission_group_router = NestedSimpleRouter(api_router, r'mission-groups', lookup='mission_group')
api_mission_group_router.register(
    r'missions', MissionViewSets.MissionList.MissionMissionGroupViewSet, base_name='api-mission-group-mission')
api_mission_group_router.register(
    r'missions', MissionViewSets.MissionInstance.MissionMissionGroupViewSet, base_name='api-mission-group-mission')
api_mission_group_router.register(
    r'available-missions', MissionViewSets.MissionList.MissionAvailableMissionGroupViewSet,
    base_name='api-mission-group-available-mission')
# --------
api_mission_router = NestedSimpleRouter(api_router, r'missions', lookup='mission')
api_mission_router.register(
    r'problems', MissionViewSets.ProblemList.ProblemViewSet, base_name='api-mission-problem')
api_mission_router.register(
    r'problems', MissionViewSets.ProblemInstance.ProblemViewSet, base_name='api-mission-problem')
api_mission_router.register(
    r'available-problems', MissionViewSets.ProblemList.ProblemAvailableViewSet,
    base_name='api-mission-available-problem')
api_mission_router.register(
    r'submissions', MissionViewSets.SubmissionList.SubmissionViewSet, base_name='api-mission-submission')
api_mission_router.register(
    r'submissions', MissionViewSets.SubmissionInstance.SubmissionViewSet, base_name='api-mission-submission')

# --------
api_patterns = []
api_patterns += api_router.urls
api_patterns += api_organization_router.urls
api_patterns += api_course_meta_router.urls
api_patterns += api_course_router.urls
api_patterns += api_course_group_router.urls
api_patterns += api_mission_group_router.urls
api_patterns += api_mission_router.urls
