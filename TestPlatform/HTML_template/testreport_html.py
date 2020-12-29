#! /usr/bin/env python
# coding=utf-8

from TestPlatform.common.DbSql import mysqlDB
from jira import JIRA
from TestPlatform.common.jiraData import Jiradata
from TestPlatform.common.figure import data_figure,crash
from TestPlatform.models import test_report,Project


from django.conf import settings

import logging
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


#项目计划
def project_plan():
    projectlist = Project.objects.get(status='True')
    data_list="" #获取项目信息
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

def total(str):
    logger.info('Bug总数')
    try:
        platform = "'Web','Server-缺陷','H5-Main-缺陷','CoinNess-APP-缺陷','Boimind-APP-缺陷'"
        data_list = test_report.objects.get(type=2)
        version = '"{0}","{1}"'.format(data_list.test_version,data_list.cns_version)
        total = Jiradata().bugtotal(platform,version,str)
    except Exception as e:
        logger.error(e)
        return False,e

    return total

#Bug详情
def buglist():
    logger.info('Bug详情')
    try:
        list = """"""
        data_list = test_report.objects.get(type=2)

        for i in ['Web','Server-缺陷','H5-Main-缺陷','CoinNess-APP-缺陷','Boimind-APP-缺陷' ]:
            buglist = []
            if i=='Boimind-APP-缺陷':
                version = data_list.test_version
            elif i=='CoinNess-APP-缺陷':
                version = data_list.cns_version
            elif i=='H5 Main-缺陷':
                version = '"{0}","{1}"'.format(data_list.test_version,data_list.cns_version)
            elif i=='Server-缺陷':
                version  = '"{0}","{1}"'.format(data_list.test_version,data_list.cns_version)

            elif i=='Web':
                version  = '"{0}","{1}"'.format(data_list.test_version,data_list.cns_version)

            for j in['最高','高','中','低','较低']:
                bugtotal = Jiradata().bug_priority(i,version,'2019-01-01','','"Open", "Progress", "Reopened","Resolved","Closed"','',[j])
                buglist.append(bugtotal)

            data="""<tr><td text-align="center" bgcolor ="#B0C4DE">%s</td>
                                        <td bgcolor ="#FF0000">%s</td> 
                                        <td bgcolor ="#FF3333">%s</td>   
                                        <td bgcolor ="#FFFF00">%s</td>           
                                        <td bgcolor ="#0033FF">%s</td>
                                        <td bgcolor ="#33FF33">%s</td>                       
                                </tr>"""%(i,buglist[0],buglist[1],buglist[2],buglist[3],buglist[4])
            list=data+list

    except Exception as e:
        logger.error(e)
        return False,e

    flist = """<table  width="800" border="1" cellspacing="0"  text-align="center">
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
    return list

# 缺陷信息
def Bug(platform,version):
    logger.info('缺陷信息')
    jira = JIRA(settings.SITE_JIRAURL, basic_auth=("yinhang", "asd123456"))
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
            bugdata="""<tr><td><a href=\"http://jira.bishijie.com/browse/ %s \"style="color: #0000E3"> %s</a></td>
                                        <td> %s</td>
                                        <td>" %s</td>
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
def report_html(test_version,cns_version,content):
    logger.info('组装 邮件html')
    mail_msg ="""<!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/html">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Boimind bishijie_version CoinNess_version 版本发布周知&质量报告</title>
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
    <h1 style="color:black;width: auto"> Boimind【"""+test_version +"""】& CoinNess【"""+cns_version+"""】版本发布周知&质量报告</h1>
    <div id="chapter1">
        <h2 style="color: red">一、项目描述</h2>
        <article>
            <h3 style="color: #000000">"""+content[0] +""""</h3>
        </article>
    </div>
    <div id="chapter4">
        <h2 class="font-color">二、需求上线情况</h2>
         <table  width="800" border="1" cellspacing="0"  text-align="center">
                        <tr bgcolor ="#B0C4DE" >
                                <td width="100" text-align="center"> 业务需求</td>
                                <td width="240" text-align="center">需求</td>
                                <td width="100">PM</td>
                                <td width="100">测试</td>
                                <td width="80">上线状态</td>
                                <td width="80" >状态</td>
                        </tr>
                        """+content[1]+"""
         </table>
    </div>
     <div id="chapter2">
        <h2 class="font-color">三、Case执行情况</h2>
        <table  width="800" border="1" cellspacing="0"  text-align="center">
                        <tr bgcolor ="#B0C4DE" >
                                <td width="100" text-align="center"> 项目列</td>
                                <td width="240" text-align="center">相关参数</td>
                                <td width="100">覆盖设备</td>
                                <td width="100">验收负责人</td>
                        </tr>
                        <tr bgcolor ="#B0C4DE" >
                                <td width="100" text-align="center"> 用例执行情况</td>
                                <td width="240" text-align="center">"""+content[2]+"""
                                </td>
                                <td width="100">Android：三星S7、vivo X9i、红米note 4x、<br>小米 MI 5、华为 P10、华为 P10 Plus、
                                华为Mate 9、<br>vivo X20、一加 5T、华为mate10、小米 MI 5等<br>
                                iOS：iPhone SE、5s、6s plus、6s、7 plus、8 plus、<br>iPhoneX，iPhone XS max</td>
                                <td width="100">"""+content[3]+"""
                                </td>
                        </tr>
                        <tr bgcolor ="#B0C4DE" >
                                <td width="100" text-align="center"> 相关的case地址</td>
                                <td width="440" text-align="center">Boimind&CoinNess</td>
                        </tr>
         </table>
    </div>
    
    <div id="chapter3">
        <h2 class="font-color">四、缺陷明细</h2>
        <h3 style="color: red">1.   本版本共"""+total("'Closed','Reopened','Resolved','open','Progress'")+"""个 bug，己解决 """+total("'Closed','Resolved'")+"""个 </h3>
        <h3 style="color: #000000">2.整体Bug jira链接信息：</h3>
        <a href="http://wiki.bishijie.com/pages/viewpage.action?pageId=3914265">点击查看</a><br/>
        <p class="font-color">Bug详情：</p>
        <table  width="800" border="1" cellspacing="0"  text-align="center">
            <tr bgcolor ="#B0C4DE" >
                <td width="300" text-align="center"> 方向/优先级</td>
                <td bgcolor ="#FF0000" width="100" text-align="center">Highest</td>
                <td bgcolor ="#FF3333" width="100">High</td>
                <td bgcolor ="#FFFF00" width="100">Medium</td>
                <td bgcolor ="#0033FF" width="100">Low</td>
                <td bgcolor ="#33FF33" width="100">Lowest</td>
            </tr>"""+buglist()+"""</table>
    </div>
    <div id="chapter3">
        <h2 class="font-color">五、性能/压力测试   </h2>
        <p class="font-color">性能测试报告地址：</p>
        <a href="http://wiki.bishijie.com/pages/viewpage.action?pageId=3914265">查看点击</a><br/>
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
    # 生成html报告
    name = test_version +"&"+ cns_version+".html"
    with open(name, 'wb') as f:
        f.write(mail_msg.encode('utf-8'))
    return mail_msg

