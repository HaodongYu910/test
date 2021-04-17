#! /usr/bin/env python
# coding=utf-8
from htmlTemplate.test_html import html
from AutoProject.models import install, dictionary, Server
from AutoDicom.models import duration_record, duration
from AutoDicom.serializers import duration_record_Deserializer
from django.conf import settings
import logging
import os, re
import shutil
import datetime
from .common.regexUtil import Weekdays
from .common.transport import SSHConnection
from .common.install import InstallThread
from AutoProject.common.PostgreSQL import connect_postgres
from django.db import transaction
from AutoDicom.common.durarion import DurationThread
from .common.message import sendMessage
from django.db.models import Count, When, Case, Max, Min, Avg

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

__author__ = ""
__version__ = ""


def mail_task():
    data = []
    try:
        if Weekdays(1) is True:
            title = data.title
            Html = html(data.test_version, data.cns_version)
            if data.receiver == 'QualityControl':  # 测试邮件
                receiver = ['hang.yin@biomind.ai', 'yinhang@bishijie.com']
                email_cc = ['yinhang@bishijie.com', 'yinhang@bishijie.com']
            else:  # 正式邮件
                receiver = ['tech@bishijie.com', 'product@bishijie.com', 'op@bishijie.com',
                            'yunwei@bishijie.com', 'qa.list@bishijie.com']
                email_cc = ['tan@bishijie.com', 'zhaoyan@bishijie.com', 'limingzhu@bishijie.com']
            # 附件
            # attach_xlsx = 'C:/Users/Hvte/Desktop/coinness1.6 行情测试用例.xlsx'
            # attach_jpg = 'D:/360Downloads/wey.png'
            try:
                [settings.MAIL_USER, receiver, email_cc, title, Html]
            except Exception as e:
                logger.info('[Error] ' + e)
        else:
            logger.info('[ 休息时间] ' + datetime.datetime.now())
    except Exception as e:
        logger.error('[Error] ' + e)


def InstallTask():
    dobj = dictionary.objects.get(type='install', key='oldversion')
    oldversion = dobj.value.split(',')
    logger.info("定时任务启动")
    try:
        downssh = SSHConnection(host='192.168.2.111', pwd='P@ssw0rd2111')
        filelist = downssh.cmd(
            "cd /lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/;ls -lR |grep -v ^d|awk '{print $9}' |tr -s '\\n';")
        for i in str(filelist, encoding="utf-8").split('\n'):
            version = i.replace('\r', "")
            version = version.replace('\n', "")
            if version not in oldversion and version:
                logger.info("Installation[定时]：新版本{}".format(version))
                try:
                    obj = install.objects.filter(status=False, crontab='crontab')
                    if int(obj.count()) >= 1:
                        downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{0}'.format(version)
                        path = '/files/History_version/{0}'.format(version[:-4])
                        if not os.path.exists(path):
                            os.makedirs(path)
                            logger.info("Installation定时：创建备份文件夹{}".format(version[:-4]))
                        localpath = '/files/History_version/{0}/{1}'.format(version[:-4], version)
                        logger.info("Installation[定时]：下载备份最新安装包{}".format(version))
                        downssh.download(localpath, downpath)
                        logger.info("Installation[定时]：下载备份最新安装包{} 完成".format(version))
                        downssh.close()
                        for j in obj:
                            logger.info("Installation[定时]:{0}".format(version[:-4]))
                            j.version = version[:-4]
                            j.save()
                            testThread = InstallThread(id=j.id)
                            testThread.setDaemon(True)
                            # 开始线程
                            testThread.start()
                        if len(version) > 4:
                            dobj.value = '{},{}'.format(str(dobj.value), version)
                            dobj.save()
                    else:
                        logger.info("Installation{定时}：无定时部署服务")
                except:
                    downssh.close()
                    logger.error("Installation{定时}：无定时部署服务")
        downssh.close()
    except Exception as e:
        downssh.close()
        logger.error(e)


