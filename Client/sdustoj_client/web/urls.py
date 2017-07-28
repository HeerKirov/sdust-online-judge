from django.conf.urls import url, include
from .views import MainPages, PersonalPages, UserAdminPages, OrganizationAdminPages,MyOrganizationPages,CourseGroup,Course,Mission,TeachingAdminPages,MissionGroup


personal_patterns = [
    url(r'^info/', PersonalPages.info, name='web-personal-info'),
    url(r'^password/', PersonalPages.password, name='web-personal-password'),
]

user_patterns = [
    url(r'^$', UserAdminPages.User.list, name='web-user-all'),
    url(r'^create/', UserAdminPages.User.create, name='web-user-create'),
    url(r'^info/([\w\-.+@]+)/', UserAdminPages.User.instance, name='web-user-instance'),
]


admin_patterns = [
    url(r'^$', UserAdminPages.Admin.list, name='web-admin-all'),
    url(r'^create/', UserAdminPages.Admin.create, name='web-admin-create'),
    url(r'^info/([\w\-.+@]+)/', UserAdminPages.Admin.instance, name='web-admin-instance'),
]

org_patterns = [
    url(r'^$', OrganizationAdminPages.Organization.list, name='web-organization'),
    url(r'^create/$', OrganizationAdminPages.Organization.create, name='web-organization-create'),
    url(r'^info/([\w\-.+@]+)/categories/create/$', OrganizationAdminPages.Category.categoriescreate, name='web-categories-create'),
    url(r'^info/([\w\-.+@]+)/categories/info/([\w\-.+@]+)/$', OrganizationAdminPages.Category.instance, name='web-categories-instance'),
    url(r'^info/([\w\-.+@]+)/categories/$', OrganizationAdminPages.Category.categories,
        name='web-organization-categories'),
    url(r'^info/([\w\-.+@]+)/$', OrganizationAdminPages.Organization.instance, name='web-organization-instance'),
    url(r'^info/([\w\-.+@]+)/edu-admins/info/([\w\-.+@]+)/$', OrganizationAdminPages.EduAdmin.instance, name='web-eduadmin-instance'),
    url(r'^info/([\w\-.+@]+)/edu-admins/create/$', OrganizationAdminPages.EduAdmin.create, name='web-eduadmin-create'),
    url(r'^info/([\w\-.+@]+)/edu-admins/$', OrganizationAdminPages.EduAdmin.list, name="web-eduadmin-list"),

]

userAdmin_patterns = [
    url(r'^$', UserAdminPages.UserAdmin.list, name='web-admin-useradmin'),
    url(r'^create/', UserAdminPages.UserAdmin.create, name='web-useradmin-create'),
    url(r'^info/([\w\-.+@]+)/', UserAdminPages.UserAdmin.instance, name='web-useradmin-instance'),
]

orgAdmin_patterns = [
    url(r'^$',UserAdminPages.OrgAdmin.list, name='web-admin-orgadmin'),
    url(r'^create/',UserAdminPages.OrgAdmin.create, name='web-orgadmin-create'),
    url(r'^info/([\w\-.+@]+)/',UserAdminPages.OrgAdmin.instance, name='web-orgadmin-instance'),
]
myOrg_patterns = [
    url(r'^$', MyOrganizationPages.Organization.list, name='web-myorganization'),
    url(r'^info/([\w\-.+@]+)/$', MyOrganizationPages.Organization.instance, name='web-myorganization-instance'),
    url(r'^info/([\w\-.+@]+)/course-meta/$', MyOrganizationPages.CourseMeta.list, name='web-course-meta-list'),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/$', MyOrganizationPages.CourseMeta.instance, name='web-course-meta-instance'),
    url(r'^info/([\w\-.+@]+)/edu-admin/$', MyOrganizationPages.EduAdmin.list, name='web-edu-admin-list'),
    url(r'^info/([\w\-.+@]+)/edu-admin/info/([\w\-.+@]+)/$', MyOrganizationPages.EduAdmin.instance, name='web-edu-admin-instance'),
    url(r'^info/([\w\-.+@]+)/teacher/$', MyOrganizationPages.Teacher.list, name='web-teacher-list'),
    url(r'^info/([\w\-.+@]+)/teacher/info/([\w\-.+@]+)/$', MyOrganizationPages.Teacher.instance, name='web-teacher-instance'),
    url(r'^info/([\w\-.+@]+)/teacher/create/$', MyOrganizationPages.Teacher.create, name='web-teacher-create'),
    url(r'^info/([\w\-.+@]+)/student/$', MyOrganizationPages.Student.list, name='web-student-list'),
    url(r'^info/([\w\-.+@]+)/student/info/([\w\-.+@]+)/$', MyOrganizationPages.Student.instance, name='web-student-instance'),
    url(r'^info/([\w\-.+@]+)/student/create/$', MyOrganizationPages.Student.create, name='web-student-create'),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/coursegroup/$',MyOrganizationPages.CourseGroup.list,name="web-course-group-list"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/coursegroup/create/$',MyOrganizationPages.CourseGroup.create,name="web-course-group-create"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/course/$',MyOrganizationPages.Course.list,name="web-myorg-coursemeta-course-list"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/course/create/$',MyOrganizationPages.Course.create,name="web-myorg-coursemeta-course-create"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/mission/$',MyOrganizationPages.Mission.list,name="web-myorg-coursemeta-mission-list"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/mission/create/$',MyOrganizationPages.Mission.create,name="web-myorg-coursemeta-mission-create"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/category/$',MyOrganizationPages.Category.list,name="web-myorg-coursemeta-category-list"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/category/create/$',MyOrganizationPages.Category.create,name="web-myorg-coursemeta-category-create"),
    url(r'^info/([\w\-.+@]+)/course-meta/info/([\w\-.+@]+)/category/info/([\w\-.+@]+)/$',MyOrganizationPages.Category.instance,name="web-myorg-coursemeta-category-instance"),
]

