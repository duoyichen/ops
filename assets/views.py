from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
#import json
from assets import models
from assets.python_snmp import *


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
    network_obj = models.NetworkAsset.objects.all()
    # # print(network_list)
    # # print(type(network_list))
    # print(network_obj)
    # for i in network_obj:
    #     print(i.get_sub_asset_type_display(),i.asset.admin.username)
    # #print(network_obj.get_sub_asset_type_display())
    # print(type(network_obj))
    return render(request,"assets/network_asset.html",locals())

def server_asset(request):
    server_list = models.ServerAsset.objects.all()
    return render(request,"assets/server_asset.html",locals())

def server_asset_detail(request,id):
    if request.method == 'GET':
        id = id
        server_obj = models.ServerAsset.objects.filter(id=id)
        # obj = models.Server_Asset.objects.filter(id=id).values(
        #     'id',
        #     'sub_asset_type',
        #     'model',
        #     'os_type',
        #     'os_distribution',
        #     'os_release',
        #     'asset__idc__name',
        #     'asset__manufacturer__name',
        #     'asset__admin__username',
        #     'asset__name',
        #     'asset__m_time',
        #     'asset__status',
        #     'asset__manage_ip',
        #     'asset__asset_code',
        # )
        # print(server_obj[0].asset.id)
        cpu_obj = models.CPU.objects.filter(asset__id=server_obj[0].asset.id)
        ram_obj = models.RAM.objects.filter(asset__id=server_obj[0].asset.id)
        # print(ram_obj)
        disk_obj = models.Disk.objects.filter(asset__id=server_obj[0].asset.id)
        nic_obj = models.NIC.objects.filter(asset__id=server_obj[0].asset.id)
        return render(request,'assets/server_asset_detail.html',locals())

def ip_asset(request):
    #ips_list = models.IP_Asset.objects.all().values('id','name','netmask','gateway_ip','first_ip','end_ip','m_time','admin_id__name','manufacturer_id__name')
    # ips_list = models.IP_Asset.objects.all().values('id','name','netmask','gateway_ip','first_ip','end_ip','m_time','admin__username','idc__name','manufacturer__name')
    ips_obj = models.IPAsset.objects.all()
    # print(ips_obj)
    return render(request,"assets/ip_asset.html",locals())

def ip_asset_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        ips_obj = models.IPAsset.objects.filter(id=id)
        print(ips_obj[0].id)
        ip_obj = models.IP.objects.filter(ip_asset=ips_obj[0].id)
        print(ip_obj)
        has_ip_flag = 1
        if ip_obj.__len__() == 0:
            has_ip_flag = 0
        return render(request, 'assets/ip_asset_detail.html', locals())

from django import forms
from django.forms import fields,widgets
from django.forms.models import ModelChoiceField

class ip_asset_form(forms.Form):
    name = fields.CharField(
        required=True,
        max_length=64,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='名称（网络号）：',
    )
    asset_code = fields.CharField(
        required=True,
        max_length=64,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='资产编码：',
    )
    netmask = fields.GenericIPAddressField(
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='掩码：',
        # initial='请输入掩码',
    )
    first_ip = fields.GenericIPAddressField(
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='开始IP：',
        # initial='请输入开始IP',
    )
    end_ip = fields.GenericIPAddressField(
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        #error_messages={},
        label='结束IP：',
        # initial='请输入结束IP',
    )
    manufacturer = ModelChoiceField(
        queryset=models.Manufacturer.objects.all(),
        widget=widgets.Select(attrs={'class':'form-control'}),
        label='运营商：',
        initial=1
    )
    # status = ModelChoiceField(
    #     queryset=dict(models.Asset.asset_status),
    #     widget=widgets.Select(attrs={'class':'form-control'}),
    #     label='状态：',
    #     initial=0
    # )
    tag = ModelChoiceField(
        queryset=models.Tag.objects.all(),
        widget=widgets.Select(attrs={'class':'form-control'}),
        label='标签',
        initial=0
    )
    idc = ModelChoiceField(
        queryset=models.IDC.objects.all(),
        widget=widgets.Select(attrs={'class':'form-control'}),
        label='所属机房',
        initial=0
    )
    comments = fields.TextInput()
    admin = ModelChoiceField(
        queryset=models.User.objects.all(),
        widget=widgets.Select(attrs={'class': 'form-control'}),
        label='管理人',
        initial=1,
    )
    approved_by = ModelChoiceField(
        queryset=models.User.objects.all(),
        widget=widgets.Select(attrs={'class': 'form-control'}),
        label='审批者',
        initial=1,
    )

