#! /usr/bin/env python
# coding=utf-8

from AutoTest.common.DbSql import mysqlDB
from jira import JIRA
from AutoTest.common.jiraData import Jiradata
from AutoTest.common.figure import data_figure,crash
from AutoTest.models import test_report,Project


from django.conf import settings

import logging,re
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


#风险点
def risk(test_version,cns_version):
    data_list = mysqlDB().selectDB("SELECT p.`name`,r.risk,r.development,r.delay,r.solution_status FROM QualityControl.test_risk r JOIN QualityControl.Project p ON r.project_id = p.id WHERE r. STATUS = 0 ORDER BY r.solution_status DESC") #获取项目信息
    list=""""""
    cn = """"""
    if len(data_list)==0:
        return """<h4 class="font-color">暂无风险</h4>"""
    else:
        for i in data_list:
            if str(i[4]) == '0':
                color = 'red'
                type = '未解决'
            elif str(i[4]) == '2':
                color = 'red'
                type = '解决中'
            else:
                color = '00A600'
                type = '已解决'
            cn = """<tr><td text-align="center">%s</td>
                                                <td>%s</td>
                                                <td>%s</td>
                                                <td>%s 天</td>                              
                                                <td bgcolor =%s>%s</td>
                                        </tr>"""%(str(i[0]),str(i[1]),str(i[2]),str(i[3]),color,type)
            list = cn + list

        risk = """<table  width="600" border="1" cellspacing="0"  text-align="center">
                                <tr  bgcolor ="#B0C4DE">
                                        <td text-align="center">项目/版本</td>
                                        <td>风险内容</td>
                                        <td>经办人</td>
                                        <td>延期时间</td>
                                        <td>解决状态</td>
                                </tr>%s</table>""" % list
        return risk

#项目计划
def project_plan():
    projectlist = Project.objects.get(status='True')
    data_list=connDB('计划','') #获取项目信息
    list=""""""

    for i in data_list:
        # # 判断进度颜色
        if str(i[5]) == '正常':
            color = '#00A600'
        elif str(i[5]) == '延期':
            color = '#FF0000'
        else:
            color = '#FFE153'

        # 判断项目计划时间是否为空
        if i[3] is None:
            end_time = ''
        elif str(i[3].strftime("%Y-%m-%d"))=="2019-01-01":
            end_time = '待定'
        else:
            end_time = str(i[3].strftime("%Y-%m-%d"))

        data="""<tr><td text-align="center">%s </td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>"%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>                                 
                                    <td bgcolor =%s>%s </td>
                            </tr>"""%(str(i[0]),str(i[4]),str(i[6]),str(i[6]),end_time,str(i[1]),str(i[2]),color,str(i[5]))
        list=data+list

    plan = """<table  width="800" border="1" cellspacing="0"  text-align="center">
                    <tr  bgcolor ="#B0C4DE">
                            <td text-align="center">项目</td>
                            <td text-align="center">版本</td>
                            <td>接口提测日期</td>
                            <td>功能提测日期</td>
                            <td>灰度测试日期</td>
                            <td>计划发布日期</td>
                            <td text-align="center">项目进度</td>
                    </tr>%s</table>"""%list
    return plan

#项目进度
def project():
    logger.info('项目进度开始')
    #projectstatus, end_date, version, status, api_date
    data_list = mysqlDB().selectDB('SELECT name,projectstatus,end_date,version,status,api_date FROM QualityControl.Project where `status`="True"') #获取项目信息
    list=""""""

    for i in data_list:
        # # 判断进度颜色
        if str(i[4]) == 'True':
            color = '#00A600'
        elif str(i[4]) == '延期':
            color = '#FF0000'
        else:
            color = '#FFE153'

        # 判断项目计划时间是否为空
        if i[2] is None:
            end_time = ''
        elif str(i[2].strftime("%Y-%m-%d"))=="2019-01-01":
            end_time = '待定'
        else:
            end_time = str(i[2].strftime("%Y-%m-%d"))

        data="""<tr><td text-align="center">%s</td>
                                    <td>%s</td>           
                                    <td>%s</td>  
                                    <td>%s</td>                           
                                    <td bgcolor =%s>正常</td>
                            </tr>"""%(str(i[0]),str(i[3]),str(i[1]),end_time,color)
        list=data+list

    project = """<table  width="800" border="1" cellspacing="0"  text-align="center">
                    <tr  bgcolor ="#B0C4DE">
                            <td text-align="center">项目</td>
                            <td text-align="center">版本</td>
                            <td text-align="center">项目进度</td>
                            <td>计划发布时间</td>
                            <td>项目状态 </td>
                    </tr>%s</table>"""%list
    logger.info('项目进度结束')
    return project

