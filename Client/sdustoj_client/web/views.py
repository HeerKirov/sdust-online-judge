from django.shortcuts import render, redirect, reverse
from rest_api.models import IdentityChoices


class Utils(object):
    class UserInfo(object):
        @staticmethod
        def basic(request):
            user = request.user
            if user.is_authenticated():
                profile = user.profile
                info = {
                    'is_authenticated': True,
                    'name': profile.name if profile.name else profile.username,
                    'user': profile,
                    'identities': profile.identities
                }
            else:
                info = {
                    'is_authenticated': False
                }
            return info
        
    class Render(object):
        @staticmethod
        def _has_site_identity(identities, id_str):
            """
            判断用户是否具备指定的全局身份。
            :param identities: 用户身份的JSON数据。
            :param id_str: 身份字符串集合或列表。
            :return: 只要identities中具备id_str中任意一个身份，即返回True；否则返回False。
            """
            for it in id_str:
                if it in identities and identities[it] is not False:
                    return True
            return False

        @staticmethod
        def _has_org_identity(identities, id_tuple):
            """
            判断用户是否具备指定的机构相关身份。
            :param identities: 用户身份的JSON数据。
            :param id_tuple: 身份信息的集合或列表。元素参见_identity_render机构相关身份元素的说明。
            :return: 只要identities中具备id_tuple中任意一个身份，即返回True；否则返回False。
            """
            for it in id_tuple:
                if it[0] in identities:
                    identity = identities[it[0]]
                    if not isinstance(identity, str) and it[1] in identity:
                        return True
            return False

        @staticmethod
        def _identity_render(request, template, id_expect, context=None):
            """
            附带用户身份检测的页面生成。
            :param request: http请求。
            :param template: 使用的模板文件。
            :param id_expect: 身份列表，即哪些身份的用户可以访问.
                              如果所有人均可访问，设置为'*'；否则为列表，列表中元素为身份，类型如下：
                                - 如果身份为全局身份，则为表示身份的字符串。
                                - 如果身份与机构相关，则为(身份字符串, 机构ID)形式的元组。
                                - 如果身份与机构相关，但任一机构均可，则为(身份字符串, None)形式的字符串。
            :param context: 需要额外传递给模板的数据。
            :return: 不要管……
            """
            user_info = Utils.UserInfo.basic(request)
            # 如果没有登录，跳转到登录页面
            if not user_info['is_authenticated']:
                return redirect(reverse('web-login'))
            # 如果用户不具备指定的权限，跳转到首页
            if id_expect != '*':
                identities = user_info['identities']
                site_identities_expect = []
                org_identities_expect = []
                for identity in id_expect:
                    if isinstance(identity, str):
                        site_identities_expect.append(identity)
                    else:
                        org_identities_expect.append(identity)
                if not (Utils.Render._has_site_identity(identities, site_identities_expect)
                        or Utils.Render._has_org_identity(identities, org_identities_expect)):
                    return redirect(reverse('web-home'))

            _context = context if context is not None else dict()
            _context['user_info'] = user_info

            return render(request, template, _context)

        @staticmethod
        def public(request, template, context=None):
            user_info = Utils.UserInfo.basic(request)
            _context = context if context is not None else dict()
            _context['user_info'] = user_info
            return render(request, template, _context)

        @staticmethod
        def all_user(request, template, context=None):
            return Utils.Render._identity_render(
                request=request,
                template=template,
                id_expect='*',
                context=context
            )

        @staticmethod
        def root(request, template, context=None):
            return Utils.Render._identity_render(
                request=request,
                template=template,
                id_expect=(IdentityChoices.root, ),
                context=context
            )

        @staticmethod
        def user_admin(request, template, context=None):
            return Utils.Render._identity_render(
                request=request,
                template=template,
                id_expect=(IdentityChoices.user_admin, IdentityChoices.root,),
                context=context
            )

        @staticmethod
        def org_admin(request, template, context=None):
            return Utils.Render._identity_render(
                request=request,
                template=template,
                id_expect=(IdentityChoices.org_admin, IdentityChoices.root,),
                context=context
            )

        @staticmethod
        def edu_admin(request, template, context=None):
            return Utils.Render._identity_render(
                request=request,
                template=template,
                id_expect=(IdentityChoices.edu_admin, IdentityChoices.root,),
                context=context
            )



class MainPages(object):
    @staticmethod
    def home(request):
        return Utils.Render.public(request, 'homepage.html')

    @staticmethod
    def to_home(request):
        if request:
            pass
        return redirect(reverse('web-home'))

    @staticmethod
    def login(request):
        if request.user.is_authenticated():
            return redirect(reverse('web-home'))
        return Utils.Render.public(request, 'login.html')


class PersonalPages(object):
    @staticmethod
    def info(request):
        return Utils.Render.all_user(request, 'personal/info.html')

    @staticmethod
    def password(request):
        return Utils.Render.all_user(request, 'personal/password.html')


