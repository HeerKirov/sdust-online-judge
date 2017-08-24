# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from config import CLIENT_SETTINGS
from .submissions import submit
from .models import *
from .utils import dict_sub


def now_dt():
    """
    返回一个当地时间。
    :return: 
    """
    now = datetime.now() + timedelta(hours=0)  # 这坑爹的时区处理……
    return now

_RESOURCE_READONLY = ('creator', 'updater', 'create_time', 'update_time')


class Utils(object):
    @staticmethod
    def validate_username(value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('User exists.')
        return value

    @staticmethod
    def validate_password(pwd):
        if pwd is None or pwd == '':
            raise serializers.ValidationError('Password can not be empty.')
        return pwd

    @staticmethod
    def validate_old_password(serializer, old_pwd):
        if old_pwd is not None:
            user = serializer.instance
            u = authenticate(username=user.username, password=old_pwd)
            if u is not None:
                if not user.is_active:
                    raise serializers.ValidationError('User disabled.')
            else:
                raise serializers.ValidationError('Password incorrect.')

            new_password = serializer.initial_data.get('new_password', None)
            if new_password is None or new_password == '':
                raise serializers.ValidationError('New password cannot be None.')

        return old_pwd

    @staticmethod
    def validate_sex(value):
        if value is not None and value not in UserProfile.SEX_CHOICES:
            raise serializers.ValidationError(
                'Sex can only be "MALE", "FEMALE" or "SECRET".'
            )
        return value


class PersonalSerializers(object):
    class LoginSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'password')
            extra_kwargs = {
                'username': {'write_only': True,
                             'validators': [RegexValidator()]},
                'password': {'write_only': True,
                             'style': {'input_type': 'password'}}
            }

    class PersonalInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserProfile
            exclude = ('user', 'is_staff', 'identities', 'courses')
            read_only_fields = (
                'username', 'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

    class UserPasswordSerializer(serializers.ModelSerializer):
        old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
        new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

        class Meta:
            model = User
            fields = ('username', 'old_password', 'new_password',)
            read_only_fields = ('username', )

        def validate_old_password(self, value):
            Utils.validate_old_password(self, value)
            return value

        @staticmethod
        def validate_new_password(value):
            return Utils.validate_password(value)

        def update(self, instance, validated_data):
            new_password = validated_data['new_password']
            instance.set_password(new_password)
            instance.save()
            return instance


class UserSerializers(object):
    # admin - 所有root
    class ListRoot(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True)

        @staticmethod
        def validate_username(value):
            return Utils.validate_username(value)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it in SITE_IDENTITY_CHOICES:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def create(self, validated_data):
            validated_data['identities'] = validated_data.pop('get_identities', {})
            profile = UserProfile.create_profile(**validated_data)
            profile.update_identities()
            return profile

    # admin - 所有root
    class InstanceRoot(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it in SITE_IDENTITY_CHOICES:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                instance.user.set_password(validated_data.pop('password'))
                instance.user.save()
            validated_data['identities'] = validated_data.pop('get_identities', {})
            ret = super().update(instance, validated_data)
            ret.update_identities()
            return instance

    # admin - 所有管理员
    class ListAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True)

        @staticmethod
        def validate_username(value):
            return Utils.validate_username(value)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it in ADMIN_IDENTITY_CHOICES:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def create(self, validated_data):
            validated_data['identities'] = validated_data.pop('get_identities', {})
            profile = UserProfile.create_profile(**validated_data)
            profile.update_identities()
            return profile

    # admin - 所有管理员
    class InstanceAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it in ADMIN_IDENTITY_CHOICES:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                instance.user.set_password(validated_data.pop('password'))
                instance.user.save()
            validated_data['identities'] = validated_data.pop('get_identities', {})
            ret = super().update(instance, validated_data)
            ret.update_identities()
            return instance

    # admin - 机构管理员
    class ListOrgAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True,
                                           read_only=True)

        @staticmethod
        def validate_username(value):
            return Utils.validate_username(value)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it == IdentityChoices.org_admin:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def create(self, validated_data):
            validated_data['identities'] = {IdentityChoices.org_admin: True}  # validated_data.pop('get_identities', {})
            profile = UserProfile.create_profile(**validated_data)
            profile.update_identities()
            return profile

    # admin - 机构管理员
    class InstanceOrgAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True,
                                           read_only=True)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it == IdentityChoices.org_admin:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                instance.user.set_password(validated_data.pop('password'))
                instance.user.save()
            # validated_data['identities'] = validated_data.pop('get_identities', {})
            ret = super().update(instance, validated_data)
            ret.update_identities()
            return instance

    # admin - 用户管理员
    class ListUserAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True,
                                           read_only=True)

        @staticmethod
        def validate_username(value):
            return Utils.validate_username(value)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it == IdentityChoices.user_admin:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def create(self, validated_data):
            validated_data['identities'] = {IdentityChoices.user_admin: True}
            profile = UserProfile.create_profile(**validated_data)
            profile.update_identities()
            return profile

    # admin - 用户管理员
    class InstanceUserAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True,
                                           read_only=True)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        @staticmethod
        def validate_identities(value):
            ret = {}
            for it in value:
                if it == IdentityChoices.user_admin:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                instance.user.set_password(validated_data.pop('password'))
                instance.user.save()
            ret = super().update(instance, validated_data)
            ret.update_identities()
            return instance

    # admin - 教务管理员
    class ListEduAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        sex = serializers.CharField(required=False)
        phone = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        github = serializers.CharField(required=False)
        qq = serializers.CharField(required=False)
        wechat = serializers.CharField(required=False)
        blog = serializers.CharField(required=False)
        introduction = serializers.CharField(required=False)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        @staticmethod
        def validate_username(value):
            return Utils.validate_username(value)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        def create(self, validated_data):
            organization = validated_data['organization']
            profile = UserProfile.create_profile(**validated_data)
            edu_admin = EduAdmin(
                user=profile.user,
                profile=profile,
                username=profile.username,
                name=profile.name,
                organization=organization,
                # 缓存项和重复项
                available=profile.available,
                deleted=profile.deleted,
                creator=profile.creator,
                updater=profile.updater,
                update_time=profile.update_time
            )
            edu_admin.save()
            profile.update_identities()
            return edu_admin

        class Meta:
            model = EduAdmin
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
            )

    # admin - 教务管理员
    class InstanceEduAdmin(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True, required=False)
        sex = serializers.CharField(required=False)
        phone = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        github = serializers.CharField(required=False)
        qq = serializers.CharField(required=False)
        wechat = serializers.CharField(required=False)
        blog = serializers.CharField(required=False)
        introduction = serializers.CharField(required=False)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                instance.user.set_password(validated_data.pop('password'))
                instance.user.save()
            ret = super().update(instance, validated_data)
            profile = ret.profile
            profile.update_identities()
            # 下面更新那些缓存项和重复项
            profile.updater = ret.updater
            profile.name = ret.name
            profile.available = ret.available
            profile.deleted = ret.deleted
            profile.save()
            return instance

        class Meta:
            model = EduAdmin
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'username',
                'creator', 'updater', 'create_time', 'update_time',
            )


