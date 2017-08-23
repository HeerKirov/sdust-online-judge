from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.contrib.postgres import fields as pg_fields
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta


# -- Tool -------------------------------------------------------------------------------

def now_dt():
    """
    返回一个时间。
    :return: 
    """
    now = datetime.now() + timedelta(hours=0)  # 遗留的代码。未来可以考虑清除掉。
    return now


# -- Resource ---------------------------------------------------------------------------

class Resource(models.Model):
    """
    SDUSTOJ资源表共有字段。
    """
    # 创建者
    creator = models.CharField(max_length=150, null=True)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 最后一次更新者
    updater = models.CharField(max_length=150, null=True)
    # 最后一次更新时间
    update_time = models.DateTimeField(auto_now=True)

    # 是否可用（当前并没什么用……）
    available = models.BooleanField(default=True)
    # 是否废弃（被废弃将不能被非管理者的任何用户、用户端或评测机发现）
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TitleMixin(models.Model):
    """
    某些需要由标题和简介的资源的共有字段。
    """
    # 题目
    title = models.CharField(max_length=128)
    # 简介
    introduction = models.CharField(max_length=512, null=True)

    class Meta:
        abstract = True


class SourceMixin(models.Model):
    """
    某些需要记录来源的资源的共有字段。
    """
    # 来源
    source = models.CharField(max_length=256, null=True)
    # 作者
    author = models.CharField(max_length=64, null=True)

    class Meta:
        abstract = True


# -- User -------------------------------------------------------------------------------

class IdentityChoices(object):
    root = 'ROOT'
    user_admin = 'USER_ADMIN'
    org_admin = 'ORG_ADMIN'
    edu_admin = 'EDU_ADMIN'
    teacher = 'TEACHER_ADMIN'
    student = 'STUDENT'

IDENTITY_CHOICES = (
    IdentityChoices.root,
    IdentityChoices.user_admin,
    IdentityChoices.org_admin,
    IdentityChoices.edu_admin,
    IdentityChoices.teacher,
    IdentityChoices.student
)

ROOT_IDENTITY_CHOICES = (
    IdentityChoices.root,
)
ADMIN_IDENTITY_CHOICES = (
    IdentityChoices.user_admin,
    IdentityChoices.org_admin
)

SITE_IDENTITY_CHOICES = (
    IdentityChoices.root,
    IdentityChoices.user_admin,
    IdentityChoices.org_admin
)

ORG_IDENTITY_CHOICES = (
    IdentityChoices.edu_admin,
    IdentityChoices.teacher,
    IdentityChoices.student
)


class PublicFieldMixin(object):
    @property
    def let_name(self):
        return getattr(self, 'name')

    @let_name.setter
    def let_name(self, value):
        setattr(self, 'name', value)
        getattr(self, 'profile').name = value

    @property
    def let_available(self):
        return getattr(self, 'available')

    @let_available.setter
    def let_available(self, value):
        setattr(self, 'available', value)
        getattr(self, 'profile').available = value

    @property
    def let_deleted(self):
        return getattr(self, 'deleted')

    @let_deleted.setter
    def let_deleted(self, value):
        setattr(self, 'deleted', value)
        getattr(self, 'profile').deleted = value

    @property
    def sex(self):
        return getattr(self, 'profile').sex

    @sex.setter
    def sex(self, value):
        getattr(self, 'profile').sex = value

    @property
    def phone(self):
        return getattr(self, 'profile').phone

    @phone.setter
    def phone(self, value):
        getattr(self, 'profile').phone = value

    @property
    def email(self):
        return getattr(self, 'profile').email

    @email.setter
    def email(self, value):
        getattr(self, 'profile').email = value

    @property
    def github(self):
        return getattr(self, 'profile').github

    @github.setter
    def github(self, value):
        getattr(self, 'profile').github = value

    @property
    def qq(self):
        return getattr(self, 'profile').qq

    @qq.setter
    def qq(self, value):
        getattr(self, 'profile').qq = value

    @property
    def wechat(self):
        return getattr(self, 'profile').wechat

    @wechat.setter
    def wechat(self, value):
        getattr(self, 'profile').wechat = value

    @property
    def blog(self):
        return getattr(self, 'profile').blog

    @blog.setter
    def blog(self, value):
        getattr(self, 'profile').blog = value

    @property
    def introduction(self):
        return getattr(self, 'profile').introduction

    @introduction.setter
    def introduction(self, value):
        getattr(self, 'profile').introduction = value

    @property
    def last_login(self):
        return getattr(self, 'profile').last_login

    @property
    def ip(self):
        return getattr(self, 'profile').ip

    @property
    def let_creator(self):
        return getattr(self, 'creator')

    @let_creator.setter
    def let_creator(self, value):
        setattr(self, 'creator', value)
        getattr(self, 'profile').creator = value

    @property
    def let_updater(self):
        return getattr(self, 'updater')

    @let_updater.setter
    def let_updater(self, value):
        setattr(self, 'updater', value)
        getattr(self, 'profile').updater = value


