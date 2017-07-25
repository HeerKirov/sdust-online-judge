from django.conf.urls import url, include
from .views import MainPages, PersonalPages, UserAdminPages, OrganizationAdminPages,MyOrganizationPages,CourseGroup,Course,Mission


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
]

course_patterns = [
    url(r'^info/([\w\-.+@]+)/$',Course.instance,name="web-course-instance"),
]

mission_patterns = [
    url(r'^info/([\w\-.+@]+)/$',Mission.instance,name="web-mission-instance"),
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


]
