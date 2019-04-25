# Generated by Django 2.0.5 on 2019-04-16 05:56

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnsiblePlaybook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(auto_created=True, default=uuid.uuid4, editable=False, max_length=50, unique=True)),
                ('file_name', models.FileField(upload_to='upload/playbooks/%Y%m%d')),
                ('file_size', models.CharField(max_length=30, verbose_name='文件大小')),
                ('md5', models.CharField(max_length=30, verbose_name='MD5值')),
                ('description', models.TextField(blank=True, null=True, verbose_name='介绍')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_shared', models.BooleanField(default=False, verbose_name='是否共享')),
            ],
            options={
                'verbose_name_plural': 'ansible playbook',
                'verbose_name': 'ansible playbook',
            },
        ),
        migrations.CreateModel(
            name='AnsibleScript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(auto_created=True, default=uuid.uuid4, editable=False, max_length=50, unique=True)),
                ('file_name', models.FileField(upload_to='upload/scripts/%Y%m%d')),
                ('detail', models.TextField(verbose_name='脚本内容')),
                ('file_size', models.CharField(max_length=30, verbose_name='文件大小')),
                ('md5', models.CharField(max_length=30, verbose_name='MD5值')),
                ('description', models.TextField(blank=True, null=True, verbose_name='介绍')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_shared', models.BooleanField(default=False, verbose_name='是否共享')),
            ],
            options={
                'verbose_name_plural': 'ansible脚本',
                'verbose_name': 'ansible脚本',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('uuid', models.CharField(auto_created=True, default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('file_name', models.FileField(upload_to='upload/files/%Y%m%d')),
                ('file_size', models.CharField(max_length=30, verbose_name='文件大小')),
                ('md5', models.CharField(max_length=30, verbose_name='MD5值')),
                ('description', models.TextField(blank=True, null=True, verbose_name='介绍')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_shared', models.BooleanField(default=False, verbose_name='是否共享')),
            ],
        ),
    ]