class UserProfile(Resource):
    SEX_CHOICES = ('MALE', 'FEMALE', 'SECRET')

    user = models.OneToOneField(User, related_name='profile', to_field='id', primary_key=True,
                                on_delete=models.CASCADE)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    name = models.CharField(max_length=150, null=True)
    sex = models.CharField(max_length=8, default='SECRET')
    phone = models.CharField(max_length=32, null=True)
    email = models.EmailField(max_length=128, null=True)
    github = models.CharField(max_length=128, null=True)
    qq = models.CharField(max_length=128, null=True)
    wechat = models.CharField(max_length=128, null=True)
    blog = models.CharField(max_length=128, null=True)

    introduction = models.TextField(max_length=256, null=True)

    last_login = models.DateTimeField(null=True)
    ip = models.GenericIPAddressField(null=True)

    is_staff = models.BooleanField(default=False)

    identities = pg_fields.JSONField(default={})
    courses = pg_fields.JSONField(default={})

    def __str__(self):
        return "<Profile %s: %s>" % (self.username, self.name)

    @property
    def let_name(self):
        return self.name

    @let_name.setter
    def let_name(self, value):
        self.name = value
        if hasattr(self, 'edu_admin_identities'):
            for i in self.edu_admin_identities.all():
                i.name = value
        if hasattr(self, 'teacher_identities'):
            for i in self.teacher_identities.all():
                i.name = value
        if hasattr(self, 'student_identities'):
            for i in self.student_identities.all():
                i.name = value

    @property
    def let_creator(self):
        return self.creator

    @let_creator.setter
    def let_creator(self, value):
        self.creator = value
        if hasattr(self, 'edu_admin_identities'):
            for i in self.edu_admin_identities.all():
                i.creator = value
        if hasattr(self, 'teacher_identities'):
            for i in self.teacher_identities.all():
                i.creator = value
        if hasattr(self, 'student_identities'):
            for i in self.student_identities.all():
                i.creator = value

    @property
    def let_updater(self):
        return self.updater

    @let_updater.setter
    def let_updater(self, value):
        self.updater = value
        if hasattr(self, 'edu_admin_identities'):
            for i in self.edu_admin_identities.all():
                i.updater = value
        if hasattr(self, 'teacher_identities'):
            for i in self.teacher_identities.all():
                i.updater = value
        if hasattr(self, 'student_identities'):
            for i in self.student_identities.all():
                i.updater = value

    def is_org_manager(self):
        """
        包装的函数。判断user是否具有一般情况下管理机构的权限。
        :return: 
        """
        return self.has_identities(IdentityChoices.edu_admin, IdentityChoices.org_admin, IdentityChoices.root)

    def is_mission_manager(self):
        """
        包装的函数。当用户是有资格管理任务的用户时返回true。
        :return: 
        """
        return self.has_identities(IdentityChoices.root,
                                   IdentityChoices.org_admin,
                                   IdentityChoices.edu_admin,
                                   IdentityChoices.teacher)

    def has_identities(self, *args):
        """
        是否拥有其中之一的权限。
        :param args: 
        :return: 
        """
        for identity, value in self.identities.items():
            if value is True or len(value) > 0:
                for arg in args:
                    if arg == identity:
                        return True
        return False

    def get_identities(self):
        ret = []
        for k, v in self.identities.items():
            if v is True or len(v) > 0:
                ret.append(k)
        return ret

    def update_identities(self):
        identities = {}
        if self.is_staff:
            if IdentityChoices.root in self.identities:
                identities[IdentityChoices.root] = True
            if IdentityChoices.user_admin in self.identities:
                identities[IdentityChoices.user_admin] = True
            if IdentityChoices.org_admin in self.identities:
                identities[IdentityChoices.org_admin] = True
        student_org = []
        student_identities = getattr(
            Student, 'objects').filter(profile=self).values('organization_id').distinct()
        for i in student_identities:
            student_org.append(i['organization_id'])
        identities[IdentityChoices.student] = student_org

        teacher_org = []
        teacher_identities = getattr(
            Teacher, 'objects').filter(profile=self).values('organization_id').distinct()
        for i in teacher_identities:
            teacher_org.append(i['organization_id'])
        identities[IdentityChoices.teacher] = teacher_org

        edu_admin_org = []
        edu_admin_identities = getattr(
            EduAdmin, 'objects').filter(profile=self).values('organization_id').distinct()
        for i in edu_admin_identities:
            edu_admin_org.append(i['organization_id'])
        identities[IdentityChoices.edu_admin] = edu_admin_org

        self.identities = identities
        self.save()

    def update_courses_cache(self):
        """
        刷新缓存的课程cid。
        :return: 
        """
        courses = {}
        # 刷新teaching courses
        teachers = getattr(self, 'teacher_identities')
        if teachers is not None:
            for teacher in teachers.all():
                for c in teacher.courses.all():
                    courses[c.cid] = 'teaching'
        # 刷新learning courses
        students = getattr(self, 'student_identities')
        if students is not None:
            for student in students.all():
                for c in student.courses.all():
                    courses[c.cid] = 'learning'
        self.courses = courses
        self.save()

    @staticmethod
    def create_profile(**kwargs):
        username = kwargs['username']
        password = kwargs['password']
        user = User(username=username)
        user.set_password(password)
        user.save()
        profile = UserProfile(user=user, username=username)
        profile.name = kwargs.get('name', None)
        profile.sex = kwargs.get('sex', 'SECRET')
        profile.phone = kwargs.get('phone', None)
        profile.email = kwargs.get('email', None)
        profile.github = kwargs.get('github', None)
        profile.qq = kwargs.get('qq', None)
        profile.wechat = kwargs.get('wechat', None)
        profile.blog = kwargs.get('blog', None)
        profile.introduction = kwargs.get('introduction', None)
        profile.is_staff = kwargs.get('is_staff', False)
        profile.identities = kwargs.get('identities', {
            IdentityChoices.student: [],
            IdentityChoices.teacher: [],
            IdentityChoices.edu_admin: []
        })
        profile.creator = kwargs.get('creator', None)
        profile.updater = kwargs.get('updater', None)
        profile.update_time = timezone.now()
        profile.available = kwargs.get('available', True)
        profile.deleted = kwargs.get('deleted', False)
        profile.save()
        return profile

    def get_organizations(self):
        """
        快速获得该用户关联的机构。仅在该用户是机构成员时才有有效结果。自动筛掉了root用户并按id排序.
        如果该用户是ROOT或者是ORG_ADMIN，那么自动获得全部机构的列表。
        :return: QuerySet<[Organization]>
        """
        organizations_id = []
        for identity, value in self.identities.items():
            if identity in ORG_IDENTITY_CHOICES and len(value) > 0:
                organizations_id += value
            elif (identity == IdentityChoices.root or identity == IdentityChoices.org_admin) and value is True:
                return Organization.objects.exclude(name='ROOT').exclude(deleted=True).all()
        return Organization.objects.filter(id__in=organizations_id).all()

    def get_courses(self, **kwargs):
        """
        快速获得该用户关联的课程。
        当存在参数时，按照参数筛选“teaching”和“learning”的课程。如果参数有“admin”且用户是教务管理员，则列出全部机构内课程。
        如果参数有admin且用户是site管理员，列出全部课程。
        1.通过course.objects->student.objects->id匹配，二重积
        2.通过relation.objects->student.id匹配，一重积，不过要并集
        3.通过cache缓存，course.objects->id匹配，一重积，可以直接用in语法
        根据设计文档，这里选择了方案3.
        :return: QuerySet<[Course]>
        """
        if len(kwargs) > 0:
            teaching = 'teaching' in kwargs and kwargs['teaching'] is True
            learning = 'learning' in kwargs and kwargs['learning'] is True
            admin = 'admin' in kwargs and kwargs['admin'] is True
        else:
            teaching = True
            learning = True
            admin = True
        courses_id = []
        for course, c_type in self.courses.items():
            if c_type == 'teaching' and teaching:
                courses_id.append(course)
            elif c_type == 'learning' and learning:
                courses_id.append(course)
        courses_edu = Course.objects.filter(cid__in=courses_id).all()
        if admin:
            organizations_id = []
            for identity, value in self.identities.items():
                if identity == IdentityChoices.edu_admin and len(value) > 0:
                    organizations_id += value
                elif (identity == IdentityChoices.root or identity == IdentityChoices.org_admin) and value is True:
                    return Course.objects.all()
            courses_admin = Course.objects.filter(organization__id__in=organizations_id).all()
        else:
            courses_admin = Course.objects.none()
        return (courses_edu | courses_admin).distinct()

    def get_course_groups(self, **kwargs):
        """
        获取所有管理的课程组。对于教师，会返回管理的课程组;对于教务管理员，会返回管理机构下的所有课程组。
        对于site管理员，返回全部课程组。
        该函数不通过缓存，直接查询。
        :return: 
        """
        if len(kwargs) > 0:
            teaching = kwargs['teaching'] if 'teaching' in kwargs else False
            admin = kwargs['admin'] if 'admin' in kwargs else False
        else:
            teaching = True
            admin = True
        course_groups = CourseGroup.objects.none()
        if admin and self.has_identities(IdentityChoices.root, IdentityChoices.org_admin):
            return CourseGroup.objects.all()
        if admin and self.has_identities(IdentityChoices.edu_admin):
            organizations = self.get_organizations()
            for org in organizations:
                if hasattr(org, 'course_groups'):
                    course_groups = course_groups | org.course_groups.all()
        if teaching and self.has_identities(IdentityChoices.teacher):
            teacher_identities = Teacher.objects.filter(profile=self).all()
            for teacher in teacher_identities:
                if hasattr(teacher, 'course_groups'):
                    course_groups = course_groups | teacher.course_groups.all()
        return course_groups.distinct()