# 机构下的用户
class OrgUserSerializers(object):
    # 教务管理员
    class ListEduAdmin(serializers.ModelSerializer):
        sex = serializers.CharField(read_only=True)
        phone = serializers.CharField(read_only=True)
        email = serializers.CharField(read_only=True)
        github = serializers.CharField(read_only=True)
        qq = serializers.CharField(read_only=True)
        wechat = serializers.CharField(read_only=True)
        blog = serializers.CharField(read_only=True)
        introduction = serializers.CharField(read_only=True)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        class Meta:
            model = EduAdmin
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
            )

    # 教务管理员
    class InstanceEduAdmin(serializers.ModelSerializer):
        sex = serializers.CharField(read_only=True)
        phone = serializers.CharField(read_only=True)
        email = serializers.CharField(read_only=True)
        github = serializers.CharField(read_only=True)
        qq = serializers.CharField(read_only=True)
        wechat = serializers.CharField(read_only=True)
        blog = serializers.CharField(read_only=True)
        introduction = serializers.CharField(read_only=True)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        class Meta:
            model = UserProfile
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'username',
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

    # 教师
    class ListTeacher(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        sex = serializers.CharField(required=False)
        phone = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        github = serializers.CharField(required=False)
        qq = serializers.CharField(required=False)
        wechat = serializers.CharField(required=False)
        blog = serializers.CharField(required=False)
        introduction = serializers.CharField(required=False)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)
        teacher_id = serializers.CharField(required=True)

        @staticmethod
        def validate_username(value):
            return Utils.validate_username(value)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        def create(self, validated_data):
            organization = validated_data['organization']
            profile = UserProfile.create_profile(**validated_data)
            teacher = Teacher(
                user=profile.user,
                profile=profile,
                username=profile.username,
                name=profile.name,
                organization=organization,
                # 缓存项和重复项
                available=profile.available,
                deleted=profile.deleted,
                creator=profile.creator,
                updater=profile.updater,
                update_time=profile.update_time,
                # 私有项
                teacher_id=validated_data['teacher_id']
            )
            teacher.save()
            profile.update_identities()
            return teacher

        class Meta:
            model = Teacher
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
            )

    # 教师
    class InstanceTeacher(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True, required=False)
        sex = serializers.CharField(required=False)
        phone = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        github = serializers.CharField(required=False)
        qq = serializers.CharField(required=False)
        wechat = serializers.CharField(required=False)
        blog = serializers.CharField(required=False)
        introduction = serializers.CharField(required=False)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                instance.user.set_password(validated_data.pop('password'))
                instance.user.save()
            ret = super().update(instance, validated_data)
            profile = ret.profile
            profile.update_identities()
            # 下面更新那些缓存项和重复项
            profile.updater = ret.updater
            profile.name = ret.name
            profile.available = ret.available
            profile.deleted = ret.deleted
            profile.save()
            return instance

        class Meta:
            model = Teacher
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'username',
                'creator', 'updater', 'create_time', 'update_time',
            )

    # 学生
    class ListStudent(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True)
        sex = serializers.CharField(required=False)
        phone = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        github = serializers.CharField(required=False)
        qq = serializers.CharField(required=False)
        wechat = serializers.CharField(required=False)
        blog = serializers.CharField(required=False)
        introduction = serializers.CharField(required=False)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)
        student_id = serializers.CharField(required=True)
        major = serializers.CharField(allow_null=True, allow_blank=True)
        grade = serializers.CharField(allow_blank=True, allow_null=True)
        class_in = serializers.CharField(allow_null=True, allow_blank=True)

        @staticmethod
        def validate_username(value):
            return Utils.validate_username(value)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        def create(self, validated_data):
            organization = validated_data['organization']
            profile = UserProfile.create_profile(**validated_data)
            student = Student(
                user=profile.user,
                profile=profile,
                username=profile.username,
                name=profile.name,
                organization=organization,
                # 缓存项和重复项
                available=profile.available,
                deleted=profile.deleted,
                creator=profile.creator,
                updater=profile.updater,
                update_time=profile.update_time,
                # 私有项
                student_id=validated_data['student_id'],
                major=validated_data['major'] if 'major' in validated_data else None,
                grade=validated_data['grade'] if 'grade' in validated_data else None,
                class_in=validated_data['class_in'] if 'class_in' in validated_data else None
            )
            student.save()
            profile.update_identities()
            return student

        class Meta:
            model = Student
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
            )

    # 学生
    class InstanceStudent(serializers.ModelSerializer):
        password = serializers.CharField(max_length=128, write_only=True, required=False)
        sex = serializers.CharField(required=False)
        phone = serializers.CharField(required=False)
        email = serializers.CharField(required=False)
        github = serializers.CharField(required=False)
        qq = serializers.CharField(required=False)
        wechat = serializers.CharField(required=False)
        blog = serializers.CharField(required=False)
        introduction = serializers.CharField(required=False)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        @staticmethod
        def validate_password(value):
            return Utils.validate_password(value)

        @staticmethod
        def validate_sex(value):
            return Utils.validate_sex(value)

        def update(self, instance, validated_data):
            if 'password' in validated_data:
                instance.user.set_password(validated_data.pop('password'))
                instance.user.save()
            ret = super().update(instance, validated_data)
            profile = ret.profile
            profile.update_identities()
            # 下面更新那些缓存项和重复项
            profile.updater = ret.updater
            profile.name = ret.name
            profile.available = ret.available
            profile.deleted = ret.deleted
            profile.save()
            return instance

        class Meta:
            model = Student
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'username',
                'creator', 'updater', 'create_time', 'update_time',
            )


