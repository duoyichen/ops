#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

# 远端服务器配置
Params = {
    "server": "122.11.59.132",
    "port": 80,
    'url': '/assets/report/',
    'request_timeout': 30,
}

# 日志文件配置

PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')


# 更多配置，请都集中在此文件中