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

auth_gid = [(1001, u"运维部"), (1002, u"架构部"), (1003, u"研发部"), (1004, u"测试部")]

class Department(models.Model):
    '''
    部门表
    '''
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'部门名称',unique=True)
    description = models.TextField(verbose_name=u"介绍", blank=True, null=True)
    department_admin = models.ForeignKey('CustomUser',blank=True,null=True,related_name='user',verbose_name='部门管理员',on_delete=models.SET_NULL)
    desc_gid = models.IntegerField(verbose_name=u"部门组", choices=auth_gid, blank=True, null=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"部门"
        verbose_name_plural = verbose_name

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)




class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    uuid = models.CharField(unique=True,auto_created=True,default=uuid.uuid4,editable=False,max_length=50,primary_key=True)
    email = models.EmailField(_(u'邮箱'), max_length=254, unique=True)
    username = models.CharField(_(u'用户名'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    department = models.ForeignKey(Department, blank=True, null=True,related_name='users', verbose_name="部门",on_delete=models.SET_NULL)
    mobile = models.CharField(_(u'手机'), max_length=30, blank=False,
                              validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                    _('Enter a valid mobile number.'),
                                                                    'invalid')])
    session_key = models.CharField(max_length=60, blank=True, null=True, verbose_name=u"session_key")
    user_key = models.TextField(blank=True, null=True, verbose_name=u"用户登录key")
    menu_status = models.BooleanField(default=False, verbose_name=u'用户菜单状态')
    user_active = models.BooleanField(verbose_name=u'设置密码状态', default=0)

    # uuid = models.CharField(default=uuid.uuid3(uuid.NAMESPACE_DNS,str(hashlib.md5(str(time.time()).encode('utf-8'))) + str("".join(random.choice("1234567890abcefg")))), max_length=64,unique=True)

    # Admin
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])