courseGroup_patterns = [
    url(r'^info/([\w\-.+@]+)/$',CourseGroup.instance,name="web-course-group-instance"),
    url(r'^info/([\w\-.+@]+)/coursebelong/$',CourseGroup.CourseBelong.list,name="web-course-group-coursebelong-list"),
    url(r'^info/([\w\-.+@]+)/coursebelong/info/([\w\-.+@]+)/$',CourseGroup.CourseBelong.instance,name="web-course-group-coursebelong-instance"),
    url(r'^info/([\w\-.+@]+)/coursebelong/create/$', CourseGroup.CourseBelong.create, name="web-course-group-coursebelong-create"),
    url(r'^info/([\w\-.+@]+)/teacher/$', CourseGroup.Teacher.list, name="web-course-group-teacher-list"),
    url(r'^info/([\w\-.+@]+)/teacher/create/$', CourseGroup.Teacher.create, name="web-course-group-teacher-create"),
    url(r'^info/([\w\-.+@]+)/teacher/info/([\w\-.+@]+)/$', CourseGroup.Teacher.instance, name="web-course-group-teacher-instance"),
    url(r'^info/([\w\-.+@]+)/mission-group/$', CourseGroup.MissionGroup.list, name="web-course-group-mission-group-list"),
    url(r'^info/([\w\-.+@]+)/mission-group/info/([\w\-.+@]+)/$', CourseGroup.MissionGroup.instance,
        name="web-course-group-mission-group-detail"),
    url(r'^info/([\w\-.+@]+)/mission-group/create/$', CourseGroup.MissionGroup.create,
        name="web-course-group-mission-group-create"),

]

course_patterns = [
    url(r'^info/([\w\-.+@]+)/$',Course.instance,name="web-course-instance"),
    url(r'^info/([\w\-.+@]+)/groupin/$',Course.Groupin.list,name="web-course-groupin-list"),
    url(r'^info/([\w\-.+@]+)/groupin/info/([\w\-.+@]+)/$',Course.Groupin.instance,name="web-course-groupin-detail"),
    url(r'^info/([\w\-.+@]+)/groupin/create/$',Course.Groupin.create,name="web-course-groupin-create"),
    url(r'^info/([\w\-.+@]+)/teacher/$',Course.Teacher.list,name="web-course-teacher-list"),
    url(r'^info/([\w\-.+@]+)/teacher/info/([\w\-.+@]+)/$', Course.Teacher.instance, name="web-course-teacher-detail"),
    url(r'^info/([\w\-.+@]+)/teacher/create/$',Course.Teacher.create,name="web-course-teacher-create"),
    url(r'^info/([\w\-.+@]+)/student/$',Course.Student.list,name="web-course-student-list"),
    url(r'^info/([\w\-.+@]+)/student/info/([\w\-.+@]+)/$', Course.Student.instance, name="web-course-student-detail"),
    url(r'^info/([\w\-.+@]+)/student/create/$',Course.Student.create,name="web-course-student-create"),
    url(r'^info/([\w\-.+@]+)/mission-group/$',Course.MissionGroup.list,name="web-course-mission-group-list"),
    url(r'^info/([\w\-.+@]+)/mission-group/info/([\w\-.+@]+)/$', Course.MissionGroup.instance, name="web-course-mission-group-detail"),
    url(r'^info/([\w\-.+@]+)/mission-group/create/$',Course.MissionGroup.create,name="web-course-mission-group-create"),
]

mission_patterns = [
    url(r'^info/([\w\-.+@]+)/$',Mission.instance,name="web-mission-instance"),
]

teachingcourse_patterns = [
    url(r'^$',TeachingAdminPages.TeachingCourse.list,name='web-teaching-course-list'),
]

teachingcoursegroup_patterns = [
    url(r'^$',TeachingAdminPages.TeachingCourseGroup.list,name='web-teaching-course-group-list'),
]
mission_group_patterns = [
    url(r'^info/([\w\-.+@]+)/$',MissionGroup.instance,name="web-mission-group-instance"),
    url(r'^info/([\w\-.+@]+)/mission/$',MissionGroup.Mission.list,name="web-mission-group-mission-list"),
    url(r'^info/([\w\-.+@]+)/mission/info/([\w\-.+@]+)/$',MissionGroup.Mission.instance,name="web-mission-group-mission-detail"),
    url(r'^info/([\w\-.+@]+)/mission/create/$',MissionGroup.Mission.create,name="web-mission-group-mission-create"),
]

url_patterns = [
    url(r'home/', MainPages.home, name='web-home'),
    url(r'login/', MainPages.login, name='web-login'),
    url(r'^personal/', include(personal_patterns)),
    url(r'^users/', include(user_patterns)),
    url(r'^admins/', include(admin_patterns)),
    url(r'^organizations/', include(org_patterns)),
    url(r'^myOrganizations/', include(myOrg_patterns)),
    url(r'^orgAdmin/', include(orgAdmin_patterns)),
    url(r'^userAdmin/', include(userAdmin_patterns)),
    url(r'^courseGroup/',include(courseGroup_patterns)),
    url(r'^course/',include(course_patterns)),
    url(r'^mission/',include(mission_patterns)),
    url(r'^teachingcourse/',include(teachingcourse_patterns)),
    url(r'^teachingcoursegroup/',include(teachingcoursegroup_patterns)),
    url(r'^mission-group/',include(mission_group_patterns)),

]
