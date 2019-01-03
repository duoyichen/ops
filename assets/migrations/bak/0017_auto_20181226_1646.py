# Generated by Django 2.1.4 on 2018-12-26 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0016_auto_20181226_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depart',
            name='c_time',
            field=models.DateTimeField(auto_now=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='depart',
            name='name',
            field=models.CharField(max_length=32, verbose_name='部门名称'),
        ),
        migrations.AlterField(
            model_name='empployee',
            name='depart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.depart', verbose_name='所属部门'),
        ),
        migrations.AlterField(
            model_name='empployee',
            name='m_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='empployee',
            name='name',
            field=models.CharField(max_length=32, verbose_name='员工姓名'),
        ),
    ]