# 课程下的用户
class CourseUserSerializers(object):
    # 教师
    class ListTeacher(serializers.ModelSerializer):
        username = serializers.SlugRelatedField(queryset=Teacher.objects.all(), slug_field='username', source='teacher')
        name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='teacher')
        teacher_id = serializers.SlugRelatedField(read_only=True, slug_field='teacher_id', source='teacher')
        sex = serializers.SlugRelatedField(read_only=True, slug_field='sex', source='teacher')
        introduction = serializers.SlugRelatedField(read_only=True, slug_field='introduction', source='teacher')

        def create(self, validated_data):
            # 做可用性检验
            teacher = validated_data['teacher']
            course = validated_data['course']
            available_teachers = course.available_teachers()
            if teacher not in available_teachers:
                raise ValidationError('teacher is not available.')
            elif course.teachers.filter(id=teacher.id).exists():
                raise ValidationError('teacher exists.')
            instance = super().create(validated_data)
            return instance

        class Meta:
            model = CourseTeacherRelation
            read_only_fields = ('id',) + _RESOURCE_READONLY
            exclude = ('course', 'teacher')

    # 教师
    class InstanceTeacher(serializers.ModelSerializer):
        username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='teacher')
        name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='teacher')
        teacher_id = serializers.SlugRelatedField(read_only=True, slug_field='teacher_id', source='teacher')
        sex = serializers.SlugRelatedField(read_only=True, slug_field='sex', source='teacher')
        introduction = serializers.SlugRelatedField(read_only=True, slug_field='introduction', source='teacher')
        phone = serializers.SlugRelatedField(read_only=True, slug_field='phone', source='teacher')
        email = serializers.SlugRelatedField(read_only=True, slug_field='email', source='teacher')
        github = serializers.SlugRelatedField(read_only=True, slug_field='github', source='teacher')
        qq = serializers.SlugRelatedField(read_only=True, slug_field='qq', source='teacher')
        wechat = serializers.SlugRelatedField(read_only=True, slug_field='wechat', source='teacher')
        blog = serializers.SlugRelatedField(read_only=True, slug_field='blog', source='teacher')
        last_login = serializers.SlugRelatedField(read_only=True, slug_field='last_login', source='teacher')
        ip = serializers.SlugRelatedField(read_only=True, slug_field='ip', source='teacher')

        class Meta:
            model = CourseTeacherRelation
            read_only_fields = ('id',) + _RESOURCE_READONLY
            exclude = ('course', 'teacher')

    # 课程可添加的教师
    class ListAvailableTeacher(serializers.ModelSerializer):
        sex = serializers.CharField(read_only=True)
        phone = serializers.CharField(read_only=True)
        email = serializers.CharField(read_only=True)
        github = serializers.CharField(read_only=True)
        qq = serializers.CharField(read_only=True)
        wechat = serializers.CharField(read_only=True)
        blog = serializers.CharField(read_only=True)
        introduction = serializers.CharField(read_only=True)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        class Meta:
            model = Teacher
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
            )

    # 学生
    class ListStudent(serializers.ModelSerializer):
        username = serializers.SlugRelatedField(queryset=Student.objects.all(), slug_field='username', source='student')
        name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='student')
        student_id = serializers.SlugRelatedField(read_only=True, slug_field='student_id', source='student')
        major = serializers.SlugRelatedField(read_only=True, slug_field='major', source='student')
        grade = serializers.SlugRelatedField(read_only=True, slug_field='grade', source='student')
        class_in = serializers.SlugRelatedField(read_only=True, slug_field='class_in', source='student')
        sex = serializers.SlugRelatedField(read_only=True, slug_field='sex', source='student')
        introduction = serializers.SlugRelatedField(read_only=True, slug_field='introduction', source='student')

        def create(self, validated_data):
            # 做可用性检验
            student = validated_data['student']
            course = validated_data['course']
            available_students = course.available_students()
            if student not in available_students:
                raise ValidationError('student is not available.')
            elif course.students.filter(id=student.id).exists():
                raise ValidationError('student exists.')
            validated_data['score_detail'] = {}
            instance = super().create(validated_data)
            return instance

        class Meta:
            model = CourseStudentRelation
            read_only_fields = ('id',) + _RESOURCE_READONLY
            exclude = ('course', 'score', 'score_detail', 'student')

    # 学生
    class InstanceStudent(serializers.ModelSerializer):
        username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='student')
        name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='student')
        student_id = serializers.SlugRelatedField(read_only=True, slug_field='student_id', source='student')
        major = serializers.SlugRelatedField(read_only=True, slug_field='major', source='student')
        grade = serializers.SlugRelatedField(read_only=True, slug_field='grade', source='student')
        class_in = serializers.SlugRelatedField(read_only=True, slug_field='class_in', source='student')
        sex = serializers.SlugRelatedField(read_only=True, slug_field='sex', source='student')
        introduction = serializers.SlugRelatedField(read_only=True, slug_field='introduction', source='student')
        phone = serializers.SlugRelatedField(read_only=True, slug_field='phone', source='student')
        email = serializers.SlugRelatedField(read_only=True, slug_field='email', source='student')
        github = serializers.SlugRelatedField(read_only=True, slug_field='github', source='student')
        qq = serializers.SlugRelatedField(read_only=True, slug_field='qq', source='student')
        wechat = serializers.SlugRelatedField(read_only=True, slug_field='wechat', source='student')
        blog = serializers.SlugRelatedField(read_only=True, slug_field='blog', source='student')
        last_login = serializers.SlugRelatedField(read_only=True, slug_field='last_login', source='student')
        ip = serializers.SlugRelatedField(read_only=True, slug_field='ip', source='student')

        class Meta:
            model = CourseStudentRelation
            read_only_fields = ('id',) + _RESOURCE_READONLY
            exclude = ('course', 'score', 'score_detail', 'student')

    # 课程可添加的教师
    class ListAvailableStudent(serializers.ModelSerializer):
        sex = serializers.CharField(read_only=True)
        phone = serializers.CharField(read_only=True)
        email = serializers.CharField(read_only=True)
        github = serializers.CharField(read_only=True)
        qq = serializers.CharField(read_only=True)
        wechat = serializers.CharField(read_only=True)
        blog = serializers.CharField(read_only=True)
        introduction = serializers.CharField(read_only=True)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        class Meta:
            model = Student
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
            )


