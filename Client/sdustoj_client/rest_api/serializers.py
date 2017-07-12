# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import *
from .utils import dict_sub
from rest_framework.serializers import ValidationError

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
                if it == IdentityChoices.edu_admin:
                    ret[it] = True
            return ret

        def create(self, validated_data):
            organization = validated_data['organization']
            profile = UserProfile.create_profile(**validated_data)
            edu_admin = EduAdmin(
                user=profile.user,
                profile=profile,
                username=profile.username,
                organization=organization
            )
            edu_admin.save()
            profile.update_identities()
            return profile

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

    # admin - 教务管理员
    class InstanceEduAdmin(serializers.ModelSerializer):
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
                if it == IdentityChoices.edu_admin:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
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


class OrgUserSerializers(object):
    # 教务管理员
    class ListEduAdmin(serializers.ModelSerializer):
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True,
                                           read_only=True)

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

    # 教务管理员
    class InstanceEduAdmin(serializers.ModelSerializer):
        identities = serializers.ListField(child=serializers.CharField(),
                                           source='get_identities',
                                           allow_null=True,
                                           allow_empty=True,
                                           read_only=True)

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

    # 教师
    class ListTeacher(serializers.ModelSerializer):
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
                if it == IdentityChoices.teacher:
                    ret[it] = True
            return ret

        def create(self, validated_data):
            organization = validated_data['organization']
            profile = UserProfile.create_profile(**validated_data)
            teacher = Teacher(
                user=profile.user,
                profile=profile,
                username=profile.username,
                organization=organization
            )
            teacher.save()
            profile.update_identities()
            return profile

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

    # 教师
    class InstanceTeacher(serializers.ModelSerializer):
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
                if it == IdentityChoices.teacher:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
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

    # 学生
    class ListStudent(serializers.ModelSerializer):
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
                if it == IdentityChoices.student:
                    ret[it] = True
            return ret

        def create(self, validated_data):
            organization = validated_data['organization']
            profile = UserProfile.create_profile(**validated_data)
            student = Student(
                user=profile.user,
                profile=profile,
                username=profile.username,
                organization=organization
            )
            student.save()
            profile.update_identities()
            return profile

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
            read_only_fields = (
                'creator', 'updater', 'create_time', 'update_time',
                'last_login', 'ip'
            )

    # 学生
    class InstanceStudent(serializers.ModelSerializer):
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
                if it == IdentityChoices.student:
                    ret[it] = True
            return ret

        class Meta:
            model = UserProfile
            exclude = ('user', 'courses', 'is_staff')
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


class OrganizationSerializers(object):
    class Organization(object):
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
        class ListOrgAdmin(serializers.ModelSerializer):

            class ListAdmin(serializers.ModelSerializer):
                class Meta:
                    model = Category
                    exclude = ('problems',)
                    read_only_fields = ('title', 'introduction', 'source', 'author',
                                        'number_problem')

            category = ListAdmin(read_only=True)
            category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')

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
                fields = ('id', 'category', 'category_id')
                read_only_fields = _RESOURCE_READONLY

        class InstanceOrgAdmin(serializers.ModelSerializer):
            class InstanceAdmin(serializers.ModelSerializer):
                problems = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

                class Meta:
                    model = Category
                    fields = ('problems',)
                    read_only_fields = ('title', 'introduction', 'source', 'author',
                                        'number_problem')
            category = InstanceAdmin(read_only=True)

            class Meta:
                model = OrganizationCategoryRelation
                fields = ('id', 'category')
                read_only_fields = _RESOURCE_READONLY

        class ListAvailableOrgAdmin(serializers.ModelSerializer):
            class Meta:
                model = Category
                exclude = ('problems',)
