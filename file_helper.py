# -*- coding:utf-8  -*-
# @Time     : 2021-01-15 00:03
# @Author   : BGLB
# @Software : PyCharm
import csv
import os


class csv_manage(object):

    @staticmethod
    def write_lines_data(path, data):
        """
        写入csv 文件
        :param path: 文件路劲
        :param data: 数据列表
        :return:
        """
        header = data[0].keys()
        os.makedirs("".join(path.split('/', )[:-2]), exist_ok=True)
        with open(path, 'w', encoding='utf8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)
