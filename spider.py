# -*- coding:utf-8  -*-
# @Time     : 2021-01-11 13:49
# @Author   : BGLB
# @Software : PyCharm


"""
html 解析
1. 搜索公司名称
2. 拿到公司id
3. 请求相关接口 拿到数据 返回list
"""
import hashlib
import json
import random
import re
import time

import requests
from lxml import html

from geetest2.geetest import crack

etree = html.etree


class SpiderTools(object):

    @staticmethod
    def get_cookie_acw_sc__v2(arg1: str) -> str:
        """
        js 设置cookie 反爬破解
        :param arg1:
        :return:
        """
        _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17,
                     0x19,
                     0xd,
                     0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3,
                     0x1c,
                     0x22, 0x25, 0xc, 0x24]
        _0x4da0dc = []
        _0x12605e = ''
        for i in _0x4b082b:
            _0x4da0dc.append(arg1[i-1])
        _0x12605e = "".join(_0x4da0dc)

        _0x5a5d3b = ''

        for i in range(len(_0x12605e)):
            if i%2 != 0: continue
            _0x401af1 = int(_0x12605e[i: i+2], 16)
            _0x105f59 = int("3000176000856006061501533003690027800375"[i: i+2], 16)
            _0x189e2c_10 = (_0x401af1 ^ _0x105f59)
            _0x189e2c = hex(_0x189e2c_10)[2:]
            if len(_0x189e2c) == 1:
                _0x189e2c = '0'+_0x189e2c
            _0x5a5d3b += _0x189e2c
        return _0x5a5d3b

    @staticmethod
    def encrypt_md5(password: str) -> str:
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        return md5.hexdigest()

    @staticmethod
    def robot_check():
        """
        机器人检测 破解 为实现
        :return:
        """
        '/captcha/checkCaptcha.json?captchaId=0e00dea5-b712-4f6f-ae14-e80f4a76e025&clickLocs=' \
        '[{"x":219,"y":69},{"x":277,"y":44},{"x":39,"y":39}]' \
        '&t=1610420286702&_=1610420087661'
        pass

    @staticmethod
    def list_set(data:list):
        data_set = []
        for item in data:
            if item not in data_set:
                data_set.append(item)
        return data_set