# 课程组下的用户
class CourseGroupUserSerializer(object):
    # 教师
    class ListTeacher(serializers.ModelSerializer):
        username = serializers.SlugRelatedField(queryset=Teacher.objects.all(), slug_field='username', source='teacher')
        name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='teacher')
        teacher_id = serializers.SlugRelatedField(read_only=True, slug_field='teacher_id', source='teacher')
        sex = serializers.SlugRelatedField(read_only=True, slug_field='sex', source='teacher')
        introduction = serializers.SlugRelatedField(read_only=True, slug_field='introduction', source='teacher')

        def create(self, validated_data):
            # 做可用性检验
            teacher = validated_data['teacher']
            course_group = validated_data['course_group']
            available_teachers = course_group.available_teachers()
            if teacher not in available_teachers:
                raise ValidationError('teacher is not available.')
            elif course_group.teachers.filter(id=teacher.id).exists():
                raise ValidationError('teacher exists.')
            instance = super().create(validated_data)
            # 与course不同，目前没有缓存group。
            return instance

        class Meta:
            model = CourseGroupTeacherRelation
            read_only_fields = ('id',) + _RESOURCE_READONLY
            exclude = ('course_group', 'teacher')

    # 教师
    class InstanceTeacher(serializers.ModelSerializer):
        username = serializers.SlugRelatedField(read_only=True, slug_field='username', source='teacher')
        name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='teacher')
        teacher_id = serializers.SlugRelatedField(read_only=True, slug_field='teacher_id', source='teacher')
        sex = serializers.SlugRelatedField(read_only=True, slug_field='sex', source='teacher')
        introduction = serializers.SlugRelatedField(read_only=True, slug_field='introduction', source='teacher')
        phone = serializers.SlugRelatedField(read_only=True, slug_field='phone', source='teacher')
        email = serializers.SlugRelatedField(read_only=True, slug_field='email', source='teacher')
        github = serializers.SlugRelatedField(read_only=True, slug_field='github', source='teacher')
        qq = serializers.SlugRelatedField(read_only=True, slug_field='qq', source='teacher')
        wechat = serializers.SlugRelatedField(read_only=True, slug_field='wechat', source='teacher')
        blog = serializers.SlugRelatedField(read_only=True, slug_field='blog', source='teacher')
        last_login = serializers.SlugRelatedField(read_only=True, slug_field='last_login', source='teacher')
        ip = serializers.SlugRelatedField(read_only=True, slug_field='ip', source='teacher')

        class Meta:
            model = CourseGroupTeacherRelation
            read_only_fields = ('id',) + _RESOURCE_READONLY
            exclude = ('course_group', 'teacher')

    # 课程组可添加的教师
    class ListAvailableTeacher(serializers.ModelSerializer):
        sex = serializers.CharField(read_only=True)
        phone = serializers.CharField(read_only=True)
        email = serializers.CharField(read_only=True)
        github = serializers.CharField(read_only=True)
        qq = serializers.CharField(read_only=True)
        wechat = serializers.CharField(read_only=True)
        blog = serializers.CharField(read_only=True)
        introduction = serializers.CharField(read_only=True)
        last_login = serializers.DateTimeField(read_only=True)
        ip = serializers.IPAddressField(read_only=True)

        class Meta:
            model = Teacher
            exclude = ('user', 'profile', 'organization')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
            )


class OrganizationSerializers(object):
    class Organization(object):
        # admin - 机构
        class ListAdmin(serializers.ModelSerializer):
            parent = serializers.SlugRelatedField(
                allow_null=False, default=getattr(Organization, 'objects').get(name='ROOT'),
                queryset=getattr(Organization, 'objects').filter(deleted=False),
                slug_field='name'
            )
            parent_caption = serializers.SlugRelatedField(
                read_only=True,
                source='parent',
                slug_field='caption'
            )

            @staticmethod
            def validate_parent(value):
                root = getattr(Organization, 'objects').get(name='ROOT')

                checked = set()
                cur = value

                while cur is not None and cur.id not in checked:
                    if cur.id == root.id:
                        return value
                    checked.add(cur.id)
                    cur = cur.parent

                raise serializers.ValidationError('Organization unreachable.')

            class Meta:
                model = Organization
                exclude = ('id', 'categories', )
                read_only_fields = ('number_organizations',
                                    'number_students',
                                    'number_teachers',
                                    'number_admins',
                                    'number_course_meta',
                                    'number_courses',
                                    'number_course_groups',
                                    'number_categories',
                                    'number_problems',
                                    'creator', 'create_time', 'updater', 'update_time')

        # 机构
        class List(serializers.ModelSerializer):
            parent = serializers.SlugRelatedField(
                read_only=True, allow_null=False, default=getattr(Organization, 'objects').get(name='ROOT'),
                slug_field='name'
            )
            parent_caption = serializers.SlugRelatedField(
                read_only=True,
                source='parent',
                slug_field='caption'
            )

            class Meta:
                model = Organization
                exclude = ('id', 'categories', )
                read_only_fields = ('number_organizations',
                                    'number_students',
                                    'number_teachers',
                                    'number_admins',
                                    'number_course_meta',
                                    'number_courses',
                                    'number_course_groups',
                                    'number_categories',
                                    'number_problems',
                                    'parent', 'parent_caption'
                                    'creator', 'create_time', 'updater', 'update_time')

        # admin - 机构
        class InstanceAdmin(serializers.ModelSerializer):
            parent = serializers.SlugRelatedField(
                allow_null=False, default=getattr(Organization, 'objects').get(name='ROOT'),
                queryset=getattr(Organization, 'objects').filter(deleted=False),
                slug_field='name'
            )
            parent_caption = serializers.SlugRelatedField(
                read_only=True,
                source='parent',
                slug_field='caption'
            )

            def validate_parent(self, value):
                root = getattr(Organization, 'objects').get(name='ROOT')

                checked = set()
                cur = value
                checked.add(self.instance.id)

                while cur is not None and cur.id not in checked:
                    if cur.id == root.id:
                        return value
                    checked.add(cur.id)
                    cur = cur.parent

                raise serializers.ValidationError('Organization unreachable.')

            class Meta:
                model = Organization
                exclude = ('id', 'categories', )
                read_only_fields = ('name',
                                    'number_organizations',
                                    'number_students',
                                    'number_teachers',
                                    'number_admins',
                                    'number_course_meta',
                                    'number_courses',
                                    'number_course_groups',
                                    'number_categories',
                                    'number_problems',
                                    'creator', 'create_time', 'updater', 'update_time')

        # 机构
        class Instance(serializers.ModelSerializer):
            parent = serializers.SlugRelatedField(
                read_only=True, allow_null=False, default=getattr(Organization, 'objects').get(name='ROOT'),
                slug_field='name'
            )
            parent_caption = serializers.SlugRelatedField(
                read_only=True,
                source='parent',
                slug_field='caption'
            )

            class Meta:
                model = Organization
                exclude = ('id', 'categories', )
                read_only_fields = ('name',
                                    'number_organizations',
                                    'number_students',
                                    'number_teachers',
                                    'number_admins',
                                    'number_course_meta',
                                    'number_courses',
                                    'number_course_groups',
                                    'number_categories',
                                    'number_problems',
                                    'parent', 'parent_caption',
                                    'creator', 'create_time', 'updater', 'update_time')


