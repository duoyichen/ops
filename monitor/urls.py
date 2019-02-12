from django.urls import path
from monitor import views


app_name = 'monitor'

urlpatterns = [
    # path('', views.index),
    path('monitor_list/', views.monitor_list),
    # path('idc/', views.idc),
]
