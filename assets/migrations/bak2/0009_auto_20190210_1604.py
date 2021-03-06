# Generated by Django 2.1.5 on 2019-02-10 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0008_auto_20190117_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='端口名称')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='IP_Port')),
                ('status', models.SmallIntegerField(choices=[(0, '未分配'), (1, '已分配'), (2, '未知')], default=0, verbose_name='端口状态')),
                ('customer', models.CharField(blank=True, max_length=64, null=True, verbose_name='客户名称')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '端口表',
                'verbose_name_plural': '端口表',
                'ordering': ['-port_name'],
            },
        ),
        migrations.RenameModel(
            old_name='IP_Asset',
            new_name='IPAsset',
        ),
        migrations.RenameModel(
            old_name='Server_Asset',
            new_name='ServerAsset',
        ),
        migrations.RenameModel(
            old_name='Network_Asset',
            new_name='NetworkAsset',
        ),
        migrations.AddField(
            model_name='port',
            name='port_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='port_net', to='assets.NetworkAsset', verbose_name='所属IP段'),
        ),
    ]
