from django.db import models

# Create your models here.


# class Monitor_Items(models.Model):
#     """
#     监控项
#     """
#     lossRatio = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="丢包率")
#     bandWidth = models.PositiveIntegerField(verbose_name="带宽")
#     delay = models.DecimalField(max_digits=7, decimal_places=3, verbose_name="丢包率")
#     comment = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')
#
#     def __str__(self):
#         return self.lossRatio
#
#     class Meta:
#         verbose_name = '监控项'
#         verbose_name_plural = "监控项"


# class Alarm_List(models.Model):
#     """
#     报警记录
#     """
#     asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
#     dev_conf = models.TextField(null=True, blank=True, verbose_name="设备配置")
#     dev_log = models.TextField(null=True, blank=True, verbose_name='设备日志')
#
#     def __str__(self):
#         return self.asset.id
#
#     class Meta:
#         verbose_name = '网络设备'
#         verbose_name_plural = "网络设备"