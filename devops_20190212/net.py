#!/usr/bin/env python
# coding: utf-8
'''
@author: duoyichen
@email: duoyichen@qq.com
@date:  
'''

from test_net_quality import count,get_net_quality

# ips = ['122.11.59.1', '122.11.59.129', '122.11.59.130', '122.11.59.131', '122.11.59.132', '122.11.59.133', '122.11.59.134', '122.11.59.135', 'www.baidu.com']
# ips = ['122.11.59.129']

with open('ip') as f:
    # ips = f.readlines()
    ips = f.read().splitlines()
    f.close()
# print(ips)
result = get_net_quality(8,ips)

print('%-18s %-24s %-10s' %('host', '延迟', '丢包率'))
for k,v in result.items():
    # print(v[0] + ': ', v[1], v[2])
    # print(v[1])
    # print(type(v[1]))
    # print(v[1] == 0)
    if v[1] == 0.0:
        v[1] = 'Unreachable'
        # print(v[1])
    print('%-18s %-24s %f' %(v[0] + ':', v[1], v[2]))

# ret = count(8,'122.11.59.129')
# print(ret)