class TianyanchaSpider(object):

    def __init__(self):
        self.session = requests.Session()
        self.referer = 'https://www.tianyancha.com/'
        self.cookies = None
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'www.tianyancha.com',
            'Origin': 'https://www.tianyancha.com',
            'Pragma': 'no-cache',
            'Referer': self.referer,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.67',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.phone_number = None
        self.password = None

    def __get_captcha(self):
        url = 'https://www.tianyancha.com/verify/geetest.xhtml'
        payload = {
            'uuid': int(time.time()*1000)
        }

        # post payload 请求需要加上这样的头
        self.headers['Content-Type'] = 'application/json; charset=UTF-8'
        # 第一次请求拿到arg1参数
        result = self.session.post(url, data=json.dumps(payload), headers=self.headers)
        arg1 = re.search('arg1=\'[0-9A-Z]+\'', result.text)
        if arg1 is not None:
            arg1 = arg1.group().replace('arg1=', '').replace('\'', '')
            cookie = {'acw_sc__v2': SpiderTools.get_cookie_acw_sc__v2(arg1)}
            # print(cookie)
            # 携带cookie再次访问
            result = self.session.post(url, data=json.dumps(payload), headers=self.headers, cookies=cookie)
        result = result.json()
        if result['state'] == 'ok':
            return result['data']['gt'], result['data']['challenge'], self.referer
        return None

    def __get_validate(self) -> dict:
        """
        返回验证码的validate值
        :return:
        """
        while True:
            data = self.__get_captcha()
            if data:
                break
            # print(data)
            time.sleep(random.random())
        result = crack(data[0], data[1], data[2])
        return result

    def __get_cookies(self) -> dict:
        """
        获取cookies
        :return:
        """
        url = "https://www.tianyancha.com/cd/login.json"
        if self.phone_number is None or self.password is None:
            raise Exception("请先登录！")
        payload = {
            'mobile': self.phone_number,
            'cdpassword': SpiderTools.encrypt_md5(self.password),
            'loginway': "PL",
            'autoLogin': False,
        }

        """
        "mobile":"",
        "cdpassword":"MD5()",
        "loginway":"PL",
        "autoLogin":false,
        "type":"",
        "challenge":"abf094a08dcc513a92f2240f6afa92f77h",
        "validate":"5b3ab89b10a728d8d16e773d232adbe7",
        "seccode":"5b3ab89b10a728d8d16e773d232adbe7|jordan"

        """

        while True:
            result_val = self.__get_validate()
            if result_val['data']['success'] == 1:
                break
        validate = {
            'challenge': result_val["challenge"],
            'validate': result_val["data"]['validate'],
            'seccode': '{}|jordan'.format(result_val["data"]['validate'])
        }
        payload.update(validate)
        resp = self.session.post(url=url, data=json.dumps(payload), headers=self.headers)
        if resp.json().get('data') is None:
            raise Exception("账号密码不匹配！")
        cookies = {}
        for key, value in self.session.cookies.items():
            cookies[key] = value
        cookies["auth_token"] = resp.json().get('data').get("token")
        return cookies

    def login(self, phone_number, password: str):
        self.phone_number = phone_number
        self.password = password
        self.cookies = self.__get_cookies()
        return True

    def __parse_pagination(self, company_id: int, page_interface, **kwargs) -> list:
        """
        分页数据解析
        :param page_type: 页面类型
        :param company_id: 公司类型
        :return: 所有分页数据的列表
        """
        data_text_list = []
        path = "/pagination/{}.xhtml".format(page_interface)
        url = self.headers['Origin']+path
        params = {
            'ps': kwargs.get('ps', 1),  # 数据条数
            'pn': kwargs.get('pn', 1),
            'id': company_id,
            'type': kwargs.get('data_type', 1)
        }
        is_login, eroot = self.__get_eroot(url, params=params)
        if eroot is None:
            return data_text_list
        page_total_text = eroot.xpath('//ul[@class="pagination"]/@page-total')
        page_count = 1
        if len(page_total_text) != 0:
            params['ps'] = 10
            page_total = int(page_total_text[0])
            if page_total > params['ps']:
                page_count = int(page_total)/params['ps']+1

        for pn in range(page_count):
            params['pn'] = pn+1
            time.sleep(1)
            is_login, eroot = self.__get_eroot(url, params=params)
            if eroot is None:
                continue
            script_text_list = eroot.xpath('//script[@type="text/html"]/text()')
            data_text_item_list = [dict(json.loads(item)) for item in script_text_list]
            data_text_list = data_text_list+data_text_item_list
        return data_text_list

    def __get_eroot(self, url, method='get', **kwargs) -> tuple:
        """
        解析响应内容 检查 机器人检测
        没有登录成功 抛出错误
        有机器人检测 抛出错误
        :param url: 请求url
        :param method: post get
        :param kwargs:
        :return: True, eroot
        """
        if method == 'get':
            response = self.session.get(url, params=kwargs.get('params', dict()), cookies=self.cookies,
                                        headers=self.headers)
        if method == 'post':
            response = self.session.post(url, data=kwargs.get('data', dict()), cookies=self.cookies,
                                         headers=self.headers)

        eroot = etree.HTML(response.content.decode('utf8'))
        if eroot is None and response.status_code == 200:
            return True, None

        login_text = eroot.xpath('//*[@id="web-content"]/div/div[2]/div/div/div[3]/div[1]/div[3]/div[1]/text()')
        robot_text = eroot.xpath('/html/body/div[2]/div/div/div[1]/text()')
        if len(login_text) != 0 and '手机扫码登录' in login_text:
            self.cookies = self.__get_cookies()
            return False, None
        if (len(robot_text) != 0 and '我们只是确认一下你不是机器人，' in robot_text) or "antirobot.tianyancha.com" in response.url:
            raise Exception('您被识别为机器人！请在天眼官网正常登录一次，然后重新运行！')
        return True, eroot

    def search_company(self, company_name_key) -> list:
        """
        搜索公司
        :param company_name_key: 公司名称关键字
        :return: 返回搜索关键字公司 list
        """
        self.referer = "https://www.tianyancha.com"
        url = "https://www.tianyancha.com/search/p{}/"
        company_data_list = []
        page_count = 5  # 普通用户 最多访问五页
        i = 0
        while i < page_count:
            is_login, eroot = self.__get_eroot(url.format(i+1), params={"key": company_name_key})
            _count = len(eroot.xpath('//ul[@class="pagination"]/li'))
            # print(_count)
            if _count < page_count:
                page_count = _count
            company_link_div = eroot.xpath(
                '//div[contains(@id,"search_company_")]//div[@class="search-result-single  "]')
            for link in company_link_div:
                name = link.xpath('.//div[@class="info"]//text()')[0]
                if company_name_key in name or name in company_name_key:  # 过滤掉公司历史名称
                    item = {
                        "company_name": name,
                        "company_id": link.xpath('./@data-id')[0]
                    }
                    # print(item)
                    company_data_list.append(item)
            i = i+1
        return SpiderTools.list_set(company_data_list)

    def get_senior_people(self, cmp_id) -> list:
        """
        拿到公司高管信息
        :param cmp_id: 公司id
        :return: 返回公司高管信息 list
        """
        page_interface = "seniorPeople"

        data_text_list = []
        for _type in range(1, 4):  # _type 代表公司高管分类 - {"董事会":1,"监事会"：2, "高管"：3}
            item_list = self.__parse_pagination(cmp_id, page_interface, data_type=_type)
            data_text_list = data_text_list+item_list
        return SpiderTools.list_set(data_text_list)

    def get_company_illegals(self, cmp_id) -> list:
        """
        :param
        cmp_id: 公司id
        :return: list
        返回公司违规数据 list
        """
        self.referer = "https://www.tianyancha.com"
        page_interface = "corpIllegals"
        data_text_list = self.__parse_pagination(cmp_id, page_interface)

        return SpiderTools.list_set(data_text_list)


if __name__ == '__main__':
    spider = TianyanchaSpider()
    spider.login('18298892447', 'abc123abcd1234')
    company_search_list = spider.search_company('云南白药集团股份有限公司')
    print(company_search_list)
    # people_data = spider.get_senior_people(company_search_list[0]["company_id"])
    # print(people_data)
    people_data1 = spider.get_senior_people("7628734")
    print(people_data1)

    # illegals_data = spider.get_company_illegals(company_search_list[0]["company_id"])
    # print(illegals_data)
    illegals_data1 = spider.get_company_illegals("7628734")
    print(illegals_data1)
