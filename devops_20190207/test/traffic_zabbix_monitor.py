#!/usr/bin/env python
import requests
import json
import time, datetime
import sys

bandwidth_threshold = 90.0
if len(sys.argv) > 1:
    bandwidth_threshold = float(sys.argv[1])
percent_threshold = 70.0
if len(sys.argv) > 2:
    percent_threshold = float(sys.argv[2])
pre_minutes = 10
if len(sys.argv) > 2:
    pre_minutes = int(sys.argv[3]) + 1

server_ip = '122.11.52.36'
port = '8191'
username = 'qiaochong_TJ'
password = '2018@Zabbix_Pass'
headers = {'Content-Type': 'application/json-rpc'}
url = 'http://%s:%s/api_jsonrpc.php' % (server_ip, port)


# 获取token
def get_token(username, password):
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password
        },
        "id": 0
    }
    request = requests.post(url=url, headers=headers, data=json.dumps(data))
    dict = json.loads(request.text)
    return dict['result']


def get_host_list(token_num):
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": "extend",
        },
        "id": 0,
        "auth": token_num,
    }
    request = requests.post(url=url, headers=headers, data=json.dumps(data))
    dict = json.loads(request.content)
    return dict['result']


def get_items_of_host(token_num, hostid):
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": hostid,
            "param": {
                "key_": "ifHCInOctets[10GE1/0/47]"
            },
            "sortfield": "name"
        },
        "id": 0,
        "auth": token_num,
    }
    request = requests.post(url=url, headers=headers, data=json.dumps(data))
    dict = json.loads(request.content)
    # print(dict)
    return dict['result']


def get_item_data(token_num, itemid):
    data = {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "output": "extend",
            "history": 3,
            "itemids": itemid,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": pre_minutes
        },
        "id": 0,
        "auth": token_num,
    }
    request = requests.post(url=url, headers=headers, data=json.dumps(data))
    dict = json.loads(request.content)
    return dict['result']


import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_mail(mail_msg):
    sender = 'robot@51ywx.com'
    smtpserver = 'smtp.51ywx.com'
    mail_user = 'robot@51ywx.com'
    mail_pass = 'XbLKzpQ40bznIC7s'

    to_reciver = ['qiaochong@51ywx.com']
    cc_reciver = ['chenying@51ywx.com']
    receiver = to_reciver + cc_reciver
    subject = '流量报警 天津移动'

    msg = MIMEText(mail_msg['mail_msg'], 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ";".join(to_reciver)
    msg['Cc'] = ";".join(cc_reciver)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, receiver, msg.as_string())
        print(mail_msg['log'])
        smtp.quit()
    except Exception as e:
        print('Error: 邮件发送失败！')
        print(e)


def process_item_data(item_data):
    value_now_time = time.strftime("%Y%m%d %H:%M:%S", time.localtime(int(item_data[0]['clock'])))
    value_now = item_data[0]['value']
    value_now_mb = int(value_now) / 1024 / 1024
    item_data.pop(0)
    value_pre = []
    for i in item_data:
        value_pre.append(int(i['value']))
    value_pre_avg = sum(value_pre) / len((value_pre))
    ratio = float(value_now) * 100 / value_pre_avg
    return value_now_mb, ratio, value_now_time


def check_item_data(value_now_mb, ratio, value_now_time, bandwidth_threshold, percent_threshold):
    print('%s bandwidth:%fMbps  ratio:%f%%  bandwidth_threshold:%fMbps  percent_threshold:%f%%' \
          % (value_now_time, value_now_mb, ratio, bandwidth_threshold, percent_threshold))
    mail_msg = {}
    if value_now_mb < bandwidth_threshold:
        mail_msg['mail_msg'] = '{time}  Warning:  The Bandwidth is:  {bandwidth} Mbps'.format(time=value_now_time,
                                                                                              bandwidth=int(
                                                                                                  value_now_mb))
        mail_msg['log'] = '请注意：带宽过低，已发送邮件！'
        send_mail(mail_msg)

    if ratio < percent_threshold:
        mail_msg['mail_msg'] = '{time}  Warning: The ratio is:  {ratio}%'.format(time=value_now_time, ratio=ratio)
        mail_msg['log'] = '请注意：带宽骤降，已发送邮件！'
        send_mail(mail_msg)
    elif ratio > 10000 / percent_threshold:
        mail_msg['mail_msg'] = '{time}  Warning: The ratio is:  {ratio}%'.format(time=value_now_time, ratio=ratio)
        mail_msg['log'] = '请注意：带宽骤升，已发送邮件！'
        send_mail(mail_msg)


if __name__ == "__main__":
    token_num = get_token(username, password)
    itemid_out = 87247
    item_data_out = get_item_data(token_num, itemid_out)
    value_now_mb_out, ratio_out, value_now_time_out = process_item_data(item_data_out)
    check_item_data(value_now_mb_out, ratio_out, value_now_time_out, bandwidth_threshold, percent_threshold)

    itemid_in = 87135

    # ret = get_host_list(token_num)
    # hostid = '10444'
    # ret = get_items_of_host(token_num,hostid)
    # for i in ret:
    #     for k,v in i.items():
    #         if v in ['ifHCInOctets[10GE1/0/47]','ifHCOutOctets[10GE1/0/47]']:
    #             print('itemid:{itemid} snmp_oid:{snmp_oid} key_:{key_}'.format(itemid=i['itemid'],snmp_oid=i['snmp_oid'],key_=i['key_']))
    # print(ret[0])
    # for k,v in ret[0].items():
    #     print(k,'-->',v)