class CategorySerializers(object):
    class Category(object):
        # admin - 机构正在使用的题库
        class ListOrgAdmin(serializers.ModelSerializer):
            category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')
            title = serializers.SlugRelatedField(slug_field='title', read_only=True, source='category')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True, source='category')
            source = serializers.SlugRelatedField(slug_field='source', read_only=True, source='category')
            author = serializers.SlugRelatedField(slug_field='author', read_only=True, source='category')
            number_problem = serializers.SlugRelatedField(slug_field='number_problem', read_only=True,
                                                          source='category')

            def create(self, validated_data):
                organization = validated_data['organization']  # 得到parent的org
                goal_category_id = validated_data['category'].id  # 欲添加的题库的id
                available_id = [i['id'] for i in organization.available_categories().values('id')]
                if goal_category_id not in available_id:
                    # 如果想要添加的题库不在可添加的题库内
                    raise ValidationError('category is not available.')
                elif organization.categories.filter(id=goal_category_id).exists():
                    raise ValidationError('category exists.')
                validated_data = dict_sub(validated_data, 'category', 'organization')
                return super().create(validated_data)

            class Meta:
                model = OrganizationCategoryRelation
                fields = ('id', 'category_id', 'title', 'introduction', 'source', 'author', 'number_problem')
                read_only_fields = _RESOURCE_READONLY

        # admin - 机构正在使用的题库
        class InstanceOrgAdmin(serializers.ModelSerializer):
            category_id = serializers.PrimaryKeyRelatedField(read_only=True, source='category')
            title = serializers.SlugRelatedField(slug_field='title', read_only=True, source='category')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True, source='category')
            source = serializers.SlugRelatedField(slug_field='source', read_only=True, source='category')
            author = serializers.SlugRelatedField(slug_field='author', read_only=True, source='category')
            number_problem = serializers.SlugRelatedField(slug_field='number_problem', read_only=True,
                                                          source='category')

            class Meta:
                model = OrganizationCategoryRelation
                fields = ('id', 'category_id', 'title', 'introduction', 'source', 'author', 'number_problem')
                read_only_fields = _RESOURCE_READONLY

        # admin - 机构可用的题库
        class ListAvailableOrgAdmin(serializers.ModelSerializer):
            class Meta:
                model = Category
                exclude = ('problems',)

    class CourseMetaCategory(object):
        # 课程基类正在使用的题库
        class List(serializers.ModelSerializer):
            category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')
            title = serializers.SlugRelatedField(slug_field='title', read_only=True, source='category')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True, source='category')
            source = serializers.SlugRelatedField(slug_field='source', read_only=True, source='category')
            author = serializers.SlugRelatedField(slug_field='author', read_only=True, source='category')
            number_problem = serializers.SlugRelatedField(slug_field='number_problem', read_only=True,
                                                          source='category')

            def create(self, validated_data):
                course_meta = validated_data['course_meta']  # 得到parent的meta
                goal_category_id = validated_data['category'].id  # 欲添加的题库的id
                available_id = [i['id'] for i in course_meta.available_categories().values('id')]
                if goal_category_id not in available_id:
                    # 如果想要添加的题库不在可添加的题库内
                    raise ValidationError('category is not available.')
                elif course_meta.categories.filter(id=goal_category_id).exists():
                    raise ValidationError('category exists.')
                validated_data = dict_sub(validated_data, 'category', 'course_meta')
                validated_data['organization'] = course_meta.organization
                return super().create(validated_data)

            class Meta:
                model = CourseMetaCategoryRelation
                fields = ('id', 'category_id', 'title', 'introduction', 'source', 'author', 'number_problem')
                read_only_fields = _RESOURCE_READONLY

        # 课程基类正在使用的题库
        class Instance(serializers.ModelSerializer):
            category_id = serializers.PrimaryKeyRelatedField(read_only=True, source='category')
            title = serializers.SlugRelatedField(slug_field='title', read_only=True, source='category')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True, source='category')
            source = serializers.SlugRelatedField(slug_field='source', read_only=True, source='category')
            author = serializers.SlugRelatedField(slug_field='author', read_only=True, source='category')
            number_problem = serializers.SlugRelatedField(slug_field='number_problem', read_only=True,
                                                          source='category')

            class Meta:
                model = CourseMetaCategoryRelation
                fields = ('id', 'category_id', 'title', 'introduction', 'source', 'author', 'number_problem')
                read_only_fields = _RESOURCE_READONLY

        # 课程基类可用的题库
        class ListAvailable(serializers.ModelSerializer):
            class Meta:
                model = Category
                exclude = ('problems',)