def add_ip_asset(request):
    if request.method == 'GET':
        obj = ip_asset_form()
        return render(request,'assets/add_ip_asset.html',{'obj':obj})
    else:
        obj = ip_asset_form(request.POST)
        if obj.is_valid():
            models.Asset.objects.create(asset_type=2)
            models.IPAsset.objects.create(**obj.cleaned_data[''])
            ips_obj = models.IPAsset.objects.filter(name=obj.cleaned_data['name'])
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
        models.IPAsset.objects.filter(id=id).delete()
        return redirect('/assets/ip_asset/')

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
    ips_obj = models.IPAsset.objects.filter(id=id)
    first_ip = ips_obj[0].first_ip
    end_ip = ips_obj[0].end_ip
    ip_asset = ips_obj[0].id
    status = 0
    customer = ''
    comment = '新添加ip'
    num1 = ip2num(first_ip)
    num2 = ip2num(end_ip)
    for i in range(num1, num2 + 1):
        # print(num2ip(i))
        try:
            models.IP.objects.create(
                ip=num2ip(i),
                status=status,
                customer=customer,
                comment=comment,
                ip_asset_id=id
            )
        except Exception as e:
            print("添加ip出错了！")
            return redirect( '/assets/ip/')
    # return render(request,'assets/ip_asset_detail.html',locals())
    # return HttpResponse("ok")
    return redirect('/assets/ip/')

def add_port(request):
    if request.method == 'GET':
        sysName  = "1.3.6.1.2.1.1.5"
        ifNumber = "1.3.6.1.2.1.2.1"
        ifDescr = "1.3.6.1.2.1.2.2.1.2"
        commu = 'ewcache-55667'
        ip_list = []
        network_assets = models.NetworkAsset.objects.all()
        for i in network_assets:
            # print(i.asset.manage_ip)
            ip_list.append(i.asset.manage_ip)

        snmp_inst = GetSnmp()

        #生成list
        oid_list = snmp_inst.make_list(
            # sysName,
            # ifNumber,
            ifDescr,
        )
        #获取设备 snmp 相关信息
        info = snmp_inst.get_info(ip_list, commu, oid_list,)
        # print(type(info))
        for k,v in info.items():
            # k 就是 ip
            print(k, ':')
            network_obj = models.NetworkAsset.objects.filter(asset__manage_ip = k)[0]
            user_obj = models.User.objects.filter(username = 'admin')
            # print(network_obj)
            for k2,v2 in v.items():
                # print('    ', k2)
                # 判断 k2 是不是等于 ifDescr 的 oid
                if k2 == '1.3.6.1.2.1.2.2.1.2':
                    for k3,v3 in v2.items():
                        print('        ', k3)
                        print('            ', v3)
                        # v3 就是端口名称
                        # port_name = v3
                        # print('    ', network_obj[0], port_name)
                        models.Port.objects.create(port = network_obj, port_name = v3, admin = user_obj[0])
                else:
                    for i in v2:
                        print('        ', i)
        return redirect('/assets/port/')
        # return HttpResponse(info)
        # print(JsonResponse(info))
        # print(json.dumps(info,indent=4))
        # return JsonResponse(info)
    else:
        return HttpResponse('This API just for GET method!')

def port(request):
    if request.method == 'GET':
        port_obj = models.Port.objects.all()
        # print(port_obj[0].port.asset.idc)
        # print(port_obj[0].port.asset.manage_ip)
        # print(port_obj[0].port_name)
        # print(port_obj[0].ip)
        # print(port_obj[0].limit_in_speed)
        # print(port_obj[0].limit_out_speed)
        # print(port_obj[0].status)
        # print(port_obj[0].admin)
        # print(port_obj[0].comment)
        # print(port_obj[0])
        return render(request, "assets/port.html", locals())