# 同步持续化数据结果
def DurationSyTask():
    infos = {}
    logger.info("持续化数据结果同步定时任务启动！~~")
    obj = duration_record.objects.filter(jobtime=None)
    sqlobj = dictionary.objects.get(key='duration', status=True, type='sql')
    Psqlobj = dictionary.objects.get(key='durationP', status=True, type='sql')
    try:
        for i in obj:
            if infos.__contains__(i.sendserver) is False:
                infos[i.sendserver] = '\'' + str(i.studyinstanceuid) + '\''
            else:
                infos[i.sendserver] = infos[i.sendserver] + ',\'' + str(i.studyinstanceuid) + '\''
        for k, v in infos.items():
            host = Server.objects.get(host=k)
            sql = sqlobj.value.format(v)
            Psql = Psqlobj.value.format(v)
            result = connect_postgres(host=host.id, sql=sql, database="orthanc")
            resultdict = result.to_dict(orient='records')
            _result = connect_postgres(host=host.id, sql=Psql, database="orthanc")
            _dict = _result.to_dict(orient='records')
            for j in resultdict:
                obj = duration_record.objects.get(studyinstanceuid=j["studyuid"])
                try:
                    obj.imagecount_server = j["imagecount_server"]
                    obj.aistatus = j["pai_status"]
                    obj.error = j["error"]
                    obj.diagnosis = j["pclassification"]
                    obj.jobtime = j["jobtime"]
                    obj.starttime = j["starttime"]
                    obj.save()
                except Exception as e:
                    logger.error('[Schedule Task Error]:duration_record update fail '.format(e))
                    continue
            for ii in _dict:
                obj = duration_record.objects.get(studyinstanceuid=ii["studyuid"])
                try:
                    obj.time = ii["predictionsec"]
                    obj.model = ii["modelname"]
                    obj.save()
                except Exception as e:
                    logger.error('[Schedule Synchronization Task Error]:predictionsec fail '.format(e))
                    continue
    except Exception as e:
        logger.error('[Schedule Synchronization Task Error]:{}'.format(e))


# 持续化定时任务启动
def DurationTask():
    logger.info("持续化定时任务启动！~~")
    obj = duration.objects.filter(sendstatus=True, type='持续化')
    try:
        for i in obj:
            if i.end_time > str(datetime.datetime.today()):
                durationThread = DurationThread(id=i.id)
                durationThread.setDaemon(True)
                # 开始线程
                durationThread.start()
            else:
                i.status = False
                i.save()
    except Exception as e:
        logger.error('[Schedule Sustainability Task Error]:{}'.format(e))


def DurationReportTask():
    logger.info("持续化报告定时任务启动！~~")
    obj = duration.objects.filter(sendstatus=True, type='持续化')
    statistics_date = '{} 00:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
    try:
        for i in obj:
            record = duration_record.objects.filter(duration_id=i.id,
                                                    create_time__lte=statistics_date).values(
                "duration_id").annotate(
                send=Count(Case(When(aistatus__in=[1, 2, 3], then=0))),
                success=Count(Case(When(aistatus__in=[2, 3], then=0))),
                fail=Count(Case(When(aistatus__in=[0, 1], then=0))),
                count=Count('id'))
            message = "【持续化进度消息】\n 测试版本：{0} \n 测试服务：{1} \n 统计截至时间：{2}  \n 共计发送：{3} 笔 \n  预测成功：{4}笔 \n 预测失败：{5}笔 \n  <a href=\"http://192.168.1.121/#/DurationReport/reportid={6}\">详细信息内网中请查看：http://192.168.1.121/#/DurationReport/reportid={7}</a>".format(
                i.version,
                i.server, statistics_date, record[0]['count'],  record[0]['success'], record[0]['fail'],
                i.id, i.id)
            sendMessage(touser='', toparty='132', message= message)
    except Exception as e:
        logger.error('[Schedule Sustainability Task Error]:{}'.format(e))

def NightlyReportTask():
    logger.info("持续化报告定时任务启动！~~")
    obj = duration.objects.filter(sendstatus=True, type='Nightly')
    try:
        for i in obj:
            record = duration_record.objects.filter(duration_id=i.id,).values(
                "duration_id").annotate(
                send=Count(Case(When(aistatus__in=[1, 2, 3], then=0))),
                success=Count(Case(When(aistatus__in=[2, 3], then=0))),
                fail=Count(Case(When(aistatus__in=[0, 1], then=0))),
                count=Count('id'))
            message = "【Nightly Build Report】\n 测试版本：{0} \n 测试服务：{1} \n 共计发送：{2} 笔 \n  预测成功：{3}笔 \n 预测失败：{4}笔 \n  <a href=\"http://192.168.1.121/#/DurationReport/reportid={5}\">详细信息内网中请查看：http://192.168.1.121/#/DurationReport/reportid={7}</a>".format(
                i.version,
                i.server,
                record[0]['count'],
                record[0]['success'],
                record[0]['fail'],
                i.id, i.id)
            sendMessage(touser='', toparty='132', message=message)
    except Exception as e:
        logger.error('[Schedule Sustainability Task Error]:{}'.format(e))
