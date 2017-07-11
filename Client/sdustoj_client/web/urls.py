from django.conf.urls import url, include
from .views import MainPages, PersonalPages, UserAdminPages, OrganizationAdminPages


personal_patterns = [
    url(r'^info/', PersonalPages.info, name='web-personal-info'),
    url(r'^password/', PersonalPages.password, name='web-personal-password'),
]

user_patterns = [
    url(r'^$', UserAdminPages.User.list, name='web-user-all'),
    url(r'^create/', UserAdminPages.User.create, name='web-user-create'),
    url(r'^info/(\S+)/', UserAdminPages.User.instance, name='web-user-instance'),
]


admin_patterns = [
    url(r'^$', UserAdminPages.Admin.list, name='web-admin-all'),
    url(r'^create/', UserAdminPages.Admin.create, name='web-admin-create'),
    url(r'^info/(\S+)/', UserAdminPages.Admin.instance, name='web-admin-instance'),
]

org_patterns = [
    url(r'^$', OrganizationAdminPages.Organization.list, name='web-organization'),
    url(r'^create/', OrganizationAdminPages.Organization.create, name='web-organization-create'),
    url(r'^info/(\S+)/', OrganizationAdminPages.Organization.instance, name='web-organization-instance'),
]

url_patterns = [
    url(r'home/', MainPages.home, name='web-home'),
    url(r'login/', MainPages.login, name='web-login'),
    url(r'^personal/', include(personal_patterns)),
    url(r'^users/', include(user_patterns)),
    url(r'^admins/', include(admin_patterns)),
    url(r'^organizations/', include(org_patterns)),
]
