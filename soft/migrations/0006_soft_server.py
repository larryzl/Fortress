# Generated by Django 2.1.8 on 2019-04-18 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20190418_0124'),
        ('soft', '0005_auto_20190417_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='soft',
            name='server',
            field=models.ManyToManyField(blank=True, to='assets.Server', verbose_name='主机'),
        ),
    ]
