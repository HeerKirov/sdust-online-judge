# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def check_init_user():
    from .models import User, UserProfile, IdentityChoices
    from config import INIT_USER_SETTINGS
    print('Checking initial user ...', end='')
    if INIT_USER_SETTINGS is None:
        print(' Skipped')
    elif User.objects.filter(username=INIT_USER_SETTINGS['username']).exists():
        print(' Done')
    else:
        print(' Initial user does not exist')
        print('-- Creating initial user ...')
        user = User(username=INIT_USER_SETTINGS['username'])
        user.set_password(INIT_USER_SETTINGS['password'])
        user.is_staff = True
        user.save()
        profile = UserProfile(user=user, username=INIT_USER_SETTINGS['username'], is_staff=True)
        if 'name' in INIT_USER_SETTINGS:
            profile.name = INIT_USER_SETTINGS['name']
        if 'sex' in INIT_USER_SETTINGS and INIT_USER_SETTINGS['sex'] in UserProfile.SEX_CHOICES:
            profile.sex = INIT_USER_SETTINGS['sex']
        if 'phone' in INIT_USER_SETTINGS:
            profile.phone = INIT_USER_SETTINGS['phone']
        if 'email' in INIT_USER_SETTINGS:
            profile.email = INIT_USER_SETTINGS['email']
        if 'github' in INIT_USER_SETTINGS:
            profile.github = INIT_USER_SETTINGS['github']
        if 'qq' in INIT_USER_SETTINGS:
            profile.qq = INIT_USER_SETTINGS['qq']
        if 'wechat' in INIT_USER_SETTINGS:
            profile.wechat = INIT_USER_SETTINGS['wechat']
        if 'blog' in INIT_USER_SETTINGS:
            profile.blog = INIT_USER_SETTINGS['blog']
        if 'introduction' in INIT_USER_SETTINGS:
            profile.introduction = INIT_USER_SETTINGS['introduction']
        profile.identities = {IdentityChoices.root: True}
        profile.save()
        print('--- Done')


def check_root_organization():
    from .models import Organization
    print('Checking root organization ...', end='')
    if getattr(Organization, 'objects').filter(name='ROOT').exists():
        print(' Done')
    else:
        print(' Root organization does not exist')
        org = Organization(name='ROOT',
                           caption='Root Organization',
                           introduction='Root of all organizations.',
                           parent=None)
        org.save()
        print('--- Done')


def callback(sender, **kwargs):
    # 去掉PyCharm的坑爹Warning ---------
    if sender:
        pass
    if kwargs:
        pass
    # ---------------------------------
    check_init_user()
    check_root_organization()


class RestApiConfig(AppConfig):
    name = 'rest_api'

    def ready(self):
        post_migrate.connect(callback, sender=self)
