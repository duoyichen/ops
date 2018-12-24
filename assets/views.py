from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
#import json
from assets import models


def index(request):
    asset_list = models.Asset.objects.all()
    # print(type(asset_list))
    # for i in asset_list:
    #     print(i.tags.all())
    return render(request, "assets/index.html", locals())

def idc(request):
    idc_list = models.IDC.objects.all()
    return render(request,"assets/idc.html",locals())
    #return render(request,"base.html",locals())

def network_asset(request):
    #network_list = models.Network_asset.objects.all().values('id','sub_asset_type','model','asset__hostname','asset__manage_ip','asset__admin__username','asset__idc__name','asset__manufacturer__name','asset__m_time')
    network_obj = models.Network_asset.objects.all()
    # # print(network_list)
    # # print(type(network_list))
    # print(network_obj)
    # for i in network_obj:
    #     print(i.get_sub_asset_type_display(),i.asset.admin.username)
    # #print(network_obj.get_sub_asset_type_display())
    # print(type(network_obj))
    return render(request,"assets/network_asset.html",locals())

def server_asset(request):
    server_list = models.Server_Asset.objects.all()
    return render(request,"assets/server_asset.html",locals())

def ip_asset(request):
    #ips_list = models.IP_Asset.objects.all().values('id','name','netmask','gateway_ip','first_ip','end_ip','m_time','admin_id__name','manufacturer_id__name')
    # ips_list = models.IP_Asset.objects.all().values('id','name','netmask','gateway_ip','first_ip','end_ip','m_time','admin__username','idc__name','manufacturer__name')
    ips_obj = models.IP_Asset.objects.all()
    # print(ips_obj)
    return render(request,"assets/ip_asset.html",locals())

from django import forms
from django.forms import fields,widgets
from django.forms.models import ModelChoiceField

class ip_asset_form(forms.Form):
    sn = fields.CharField(
        required=True,
        min_length=8,
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='序列号',
        # initial='请输入 8 到 32 位序列号',
    )
    name = fields.GenericIPAddressField(
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='网络号',
        # initial='请输入网络号',
    )
    netmask = fields.GenericIPAddressField(
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='掩码',
        # initial='请输入掩码',
    )
    first_ip = fields.GenericIPAddressField(
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='开始IP',
        # initial='请输入开始IP',
    )
    end_ip = fields.GenericIPAddressField(
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='结束IP',
        # initial='请输入结束IP',
    )

    admin = ModelChoiceField(
        queryset=models.User.objects.all(),
        widget=widgets.Select(attrs={'class': 'form-control'}),
        label='管理者',
        initial=2,
    )

    approved_by = ModelChoiceField(
        queryset=models.User.objects.all(),
        widget=widgets.Select(attrs={'class': 'form-control'}),
        label='审批者',
        initial=1,
    )

    idc = ModelChoiceField(
        queryset=models.IDC.objects.all(),
        widget=widgets.Select(attrs={'class': 'form-control'}),
        label='所属机房',
        initial=2,
    )

    manufacturer = ModelChoiceField(
        queryset=models.Manufacturer.objects.all(),
        widget=widgets.Select(attrs={'class': 'form-control'}),
        label='运营商',
        initial=1,
    )

def add_ip_asset(request):
    if request.method == 'GET':
        obj = ip_asset_form()
        return render(request,'assets/add_ip_asset.html',{'obj':obj})
    else:
        obj = ip_asset_form(request.POST)
        if obj.is_valid():
            models.IP_Asset.objects.create(**obj.cleaned_data)
            ips_obj = models.IP_Asset.objects.filter(name=obj.cleaned_data['name'])
            # print(ips_obj,type(ips_obj))
            # return redirect(request, '/assets/ip_asset/')
            # return redirect(request, 'assets/ip_asset_detail.html')
            # return redirect('/assets/ip_asset_detail.html')
            return redirect('/assets/ip_asset/')
        else:
            #print(obj.cleaned_data)
            #print('验证失败',obj.errors)
            return render(request,'assets/add_ip_asset.html',{'obj':obj})

def del_ip_asset(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        # print(id)
        models.IP_Asset.objects.filter(id=id).delete()
        return redirect('/assets/ip_asset/')

def ip_asset_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        ips_obj = models.IP_Asset.objects.filter(id=id)
        print(ips_obj[0].id)
        ip_obj = models.IP.objects.filter(ip_asset=ips_obj[0].id)
        print(ip_obj)
        has_ip_flag = 1
        if ip_obj.__len__() == 0:
            has_ip_flag = 0
        return render(request, 'assets/ip_asset_detail.html', locals())

def ip(request):
    if request.method == 'GET':
        ip_obj = models.IP.objects.all()
    return render(request,"assets/ip.html",locals())

def ip2num(ip_add):
    lp = [int(x) for x in ip_add.split('.')]
    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]

def num2ip(num):
    ip_add2 = ['', '', '', '']
    ip_add2[3] = (num & 0xff)
    ip_add2[2] = (num & 0xff00) >> 8
    ip_add2[1] = (num & 0xff0000) >> 16
    ip_add2[0] = (num & 0xff000000) >> 24
    return '%s.%s.%s.%s' % (ip_add2[0], ip_add2[1], ip_add2[2], ip_add2[3])

def add_ip(request):

    id = request.GET.get('id')
    print(id)
    ips_obj = models.IP_Asset.objects.filter(id=id)
    first_ip = ips_obj[0].first_ip
    end_ip = ips_obj[0].end_ip
    name = ips_obj[0].name
    ip_asset = ips_obj[0].id
    status = 0
    customer = ''
    memo = '新添加ip'
    num1 = ip2num(first_ip)
    num2 = ip2num(end_ip)
    for i in range(num1, num2 + 1):
        # print(num2ip(i))
        try:
            models.IP.objects.create(
                ip=num2ip(i),
                status=status,
                customer=customer,
                memo=memo,
                ip_asset_id=id
            )
        except Exception as e:
            print("添加ip出错了！")
            return redirect( '/assets/ip/')
    # return render(request,'assets/ip_asset_detail.html',locals())
    # return HttpResponse("ok")
    return redirect('/assets/ip/')
