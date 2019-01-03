# Generated by Django 2.1.4 on 2019-01-02 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20181228_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('cpu_count', models.PositiveSmallIntegerField(default=1, verbose_name='物理CPU个数')),
                ('cpu_core_count', models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')),
                ('asset', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'CPU',
                'verbose_name_plural': 'CPU',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, verbose_name='硬盘SN号')),
                ('slot', models.CharField(blank=True, max_length=64, null=True, verbose_name='所在插槽位')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘型号')),
                ('manufacturer', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘制造商')),
                ('capacity', models.FloatField(blank=True, null=True, verbose_name='磁盘容量(GB)')),
                ('interface_type', models.CharField(choices=[('SATA', 'SATA'), ('SAS', 'SAS'), ('SCSI', 'SCSI'), ('SSD', 'SSD'), ('unknown', 'unknown')], default='unknown', max_length=16, verbose_name='接口类型')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset')),
            ],
            options={
                'verbose_name': '硬盘',
                'verbose_name_plural': '硬盘',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='网卡名称')),
                ('model', models.CharField(max_length=128, verbose_name='网卡型号')),
                ('mac', models.CharField(max_length=64, verbose_name='MAC地址')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('net_mask', models.CharField(blank=True, max_length=64, null=True, verbose_name='掩码')),
                ('bonding', models.CharField(blank=True, max_length=64, null=True, verbose_name='绑定地址')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset')),
            ],
            options={
                'verbose_name': '网卡',
                'verbose_name_plural': '网卡',
            },
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(blank=True, max_length=128, null=True, verbose_name='SN号')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='内存型号')),
                ('manufacturer', models.CharField(blank=True, max_length=128, null=True, verbose_name='内存制造商')),
                ('slot', models.CharField(max_length=64, verbose_name='插槽')),
                ('capacity', models.IntegerField(blank=True, null=True, verbose_name='内存大小(GB)')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset')),
            ],
            options={
                'verbose_name': '内存',
                'verbose_name_plural': '内存',
            },
        ),
        migrations.AddField(
            model_name='newassetapprovalzone',
            name='asset_code',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='资产编码'),
        ),
        migrations.AlterField(
            model_name='newassetapprovalzone',
            name='asset_type',
            field=models.CharField(blank=True, choices=[('network_device', '网络设备'), ('server_device', '服务器设备'), ('ip_device', 'IP资源'), ('o_device', '其他设备')], default='server', max_length=64, null=True, verbose_name='资产类型'),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together={('asset', 'slot')},
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together={('asset', 'model', 'mac')},
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together={('asset', 'sn')},
        ),
    ]
