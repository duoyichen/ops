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


global result
result = {}

def usage():
    print("USEAGE:")
    print("\t%s -i ip [-t secs] [-f file]" %sys.argv[0])
    print("\t-i  多个ip用 , 隔开")
    print("\t-t secs 测试的时间;默认为60秒;")
    print("\t-f file 输出结果到文件;默认为当前目录文本文件ping.result")
    print("\t-h|-?, 帮助信息")
    print("for example:")
    print("\t./test_net_quality.py -i 10.1.1.1 -t 60")
    print("\t表示测试测试点（本机）到 10.1.1.1 ，测试时间60秒;")

def pin(IP):
    # print("ping -c1 %s" %IP)
    xpin=subprocess.getoutput("ping -c 1 %s" %IP)
    # print(subprocess.getoutput("ping -c1 %s" %IP))
    # print(subprocess.getoutput('ping -c 1 122.11.59.129'))
    # print(xpin)
    ms='time=\d+.\d+'
    mstime=re.search(ms,xpin)
    # print(mstime)
    if not mstime:
        MS='timeout'
        return MS
    else:
        MS=mstime.group().split('=')[1]
        return MS

def count(sec,I):
    nowsecond = int(time.time())
    second = sec
    endtime = nowsecond + second
    nums = 0
    oknums = 0
    timeout = 0
    lostpacket = 0.0
    total_ms = 0.0
    avgms = 0.0
    while nowsecond <= endtime:
        nums += 1
        MS = pin(I)
        if MS == 'timeout':
            timeout += 1
            lostpacket = timeout*100.0 / nums
        else:
            oknums += 1
            total_ms = total_ms + float(MS)
            if oknums == 0:
                oknums = 1
                avgms = total_ms / oknums
            avgms = total_ms / oknums
        result[I]=(I,avgms,lostpacket)
        # print(result)
        nowsecond = int(time.time())


file = 'ping.result'
secs = 20
args = sys.argv[1:]
try:
    (opts, getopts) = getopt.getopt(args, 'i:f:t:h?')
except:
    print("\nInvalid command line option detected.")
    usage()
    sys.exit(1)

for opt, arg in opts:
    if opt in ('-i'):
        ip = arg
    if opt in ('-h', '-?'):
        usage()
        sys.exit(0)
    if opt in ('-f'):
        file = arg
    if opt in ('-t'):
        secs = int(arg)

if os.path.dirname(file):
    if os.path.exists(os.path.dirname(file)):
        f = open(file, 'w')
    else:
        print("File's path is wrong. please check it.")
        usage()
        sys.exit(0)
else:
    f = open(file, 'w')

if not isinstance(secs,int):
    usage()
    sys.exit(0)
else:
    ips = ip.split(',')
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



    print('%-18s %-6s %-6s' %('host', '延迟', '丢包率'))
    for k,v in result.items():
        # print(v[0] + ': ', v[1], v[2])
        # print(v[1])
        print(type(v[1]))
        if v[1] < 0.01:
            v[1] == '网络不通'
        print('%-18s %f %f' %(v[0] + ':', v[1], v[2]))