class Student(Resource, PublicFieldMixin):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(User, related_name='student_identities', to_field='id',
                             on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, related_name='student_identities', to_field='user',
                                on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', related_name='students', to_field='id',
                                     on_delete=models.CASCADE)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=150)

    student_id = models.CharField(max_length=32)
    major = models.CharField(max_length=128, null=True)
    grade = models.CharField(max_length=32, null=True)
    class_in = models.CharField(max_length=128, null=True)

    def __str__(self):
        return "<Student %s: %s>" % (self.username, self.name)

    def get_sex(self):
        return self.profile.sex

    def get_phone(self):
        return self.profile.phone

    def get_email(self):
        return self.profile.email


class Teacher(Resource, PublicFieldMixin):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(User, related_name='teacher_identities', to_field='id',
                             on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, related_name='teacher_identities', to_field='user',
                                on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', related_name='teachers', to_field='id',
                                     on_delete=models.CASCADE)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=150)

    teacher_id = models.CharField(max_length=32)

    def __str__(self):
        return "<Teacher %s: %s>" % (self.username, self.name)

    def get_sex(self):
        return self.profile.sex

    def get_phone(self):
        return self.profile.phone

    def get_email(self):
        return self.profile.email


class EduAdmin(Resource, PublicFieldMixin):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(User, related_name='edu_admin_identities', to_field='id',
                             on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, related_name='edu_admin_identities', to_field='user',
                                on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', related_name='edu_admins', to_field='id',
                                     on_delete=models.CASCADE)

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=150)

    def __str__(self):
        return "<Edu Admin %s: %s>" % (self.username, self.name)


