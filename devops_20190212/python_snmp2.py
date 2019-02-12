#!/usr/bin/env python
# coding: utf-8
# --------------------------------
# author: duoyichen
# email: duoyichen@qq.com
# Date:  20190210 02:59
# --------------------------------

#from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json

class GetSnmp():
    #oid列表
    def make_list(self,*oid):
        oid_list = []
        for o in oid:
            oid_list.append(o)
        return oid_list

    #获取snmp信息
    def info(self,oid,ip,commu):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(commu),
            cmdgen.UdpTransportTarget((ip, 161)),
            oid,
        )
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1][0] or '?'
                    )
                )
            else:
                var_dict={}
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        var_dict[name.prettyPrint()]=str(val.prettyPrint())
                return var_dict

    #循环oid表，提取整理信息
    def get_info(self,oid,ip,commu='ewcache-55667'):
        info_dict={}
        for o in oid:
            info = self.info(o,ip,commu)
            info_dict[o]=info
        info_json = json.dumps(info_dict,indent=4)
        return info_json

if __name__ == "__main__":
    sysName  = "1.3.6.1.2.1.1.5"
    sysDescr = "1.3.6.1.2.1.1.1"
    ifNumber = "1.3.6.1.2.1.2.1"
    ifDescr = "1.3.6.1.2.1.2.2.1.2"
    ifInOctet = "1.3.6.1.2.1.2.2.1.10"
    ifOutOctet = "1.3.6.1.2.1.2.2.1.16"
    ifInUcastPkts = "1.3.6.1.2.1.2.2.1.11"
    ifOutUcastPkts = "1.3.6.1.2.1.2.2.1.17"
    ipNetToMediaPhysAddress = "1.3.6.1.2.1.4.22.1.2"
    ipOperStatus = "1.3.6.1.2.1.2.2.1.8"
    #实例化类
    test = GetSnmp()

    #生成list
    oid_list = test.make_list(
        sysName,
        # sysDescr,
        ifNumber,
        ifDescr,
        ifInOctet,
        ifOutOctet,
        # ifInUcastPkts,
        # ifOutUcastPkts,
        # ipNetToMediaPhysAddress,
        # ipOperStatus,
    )
    #输出信息
    info = test.get_info(oid_list,"222.73.119.242")
    print(info)