# -*- coding:utf-8  -*-
# @Time     : 2021-01-11 23:28
# @Author   : BGLB
# @Software : PyCharm
from sqlalchemy import and_

import models
from config import check_config
from db_helper import create_db
from file_helper import csv_manage
from spider import TianyanchaSpider
from viewmodel import *


def save_to_database(_com_id=0, company_data=None, com_people_data=None, com_illegals_data=None):
    """
    入库操作
    :param _com_id:
    :param company_data:
    :param com_people_data:
    :param com_illegals_data:
    :return:
    """
    _company_person_list = []
    _company_senior_list = []
    _company_illegals_list = []
    _company_salary_list = []
    _company_list = []
    if company_data:
        for item in company_data:
            rows = CompanyModel().query().get(str(item["company_id"]))
            # print(rows)
            if rows is None:
                model = models.Company(**item)
                _company_list.append(model)
        CompanyModel().write_all_data(_company_list)
        print("公司信息入库完毕")

    if com_people_data:
        for item in com_people_data:
            person_id = str(item['id'])
            company_id = str(item['cid'])
            group_id = str(item['managerGroup'])
            rows = PersonModel().query().get(person_id)
            # print(rows)
            if rows is None:
                model = models.CompanyPerson(**item)
                _company_person_list.append(model)
            rows = SalaryTableModel().query().filter(
                and_(models.SalaryTable.company_id == company_id, models.SalaryTable.person_id == person_id))
            # print(rows.first())
            if rows.first() is None:
                model = models.SalaryTable(**item)
                _company_salary_list.append(model)
            rows = CompanyExecutiveModel().query().filter(
                and_(models.CompanyExecutive.company_id == company_id, models.CompanyExecutive.person_id == person_id,
                     models.CompanyExecutive.group_id == group_id))
            if rows.first() is None:
                model = models.CompanyExecutive(**item)
                _company_senior_list.append(model)
        PersonModel().write_all_data(_company_person_list)  # 公司人员信息入库
        CompanyExecutiveModel().write_all_data(_company_senior_list)  # 公司高管信息入库
        SalaryTableModel().write_all_data(_company_salary_list)  # 公司薪酬信息入库
        print({"{}-{}-员工岗位及员工薪酬-入库完毕".format(com_name, com_id)})
    # 公司违规处理
    if com_illegals_data and _com_id != 0:
        for item in com_illegals_data:
            rows = CompanyIllegalModel().query().get(item['disposerGid'])
            if rows is None:
                model = models.CompanyIllegal(_com_id, **item)
                _company_illegals_list.append(model)
        CompanyIllegalModel().write_all_data(_company_illegals_list)  # 公司违规信息入库

        print({"{}-{}-违规信息入库-入库完毕".format(com_name, com_id)})


if __name__ == '__main__':
    check_config()  # 检查数据库配置
    create_db()  # 初始化数据库，请确保config里面的数据库存在
    csv_dir = "./csv/"
    spider = TianyanchaSpider()
    print("登录中……")
    spider.login(phone_number='18298892447', password='abc123abcd1234')
    print("登录成功")
    search_key = ['云南白药', '长沙景嘉微']
    for key in search_key:
        print("{}搜索中……".format(key))
        company_search_data = spider.search_company(key)
        print("关键字-{}共有{}家公司".format(key, len(company_search_data)))

        if len(company_search_data) > 0:
            save_to_database(company_data=company_search_data)
        for company in company_search_data[:5]:
            com_name = company['company_name']
            com_id = company['company_id']
            people_data = spider.get_senior_people(com_id)
            illegals_data = spider.get_company_illegals(com_id)

            print("{}-高管人数-{}".format(com_name, len(people_data)))
            print("{}-违规处理数量-{}".format(com_name, len(illegals_data)))

            for item in people_data:
                item['company_name'] = com_name
                item['numberOfSharesWithUnit'] = item.get('numberOfSharesWithUnit', '0')
                item['shareUnit'] = item.get('shareUnit', '股')

            if len(people_data) > 0:
                csv_manage.write_lines_data(csv_dir+"senior_people.csv", people_data)
            if len(illegals_data) > 0:
                csv_manage.write_lines_data(csv_dir+"illegals_data.csv", illegals_data)

            save_to_database(_com_id=com_id, com_people_data=people_data, com_illegals_data=illegals_data)
