#!/usr/bin/env python
# coding: utf-8
'''
@author: duoyichen
@email: duoyichen@qq.com
@date:  
'''

#!/usr/bin/env python
# coding: utf-8
# coding: cp950
''''' 
Create Date: 2012-11-06 
Version: 1.0 
Description: Detection host survival 
Author: Victor 
QQ: 1409175531 
'''
''''' Please run the script with root '''
# import ping
import sys


def help():
 print(''''' 
Usage: 
%s <Dest_addr> <percent loss packages> <max round trip time> 
''' % (sys.argv[0]) )

# try:
#     ret = ping



# try:
#  result = ping.quiet_ping(sys.argv[1], timeout=2, count=10, psize=64)
#  if int(result[0]) == 100:
#  print 'Critical - 宕机, 丢包率:%s%% | 报警阀值: >= %s%% 或 >=%s ms' % (result[0], int(sys.argv[2]), int(sys.argv[3]))
#  sys.exit(2)
#  else:
#  max_time = round(result[1], 2)
#  if int(result[0]) < int(sys.argv[2]) and int(result[1]) < int(sys.argv[3]):
#  print 'OK - 丢包率:%s%%, 最大响应时间:%s ms | 报警阀值: >= %s%% 或 >=%s ms' % (result[0], max_time, int(sys.argv[2]), int(sys.argv[3]))
#  sys.exit(0)
#  elif int(result[0]) >= int(sys.argv[2]) or int(result[1]) >= int(sys.argv[3]):
#  print 'Warning - 丢包率:%s%%, 最大响应时间:%s ms | 报警阀值: >= %s%% 或 >=%s ms' % (result[0], max_time, int(sys.argv[2]), int(sys.argv[3]))
#  sys.exit(1)
#  else:
#  print 'Unknown'
#  sys.exit(3)
# except IndexError:
#  help()
#  sys.exit(3)