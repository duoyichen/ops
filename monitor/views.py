from assets import models
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

# Create your views here.

def monitor_list(request):
    network_obj = models.NetworkAsset.objects.all()
    print(network_obj)
    return render(request,"monitor/monitor_list.html",locals())