#!/usr/bin/env python
# coding: utf-8
'''
@author: duoyichen
@email: duoyichen@qq.com
@date:  
'''

import sys
import os
import getopt
import subprocess
import re
import time
import threading


def ping_(ip):
    # print("ping -c1 %s" %IP)
    # print(type(ip),ip)
    # print(("ping -c 1 %s" %ip))
    xpin=subprocess.getoutput("ping -c 1 %s" %ip)
    # print(subprocess.getoutput("ping -c1 %s" %IP))
    # print(subprocess.getoutput('ping -c 1 122.11.59.129'))
    # print(xpin)
    ms0='time=\d+.\d+'
    mstime=re.search(ms0,xpin)
    # print(mstime)
    if not mstime:
        ms='timeout'
        return ms
    else:
        ms=mstime.group().split('=')[1]
        return ms

result = {}

def count(sec,ip):
    nowsecond = int(time.time())
    second = sec
    endtime = nowsecond + second
    nums = 0
    oknums = 0
    timeout = 0
    lostpacket = 0.0
    total_ms = 0.0
    avgms = 0.0
    # print(type(ip),ip)

    while nowsecond <= endtime:
        nums += 1
        ms = ping_(ip)
        if ms == 'timeout':
            timeout += 1
            lostpacket = timeout*100.0 / nums
        else:
            oknums += 1
            total_ms = total_ms + float(ms)
            if oknums == 0:
                oknums = 1
                avgms = total_ms / oknums
            avgms = total_ms / oknums
        # print(avgms,lostpacket)
        result[ip] = [ip, avgms, lostpacket]
        # print(result)
        nowsecond = int(time.time())
    # print(type(result))
    # print(result)

def get_net_quality(secs,ips):
    # ips = ips
    # print(type(ips),ips)
    # print('Starting')
    threads = []
    loops = range(len(ips))
    # print('Total %s Threads is working' %len(ips))

    for i in loops:
        t = threading.Thread(target=count, args=(secs, ips[i]))
        threads.append(t)
    for i in loops:
        threads[i].start()
    for i in loops:
        threads[i].join()

    return result


