from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    """    所有资产的共有数据表    """
    asset_type_choice = (
        ('network_device', '网络设备'),
        ('server_device', '服务器设备'),
        ('o_device', '其他设备'),
    )

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
        )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='network_asset', verbose_name="资产类型")
    name = models.CharField(max_length=64, unique=True, verbose_name="资产名称")     # 不可重复
    sn = models.CharField(max_length=128, unique=True, verbose_name="资产序列号")  # 不可重复
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='厂商')

    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属业务线')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='资产管理员', related_name='admin_asset')
    idc = models.ForeignKey('IDC', null=True, blank=True, on_delete=models.CASCADE, verbose_name='所在机房')
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='批准人', related_name='approved_by_asset')

    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"
        ordering = ['-c_time']

class Network_asset(models.Model):
    """网络设备"""
    sub_asset_type_choice = (
        (0, '交换机'),
        (1, '路由器'),
        (2, 'VPN设备'),
        (4, '防火墙'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="网络设备类型")

    #vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="VLanIP")
    #intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="内网IP")

    model = models.CharField(max_length=128, null=True, blank=True, verbose_name="网络设备型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="设备固件版本")
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="端口个数")
    device_detail = models.TextField(null=True, blank=True, verbose_name="设备配置")
    device_log = models.TextField(null=True, blank=True, verbose_name='设备日志')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"

class Server_Asset(models.Model):
    """服务器设备"""
    sub_asset_type_choice = (
        (0, '机架式服务器'),
        (1, '其他类型服务器'),
        (2, '虚拟机'),
        (3, '容器'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="服务器类型")
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="添加方式")
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server',
                                  blank=True, null=True, on_delete=models.CASCADE, verbose_name="宿主机")  # 虚拟机专用字段
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')

    os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('发行版本', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

class IDC(models.Model):
    """机房"""
    name = models.CharField(max_length=64, unique=True, verbose_name="机房名称")
    sw_core = models.CharField(max_length=64, verbose_name="核心交换机")
    bandwidth = models.PositiveIntegerField(verbose_name="带宽")
    isp = models.CharField(max_length=64,verbose_name="ISP服务商")
    city = models.CharField(max_length=32,verbose_name="城市")
    address = models.CharField(max_length=128,verbose_name="机房地址")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"

class IP_Asset(models.Model):
    asset_status = (
        (0, '未分配'),
        (1, '已分配'),
        (2, '未知'),
        )

    #asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='network_asset', verbose_name="资产类型")
    name = models.CharField(max_length=64, unique=True, verbose_name="资产名称")     # 不可重复
    sn = models.CharField(max_length=128, unique=True, verbose_name="资产序列号")  # 不可重复
    #business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属业务线')
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')

    #hostname = models.CharField(max_length=128, null=True, blank=True, verbose_name="主机名")
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='厂商')
    netmask = models.GenericIPAddressField(null=True, blank=True, verbose_name='掩码')
    gateway_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    first_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='开始IP')
    end_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='结束IP')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='资产管理员', related_name='admin_ip_asset')
    idc = models.ForeignKey('IDC', null=True, blank=True, on_delete=models.CASCADE, verbose_name='所在机房')
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='批准人', related_name='approved_by_ip_asset')

    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = 'IP段表'
        verbose_name_plural = "IP段表"
        ordering = ['-m_time']

class IP(models.Model):
    """    所有ip数据表    """
    asset_status = (
        (0, '未分配'),
        (1, '已分配'),
        (2, '未知'),
        )

    ip = models.GenericIPAddressField(null=True, blank=True, unique=True, verbose_name='IP')
    # sn = models.CharField(max_length=128, unique=True, verbose_name="资产序列号")  # 不可重复
    ip_asset = models.ForeignKey('IP_Asset', null=True, blank=True, on_delete=models.CASCADE,verbose_name='所属IP段',related_name='ips_ip')
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='IP状态')
    customer = models.CharField(null=True, blank=True, max_length=64, verbose_name="客户名称")
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '%s' % (self.ip)

    class Meta:
        verbose_name = 'IP表'
        verbose_name_plural = "IP表"
        ordering = ['-ip']


class Manufacturer(models.Model):
    """厂商"""

    name = models.CharField('厂商名称', max_length=64, unique=True)
    telephone = models.CharField('支持电话', max_length=30, blank=True, null=True)
    memo = models.CharField('备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"

class BusinessUnit(models.Model):
    """业务线"""

    parent_unit = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='parent_level')
    name = models.CharField('业务线', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"

class Tag(models.Model):
    """标签"""
    name = models.CharField('标签名', max_length=32, unique=True)
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"

class EventLog(models.Model):
    """
    日志，在关联对象被删除的时候，不能一并删除，需保留日志。
    因此，on_delete=models.SET_NULL
    """

    name = models.CharField('事件名称', max_length=128)
    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
    )
    asset = models.ForeignKey('Asset', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批成功时有这项数据
    new_asset = models.ForeignKey('NewAssetApprovalZone', blank=True, null=True, on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.SmallIntegerField('事件类型', choices=event_type_choice, default=4)
    component = models.CharField('事件子项', max_length=256, blank=True, null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人', on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    memo = models.TextField('备注', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"

class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    sn = models.CharField('资产SN号', max_length=128, unique=True)  # 此字段必填
    asset_type_choice = (
        ('network_device', '网络设备'),
        ('server_device', '服务器'),
        ('o_device', '安全设备'),
        ('IDC', '机房'),
    )
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='资产类型')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)

    data = models.TextField('资产数据')  # 此字段必填

    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"
        ordering = ['-c_time']