class CourseSerializers(object):
    class CourseMeta(object):
        # 机构下的课程基类
        class ListOrg(serializers.ModelSerializer):
            class Meta:
                model = CourseMeta
                exclude = ('organization', 'categories')
                read_only_fields = ('number_courses',
                                    'number_course_groups',
                                    'number_categories',
                                    'number_problems',
                                    'creator', 'updater', 'create_time', 'update_time',)

        class InstanceOrg(serializers.ModelSerializer):
            class Meta:
                model = CourseMeta
                exclude = ('organization', 'categories')
                read_only_fields = ('number_courses',
                                    'number_course_groups',
                                    'number_categories',
                                    'number_problems',
                                    'creator', 'updater', 'create_time', 'update_time',)

    class Course(object):
        class List(serializers.ModelSerializer):
            meta = serializers.PrimaryKeyRelatedField(read_only=True)
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='meta')

            def create(self, validated_data):
                unit = CourseUnit.objects.create(type='COURSE')
                meta = validated_data['meta']
                unit.save()
                validated_data['course_unit'] = unit
                validated_data['cid'] = unit.id
                validated_data['organization'] = meta.organization
                return super().create(validated_data)

            class Meta:
                model = Course
                exclude = ('organization', 'course_unit', 'teachers', 'students',)
                read_only_fields = ('cid', 'meta', 'meta_caption', 'creator', 'updater', 'create_time', 'update_time',)

        class Instance(serializers.ModelSerializer):
            meta = serializers.PrimaryKeyRelatedField(read_only=True)
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='meta')

            class Meta:
                model = Course
                exclude = ('organization', 'course_unit', 'teachers', 'students',)
                read_only_fields = ('cid', 'meta', 'meta_caption', 'creator', 'updater', 'create_time', 'update_time',)

    class CourseGroup(object):
        class List(serializers.ModelSerializer):
            meta = serializers.PrimaryKeyRelatedField(read_only=True)
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='meta')

            def create(self, validated_data):
                unit = CourseUnit.objects.create(type='GROUP')
                meta = validated_data['meta']
                unit.save()
                validated_data['course_unit'] = unit
                validated_data['gid'] = unit.id
                validated_data['organization'] = meta.organization
                return super().create(validated_data)

            class Meta:
                model = CourseGroup
                exclude = ('organization', 'course_unit', 'teachers', 'courses',)
                read_only_fields = ('gid', 'meta', 'meta_caption', 'creator', 'updater', 'create_time', 'update_time',)

        class Instance(serializers.ModelSerializer):
            meta = serializers.PrimaryKeyRelatedField(read_only=True)
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='meta')

            class Meta:
                model = CourseGroup
                exclude = ('organization', 'course_unit', 'teachers', 'courses',)
                read_only_fields = ('gid', 'meta', 'meta_caption', 'creator', 'updater', 'create_time', 'update_time',)

    class CourseCourseGroup(object):
        # 课程所属的课程组
        class List(serializers.ModelSerializer):
            gid = serializers.SlugRelatedField(queryset=CourseGroup.objects.all(), slug_field='gid',
                                               source='course_group')
            caption = serializers.SlugRelatedField(slug_field='caption', read_only=True, source='course_group')
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='meta_caption',
                                                        source='course_group')
            meta = serializers.PrimaryKeyRelatedField(read_only=True, source='course_group')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True, source='course_group')

            def create(self, validated_data):
                course = validated_data['course']
                course_group = validated_data['course_group']
                available_course_groups = course.available_course_groups()
                if course_group not in available_course_groups:
                    raise ValidationError('course group is not available.')
                elif course.course_groups.filter(gid=course_group.gid).exists():
                    raise ValidationError('course group exists.')
                instance = super().create(validated_data)
                return instance

            class Meta:
                model = CourseGroupRelation
                read_only_fields = ('id',) + _RESOURCE_READONLY
                exclude = ('course', 'course_group')

        # 课程所属的课程组
        class Instance(serializers.ModelSerializer):
            gid = serializers.SlugRelatedField(read_only=True, slug_field='gid', source='course_group')
            caption = serializers.SlugRelatedField(slug_field='caption', read_only=True, source='course_group')
            meta = serializers.PrimaryKeyRelatedField(read_only=True, source='course_group')
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='meta_caption',
                                                        source='course_group')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True,
                                                        source='course_group')

            class Meta:
                model = CourseGroupRelation
                read_only_fields = ('id',) + _RESOURCE_READONLY
                exclude = ('course', 'course_group')

        # 课程可以加入的课程组
        class ListAvailable(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='meta')

            class Meta:
                model = CourseGroup
                exclude = ('course_unit', 'courses', 'teachers', 'organization')
                read_only_fields = (
                    'creator', 'updater', 'create_time', 'update_time',
                )

    class CourseGroupCourse(object):
        # 课程组所拥有的课程
        class List(serializers.ModelSerializer):
            cid = serializers.SlugRelatedField(queryset=Course.objects.all(), slug_field='cid', source='course')
            caption = serializers.SlugRelatedField(slug_field='caption', read_only=True, source='course')
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='meta_caption', source='course')
            meta = serializers.PrimaryKeyRelatedField(read_only=True, source='course')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True, source='course')
            start_time = serializers.SlugRelatedField(slug_field='start_time', read_only=True, source='course')
            end_time = serializers.SlugRelatedField(slug_field='end_time', read_only=True, source='course')

            def create(self, validated_data):
                course = validated_data['course']
                course_group = validated_data['course_group']
                available_courses = course_group.available_courses()
                if course not in available_courses:
                    raise ValidationError('course is not available.')
                elif course_group.courses.filter(cid=course.cid).exists():
                    raise ValidationError('course exists.')
                instance = super().create(validated_data)
                return instance

            class Meta:
                model = CourseGroupRelation
                read_only_fields = ('id',) + _RESOURCE_READONLY
                exclude = ('course', 'course_group')

        # 课程组所拥有的课程
        class Instance(serializers.ModelSerializer):
            cid = serializers.SlugRelatedField(read_only=True, slug_field='cid', source='course')
            caption = serializers.SlugRelatedField(slug_field='caption', read_only=True, source='course')
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='meta_caption', source='course')
            meta = serializers.PrimaryKeyRelatedField(read_only=True, source='course')
            introduction = serializers.SlugRelatedField(slug_field='introduction', read_only=True, source='course')
            start_time = serializers.SlugRelatedField(slug_field='start_time', read_only=True, source='course')
            end_time = serializers.SlugRelatedField(slug_field='end_time', read_only=True, source='course')

            class Meta:
                model = CourseGroupRelation
                read_only_fields = ('id',) + _RESOURCE_READONLY
                exclude = ('course', 'course_group')

        # 课程组可以添加的课程
        class ListAvailable(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='meta')

            class Meta:
                model = Course
                exclude = ('course_unit', 'students', 'teachers', 'organization')
                read_only_fields = (
                    'creator', 'updater', 'create_time', 'update_time',
                )


