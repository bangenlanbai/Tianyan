# -*- coding:utf-8  -*-
# @Time     : 2021-01-09 18:31
# @Author   : BGLB
# @Software : PyCharm


# 数据库配置
DBCONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'tianyanchadb',
    'charset': 'UTF8',
}


def check_config():
    for k, v in DBCONFIG.items():
        if v in [None, '', 0, '0']:
            raise KeyError("您未正确配置数据库")


ENGINE_STR = "{}+mysqlconnector://{user}:{password}@{host}:{port}/{database}".format("mysql", **DBCONFIG)