# -- Organization -----------------------------------------------------------------------

class Organization(Resource):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        max_length=32,
        unique=True,
        help_text=_('Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A organization with that name already exists."),
        },
    )
    caption = models.CharField(max_length=150)
    introduction = models.TextField(max_length=1024, null=True)

    parent = models.ForeignKey('self', related_name='children', to_field='name', null=True,
                               on_delete=models.CASCADE)

    number_organizations = models.IntegerField(default=0)
    number_students = models.IntegerField(default=0)
    number_teachers = models.IntegerField(default=0)
    number_admins = models.IntegerField(default=0)

    number_course_meta = models.IntegerField(default=0)
    number_courses = models.IntegerField(default=0)
    number_course_groups = models.IntegerField(default=0)

    categories = models.ManyToManyField('Category', related_name='organizations',
                                        through='OrganizationCategoryRelation',
                                        through_fields=('organization', 'category'))

    number_categories = models.IntegerField(default=0)
    number_problems = models.IntegerField(default=0)

    def update_numbers(self):
        number_organizations = getattr(Organization, 'objects').filter(parent=self).count()
        number_students = getattr(Student, 'objects').filter(organization=self).count()
        number_teachers = getattr(Teacher, 'objects').filter(organization=self).count()
        number_admins = getattr(EduAdmin, 'objects').filter(organization=self).count()

        number_course_meta = getattr(CourseMeta, 'objects').filter(organization=self).count()

        self.number_organizations = number_organizations
        self.number_students = number_students
        self.number_teachers = number_teachers
        self.number_admins = number_admins

        self.number_course_meta = number_course_meta

        self.number_categories = getattr(OrganizationCategoryRelation, 'objects').filter(organization=self).count()
        self.number_courses = getattr(Course, 'objects').filter(organization=self).count()
        self.number_course_groups = getattr(CourseGroup, 'objects').filter(organization=self).count()
        self.number_categories = getattr(OrganizationCategoryRelation, 'objects').filter(organization=self).count()
        self.number_problems = 0
        for v in getattr(OrganizationCategoryRelation, 'objects').filter(organization=self).all():
            self.number_problems += v.category.number_problem
        self.save()

    def available_categories(self):
        """
        获得所有该机构可用的题库的查询集。
        :return: QuerySet<[Category]>
        """
        org_root = Organization.objects.filter(name='ROOT').first()  # 获得org内的root机构
        if org_root.id == self.id:  # 自身是root机构，全题库
            return Category.objects
        elif self.parent is not None:
            if self.parent.id == org_root.id:  # 上级是root机构，全题库
                return Category.objects
            else:  # 不是，需要从上级题库中筛选
                return self.parent.categories
        else:  # 无上级(错误),全题库
            return Category.objects

    def __str__(self):
        return '<Organization %s: %s>' % (self.name, self.caption)


class CourseMeta(Resource):
    id = models.BigAutoField(primary_key=True)
    organization = models.ForeignKey(Organization,
                                     related_name='course_meta',
                                     to_field='name',
                                     on_delete=models.CASCADE)

    caption = models.CharField(max_length=150)
    categories = models.ManyToManyField('Category', related_name='course_meta',
                                        through='CourseMetaCategoryRelation',
                                        through_fields=('course_meta', 'category'))

    number_courses = models.IntegerField(default=0)
    number_course_groups = models.IntegerField(default=0)
    number_categories = models.IntegerField(default=0)
    number_problems = models.IntegerField(default=0)

    def __str__(self):
        return "<Course Meta %s: %s>" % (self.id, self.caption)

    def update_numbers(self):
        self.number_courses = getattr(Course, 'objects').filter(meta=self).count()
        self.number_course_groups = getattr(CourseGroup, 'objects').filter(meta=self).count()
        self.number_categories = self.categories.count()
        self.number_problems = sum(i.number_problem for i in self.categories.all())
        self.save()

    def available_categories(self):
        parent_available = self.organization.available_categories()
        exist_id = [i.id for i in self.categories.all()]  # 获得该meta旗下的所有的已用题库的id-list
        return parent_available.exclude(id__in=exist_id).all()


