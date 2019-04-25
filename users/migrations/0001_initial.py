# Generated by Django 2.0.5 on 2019-04-16 05:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('uuid', models.CharField(auto_created=True, default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='用户名')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('mobile', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+()-]+$', 'Enter a valid mobile number.', 'invalid')], verbose_name='手机')),
                ('session_key', models.CharField(blank=True, max_length=60, null=True, verbose_name='session_key')),
                ('user_key', models.TextField(blank=True, null=True, verbose_name='用户登录key')),
                ('menu_status', models.BooleanField(default=False, verbose_name='用户菜单状态')),
                ('user_active', models.BooleanField(default=0, verbose_name='设置密码状态')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('uuid', models.CharField(auto_created=True, default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('department_name', models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='部门名称')),
                ('description', models.TextField(blank=True, null=True, verbose_name='介绍')),
                ('desc_gid', models.IntegerField(blank=True, choices=[(1001, '运维部'), (1002, '架构部'), (1003, '研发部'), (1004, '测试部')], null=True, verbose_name='部门组')),
                ('department_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='部门管理员')),
            ],
            options={
                'verbose_name_plural': '部门',
                'verbose_name': '部门',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='users.Department', verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
