#! /usr/bin/env python
# coding=utf-8

import logging
import re
from jira import JIRA
import datetime
from django.conf import settings
from AutoProject.models import Project
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


__author__ = "vte"
__version__ = "0.0.1"

class Jiradata():
    def __init__(self):
        self.jira = JIRA(settings.SITE_JIRAURL, basic_auth=('yinhang', '123456'))

    # 查询项目排期数据
    def date_time(self,platform):
        if platform =='Server':
            platform = 'Boimind'
        timeData = Project.objects.get(name=platform,status="True",client = 2)
        test_time = datetime.datetime.today() - timeData.start_date
        return timeData.start_date,int(test_time.days)

    # 查询 缺陷（入参：模块，优先级，项目，版本）
    def search_bug_total(self,project,platform,sprint_version,starttime,days,status,component,priority):
        list=[]
        #默认优先级
        if priority == '':
            priority = '("最高","高","中", "低", "较低")'
        #默认模块
        if component == '':
            component = '" 平台基础-我的", "交易-交易", "交易-积分", "交易-糖果", 交易-钱包, 信息流-广告, 信息流-快讯, 信息流-深度, 基本面-交易所, 基本面-币种, 平台基础-分享, 技术面-行情'
        if status == '':
            status ='("Open","Progress", "Reopened")'
    
        issue = self.jira.search_issues('project = {0} AND issuetype ={1} AND status in {2}  AND affectedVersion = {4} '
                                       'AND priority in {3}  ORDER BY priority ASC' .format(
            project,platform,status,priority,sprint_version,component))
    
        for i in range(int(issue.total)):
            issue_id = issue[i].key
            # if platform == "信息服务":
            #     story_name = ''
            # else:
            #     story_name = self.jira.issue(issue_id).fields.issuetype  # 客户端名称
    
            if len(self.jira.issue(issue_id).fields.components):
                measures = self.jira.issue(issue_id).fields.components
            else:
                measures = ' '  # 模块
            priority = self.jira.issue(issue_id).fields.priority  # 优先级
            summary = self.jira.issue(issue_id).fields.summary  # 概要
            # cause = self.jira.issue(issue_id).fields.customfield_13511  # 缺陷原因
            affect = self.jira.issue(issue_id).fields.versions  # 影响版本
            status = self.jira.issue(issue_id).fields.status  # 状态
            assignee = self.jira.issue(issue_id).fields.assignee  # 处理人
            issuetype = self.jira.issue(issue_id).fields.issuetype   # 缺陷类型
            reporter = self.jira.issue(issue_id).fields.reporter   # 报告人
    
            data = {'issue_id': issue_id, 'measures': str(measures[0]), 'priority': str(priority), 'summary': str(summary), 'affect': str(affect[0]), 'status': str(status), 'assignee': str(assignee), 'issuetype': str(issuetype), 'reporter': str(reporter)}
    
            list.append(data)
    
        return list

    # 查询 缺陷（入参：模块，优先级，项目，版本）
    def search_total(self,priority,platform, sprint_version):
        # 默认优先级
        if priority == '':
            priority = '("最高","高","中", "低", "较低")'
        # 默认模块
        component = '" 平台基础-我的", "交易-交易", "交易-积分", "交易-糖果", 交易-钱包, 信息流-广告, 信息流-快讯, 信息流-深度, 基本面-交易所, 基本面-币种, 平台基础-分享, 技术面-行情'
        if platform == 'CoinNess':
            issue = self.jira.search_issues(
                'project = "BUG" AND issuetype ="CoinNess-APP-缺陷" AND status in ("Open","Progress", "Reopened")  AND affectedVersion = {2} '
                'AND priority in {1}  ORDER BY priority ASC'.format(
                    component, priority, sprint_version))
        elif platform == 'Boimind':
            issue = self.jira.search_issues(
                'project = "BUG" AND issuetype = "Boimind-APP-缺陷" AND status in ("Open","Progress", "Reopened") and affectedVersion = {1} AND priority in {0} ORDER BY priority ASC'.format(
                    priority, sprint_version))
        elif platform == 'h5':
            issue = self.jira.search_issues(
                'project = "BUG" AND issuetype = "H5 Main-缺陷" AND status in ("Open","Progress", "Reopened") and affectedVersion = {1} AND priority in {0} ORDER BY priority ASC'.format(
                    priority, sprint_version))
        elif platform == 'online':
            issue = self.jira.search_issues(
                'project = "online" AND issuetype = "故障" AND status in ("Open","Progress", "Reopened") AND priority in ("最高","高") ORDER BY priority ASC')
        elif platform == '信息服务':
            issue = self.jira.search_issues(
                'project = "BUG" AND issuetype = "Server-缺陷" AND status in ("Open","Progress", "Reopened") and affectedVersion in ({1}) AND priority in {0} ORDER BY priority ASC'.format(
                    priority, sprint_version))

        return issue
    
    # 查询jira 创建和解决问题 缺陷生成图表数据（入参 项目，版本）
    def bug_create_solution (self,project,platform,sprint_version,starttime,days,status,component,priority):  # 入参 项目
        createdlist = []
        resolvelist = []
        daylist =[]

        if days =="":
            days=7

        if starttime =="":
            starttime=datetime.datetime.today()
    
        for item in range(days+1):
            component=''
            days_ago=(starttime - datetime.timedelta(days=(days-item))).strftime("%Y-%m-%d")


            created = self.jira.search_issues('project = {0} AND issuetype ={1} AND affectedVersion in ({2}) AND created >= {3} AND created <= "{3} 23:59"'.format(
                project,str(platform),sprint_version,days_ago))
            resolve = self.jira.search_issues('project = {0} AND issuetype ={1} AND affectedVersion in ({2}) AND resolutiondate >= {3} AND resolutiondate <= "{3} 23:59"'.format(
                project,platform, sprint_version, days_ago))
    
            # if created.total == 0 and resolve.total == 0 and is_holiday(days_ago_temp[item].strftime('%Y%m%d')):
            #     days_ago_temp.pop(item)
            #     continue
            createdlist.append(int(created.total))
            resolvelist.append(int(resolve.total))
            daylist.append(days_ago)
            list = [daylist,createdlist,resolvelist]
        return list
    
    
    # 查询bug解决状态（入参 项目，版本）
    def bug_solution_state(self,project,platform,sprint_version,starttime,days,status,component,priority):
        list = []
        for item in ['Closed','Reopened','Resolved','open',"Progress"]:
            component=''
            total_a = self.jira.search_issues('project = {0} AND issuetype = {1} AND affectedVersion ={2} AND status = {3} '.format(project,platform,sprint_version,item,component))
            list.append({"value":int(total_a.total), "name": item})
    
        return list
    
    # 查询 缺陷（入参：模块，优先级，项目，版本）
    def bug_priority(self,issuetype,sprint_version,starttime,days,status,component,priority):

        bugtotal = []
        today = datetime.date.today()

        if priority=='':# 默认优先级
            priority = ["最高", "高", "其他"]
        if status=='':
            status= '("Open", "Progress", "Reopened")'

        for i in priority:
            if i=='其他':
                issue = self.jira.search_issues(
                    'project = "BUG" AND issuetype = {3}  AND status in ("Open","Progress", "Reopened")  AND affectedVersion in ({1}) '
                    'AND priority in {2} AND created <= "{0} 23:59" ORDER BY priority ASC'.format(today, sprint_version,'("中","低","较低")',issuetype))
            else:
                logger.info('project = "BUG" AND issuetype = {3}  AND status in ({4})  AND affectedVersion in ({1}) '
                                           'AND priority = {2} AND created <= "{0} 23:59" ORDER BY priority ASC' .format(today,str(sprint_version),str(i),issuetype,status))
                issue = self.jira.search_issues('project = "BUG" AND issuetype = {3}  AND status in ({4})  AND affectedVersion in ({1}) '
                                           'AND priority = {2} AND created <= "{0} 23:59" ORDER BY priority ASC' .format(today,str(sprint_version),str(i),issuetype,status))
            bugtotal.append(issue.total)
        return bugtotal

    def bug_data(self,platform,sprint_version):
        issue = []
        for item in ['Closed', 'Reopened', 'Resolved', 'open', "Progress"]:
            component = ''
            if platform == 'online':
                total_a = self.jira.search_issues(
                    'project = online AND issuetype = "故障"  AND affectedVersion = {2}'.format(
                        component))
                issue.append(int(total_a.total))
            else:
                total_a = self.jira.search_issues(
                    'project = "BUG" AND issuetype ={0} AND affectedVersion in ({1}) AND status = {2} '.format(
                        platform, sprint_version, item,component))
                issue.append(int(total_a.total))
        return issue

    # 查询jira缺陷生成图表数据（入参 项目，版本）
    def figurs_data(self,platform, sprint_version):
        project = 'BUG'
        if platform == 'online':
            issuetype = '故障'
        else:
            issuetype = platform

        issue = []
        pname=str(re.findall(r"(.+?)-", platform)[0])

        for item in range(Jiradata().date_time(pname)[1] + 1):
            component = ''
            days_ago = (Jiradata().date_time(pname)[0] + datetime.timedelta(days=item)).strftime("%Y-%m-%d")
            created = self.jira.search_issues(
                'project = {0} AND issuetype ={1} AND affectedVersion in ({2}) AND created >= {3} AND created <= "{3} 23:59"'.format(
                    project, str(issuetype), sprint_version, days_ago))
            resolve = self.jira.search_issues(
                'project = {0} AND issuetype ={1} AND affectedVersion in ({2}) AND resolutiondate >= {3} AND resolutiondate <= "{3} 23:59"'.format(
                    project, issuetype, sprint_version, days_ago))
            # if created.total == 0 and resolve.total == 0 and is_holiday(days_ago_temp[item].strftime('%Y%m%d')):
            #     days_ago_temp.pop(item)
            #     continue
            issue.append([int(created.total), int(resolve.total)])
        return issue

    def Pending(self,user):

        bug_todo = self.jira.search_issues(
                'project = {0} AND status in (Open,Reopened,Resolved) AND reporter in ({1})'.format(
                    'BUG',user))
        task_todo = self.jira.search_issues(
            'project = {0} AND status in ("已提测", "测试中", "Pending", "待发布上线", "灰度验收", "待上线", "线上验收", "待CR") AND reporter in ({1})'.format(
                'SXLC', user))

        online_todo = self.jira.search_issues(
            'project = {0} AND status in (Open,"处理中", Reopened, Resolved)  AND assignee  in ({1})'.format(
                'ONLINE', user))

        return [int(bug_todo.total),int(task_todo.total),int(online_todo.total)]

    def bugtotal(self,platform,sprint_version,status):
        issue = []
        component = ''
        if platform == 'online':
            total_a = self.jira.search_issues(
                    'project = online AND issuetype = "故障"  AND affectedVersion in ({2})'.format(
                        component))
            issue.append(int(total_a.total))
        else:
            logger.info('project = "BUG" AND issuetype in ({0}) AND affectedVersion in ({1}) AND status = {2} '.format(
                        platform, sprint_version,status,component))
            total_a = self.jira.search_issues(
                    'project = "BUG" AND issuetype in ({0}) AND affectedVersion in ({1}) AND status in ({2}) '.format(
                        platform, sprint_version,status,component))
        return str(total_a.total)