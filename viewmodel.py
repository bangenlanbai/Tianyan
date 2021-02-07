# -*- coding:utf-8  -*-
# @Time     : 2021-01-15 00:19
# @Author   : BGLB
# @Software : PyCharm

from db_helper import BaseModel
from models import *


class PersonModel(BaseModel):
    def __init__(self):
        super().__init__(CompanyPerson)


class CompanyModel(BaseModel):
    def __init__(self):
        super().__init__(Company)


class CompanyExecutiveModel(BaseModel):
    def __init__(self):
        super().__init__(CompanyExecutive)


class CompanyIllegalModel(BaseModel):
    def __init__(self):
        super().__init__(CompanyIllegal)


class SalaryTableModel(BaseModel):
    def __init__(self):
        super().__init__(SalaryTable)
