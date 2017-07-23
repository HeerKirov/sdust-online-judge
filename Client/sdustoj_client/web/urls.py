from django.conf.urls import url, include
from .views import MainPages, PersonalPages, UserAdminPages, OrganizationAdminPages


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
    url(r'^info/([\w\-.+@]+)/categories/create/$',OrganizationAdminPages.Category.categoriescreate, name='web-categories-create'),
    url(r'^info/([\w\-.+@]+)/categories/info/([\w\-.+@]+)/$',OrganizationAdminPages.Category.instance, name='web-categories-instance'),
    url(r'^info/([\w\-.+@]+)/categories/$', OrganizationAdminPages.Category.categories,
        name='web-organization-categories'),
    url(r'^info/([\w\-.+@]+)/$', OrganizationAdminPages.Organization.instance, name='web-organization-instance'),

    url(r'^info/([\w\-.+@]+)/edu-admins/info/([\w\-.+@]+)/$',OrganizationAdminPages.EduAdmin.instance, name='web-eduadmin-instance'),
    url(r'^info/([\w\-.+@]+)/edu-admins/create/$',OrganizationAdminPages.EduAdmin.create, name='web-eduadmin-create'),
    url(r'^info/([\w\-.+@]+)/edu-admins/$',OrganizationAdminPages.EduAdmin.list, name="web-eduadmin-list"),

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
url_patterns = [
    url(r'home/', MainPages.home, name='web-home'),
    url(r'login/', MainPages.login, name='web-login'),
    url(r'^personal/', include(personal_patterns)),
    url(r'^users/', include(user_patterns)),
    url(r'^admins/', include(admin_patterns)),
    url(r'^organizations/', include(org_patterns)),
    url(r'^orgAdmin/', include(orgAdmin_patterns)),
    url(r'^userAdmin/', include(userAdmin_patterns)),

]
