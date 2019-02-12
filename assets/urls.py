from django.urls import path
from  assets import views


app_name = 'assets'

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('idc/', views.idc),
    path('network_asset/', views.network_asset),
    path('server_asset/', views.server_asset),
    path('server_asset/<int:id>', views.server_asset_detail),
    path('ip_asset/', views.ip_asset),
    path('ip/', views.ip),
    path('add_ip_asset/', views.add_ip_asset),
    path('del_ip_asset.html', views.del_ip_asset),
    path('ip_asset_detail.html', views.ip_asset_detail),
    path('add_ip.html', views.add_ip),
    path('port/', views.port),
    path('add_port/', views.add_port),
    # For AutoCollect
    path('report/', views.report, name='report'),

    path('employee/', views.employee),
    path('add_employee/', views.add_employee),
    path('edit_employee/', views.edit_employee),
    path('edit_employee/<int:emp_id>/', views.edit_employee),
    path('depart/', views.add_depart),
    path('add_depart/', views.add_depart),
]
