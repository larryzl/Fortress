# Generated by Django 2.0.5 on 2019-04-16 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20190416_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverlog',
            name='detail',
            field=models.CharField(blank=True, max_length=30, verbose_name='详细字段'),
        ),
    ]