#测试标准
def standard():
    logger.info('测试标准')
    try:
        data_list = test_report.objects.get(type=1)
        list=""""""
        for i in ["H5-Main-缺陷","Web-缺陷","Server-缺陷","Boimind-APP-缺陷","CoinNess-APP-缺陷"]:
            if i=='Boimind-APP-缺陷':
                projectname='BoimindAPP'
                version = data_list.test_version
            elif i=='CoinNess-APP-缺陷':
                projectname = 'CoinNess APP'
                version = data_list.cns_version
            else:
                projectname =str(re.findall(r"(.+?)-", i)[0])
                version = data_list.cns_version +','+ data_list.test_version

            bugtotal = Jiradata().bug_priority(i,version,'','','','','')
            # # 判断进度颜色
            if str(bugtotal[0]) == '0':
                color = '#00A600'
            else:
                color = '#FF0000'
            if str(bugtotal[1]) == '0':
                color1 = '#00A600'
            else:
                color1 = '#FF0000'
            if str(bugtotal[2]) < '10':
                color2 = '#00A600'
            else:
                color2 = '#FF0000'

            data="""<tr><td text-align="center">%s</td>
                                        <td>%s</td>   
                                        <td bgcolor =%s>%s</td>           
                                        <td bgcolor =%s>%s</td>
                                        <td bgcolor =%s>%s</td>                       
                                </tr>"""%(projectname,version,color,str(bugtotal[0]),color1,str(bugtotal[1]),color2,str(bugtotal[2]))
            list=data+list
    except Exception as e:
        logger.error(e)
        return False,e

    projec_standard = """<table  width="800" border="1" cellspacing="0"  text-align="center">
                    <tr  bgcolor ="#B0C4DE">
                            <td text-align="center">项目</td>
                            <td>版本</td>
                            <td text-align="center">P0 等级缺陷</td>
                            <td text-align="center">P1 等级缺陷</td>
                            <td>P2 以下缺陷</td>
                    </tr>
                    <tr  bgcolor ="#FFE153">
                            <td text-align="center">正常上线标准</td>
                            <td>--</td>
                            <td text-align="center"> 0 个</td>
                            <td text-align="center"> 0 个</td>
                            <td>小于 10 个</td>

                    </tr>%s</table>"""%list
    logger.info('测试标准结束')
    return projec_standard

# 缺陷信息
def Bug(platform,version):
    logger.info('缺陷信息')
    jira = JIRA(settings.SITE_JIRAURL, basic_auth=('yinhang', '123456'))
    buglist=""""""
    if platform =="online":

        bug=Jiradata().search_total('','online','')#获取线上bug数据
        title="""<p style="color: red"> @经办人 注重关注</p>"""
    else:
        bug = Jiradata().search_total('',platform,version)  # 获取bug数据
        title = ("""<a href="http://jira.bishijie.com/" style="color: #0000E3"> {0} 问题列表</a>""").format(platform)
    if bug.total == 0:
        bug_list = """<p  style="color: #000000">%s 缺陷已全部修复</p>"""%platform
    else:
        for i in range(int(bug.total)):
            issue_id = bug[i].key
            # if platform == "信息服务":
            #     story_name = ''
            # else:
            #     story_name = jira.issue(issue_id).fields.issuetype  # 客户端名称

            if len(jira.issue(issue_id).fields.components):
                measures = jira.issue(issue_id).fields.components

            else:
                measures = ' '  # 模块
            priority = jira.issue(issue_id).fields.priority  # 优先级
            summary = jira.issue(issue_id).fields.summary #概要
            # cause = jira.issue(issue_id).fields.customfield_13511  # 缺陷原因
            # affect = jira.issue(issue_id).fields.versions  # 影响版本
            status =jira.issue(issue_id).fields.status  # 状态
            assignee = jira.issue(issue_id).fields.assignee  # 处理人

            if str(priority)=='Highest':
                color='#CE0000'
            elif str(priority)=='High':
                color = '#FF5151'
            elif str(priority)=='Medium':
                color = '#FF9224'
            else:
                color='#01B468'
            bugdata="""<tr><td><a href=\"http://jira.bishijie.com/browse/%s \"style="color: #0000E3"> %s</a></td>
                                        <td> %s</td>
                                        <td> %s</td>
                                        <td bgcolor = %s> %s</td>
                                        <td> %s</td>
                                        <td> %s </td>
                                </tr>"""%(str(issue_id),str(issue_id),str(summary),str(measures[0]),color,str(priority),str(assignee),str(status))
            buglist=bugdata+buglist
        bug_list = title+"""<table  width="800" border="1" cellspacing="0"  text-align="center">
                        <tr bgcolor ="#B0C4DE" >
                                <td width="100" text-align="center"> 关键字</td>
                                <td width="240" text-align="center">概要</td>
                                <td width="100">模块</td>
                                <td width="100">优先级</td>
                                <td width="80">经办人</td>
                                <td width="80" >状态</td>
                        </tr>%s</table>"""%buglist
    logger.info('缺陷信息结束')
    return bug_list

# 组装 邮件html
def html(bishijie_version,CoinNess_version):
    logger.info('组装 邮件html')
    mail_msg ="""<!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/html">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Boimind platform CoinNess_version 版本项目进度报告</title>
        <!-- <link rel="stylesheet" href="css/style.css" type="text/css"> -->
        <style type="text/css">
            *{
                font-family:Helvetica;
            }
            html, body{
                padding:0;
                margin:0;
                position:relative;
                background:url(../img/body.jpg);
                background-repeat:repeat;
                color:#fff;
                letter-spacing:1px;
                font-family:Georgia, "Times New Roman", Times, serif;
                }
    
            #container{
                width:960px;
                margin:0 auto;
            }
    
            table {
                border-collapse: collapse;
                border-spacing: 0;
                width:100%;
                -webkit-box-shadow:  0px 2px 1px 5px rgba(242, 242, 242, 0.1);
                box-shadow:  0px 2px 1px 5px rgba(242, 242, 242, 0.1);
            }
    
            .zebra {
                border: 1px solid #555;
                font-size: 8pt;
            }
    
            .zebra td {
                border-left: 1px solid #555;
                border-top: 1px solid #555;
                padding: 10px;
                text-align: left;
            }
    
            .zebra th, .zebra th:hover {
                border-left: 1px solid #555;
                border-bottom: 1px solid #828282;
                padding: 10px;
                background-color:#ddd !important;
                background-image: -webkit-gradient(linear, left top, left bottom, from(#ddd), to(#eee)) !important;
                background-image: -webkit-linear-gradient(top, #ddd, #eee) !important;
                background-image:    -moz-linear-gradient(top, #ddd, #eee) !important;
                background-image:     -ms-linear-gradient(top, #ddd, #eee) !important;
                background-image:      -o-linear-gradient(top, #ddd, #eee) !important;
                background-image:         linear-gradient(top, #ddd, #eee) !important;
                color:#000 !important;
                font-weight:normal;
            }
            .zebra{
                width: 720px;
                margin-left:50px;
            }
            .trend{
                width: 820px;
                margin-left:50px;
            }
    
            .zebra tbody tr:nth-child(even) {
                background: #fff !important;
                color:#000;
            }
    
            .zebra tr:hover *{
                background: #eeeeee;
                color: #555;
            }
    
            .zebra tr {
                background:#fff;
                color:#000;
            }
            tbody td{
                height: 20px;
                width: 920px;
            }
        </style>
        <style type="text/css">
            html, body{
                padding:0;
                margin:0;
                position:relative;
                background:url(../img/body.jpg);
                background-repeat:repeat;
                color:#fff;
                letter-spacing:1px;
                font-family:Georgia, "Times New Roman", Times, serif;
                }
    
            #container{
                width:960px;
                margin:0 auto;
            }
    
            table {
                border-collapse: collapse;
                border-spacing: 0;
                width:100%;
                -webkit-box-shadow:  0px 2px 1px 5px rgba(242, 242, 242, 0.1);
                box-shadow:  0px 2px 1px 5px rgba(242, 242, 242, 0.1);
            }
    
            .bug {
                border: 1px solid #555;
                font-size: 8pt;
            }
    
            .bug td {
                border-left: 1px solid #555;
                border-top: 1px solid #555;
                padding: 5px;
                text-align: left;
            }
    
            .bug th, .bug th:hover {
                border-left: 1px solid #555;
                border-bottom: 1px solid #828282;
                padding: 5px;
                background-color:#ddd !important;
                background-image: -webkit-gradient(linear, left top, left bottom, from(#ddd), to(#eee)) !important;
                background-image: -webkit-linear-gradient(top, #ddd, #eee) !important;
                background-image:    -moz-linear-gradient(top, #ddd, #eee) !important;
                background-image:     -ms-linear-gradient(top, #ddd, #eee) !important;
                background-image:      -o-linear-gradient(top, #ddd, #eee) !important;
                background-image:         linear-gradient(top, #ddd, #eee) !important;
                color:#000 !important;
                font-weight:normal;
            }
            .bug{
                width: 920px;
                margin-left:50px;
            }
    
            .bug tbody tr:nth-child(even) {
                background: #fff !important;
                color:#000;
            }
    
            .bug tr:hover *{
                background: #eeeeee;
                color: #555;
            }
    
            .bug tr {
                background:#fff;
                color:#000;
            }
            tbody td{
                height: 20px;
                width: 920px;
            }
        </style>
        <style type="text/css">
            body{
                padding: 0 5%;
            }
            .font-color{
                color: black;
            }
            .font-color-red{
                color: red;
            }
            .font-color-darkblue{
                color: darkblue;
            }
            .sj{
                color: black;
                text-indent: 5%;
            }
            .db{
                color: green;
                text-indent:9% ;
            }
            .ndb{
                color: red;
                text-indent:9% ;
            }
            .bdb{
                color: black;
                text-indent:9% ;
            }
            .image{
                width: 620px;
                height: 220px;
            }
        </style>
    </head>
    <body>
    <h1 style="color:black;width: auto"> Boimind & CoinNess 项目进度报告：</h1>
    <div id="chapter1">
        <h2 style="color: red">一、风险及项目进度周知</h2>
        <article>
            <h3 style="color: red">1.1、项目风险周知：</h3>
            """+ risk(bishijie_version,CoinNess_version) +"""
            <h3 style="color: #000000">1.2、项目进度</h3>
            """+ project() +"""
            <h3 style="color: #000000">1.3、上线标准</h3>
           """+ standard()  +"""
        </article>
    </div>
    <div id="chapter4">
        <h2 class="font-color">二、Bug详细情况</h2>
        <h3 class="font-color">2.1、缺陷收敛图表</h3>
        """+ data_figure("Boimind-APP-缺陷",bishijie_version) +"""
        """+ data_figure("CoinNess-APP-缺陷",CoinNess_version) +"""
        """+ data_figure("Server-缺陷",str(bishijie_version)+","+str(CoinNess_version))+"""
        <p> </p>
        <p class="sj"\>2.1.1 未解决缺陷明细</p>
        """+Bug("Boimind",bishijie_version)+"""
        <p></p>"""+Bug("CoinNess",CoinNess_version)+"""
        <p></p>"""+Bug("信息服务",bishijie_version+','+CoinNess_version)+"""
        <p></p>
        <h3 class="font-color">2.2 线上缺陷情况</h3>
        """+ Bug("online",'')  +"""
    </div>
     <div id="chapter2">
        <h2 class="font-color">三、各版本Crash次数</h2>
        """+ crash()  +"""
    </div>
   
    
    <div id="chapter3">
        <h2 class="font-color">四、排期计划</h2>
        <p class="font-color">QA测试计划排期详见：</p>
        <a href="http://wiki.bishijie.com/pages/viewpage.action?pageId=3914265">查看排期点击这里</a><br/>
    </div>
    <br><br>
    <div class="font-color">
    <p>________________________</p>
    <p><b>测试组 | QA</b></p>
    <p><img src="https://img.bishijie.com/news_154268282784004.jpg" style="height: 100px; width: 100px"></img></p>
    <p>邮 箱：qa@bishijie.com</p>
    <p>地 址：北京市朝阳区望京街道浦项中心27层</p>
    </div>
    </body>
    </html>
    """
    return mail_msg