class MissionSerializers(object):
    class Mission(object):
        class List(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(slug_field='caption', source='course_meta', read_only=True)
            start_time = serializers.DateTimeField()
            end_time = serializers.DateTimeField()
            config = serializers.JSONField(write_only=True, required=False, allow_null=True)
            mode = serializers.CharField(write_only=True)

            def validate(self, attrs):
                if attrs['start_time'] >= attrs['end_time']:
                    raise ValidationError('Start time must be early than End time.')
                mode = attrs['mode']
                if mode == 'CUSTOM':  # 要求自定义的情况下必须提供config信息
                    if 'config' in attrs:
                        config = attrs['config']  # 这个东西需要做严格的验证。
                        message = Mission.validate_config(config)
                        if message is not None:
                            raise ValidationError(message)
                    else:
                        raise ValidationError('You must give the config if you want custom.')
                else:  # 采用自定义模式下，config的信息不管用，直接从默认配置里拉取
                    attrs['config'] = Mission.default_mode_config(mode)
                return attrs

            def create(self, validated_data):
                meta = validated_data['course_meta']
                validated_data['organization'] = meta.organization
                return super().create(validated_data)

            class Meta:
                model = Mission
                exclude = ('organization', 'problems')
                read_only_fields = ('id', 'course_meta') + _RESOURCE_READONLY

        class Instance(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(slug_field='caption', source='course_meta', read_only=True)
            start_time = serializers.DateTimeField()
            end_time = serializers.DateTimeField()
            config = serializers.JSONField(required=False, allow_null=True)

            def validate(self, attrs):
                obj = self.instance
                start_time = attrs['start_time'] if 'start_time' in attrs else obj.start_time
                end_time = attrs['end_time'] if 'end_time' in attrs else obj.end_time
                if start_time >= end_time:
                    raise ValidationError('Start time must be early than End time.')
                if 'mode' in attrs:
                    mode = attrs['mode']
                    if mode == 'CUSTOM':  # 要求自定义的情况下必须提供config信息
                        if 'config' in attrs:
                            config = attrs['config']  # 这个东西需要做严格的验证。
                            message = Mission.validate_config(config)
                            if message is not None:
                                raise ValidationError(message)
                        else:
                            raise ValidationError('You must give the config if you want custom.')
                    else:  # 采用自定义模式下，config的信息不管用，直接从默认配置里拉取
                        attrs['config'] = Mission.default_mode_config(mode)
                return attrs

            class Meta:
                model = Mission
                exclude = ('organization', 'problems')
                read_only_fields = ('id', 'course_meta') + _RESOURCE_READONLY

    class MissionMissionGroup(object):
        # 任务组所拥有的任务
        class List(serializers.ModelSerializer):
            mission_id = serializers.PrimaryKeyRelatedField(queryset=Mission.objects.all(), source='mission')
            caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='mission')
            course_meta = serializers.PrimaryKeyRelatedField(read_only=True, source='mission')
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='meta_caption', source='mission')
            start_time = serializers.SlugRelatedField(read_only=True, slug_field='start_time', source='mission')
            end_time = serializers.SlugRelatedField(read_only=True, slug_field='end_time', source='mission')

            def create(self, validated_data):
                mission = validated_data['mission']
                mission_group = validated_data['mission_group']
                available_missions = mission_group.available_missions()
                if mission not in available_missions:
                    raise ValidationError('mission is not available.')
                elif mission_group.missions.filter(id=mission.id).exists():
                    raise ValidationError('mission exists.')
                instance = super().create(validated_data)
                return instance

            class Meta:
                model = MissionGroupRelation
                exclude = ('mission', 'mission_group')
                read_only_fields = ('id',) + _RESOURCE_READONLY

        # 任务组所拥有的任务
        class Instance(serializers.ModelSerializer):
            mission_id = serializers.PrimaryKeyRelatedField(read_only=True, source='mission')
            caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='mission')
            course_meta = serializers.PrimaryKeyRelatedField(read_only=True, source='mission')
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='meta_caption', source='mission')
            start_time = serializers.SlugRelatedField(read_only=True, slug_field='start_time', source='mission')
            end_time = serializers.SlugRelatedField(read_only=True, slug_field='end_time', source='mission')

            class Meta:
                model = MissionGroupRelation
                exclude = ('mission', 'mission_group')
                read_only_fields = ('id',) + _RESOURCE_READONLY

        # 任务组可添加的任务
        class ListAvailable(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(read_only=True, slug_field='caption', source='course_meta')

            class Meta:
                model = Mission
                exclude = ('problems', 'organization')
                read_only_fields = ('id',) + _RESOURCE_READONLY

    class MissionGroup(object):
        # 课程下属的任务组
        class ListCourse(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(slug_field='caption', source='course_meta', read_only=True)

            def create(self, validated_data):
                unit = validated_data['course_unit']
                if unit.type == 'GROUP':
                    meta = unit.course_group.meta
                else:
                    meta = unit.course.meta
                validated_data['course_meta'] = meta
                validated_data['organization'] = meta.organization
                return super().create(validated_data)

            class Meta:
                model = MissionGroup
                exclude = ('organization', 'missions', 'course_unit')
                read_only_fields = ('id', 'course_meta') + _RESOURCE_READONLY

        # 课程组下属的任务组
        class ListCourseGroup(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(slug_field='caption', source='course_meta', read_only=True)

            def create(self, validated_data):
                unit = validated_data['course_unit']
                if unit.type == 'GROUP':
                    meta = unit.course_group.meta
                else:
                    meta = unit.course.meta
                validated_data['course_meta'] = meta
                validated_data['organization'] = meta.organization
                return super().create(validated_data)

            class Meta:
                model = MissionGroup
                exclude = ('organization', 'missions', 'course_unit')
                read_only_fields = ('id', 'course_meta') + _RESOURCE_READONLY

        # 任务组
        class Instance(serializers.ModelSerializer):
            meta_caption = serializers.SlugRelatedField(slug_field='caption', source='course_meta', read_only=True)

            class Meta:
                model = MissionGroup
                exclude = ('organization', 'missions', 'course_unit')
                read_only_fields = ('id', 'course_meta') + _RESOURCE_READONLY


class ProblemSerializers(object):
    class ProblemList(serializers.ModelSerializer):
        class Meta:
            model = Problem
            exclude = ('number_invalid_word',)

    class ProblemInstance(serializers.ModelSerializer):
        class Limit(serializers.ModelSerializer):
            class Meta:
                model = Limit
                exclude = ('problem',)

        limit = Limit(read_only=True, many=True, source='get_limits')

        class Meta:
            model = Problem
            exclude = ('number_invalid_word',)

    class Environment(serializers.ModelSerializer):
        class Meta:
            model = Environment
            fields = ('id', 'name')


class ProblemRelationSerializers(object):
    class List(serializers.ModelSerializer):
        problem_id = serializers.PrimaryKeyRelatedField(read_only=True, source='problem')
        title = serializers.SlugRelatedField(read_only=True, source='problem', slug_field='title')
        introduction = serializers.SlugRelatedField(read_only=True, source='problem', slug_field='introduction')
        source = serializers.SlugRelatedField(read_only=True, source='problem', slug_field='source')
        author = serializers.SlugRelatedField(read_only=True, source='problem', slug_field='author')

        def create(self, validated_data):
            problem = validated_data['problem']
            mission = validated_data['mission']
            available_problems = mission.available_problems()
            if problem not in available_problems:
                raise ValidationError('problem is not available.')
            elif mission.problems.filter(id=problem.id).exists():
                raise ValidationError('problem exists.')
            instance = super().create(validated_data)
            return instance

        class Meta:
            model = MissionProblemRelation
            exclude = ('mission', )
            read_only_fields = ('id',) + _RESOURCE_READONLY

    class Instance(serializers.ModelSerializer):
        problem = ProblemSerializers.ProblemInstance(read_only=True)

        class Meta:
            model = MissionProblemRelation
            exclude = ('mission', )
            read_only_fields = ('id',) + _RESOURCE_READONLY

    class ListAvailable(serializers.ModelSerializer):
        category = serializers.SlugRelatedField(slug_field='title', read_only=True)
        directory = serializers.ListField(read_only=True)
        problem = ProblemSerializers.ProblemList(read_only=True)

        class Meta:
            model = CategoryProblemRelation
            fields = ('id', 'category', 'directory', 'problem')


class SubmissionSerializers(object):
    class List(serializers.ModelSerializer):
        problem = serializers.PrimaryKeyRelatedField(queryset=Problem.objects.all())
        problem_title = serializers.SlugRelatedField(read_only=True, slug_field='title', source='problem')
        environment = serializers.PrimaryKeyRelatedField(queryset=Environment.objects.all())
        env_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='environment')
        user = serializers.SlugRelatedField(read_only=True, slug_field='username')
        user_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='user')
        code = serializers.CharField(write_only=True)

        status_word = serializers.CharField(read_only=True, source='get_status_display')

        def create(self, validated_data):
            # 需要做范围限制判定。
            # 1 题目限制在mission的范围内
            # 3 编程环境限制在题目范围内
            # 之后手动生成提交信息
            # 提交到server端
            # 生成submission实例
            profile = validated_data['profile']
            problem = validated_data['problem']
            mission = validated_data['mission']
            env = validated_data['environment']
            code = validated_data['code']
            user = CLIENT_SETTINGS['username']
            if problem not in mission.problems.all():
                raise ValidationError('problem is not available.')
            if env not in problem.get_environments():
                raise ValidationError('environment is not available.')
            submission_json = {
                'problem_id': problem.id,
                'env_id': env.id,
                'code': code,
                'user': user,
                'contest': '%s' % (mission.id,),
            }
            result = submit(submission_json)
            submission = Submission(
                sid=result['id'],
                problem=problem,
                environment=env,
                time=result['time'],
                memory=result['memory'],
                length=result['length'],
                user=profile,
                status=result['status'],
                finished=result['finished'],
                submit_time=result['submit_time'],
                update_time=result['update_time'],
                ip=profile.ip,
                mission=mission,
                organization=mission.organization
            )
            submission.save()
            compile_info = CompileInfo(submission=submission)
            compile_info.save()
            test_data_status = TestDataStatus(submission=submission, status={})
            test_data_status.save()
            submission_code = SubmissionCode(submission=submission, code={})
            submission_code.save()
            return submission

        class Meta:
            model = Submission
            read_only_fields = ('id', 'time', 'length', 'memory', 'status', 'finished', 'score',
                                'submit_time', 'update_time', 'ip')
            exclude = ('organization', 'mission', 'sid')

    class Instance(serializers.ModelSerializer):
        problem = serializers.PrimaryKeyRelatedField(read_only=True)
        problem_title = serializers.SlugRelatedField(read_only=True, slug_field='title', source='problem')
        environment = serializers.PrimaryKeyRelatedField(read_only=True)
        env_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='environment')
        user = serializers.SlugRelatedField(read_only=True, slug_field='username')
        user_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='user')

        code = serializers.SlugRelatedField(read_only=True, slug_field='code')
        compile_info = serializers.SlugRelatedField(read_only=True, slug_field='info')
        test_data_status = serializers.SlugRelatedField(read_only=True, slug_field='status')

        status_word = serializers.CharField(read_only=True, source='get_status_display')

        class Meta:
            model = Submission
            read_only_fields = ('id', 'sid', 'time', 'length', 'memory', 'status', 'finished', 'score',
                                'submit_time', 'update_time', 'ip')
            exclude = ('organization', 'mission')


class RankSerializers(object):
    class Instance(serializers.ModelSerializer):
        mission_mode = serializers.SlugRelatedField(read_only=True, source='mission', slug_field='mode')
        mission_config = serializers.SlugRelatedField(read_only=True, source='mission', slug_field='config')

        class Meta:
            model = Rank
            exclude = ('organization', 'mission', 'user')
            read_only_fields = ('sub_count', 'solved', 'penalty', 'sum_score', 'result') + _RESOURCE_READONLY
