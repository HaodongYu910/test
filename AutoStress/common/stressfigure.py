#! /usr/bin/env python
# coding=utf-8

__author__ = "vte"
__version__ = "0.0.1"
import re
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models import Q
from AutoTest.models import dictionary
from ..models import stress,stress_result
from ..serializers import stress_Deserializer
# from AutoTest.common.excel_data import *
import logging
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。

plt.rcParams['font.family'] = ['Times New Roman']
# plt.rcParams.update({'font.size': 12})

#jira 数据图表
def stressdataFigure(type):
    version = []
    modelname = []
    if type in ['lung_prediction','lung_job','lung_JZ','lung_jobJZ','lung_dy','lung_jobdy']:
        stressobj = stress.objects.filter(status=True).order_by("version")
        model = stress_result.objects.values("slicenumber").order_by("slicenumber").distinct()
    else:
        stressobj = stress.objects.filter(status=True, projectname='晨曦').order_by("version")
        model = dictionary.objects.filter(type='model')

    for i in stressobj:
        version.append(i.version)
    figureData = [version]

    for k in model:
        avg = []
        if type in ['lung_prediction','lung_job','lung_JZ','lung_jobJZ','lung_dy','lung_jobdy']:
            if k["slicenumber"] is None:
                continue
            modelname.append(k["slicenumber"])
        else:
            obj = dictionary.objects.get(id=k.id)
            modelname.append(obj.key)
        for j in version:
            try:
                if type in ['lung_prediction','lung_job','lung_JZ','lung_jobJZ','lung_dy','lung_jobdy']:
                    resultobj = stress_result.objects.get(type=type, slicenumber=str(k["slicenumber"]), version=j)
                else:
                    resultobj = stress_result.objects.get(type=type, modelname=k.id, version=j)
                avg.append(resultobj.avg)
            except:
                avgvalue = '0'
                avg.append(avgvalue)
                continue
        figureData.append(avg)
    return figureData,modelname
#
# # 绘制 创建与解决问题数据
# def dataframe(platform, sprint_version):
#     try:
#         data = Jiradata().figurs_data(platform, sprint_version)
#         starttime=(Jiradata().date_time(str(re.findall(r"(.+?)-", platform)[0]))[0]).strftime("%Y-%m-%d")
#         line(data,starttime,int(len(data)),['Problems created', 'Problems solved'])
#         imcd=figure_html()
#     except Exception as e:
#         logger.error('绘制 创建与解决问题数据',e)
#         return False
#     return imcd
#
# # 缺陷状态数据
# def frame(platform, sprint_version):
#     #获取数据
#     try:
#         status = Jiradata().bug_data(platform, sprint_version)
#         pie(status,['Closed :' + str(status[0]), 'Reopen :' + str(status[1]),
#                     'Resolved :' + str(status[2]), 'Open :' + str(status[3]),
#                     'Processing ：' + str(status[4])],[u''])
#         imcd =figure_html()
#     except Exception as e:
#         logging.exception(e)
#         return False
#     return imcd
#
# # 总崩溃图
# def crash():
#     days=7
#     today = datetime.date.today()
#     line(excel(days),(today - datetime.timedelta(days=7)).strftime("%Y%m%d"),int(days),['bishijie_Android', 'bishijie_iOS', 'CoinNess_Android', 'CoinNess_New_Android','CoinNess_iOS'])
#     line_imcd = figure_html()
#     data=excel(1)
#     pie(data[0],['bishijie_Android :'+ str(data[0][0]), 'bishijie_iOS :'+ str(data[0][1]), 'CoinNess_Android :'+ str(data[0][2]),'New_Android :'+ str(data[0][3]),'CoinNess_iOS :'+ str(data[0][4])],[u''])
#     pie_imcd = figure_html()
#     iris = """<h4 style="color:#000000">崩溃数据汇总</h4><img width="500"src="%s"><img width="500"src="%s">"""%(line_imcd,pie_imcd)
#     return iris
#
# #按 版本、崩溃率图
# def versoin_crash(list,name):
#     days=7
#     today = datetime.date.today()
#     data=excel_data(list,name,days)
#     cylindrical(data,date_list(),list)
#     cylindrical_imcd = figure_html()
#     pie(excel_day(name),['Bug_total:'+str(excel_day(name)[0]),'Crash_total:'+str(excel_day(name)[1])],['Yesterday Total'])
#     pie_imcd = figure_html()
#     iris_cylindrical = """<img width="500"src="%s">""" % cylindrical_imcd
#     iris_pie = """<img width="500"src="%s">""" % pie_imcd
#     iris = iris_cylindrical+iris_pie
#     return iris
#
#
# #画折线图
# def line(data,x_index,x_periods,z_columns):
#     df = pd.DataFrame(data,index=pd.date_range(x_index,periods=x_periods), columns=z_columns)
#     return df.plot()
#
# #画饼图
# def pie(data,x_data,title):
#     df = pd.DataFrame(data, index=x_data,columns=title)
#     return df.plot.pie(subplots=True)
#
# # #画饼图
# # def pie_x(data,x_data,title):
# #     explode =(0,0.1,0,0)
# #     plt.pie(data,explode=explode, index=x_data,shadow=True,startangle=90)
# #     plt.axis('equal')
# #     return plt.show()
#
# #柱型图
# def cylindrical(data,x_index,x_columns):
#     df = pd.DataFrame(data,index=x_index,columns=x_columns)
#     return df.plot.bar()
#
#
# # 转化html
# def figure_html():
#     # figure 保存为二进制文件
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#
#     # 图像数据转化为 HTML 格式
#     imcb = base64.b64encode(plot_data)
#     # imb = plot_data.encode('base64')   # 对于 Python 2.7可用
#     imcs = imcb.decode()
#     imcd = "data:image/png;base64," + imcs
#
#     # # lxml 库的 etree 解析字符串为 html 代码，并写入文件
#     # html = etree.HTML(root)
#     # tree = etree.ElementTree(html)
#     # tree.write('iris.html')
#     return imcd





# pandas 的 DataFrame 数据直接装换为 html 代码字符串
# url = "http://aima.cs.berkeley.edu/data/iris.csv"
# setl = urllib.request.Request(url)
# iris_p = urllib.request.urlopen(setl)
# iris = pd.read_csv(iris_p, sep=',', decimal='.', header=None, names=['测试', '开发', '运维', '运营', '产品'])
#
# iris_des = """<h1>AutoTest</h1>""" + iris.describe().T.to_html()

# matplotlib 绘制一张图
# fig,axes = plt.subplots(1,4,sharey = True)
# for n in range(4):
#     axes[n].hist( iris.iloc[:,n],bins = 15,color = 'b',alpha = 0.5,rwidth= 0.8 )
#     axes[n].set_xlabel(iris.columns[n])
# plt.subplots_adjust(wspace = 0)
