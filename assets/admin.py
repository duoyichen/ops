from django.contrib import admin
from . import models


class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'name', 'status', 'approved_by', 'c_time', "m_time"]

admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Network_asset)
admin.site.register(models.Server_Asset)
admin.site.register(models.IDC)
admin.site.register(models.IP_Asset)
admin.site.register(models.IP)
admin.site.register(models.Manufacturer)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Tag)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprovalZone)