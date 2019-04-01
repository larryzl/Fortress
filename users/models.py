# Create your models here.

from django.db import models
# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
import uuid
from django.contrib.auth.models import BaseUserManager
import random, time
import hashlib


class Department(models.Model):
    '''
    部门表
    '''
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50)
    name = models.CharField(max_length=10,unique=True,blank=False,null=False,verbose_name='部门名称')
    description = models.TextField(verbose_name='介绍',blank=True,null=True)

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given email must be set')
        user = self.model(is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,null=False,blank=False)
    username = models.CharField(_('用户名'), max_length=30, unique=True)
    department = models.ForeignKey(Department,blank=True,null=True,related_name='user_uuid',verbose_name='部门',on_delete=models.SET_NULL)
    key = models.TextField(blank=True, null=True, verbose_name='用户登录key')
    session_key = models.CharField(max_length=60, blank=True, null=True, verbose_name='session_key')
    email = models.EmailField(_('邮箱'), max_length=254, unique=True)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = username
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('username')
        verbose_name_plural = _('username')