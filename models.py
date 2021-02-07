# coding: utf-8
import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Text, text, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config import ENGINE_STR

Base = declarative_base(ENGINE_STR)
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'company'

    company_id = Column(String(20), primary_key=True, autoincrement=False)
    company_name = Column(VARCHAR(50), nullable=False)
    mod_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def __init__(self, **kwargs):
        self.company_name = str(kwargs.get('company_name'))
        self.company_id = str(kwargs.get('company_id'))

    def __str__(self):
        return "{}-{}".format(self.company_name, self.company_id)


class CompanyPerson(Base):
    __tablename__ = 'company_person'

    id = Column(String(20), primary_key=True, autoincrement=False)
    name = Column(VARCHAR(5), nullable=False)
    age = Column(Integer)
    sex = Column(VARCHAR(1), server_default=text("'男'"))
    education = Column(VARCHAR(5))
    resume = Column(Text)
    mod_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def __init__(self, **kwargs):
        self.id = str(kwargs.get('id'))
        self.name = kwargs.get('name')
        self.sex = kwargs.get('sex', None)
        self.age = kwargs.get('age', 0)
        self.education = kwargs.get('education', '不详')
        self.resume = kwargs.get('resume', '暂无简介')

    def __str__(self):
        return "{}-{}".format(self.name, self.id)


class ExecutiveGroup(Base):
    __tablename__ = 'executive_group'

    group_id = Column(Integer, primary_key=True, autoincrement=False)
    group_name = Column(VARCHAR(5), nullable=False)

    def __str__(self):
        return "{}-{}".format(self.group_name, self.group_id)

    # def __init__(self):


class CompanyExecutive(Base):
    __tablename__ = 'company_executive'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(ForeignKey('company.company_id'), index=True)
    group_id = Column(ForeignKey('executive_group.group_id'), nullable=False, index=True)
    position = Column(VARCHAR(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    report_date = Column(Date, nullable=False)
    mod_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    person_id = Column(ForeignKey('company_person.id'), nullable=False, index=True)

    company = relationship('Company')
    group = relationship('ExecutiveGroup')
    person = relationship('CompanyPerson')

    def __init__(self, **kwargs):
        self.position = kwargs.get('position')
        strip_index = str(kwargs.get('term')).index('至')
        self.start_date = str(kwargs.get('term')[:strip_index])
        self.end_date = str(kwargs.get('term')[strip_index+1:])
        self.report_date = kwargs.get('reportDate')
        self.person_id = str(kwargs.get('id'))
        self.group_id = int(kwargs.get('managerGroup'))
        self.company_id = str(kwargs.get('cid'))

    def __str__(self):
        return "{}-{}-{}".format(self.group_id, self.id, self.position)


class CompanyIllegal(Base):
    __tablename__ = 'company_illegals'

    id = Column(String(20), primary_key=True)
    company_id = Column(ForeignKey('company.company_id'), index=True)
    disposer = Column(VARCHAR(50))
    default_type = Column(VARCHAR(10))
    illegal_act_withlink = Column(Text)
    punish_type = Column(VARCHAR(10))
    punish_explain_withlink = Column(Text)
    punish_object = Column(VARCHAR(20))
    announcement_date = Column(Date)
    currency_unit = Column(VARCHAR(10))

    mod_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    company = relationship('Company')

    def __init__(self, company_id, **kwargs):
        self.company_id = str(company_id)
        self.id = str(kwargs.get('disposerGid'))
        self.disposer = kwargs.get('disposer')
        self.default_type = kwargs.get('default_type')
        self.illegal_act_withlink = kwargs.get('illegalActWithLink')
        self.punish_type = kwargs.get('punish_type')
        self.punish_object = kwargs.get('punish_object')
        self.punish_explain_withlink = kwargs.get('punishExplainWithLink')
        time_stamp = int(kwargs.get('announcement_date'))/1000
        self.announcement_date = datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d")
        self.currency_unit = kwargs.get('currency_unit')

    def __str__(self):
        return "{}-{}".format(self.id, self.company_id)


class SalaryTable(Base):
    __tablename__ = 'salary_table'

    id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('company_person.id'), nullable=False, index=True)
    company_id = Column(ForeignKey('company.company_id'), index=True)
    money = Column(VARCHAR(10))
    number_of_shares_with_unit = Column(VARCHAR(10))
    mod_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    company = relationship('Company')
    person = relationship('CompanyPerson')

    def __init__(self, **kwargs):
        self.person_id = str(kwargs.get('id'))
        self.company_id = str(kwargs.get('cid'))
        self.number_of_shares_with_unit = kwargs.get('numberOfSharesWithUnit')
        self.money = kwargs.get('salary')

    def __str__(self):
        return "{}-{}-{}".format(self.money, self.person_id, self.company_id)
