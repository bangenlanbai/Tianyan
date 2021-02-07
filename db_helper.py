# -*- coding:utf-8  -*-
# @Time     : 2021-01-14 21:49
# @Author   : BGLB
# @Software : PyCharm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import ENGINE_STR
from models import metadata, ExecutiveGroup


def create_db():
    """
    初始化数据库，请保证config.py 里面配置的数据库已经存在！
    :return:
    """
    # 清空数据库
    metadata.drop_all()
    # 创建models 下 的所有表
    try:
        metadata.create_all()
        group_model = BaseModel(ExecutiveGroup)
        models = [
            ExecutiveGroup(group_id=1, group_name='董事会'),
            ExecutiveGroup(group_id=2, group_name='监事会'),
            ExecutiveGroup(group_id=3, group_name='高管'),
        ]
        group_model.write_all_data(models)
        print("初始化数据库成功")
    except Exception as e:
        print("初始化数据库失败")


class BaseModel(object):

    def __init__(self, model):
        self.session = sessionmaker(bind=create_engine(ENGINE_STR))()
        self.model = model

    def write_single_data(self, data):
        try:
            self.session.add(data)
            self.session.commit()
        except():
            self.session.rollback()
        finally:
            self.session.close()

    def write_all_data(self, data):
        try:
            # print(data)
            self.session.add_all(data)
            self.session.commit()
        except():
            self.session.rollback()
        finally:
            self.session.close()

    def query(self):

        return self.session.query(self.model)

    def close_session(self):
        if self.session:
            self.session.close()

    def __del__(self):
        self.close_session()


if __name__ == '__main__':
    create_db()
