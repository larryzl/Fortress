# Generated by Django 2.1.8 on 2019-04-18 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_serversoft'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='soft',
        ),
    ]