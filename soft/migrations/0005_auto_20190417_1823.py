# Generated by Django 2.1.8 on 2019-04-17 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soft', '0004_auto_20190417_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soft',
            name='soft_icon',
            field=models.ImageField(upload_to='soft_icons/', verbose_name='软件ICON'),
        ),
    ]