class CourseUnit(models.Model):
    TYPE_CHOICE = (('GROUP', 'GROUP'), ('COURSE', 'COURSE'))

    id = models.BigAutoField(primary_key=True)
    type = models.CharField(choices=TYPE_CHOICE, max_length=8)


class CourseGroup(Resource):
    course_unit = models.OneToOneField(CourseUnit, related_name='course_group', primary_key=True,
                                       to_field='id', on_delete=models.CASCADE)

    gid = models.BigIntegerField(unique=True)
    meta = models.ForeignKey(CourseMeta, related_name='course_groups',
                             to_field='id', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='course_groups',
                                     to_field='name', on_delete=models.CASCADE)

    caption = models.CharField(max_length=256)
    introduction = models.TextField(max_length=1024, null=True)

    courses = models.ManyToManyField('Course', related_name='course_groups',
                                     through='CourseGroupRelation',
                                     through_fields=('course_group', 'course'))
    teachers = models.ManyToManyField('Teacher', related_name='course_groups',
                                      through='CourseGroupTeacherRelation',
                                      through_fields=('course_group', 'teacher'))

    def __str__(self):
        return "<Course Group %s: %s>" % (self.gid, self.caption)

    @property
    def meta_caption(self):
        return self.meta.caption

    def available_teachers(self, filter_exists=False):
        """
        获得该课程组所有可用的教师的查询集。该查询集仅基于父机构的所有教师进行返回查询。
        如果指定了filter_exists，那么就会自动筛选掉已经在课程组中的教师。
        :return: QuerySet<[Teacher]>
        """
        org = self.organization
        if hasattr(org, 'teachers'):
            all_teachers = org.teachers.exclude(deleted=True).all()
            if filter_exists and hasattr(self, 'teachers'):
                exists_teachers_id = [v['id'] for v in self.teachers.all().values('id')]
                all_teachers = all_teachers.exclude(id__in=exists_teachers_id)
            return all_teachers
        else:
            return Teacher.objects.none()

    def available_courses(self, filter_exists=False):
        """
        获得所有可纳入的课程。调用参数使其过滤掉所有已经纳入的课程。
        :param filter_exists: 
        :return: 
        """
        org = self.organization
        if hasattr(org, 'courses'):
            all_courses = org.courses.exclude(deleted=True).all()
            if filter_exists and hasattr(self, 'courses'):
                exists_courses_id = [v['cid'] for v in self.courses.all().values('cid')]
                all_courses = all_courses.exclude(cid__in=exists_courses_id)
            return all_courses
        else:
            return Course.objects.none()


class Course(Resource):
    course_unit = models.OneToOneField(CourseUnit, related_name='course', primary_key=True,
                                       to_field='id', on_delete=models.CASCADE)

    cid = models.BigIntegerField(unique=True)
    meta = models.ForeignKey(CourseMeta, related_name='courses',
                             to_field='id', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='courses',
                                     to_field='name', on_delete=models.CASCADE)

    caption = models.CharField(max_length=256)
    introduction = models.TextField(max_length=1024, null=True)

    start_time = models.DateField()
    end_time = models.DateField()

    teachers = models.ManyToManyField('Teacher', related_name='courses',
                                      through='CourseTeacherRelation',
                                      through_fields=('course', 'teacher'))
    students = models.ManyToManyField('Student', related_name='courses',
                                      through='CourseStudentRelation',
                                      through_fields=('course', 'student'))

    def __str__(self):
        return "<Course %s: %s>" % (self.cid, self.caption)

    @property
    def meta_caption(self):
        return self.meta.caption

    def available_teachers(self, filter_exists=False):
        """
        获得该课程所有可用的教师的查询集。该查询集仅基于父机构的所有教师进行返回查询。
        如果指定了filter_exists，那么就会自动筛选掉已经在课程中的教师。
        :return: QuerySet<[Teacher]>
        """
        org = self.organization
        if hasattr(org, 'teachers'):
            all_teachers = org.teachers.exclude(deleted=True).all()
            if filter_exists and hasattr(self, 'teachers'):
                exists_teachers_id = [v['id'] for v in self.teachers.all().values('id')]
                all_teachers = all_teachers.exclude(id__in=exists_teachers_id)
            return all_teachers
        else:
            return Teacher.objects.none()

    def available_students(self, filter_exists=False):
        """
        获得该课程所有可用的学生的查询集。该查询集仅基于父机构的所有学生进行返回查询。
        如果指定了filter_exists，那么就会自动筛选掉已经在课程中的学生。
        :return: QuerySet<[Teacher]>
        """
        org = self.organization
        if hasattr(org, 'students'):
            all_students = org.students.exclude(deleted=True).all()
            if filter_exists and hasattr(self, 'students'):
                exists_students_id = [v['id'] for v in self.students.all().values('id')]
                all_students = all_students.exclude(id__in=exists_students_id)
            return all_students
        else:
            return Student.objects.none()

    def available_course_groups(self, filter_exists=False):
        """
        获得该课程可加入的所有课程组的查询集。通过参数过滤掉已经加入的课程组。
        :param filter_exists: 
        :return: 
        """
        org = self.organization
        if hasattr(org, 'course_groups'):
            all_groups = org.course_groups.exclude(deleted=True).all()
            if filter_exists and hasattr(self, 'course_groups'):
                exists_groups_id = [v['gid'] for v in self.course_groups.all().values('gid')]
                all_groups = all_groups.exclude(gid__in=exists_groups_id)
            return all_groups
        else:
            return CourseGroup.objects.none()


