

# 天眼数据抓取项目

[TOC]



## 项目简介

------

- 项目说明 ：
  1. 抓取数据：破解登录的滑动验证码和机器人检测 - （机器人检测 还未破解）
  2. 数据模型转换  爬取的数据字典 转为 数据库映射类的模型
  3. 入库 存入数据库
- 项目数据库 ： `mysql`，当然也可以是其他数据库，只需要更改其`config.py` 文件中的相关配置。
- 项目源文件介绍：
  - `main.py` - 项目入口文件
  - `models.py` - 数据库实体
  - `db_helper.py` - 数据库操作根
  - `file_helper.py` - 文件操作
  - `config.py` - 项目配置
  - `geetest2`包 - 来自于github 开源项目 破解天眼的滑动验证码
  - `spider.py` - 爬虫程序
  - `viewmodel.py` - 继承自db_helper的BaseModel 根
- 项目运行产生的文件介绍：
  - `senior_people.csv` - 公司高管信息（包含所有维度）
  - `illegals_data.csv` - 公司违规信息（所有维度）

## 一、数据库设计



### 1. 数据库表及字段详解

------

#### company(公司表)

| 字段名称     | 字段类型    | 字段属性        | 字段注解 |
| ------------ | ----------- | --------------- | -------- |
| company_id   | varchar(20) | 主键            | 公司id   |
| company_name | varchar(50) |                 | 公司名称 |
| mod_time     | datetime    | 默认值 写入时间 | 修改时间 |

#### company_person(公司人员表)

| 字段名称  | 字段类型    | 字段属性 | 字段注解 |
| --------- | ----------- | -------- | -------- |
| id        | varchar(20) | 主键     | id       |
| name      | varchar(5)  |          | 姓名     |
| age       | int         |          | 年龄     |
| sex       | varchar(1)  |          | 性别     |
| eduaction | varchar(5)  |          | 学历     |
| resume    | text        |          | 个人简介 |
| mod_time  | datetime    |          | 修改时间 |

#### executive_group(高管分组表)

| 字段名称   | 字段类型   | 字段属性 | 字段注解                        |
| ---------- | ---------- | -------- | ------------------------------- |
| group_id   | int        | 主键     | 分组id                          |
| group_name | varchar(5) |          | 分组名称-(董事会，监事会，高管) |

#### company_executive(高管表)

| 字段名称    | 字段类型    | 字段属性        | 字段注解     |
| ----------- | ----------- | --------------- | ------------ |
| id          | int         | 主键,自增       | 主键id       |
| company_id  | varchar(20) | 外键            | 公司id       |
| group_id    | int         | 外键            | 分组id       |
| person_id   | varchar(20) | 外键            | 人员id       |
| position    | varchar(50) |                 | 职称描述     |
| start_date  | date        |                 | 任职开始日期 |
| end_date    | date        |                 | 任职结束日期 |
| report_date | date        |                 | 公告日期     |
| mod_time    | datetime    | 默认值-写入时间 | 修改时间     |

#### salary_table(薪酬表)

| 字段名称                   | 字段类型    | 字段属性        | 字段注解 |
| -------------------------- | ----------- | --------------- | -------- |
| id                         | int         | 主键,自增       | 主键id   |
| company_id                 | varchar(20) | 外键            | 公司id   |
| person_id                  | varchar(20) | 外键            | 人员id   |
| money                      | varchar(10) |                 | 薪资金额 |
| number_of_shares_with_unit | varchar(10) |                 |          |
| mod_time                   | datetime    | 默认值-写入时间 | 修改时间 |

#### company_illegals(公司违规处理表)

| 字段名称                | 字段类型    | 字段属性            | 字段注解              |
| ----------------------- | ----------- | ------------------- | --------------------- |
| id                      | int         | 主键,自增           | 主键id                |
| company_id              | varchar(20) | 外键                | 违规公司id            |
| disposer                | varchar(50) | 外键                | 处理机构              |
| default_type            | varchar(10) |                     | 违规类型              |
| illegal_act_withlink    | text        |                     | 违规详情              |
| punish_type             | varchar(10) |                     | 处理类型-（惩罚类型） |
| punish_explain_withlink | text        |                     | 处理详情              |
| punish_object           | varchar(20) |                     | 被处理对象            |
| announcement_date       | date        |                     | 公告日期              |
| currency_unit           | varchar(10) |                     | 涉及金额              |
| mod_time                | datetime    | 默认值-（写入时间） | 修改时间              |



### 2. 数据库E-R图

![tianyanchadb](https://blog.bglb.work/img/20210114230750.png?x-oss-process=style/blog_img)



## 二、数据抓取

### 1. 登录 获取cookie

### 2. 搜索（普通用户只能够访问前5页数据）

- 接口： `https://www.tianyancha.com/search/p{}/key='company_name'`

### 3. 获取公开的董监高数据

- 接口 ： `https://www.tianyancha.com/pagination/seniorPeople.xhtml`

### 4. 获取公司违规信息

- 接口：`https://www.tianyancha.com/pagination/corpIllegals.xhtml`

  **违规信息太少了 根据上面的董监高接口猜出来的**



## 三、相关截图



### 1. 运行截图

![image-20210115035817689](https://blog.bglb.work/img/20210115035817.png?x-oss-process=style/blog_img)



### 2. csv文件截图

![image-20210115042149538](https://blog.bglb.work/img/20210115042149.png?x-oss-process=style/blog_img)



### 3. 数据库截图

![image-20210115042322257](https://blog.bglb.work/img/20210115042322.png?x-oss-process=style/blog_img)

![image-20210115042339227](https://blog.bglb.work/img/20210115042339.png?x-oss-process=style/blog_img)

![image-20210115042355124](https://blog.bglb.work/img/20210115042355.png?x-oss-process=style/blog_img)

![image-20210115042408204](https://blog.bglb.work/img/20210115042408.png?x-oss-process=style/blog_img)

## 四、数据呈现

**由于时间问题，这块内容未实现，下面只是一些想法**

1. 数据展示 ： 用现在的数据可视化技术（python 数据分析）（js `echart.js` 图表库）比如可以做一个 公司高管薪资水平图表
2. 数据挖掘 ：处理分析公司的违规信息，做简单的公司风险预测（还没有尝试过）

## 五、免责声明

本项目**仅仅只用与面试**（某面试）若用于其他用途，请自行承担相关责任！

