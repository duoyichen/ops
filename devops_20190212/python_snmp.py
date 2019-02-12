#!/usr/bin/env python
# coding: utf-8
# --------------------------------
# author: duoyichen
# email: duoyichen@qq.com
# Date:  20190210 00:46
# --------------------------------

from pysnmp.hlapi import *

deviceIP = "222.73.119.242"
snmpv2Community = "ewcache-55667"

def get_ifDescr(deviceIP, snmpCommunity):
    # deviceNameOID = "1.3.6.1.2.1.1.5.0"
    # deviceNameOID = "ifDescr"
    # OID = "1.3.6.1.2.1.1.1.0"
    # OID = "1.3.6.1.2.1.1.6.0"
    OID = "1.3.6.1.2.1.1.4.0"

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(snmpCommunity),
               UdpTransportTarget((deviceIP, 161)),
               ContextData(),
               # ObjectType(ObjectIdentity(OID))
               ObjectType(ObjectIdentity('IF-MIB', 'ifDescr', 0))
               )
    )

    if errorIndication:
        print('E1:',errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))

def main():
    get_ifDescr(deviceIP, snmpv2Community)


main()