class CourseGroupRelation(Resource):
    id = models.BigAutoField(primary_key=True)

    course_group = models.ForeignKey(CourseGroup, related_name='course_relations',
                                     to_field='gid', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_group_relations',
                               to_field='cid', on_delete=models.CASCADE)
    weight = models.DecimalField(default=1, max_digits=19, decimal_places=10)


class CourseTeacherRelation(Resource):
    id = models.BigAutoField(primary_key=True)

    course = models.ForeignKey(Course, related_name='teacher_relations',
                               to_field='cid', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='course_relations',
                                to_field='id', on_delete=models.CASCADE)


class CourseStudentRelation(Resource):
    id = models.BigAutoField(primary_key=True)

    course = models.ForeignKey(Course, related_name='student_relations',
                               to_field='cid', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='course_relations',
                                to_field='id', on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    score_detail = pg_fields.JSONField()


class CourseGroupTeacherRelation(Resource):
    id = models.BigAutoField(primary_key=True)
    course_group = models.ForeignKey(CourseGroup, related_name='teacher_relations',
                                     to_field='gid', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='course_group_relations',
                                to_field='id', on_delete=models.CASCADE)


# -- Mission ----------------------------------------------------------------------------

class MissionState:
    not_started = 'NOT_STARTED'
    running = 'RUNNING'
    ended = 'ENDED'

MISSION_STATE = (
    'NOT_STARTED',
    'RUNNING',
    'ENDED'
)
MISSION_MODE = (
    ('CUSTOM', 'CUSTOM'),
    ('ACM', 'ACM'),
    ('C4', 'C4'),
    ('CCF', 'CCF')
)


class Mission(Resource):
    id = models.BigAutoField(primary_key=True)
    caption = models.CharField(max_length=150)
    course_meta = models.ForeignKey(CourseMeta, related_name='missions',
                                    to_field='id', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='missions',
                                     to_field='id', on_delete=models.CASCADE)
    problems = models.ManyToManyField('Problem', related_name='missions',
                                      through='MissionProblemRelation',
                                      through_fields=('mission', 'problem'))
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    mode = models.CharField(choices=MISSION_MODE, max_length=6, default='CUSTOM')
    config = pg_fields.JSONField(null=True)

    @staticmethod
    def validate_config(data):
        """
        用来验证config的配置是否合法。
        :param data: 
        :return: 如果合法，返回None，否则返回错误字符串。
        """
        template = {
            'type': {
                'acm': None,
                'oi': {
                    'valid_submission': {
                        'highest': None,
                        'latest': None
                    }
                }
            },
            'submission_display': {
                'self': None,
                'all': None,
                'no': None
            },
            'score_display': {
                'yes': None,
                'close': None,
                'no': None
            }
        }

        def validate_level(json, temp):
            for config_name, config_list in temp.items():
                if config_name not in json:
                    return 'Config "%s" is not exist.' % (config_name,)
                flag = False
                for item, sub_config in config_list.items():
                    if json[config_name] == item:  # 匹配到了可用的内容。
                        flag = True
                        if sub_config is not None:  # 表示匹配到了当前选项存在参数。
                            if "%s_config" % (config_name,) not in json:
                                return 'Sub config of "%s" is not exist.' % (config_name,)
                            ret = validate_level(json["%s_config" % (config_name,)], sub_config)
                            if ret is not None:
                                return ret
                        break
                if not flag:  # 这表示没有正确的匹配。
                    return 'Config "%s" is not valid.' % (config_name,)
            return None
        return validate_level(data, template)

    @staticmethod
    def default_mode_config(mode):
        acm_config = {
            'type': 'acm',
            'submission_display': 'self',
            'score_display': 'yes'
        }
        c4_config = {
            'type': 'oi',
            'type_config': {
                'valid_submission': 'highest'
            },
            'submission_display': 'self',
            'score_display': 'yes'
        }
        ccf_config = {
            'type': 'oi',
            'type_config': {
                'valid_submission': 'latest'
            },
            'submission_display': 'self',
            'score_display': 'close'
        }
        if mode == 'ACM':
            return acm_config
        elif mode == 'C4':
            return c4_config
        elif mode == 'CCF':
            return ccf_config
        else:
            return None

    @property
    def meta_caption(self):
        return self.course_meta.caption

    def available_problem_relations(self):
        """
        给出任务可以使用的全部的题目的依赖关系的查询集，包括已经添加在内的题目。
        :return: 
        """
        meta = self.course_meta
        available_cat = meta.categories.all()  # 给出所处课程基类被分配使用的全部题库
        relations = CategoryProblemRelation.objects.none()
        for cat in available_cat.all():
            relations = relations | CategoryProblemRelation.objects.filter(category=cat).all()
        return relations.distinct()

    def available_problems(self):
        """
        给出任务可以使用的全部的题目的查询集，包括已经添加的题目在内。
        :return: 
        """
        meta = self.course_meta
        available_cat = meta.categories.all()
        problems = Problem.objects.none()
        for cat in available_cat.all():
            problems = problems | cat.problems.all()
        return problems.distinct()

    def get_state(self):
        """
        返回该任务的进行状态，使用一个具有代号的字符串来表示。
        :return: MISSION_STATE
        """
        now = now_dt()
        if now > self.end_time.replace(tzinfo=None):
            return MissionState.ended
        elif now >= self.start_time.replace(tzinfo=None):
            return MissionState.running
        else:
            return MissionState.not_started

    def get_config(self):
        if self.mode == 'CUSTOM':
            return self.config
        else:
            return Mission.default_mode_config(self.mode)

    def __str__(self):
        return "<Mission %s: %s >" % (self.id, self.caption)


class MissionGroup(Resource):
    id = models.BigAutoField(primary_key=True)
    caption = models.CharField(max_length=150)
    course_meta = models.ForeignKey(CourseMeta, related_name='mission_groups',
                                    to_field='id', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='mission_groups',
                                     to_field='id', on_delete=models.CASCADE)
    course_unit = models.ForeignKey(CourseUnit, related_name='mission_groups',
                                    to_field='id', on_delete=models.CASCADE)
    missions = models.ManyToManyField(Mission, related_name='groups',
                                      through='MissionGroupRelation',
                                      through_fields=('mission_group', 'mission'))
    weight = models.DecimalField(default=1, max_digits=19, decimal_places=10)

    def __str__(self):
        return "<Mission Group %s: %s>" % (self.id, self.caption)

    def available_missions(self, filter_exists=False):
        org = self.organization
        if hasattr(org, 'missions'):
            missions = org.missions.exclude(deleted=True).all()
            if filter_exists and hasattr(self, 'missions'):
                exists_id = [v['id'] for v in self.missions.all().values('id')]
                missions = missions.exclude(id__in=exists_id)
            return missions
        else:
            return Mission.objects.none()


class MissionGroupRelation(Resource):
    id = models.BigAutoField(primary_key=True)
    mission = models.ForeignKey(Mission, related_name='group_relations',
                                to_field='id', on_delete=models.CASCADE)
    mission_group = models.ForeignKey(MissionGroup, related_name='mission_relations',
                                      to_field='id', on_delete=models.CASCADE)
    weight = models.DecimalField(default=1, max_digits=19, decimal_places=10)


class MissionProblemRelation(Resource):
    id = models.BigAutoField(primary_key=True)
    mission = models.ForeignKey(Mission, related_name='problem_relations',
                                to_field='id', on_delete=models.CASCADE)
    problem = models.ForeignKey('Problem', related_name='mission_relations',
                                to_field='id', on_delete=models.CASCADE)
    weight = models.DecimalField(default=1, max_digits=19, decimal_places=10)


class Rank(models.Model):
    id = models.BigAutoField(primary_key=True)
    mission = models.ForeignKey(Mission, related_name='ranks', to_field='id', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='ranks', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, to_field='user', related_name='ranks', on_delete=models.CASCADE)

    sub_count = models.IntegerField(default=0)
    solved = models.IntegerField(default=0)
    penalty = models.BigIntegerField(default=0)
    sum_score = models.FloatField(default=0)
    result = pg_fields.JSONField()


# -- Problem ------------------------------------------------------------------

class Problem(models.Model):
    id = models.BigIntegerField(primary_key=True)
    description = models.TextField()
    sample = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    title = models.CharField(max_length=128)
    introduction = models.CharField(max_length=512, null=True)
    source = models.CharField(max_length=256, null=True)
    author = models.CharField(max_length=64, null=True)
    is_special_judge = models.BooleanField()
    number_test_data = models.IntegerField()
    number_limit = models.IntegerField()
    number_category = models.IntegerField()
    number_invalid_word = models.IntegerField()

    def __str__(self):
        return "<Problem %s: %s >" % (self.id, self.title)

    def get_limits(self):
        if hasattr(self, 'limits'):
            return self.limits
        else:
            return Limit.objects.none()

    def get_environments(self):
        if hasattr(self, 'limits'):
            limits = self.limits
            environments = Environment.objects.none()
            for limit in limits.all():
                environments = environments | Environment.objects.filter(id=limit.environment_id)
            return environments.distinct()
        else:
            return Environment.objects.none()


class Environment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return "<Environment %s: %s >" % (self.id, self.name)


class Limit(models.Model):
    id = models.BigAutoField(primary_key=True)
    problem = models.ForeignKey(Problem, related_name='limits',
                                to_field='id', on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, related_name='limits',
                                    to_field='id', on_delete=models.CASCADE)
    env_name = models.CharField(max_length=128)
    # 时间限制
    time_limit = models.IntegerField(default=-1)
    # 内存限制
    memory_limit = models.IntegerField(default=-1)
    # 代码长度限制
    length_limit = models.IntegerField(default=-1)

    def __str__(self):
        return "<Limit %s: %s>" % (self.id, self.env_name)


# -- Category -----------------------------------------------------------------

class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    introduction = models.CharField(max_length=512, null=True)
    source = models.CharField(max_length=256, null=True)
    author = models.CharField(max_length=64, null=True)
    problems = models.ManyToManyField(Problem, related_name='categories',
                                      through='CategoryProblemRelation',
                                      through_fields=('category', 'problem'))
    number_problem = models.IntegerField(default=0)

    def __str__(self):
        return "<Category %s: %s>" % (self.id, self.title)


class CategoryProblemRelation(models.Model):
    id = models.BigIntegerField(primary_key=True)
    category = models.ForeignKey(Category, related_name='problem_relations',
                                 to_field='id', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name='category_relations',
                                to_field='id', on_delete=models.CASCADE)
    directory = pg_fields.ArrayField(models.CharField(max_length=128))

    def __str__(self):
        return "<Category - Problem Relation %s: %s - %s>" % (self.id, self.category.id, self.problem.id)


class OrganizationCategoryRelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    organization = models.ForeignKey(Organization, related_name='category_relations',
                                     to_field='id', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='organization_relations',
                                 to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return "<Organization - Category Relation %s: %s - %s>" % (self.id, self.organization.name, self.category.id)


class CourseMetaCategoryRelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    organization = models.ForeignKey(Organization, related_name='course_meta_category_relations',
                                     to_field='id', on_delete=models.CASCADE)
    course_meta = models.ForeignKey(CourseMeta, related_name='category_relations',
                                    to_field='id', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='course_meta_relations',
                                 to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return "<CourseMeta - Category Relation %s: %s - %s>" % (self.id, self.course_meta.id, self.category.id)


# -- Submission ---------------------------------------------------------------

class Submission(models.Model):
    STATUS_CHOICES = (
        ('PD', 'Pending'),
        ('PDR', 'Pending Rejudge'),
        ('CP', 'Compiling'),
        ('CE', 'Compile Error'),
        ('CD', 'Compile Done'),
        ('RJ', 'Running & Judging'),
        ('RN', 'Running'),
        ('RE', 'Runtime Error'),
        ('TLE', 'Time Limit Exceed'),
        ('MLE', 'Memory Limit Exceed'),
        ('OLE', 'Output Limit Exceed'),
        ('IW', 'Invalid Word'),
        ('LLE', 'Length Limit Exceed'),
        ('RD', 'Running Done'),
        ('JD', 'Judging'),
        ('WA', 'Wrong Answer'),
        ('PE', 'Presentation Error'),
        ('AC', 'Accepted'),
    )

    id = models.BigAutoField(primary_key=True)
    sid = models.BigIntegerField(unique=True)
    problem = models.ForeignKey(Problem, related_name='submissions', null=True,
                                to_field='id', on_delete=models.SET_NULL)
    environment = models.ForeignKey(Environment, related_name='submissions', null=True,
                                    to_field='id', on_delete=models.SET_NULL)

    time = models.IntegerField(default=-1)
    memory = models.IntegerField(default=-1)
    length = models.IntegerField(default=-1)

    user = models.ForeignKey(UserProfile, related_name='submissions', null=True,
                             to_field='user', on_delete=models.SET_NULL)
    status = models.CharField(max_length=4, default='PD', choices=STATUS_CHOICES)
    score = models.FloatField(default=None, null=True)
    finished = models.BooleanField(default=False)

    submit_time = models.DateTimeField()
    update_time = models.DateTimeField()
    ip = models.GenericIPAddressField()

    mission = models.ForeignKey(Mission, related_name='submissions', null=True,
                                to_field='id', on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, related_name='submissions', null=True,
                                     to_field='id', on_delete=models.SET_NULL)

    def __str__(self):
        return "<Submission %s of by %s in %s>" % (self.id, self.problem_id, self.environment_id)


class CompileInfo(models.Model):
    # 所属的提交
    submission = models.OneToOneField(Submission, related_name='compile_info', to_field='id', primary_key=True)
    # 编译信息
    info = models.TextField(null=True)

    def __str__(self):
        return "<Compile Info %s>" % (self.submission_id,)


class TestDataStatus(models.Model):
    # 所属的提交
    submission = models.OneToOneField(Submission, related_name='test_data_status',
                                      to_field='id', primary_key=True)
    # 状态
    status = pg_fields.JSONField()

    def __str__(self):
        return "<Test Data Status %s>" % (self.submission_id,)


class SubmissionCode(models.Model):
    # 所属的提交
    submission = models.OneToOneField(Submission, related_name='code',
                                      to_field='id', primary_key=True)
    # 代码
    code = pg_fields.JSONField()

    def __str__(self):
        return "<Submission Code %s>" % (self.submission_id,)
