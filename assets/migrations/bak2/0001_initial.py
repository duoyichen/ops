# Generated by Django 2.1.4 on 2018-12-28 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(choices=[('network_device', '网络设备'), ('server_device', '服务器设备'), ('ip_device', 'IP资源'), ('o_device', '其他设备')], default='network_device', max_length=64, verbose_name='资产类型')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='资产名称')),
                ('asset_code', models.CharField(max_length=128, unique=True, verbose_name='资产编码')),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('status', models.SmallIntegerField(choices=[(0, '在线'), (1, '下线'), (2, '故障'), (3, '未知')], default=0, verbose_name='设备状态')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_asset', to=settings.AUTH_USER_MODEL, verbose_name='资产管理员')),
            ],
            options={
                'verbose_name': '资产总表',
                'verbose_name_plural': '资产总表',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='业务线')),
                ('memo', models.CharField(blank=True, max_length=64, null=True, verbose_name='备注')),
                ('parent_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_level', to='assets.BusinessUnit')),
            ],
            options={
                'verbose_name': '业务线',
                'verbose_name_plural': '业务线',
            },
        ),
        migrations.CreateModel(
            name='depart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='部门名称')),
                ('c_time', models.DateTimeField(auto_now=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
            },
        ),
        migrations.CreateModel(
            name='empployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='员工姓名')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('depart', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.depart', verbose_name='所属部门')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='事件名称')),
                ('event_type', models.SmallIntegerField(choices=[(0, '其它'), (1, '硬件变更'), (2, '新增配件'), (3, '设备下线'), (4, '设备上线'), (5, '定期维护'), (6, '业务上线\\更新\\变更')], default=4, verbose_name='事件类型')),
                ('component', models.CharField(blank=True, max_length=256, null=True, verbose_name='事件子项')),
                ('detail', models.TextField(verbose_name='事件详情')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='事件时间')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset')),
            ],
            options={
                'verbose_name': '事件纪录',
                'verbose_name_plural': '事件纪录',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='机房名称')),
                ('sw_core', models.CharField(max_length=64, verbose_name='核心交换机')),
                ('bandwidth', models.PositiveIntegerField(verbose_name='带宽')),
                ('isp', models.CharField(max_length=64, verbose_name='ISP服务商')),
                ('city', models.CharField(max_length=32, verbose_name='城市')),
                ('address', models.CharField(max_length=128, verbose_name='机房地址')),
                ('comment', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '机房',
                'verbose_name_plural': '机房',
            },
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='IP')),
                ('status', models.SmallIntegerField(choices=[(0, '未分配'), (1, '已分配'), (2, '未知')], default=0, verbose_name='IP状态')),
                ('customer', models.CharField(blank=True, max_length=64, null=True, verbose_name='客户名称')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': 'IP表',
                'verbose_name_plural': 'IP表',
                'ordering': ['-ip'],
            },
        ),
        migrations.CreateModel(
            name='IP_Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, '已分配'), (1, '未分配'), (2, '未知')], default=0, verbose_name='资产状态')),
                ('netmask', models.GenericIPAddressField(blank=True, null=True, verbose_name='掩码')),
                ('gateway_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='网关IP')),
                ('first_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='开始IP')),
                ('end_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='结束IP')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'verbose_name': 'IP段表',
                'verbose_name_plural': 'IP段表',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='厂商名称')),
                ('telephone', models.CharField(blank=True, max_length=30, null=True, verbose_name='支持电话')),
                ('comment', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '厂商',
                'verbose_name_plural': '厂商',
            },
        ),
        migrations.CreateModel(
            name='Network_Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产序列号')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='设备型号')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('dev_conf', models.TextField(blank=True, null=True, verbose_name='设备配置')),
                ('dev_log', models.TextField(blank=True, null=True, verbose_name='设备日志')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '交换机'), (1, '路由器'), (2, 'VPN设备'), (4, '防火墙')], default=0, verbose_name='设备类型')),
                ('firmware', models.CharField(blank=True, max_length=128, null=True, verbose_name='固件版本')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_network', to=settings.AUTH_USER_MODEL, verbose_name='所有者')),
            ],
            options={
                'verbose_name': '网络设备',
                'verbose_name_plural': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产SN号')),
                ('asset_type', models.CharField(blank=True, choices=[('network_device', '网络设备'), ('server_device', '服务器'), ('o_device', '安全设备'), ('IDC', '机房')], default='server', max_length=64, null=True, verbose_name='资产类型')),
                ('manufacturer', models.CharField(blank=True, max_length=64, null=True, verbose_name='生产厂商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('ram_size', models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')),
                ('cpu_model', models.CharField(blank=True, max_length=128, null=True, verbose_name='CPU型号')),
                ('cpu_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cpu_core_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True)),
                ('os_type', models.CharField(blank=True, max_length=64, null=True)),
                ('os_release', models.CharField(blank=True, max_length=64, null=True)),
                ('data', models.TextField(verbose_name='资产数据')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='汇报日期')),
                ('m_time', models.DateTimeField(auto_now=True, verbose_name='数据更新日期')),
                ('approved', models.BooleanField(default=False, verbose_name='是否批准')),
            ],
            options={
                'verbose_name': '新上线待批准资产',
                'verbose_name_plural': '新上线待批准资产',
                'ordering': ['-c_time'],
            },
        ),
        migrations.CreateModel(
            name='Server_Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=128, unique=True, verbose_name='资产序列号')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='服务器型号')),
                ('os_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统类型')),
                ('os_distribution', models.CharField(blank=True, max_length=64, null=True, verbose_name='发行版本')),
                ('os_release', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统版本')),
                ('raid_type', models.CharField(blank=True, max_length=512, null=True, verbose_name='Raid类型')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '机架式服务器'), (1, '其他类型服务器'), (2, '虚拟机'), (3, '容器')], default=0, verbose_name='服务器类型')),
                ('created_by', models.CharField(choices=[('auto', '自动添加'), ('manual', '手工录入')], default='auto', max_length=32, verbose_name='添加方式')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
                ('hosted_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hosted_on_server', to='assets.Server_Asset', verbose_name='宿主机')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_server', to=settings.AUTH_USER_MODEL, verbose_name='所有者')),
            ],
            options={
                'verbose_name': '服务器',
                'verbose_name_plural': '服务器',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='标签名')),
                ('c_day', models.DateField(auto_now_add=True, verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='ip',
            name='ip_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ips_ip', to='assets.IP_Asset', verbose_name='所属IP段'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='new_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.NewAssetApprovalZone'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='事件执行人'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.IDC', verbose_name='所在机房'),
        ),
        migrations.AddField(
            model_name='asset',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Manufacturer', verbose_name='厂商'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tag',
            field=models.ManyToManyField(blank=True, to='assets.Tag', verbose_name='标签'),
        ),
    ]