class UserAdminPages(object):
    class User(object):
        @staticmethod
        def list(request):
            return Utils.Render.user_admin(request, 'user/user/list.html')

        @staticmethod
        def create(request):
            return Utils.Render.user_admin(request, 'user/user/create.html')

        @staticmethod
        def instance(request, username):
            return Utils.Render.user_admin(request, 'user/user/instance.html', {'u': username})

    class Admin(object):
        @staticmethod
        def list(request):
            return Utils.Render.user_admin(request, 'user/admin/list.html')

        @staticmethod
        def create(request):
            return Utils.Render.user_admin(request, 'user/admin/create.html')

        @staticmethod
        def instance(request, username):
            return Utils.Render.user_admin(request, 'user/admin/instance.html', {'u': username})
    class UserAdmin(object):
        @staticmethod
        def list(request):
            return Utils.Render.user_admin(request,'user/userAdmin/list.html')

        @staticmethod
        def create(request):
            return Utils.Render.user_admin(request,'user/userAdmin/create.html')

        @staticmethod
        def instance(request,username):
            return Utils.Render.user_admin(request,'user/userAdmin/instance.html',{'u': username})

    class OrgAdmin(object):
        @staticmethod
        def list(request):
            return Utils.Render.user_admin(request,'user/orgAdmin/list.html')

        @staticmethod
        def create(request):
            return Utils.Render.user_admin(request,'user/orgAdmin/create.html')

        @staticmethod
        def instance(request,username):
            return Utils.Render.user_admin(request,'user/orgAdmin/instance.html',{'u': username})


class OrganizationAdminPages(object):
    class Organization(object):
        @staticmethod
        def list(request):
            return Utils.Render.org_admin(request, 'organization/list.html')

        @staticmethod
        def create(request):
            return Utils.Render.org_admin(request, 'organization/create.html')

        @staticmethod
        def instance(request, oid):
            return Utils.Render.org_admin(request, 'organization/instance.html', {
                'oid': oid
            })
    class Category(object):
        @staticmethod
        def categories(request,oid):
            return Utils.Render.org_admin(request,'organization/categories/list.html',{
                'oid': oid
            })
        @staticmethod
        def categoriescreate(request,oid):
            return Utils.Render.org_admin(request,'organization/categories/create.html',{
                "oid": oid
            })
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
=======
>>>>>>> HeerKirov/master
=======
        @staticmethod
        def instance(request,oid,cid):
            return Utils.Render.org_admin(request,'organization/categories/instance.html',{
                "oid": oid,
                "cid": cid
            })
>>>>>>> HeerKirov/master
    class EduAdmin(object):
        @staticmethod
        def list(request,oid):
            return Utils.Render.org_admin(request,'organization/eduadmin/list.html',{
                "oid": oid
            })

        @staticmethod
        def create(request,oid):
            return Utils.Render.org_admin(request,'organization/eduadmin/create.html',{
                "oid": oid
            })

        @staticmethod
        def instance(request ,oid ,uid):
            return Utils.Render.org_admin(request,'organization/eduadmin/instance.html',{
                "oid": oid,
                "uid": uid
            })
<<<<<<< HEAD
>>>>>>> HeerKirov/master
=======
>>>>>>> HeerKirov/master

class MyOrganizationPages(object):
    class Organization(object):
        @staticmethod
        def list(request):
            return Utils.Render.all_user(request, 'myorganization/list.html')

        @staticmethod
        def instance(request, oid):
            return Utils.Render.all_user(request, 'myorganization/instance.html', {
                'oid': oid
            })

    class CourseMeta(object):
        @staticmethod
        def list(request, oid):
            return Utils.Render.edu_admin(request, 'myorganization/course-meta/list.html',{
                'oid': oid
            })

        @staticmethod
        def instance(request, oid, uid):
            readonly = IdentityChoices.edu_admin in request.user.profile.identities or \
                    IdentityChoices.root in request.user.profile.identities
            return Utils.Render.edu_admin(request, 'myorganization/course-meta/instance.html', {
                'oid': oid,
                "uid": uid,
                "readonly": "true" if not readonly else "false"
            })
    class CourseGroup(object):
        @staticmethod
        def list(request,oid,uid):
            return Utils.Render.all_user(request, 'myorganization/course-meta/coursegroup/list.html',{
                "oid": oid,
                "uid": uid
            })

        @staticmethod
        def create(request,oid,uid):
            return Utils.Render.all_user(request,"myorganization/course-meta/coursegroup/create.html",{
                "oid": oid,
                "uid": uid
            })

    class Course(object):
        @staticmethod
        def list(request,oid,uid):
            return Utils.Render.all_user(request,'myorganization/course-meta/course/list.html',{
                "oid": oid,
                "uid": uid
            })

        @staticmethod
        def create(request, oid, uid):
            return Utils.Render.all_user(request, "myorganization/course-meta/course/create.html", {
                "oid": oid,
                "uid": uid
            })

    class Mission(object):
        @staticmethod
        def list(request, oid, uid):
            return Utils.Render.all_user(request, 'myorganization/course-meta/mission/list.html', {
                "oid": oid,
                "uid": uid
            })

        @staticmethod
        def create(request, oid, uid):
            return Utils.Render.all_user(request, "myorganization/course-meta/mission/create.html", {
                "oid": oid,
                "uid": uid
            })

    class Category(object):
        @staticmethod
        def list(request, oid, uid):
            return Utils.Render.all_user(request, 'myorganization/course-meta/category/list.html', {
                "oid": oid,
                "uid": uid
            })

        @staticmethod
        def create(request, oid, uid):
            return Utils.Render.all_user(request, "myorganization/course-meta/category/create.html", {
                "oid": oid,
                "uid": uid
            })
        @staticmethod
        def instance(request, oid, mid,cid):
            return Utils.Render.all_user(request, "myorganization/course-meta/category/instance.html", {
                "oid": oid,
                "mid": mid,
                "cid": cid
            })

class CourseGroup(object):
    @staticmethod
    def instance(request, gid):
        return Utils.Render.all_user(request, "course-group/instance.html", {
            "gid": gid,
        })


class Course(object):
    @staticmethod
    def instance(request, cid):
        return Utils.Render.all_user(request, "course/instance.html", {
            "cid": cid,
        })

class Mission(object):
    @staticmethod
    def instance(request, id):
        return Utils.Render.all_user(request, "mission/instance.html", {
            "id": id,
        })

