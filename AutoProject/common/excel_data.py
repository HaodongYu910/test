#! /usr/bin/env python
# coding=utf-8

import xlrd
import os
import datetime
import logging
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。



__author__ = "vte"
__version__ = "0.0.1"

#日期线
def date_list():
    days=7
    list=[]
    today = datetime.date.today()
    for i in range(days):
        j=days-i
        new_date=(today - datetime.timedelta(days=j)).strftime("%m-%d")
        list.append(new_date)
    return list

# 七日各个app崩溃数据
def excel(day):
    datalist=[]
    today = datetime.date.today()
    name_list = ['-BoimindAndroid--崩溃信息日报.xls', '-Boimindios--崩溃信息日报.xls', '-Coinness_Android--崩溃信息日报.xls',
                 '-Coinness_International--崩溃信息日报.xls', '-Coinness_iOS--崩溃信息日报.xls']

    for k in range(day):
        l =day-k-1
        today_time = (today - datetime.timedelta(days=l)).strftime("%Y%m%d")
        #获取路径
        list = []
        for xname in name_list:
            #获取路径
            Excel_PATH = os.path.abspath(os.path.join(os.getcwd())) + "/logs/" +today_time +xname
            #验证文件
            file = os.path.exists(Excel_PATH)
            #打开excel
            if file is True:
                data = xlrd.open_workbook(Excel_PATH,encoding_override="utf-8")
                worksheet = data.sheet_by_name("Sheet1")
                nrows = worksheet.nrows  # 获取表的行数
                ncols = worksheet.ncols  # 获取表的列数
                # 读取数据
                total = 0
                for i in range(nrows):
                    if i>1:
                        cell = int(worksheet.cell_value(i, 5))
                        total =int(cell)+total
                list.append(total)
            else:
                list.append(0)
        datalist.append(list)
    return datalist

#各个app 版本崩溃率
def excel_data(versoin_list,name_list,day):
    datalist=[]
    today = datetime.date.today()
    for k in range(day):
        l =day-k-1
        today_time = (today - datetime.timedelta(days=l)).strftime("%Y%m%d")

        #获取路径
        Excel_PATH = os.path.abspath(os.path.join(os.getcwd(), "../.."))+ "/logs/" +today_time +name_list

        #打开excel
        file=os.path.exists(Excel_PATH)
        if file is True:
            data = xlrd.open_workbook(Excel_PATH,encoding_override="utf-8")
            worksheet = data.sheet_by_name("Sheet1")
            nrows = worksheet.nrows  # 获取表的行数
            ncols = worksheet.ncols  # 获取表的列数
            # 读取数据
            a_versoin = 0
            b_versoin = 0
            c_versoin = 0
            d_versoin = 0

            for i in range(nrows):
                if i>1:
                    cell = int(worksheet.cell_value(i, 5))
                    cell_versoin = str(worksheet.cell_value(i, 3))[0:5]
                    if cell_versoin == versoin_list[0]:
                        a_versoin=int(cell)+a_versoin
                    elif cell_versoin == versoin_list[1]:
                        b_versoin = int(cell) + b_versoin
                    elif cell_versoin == versoin_list[2]:
                        c_versoin = int(cell) + c_versoin
                    else:
                        d_versoin = int(cell) + d_versoin
            list = [a_versoin, b_versoin, c_versoin, d_versoin]
        else:
            list = [0, 0, 0, 0]
        datalist.append(list)
    return datalist


# 单日崩溃数据
def excel_day(name):
    today_time = datetime.date.today().strftime("%Y%m%d")
    #获取路径
    # os.path.abspath(os.path.join(os.getcwd(), "../..")) +
    Excel_PATH = "/usr/project_env/platform/logs/" +today_time + name

    file = os.path.exists(Excel_PATH)
    #打开excel
    if file is True:
        data = xlrd.open_workbook(Excel_PATH,encoding_override="utf-8")
        worksheet = data.sheet_by_name("Sheet1")
        nrows = worksheet.nrows  # 获取表的行数
        # 读取数据
        total = 0
        bug_total=0
        for i in range(nrows):
            if i>1:
                cell = int(worksheet.cell_value(i, 5))
                bug_total=bug_total+1
                total =int(cell)+total
        list=[bug_total,total]
    else:
        list = [0, 0]
    return list



# # 七日各个app崩溃数据
# def excel_rd(name,day):
#     datalist=[]
#     today = datetime.date.today()
#     #判断打开的文件名
#     if name =='':
#         name_list = ['-BoimindAndroid--崩溃信息日报.xls', '-Boimindios--崩溃信息日报.xls', '-Coinness_Android--崩溃信息日报.xls',
#                  '-Coinness&nbsp;International--崩溃信息日报.xls', '-Coinness_iOS--崩溃信息日报.xls']
#
#     # 获取几天的数据
#     for k in range(day):
#         l =day-k
#         today_time = (today - datetime.timedelta(days=l)).strftime("%Y%m%d")
#         #获取路径
#         list = []
#         for nm in name_list:
#             BASE_PATH = os.path.dirname(__file__)
#             Excel_PATH = BASE_PATH + "/tingyun/" +today_time +nm
#             #打开excel
#             try:
#                 data = xlrd.open_workbook(Excel_PATH)
#                 worksheet = data.sheet_by_name("Sheet1")
#                 nrows = worksheet.nrows  # 获取表的行数
#                 ncols = worksheet.ncols  # 获取表的列数
#                 print(worksheet)
#             except Exception as e:
#                 print("没有当天数据"%e)
#                 continue
#
#     return worksheet
#
#
# excel_rd('',0)