# @csrf_exempt
# def report(request):
#     if request.method == "POST":
#         asset_data = request.POST.get('asset_data')
#         print(type(asset_data))
#         print(asset_data)
#         # for k,v in asset_data:
#         #     print(k,v)
#         return HttpResponse("成功收到数据！")

import json
from . import asset_handler
@csrf_exempt
def report(request):
    """
    通过csrf_exempt装饰器，跳过Django的csrf安全机制，让post的数据能被接收，但这又会带来新的安全问题。
    可以在客户端，使用自定义的认证token，进行身份验证。这部分工作，请根据实际情况，自己进行。
    :param request:
    :return:
    """
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        # 各种数据检查，请自行添加和完善！
        if not data:
            return HttpResponse("没有数据！")
        if not issubclass(dict, type(data)):
            return HttpResponse("数据必须为字典格式！")
        # 是否携带了关键的sn号
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Asset.objects.filter(server_asset__sn=sn)
            if asset_obj:
                # 进入已上线资产的数据更新流程
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse("资产数据已经更新！")
            else:   # 如果已上线资产中没有，那么说明是未批准资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("没有资产sn序列号，请检查数据！")
    else:
        return HttpResponse('This API just for AutoCollect!')




class emp_form(forms.Form):
    id = fields.IntegerField(
        label='员工ID：',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    name = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        label='姓名：',
    )
    depart = ModelChoiceField(
        queryset=models.depart.objects.all(),
        widget=widgets.Select(attrs={'class':'form-control'}),
        label='部门：',
    )
    m_time = fields.DateTimeField(
        label='修改时间：',
        widget=widgets.DateTimeInput(attrs={'class': 'form-control'}),
    )

class depart_form(forms.Form):
    name = fields.CharField(
        max_length=32,
        label='部门名称：',
    )

def add_employee(request):
    if request.method == 'GET':
        obj = emp_form()
        return render(request,'assets/employee.html',locals())
    else:
        obj = emp_form(request.POST)
        if obj.is_valid():
            models.empployee.objects.create(**obj.cleaned_data)
            return HttpResponse('员工添加成功！')
        else:
            return render(request,'assets/employee.html',locals())


from django.forms.models import model_to_dict

def edit_employee(request,emp_id,*args,**kwargs):
    if request.method == 'GET':
        emp_obj = models.empployee.objects.all().filter(id=emp_id).values('id','name','depart','m_time')
        # emp_obj = emp_obj0[0]
        # # emp_obj['name'] = emp_obj0[0].name
        # # emp_obj['depart'] = emp_obj0[0].depart
        # # emp_obj = models.empployee.objects.all().filter(id=emp_id)
        # print(emp_obj,type(emp_obj))
        # emp_dic = {}
        # emp_dic['id'] = emp_obj.[0]
        # emp_obj = model_to_dict(emp_obj0)
        # print(emp_obj0,type(emp_obj0))
        # emp_obj = dict(emp_obj0)
        # print(type(emp_obj))
        # for k,v in emp_obj.items():
        #     print(k,v)
        # print(emp_obj,type(emp_obj))
        # values = {'name': 'root', 'depart': 2}
        # print(values,type(values))
        obj = emp_form(emp_obj[0])
        # print(obj.id)
        # print(obj,type(obj))
        return render(request,'assets/edit_employee.html',locals())
        # return redirect('/assets/')
        # return HttpResponse(emp_id)
    else:
        obj = emp_form(request.POST)
        if obj.is_valid():
            # print(obj.cleaned_data['name'])
            # print(obj.cleaned_data[name])
            import datetime
            models.empployee.objects.filter(id=emp_id).update(
                name=obj.cleaned_data['name'],
                depart=obj.cleaned_data['depart'],
                m_time=datetime.datetime.now()
            )
            return redirect('/assets/employee/')
        return render(request,'assets/edit_employee.html',locals())


def add_depart(request):
    if request.method == 'GET':
        obj = depart_form()
        return render(request,'assets/depart.html',locals())
    else:
        obj = depart_form(request.POST)
        if obj.is_valid():
            models.depart.objects.create(**obj.cleaned_data)
            return HttpResponse("部门添加成功")
        else:
            return render(request,'assets/depart.html',locals())

def employee(request):
    obj = models.empployee.objects.all().values('id','name','depart__name','m_time')
    return render(request,'assets/employee.html',locals())
