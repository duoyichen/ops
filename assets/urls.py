from django.urls import path
from  assets import views


app_name = 'assets'

urlpatterns = [
    # path('', views.index),
    path('index/', views.index),
    path('idc/', views.idc),
    path('network_asset/', views.network_asset),
    path('server_asset/', views.server_asset),
    path('ip_asset/', views.ip_asset),
    path('ip/', views.ip),
    path('add_ip_asset/', views.add_ip_asset),
    path('del_ip_asset.html', views.del_ip_asset),
    path('ip_asset_detail.html', views.ip_asset_detail),
    path('add_ip.html', views.add_ip),
]
