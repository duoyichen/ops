# Generated by Django 2.1.4 on 2018-12-26 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0015_auto_20181226_1017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='depart',
            options={'verbose_name': '部门', 'verbose_name_plural': '部门'},
        ),
        migrations.AlterModelOptions(
            name='empployee',
            options={'verbose_name': '员工', 'verbose_name_plural': '员工'},
        ),
    ]
