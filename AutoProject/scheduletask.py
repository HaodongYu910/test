#! /usr/bin/env python
# coding=utf-8

from AutoProject.models import message_group, dictionary, Server, project_version
from AutoDicom.models import duration_record, duration
from django.conf import settings
import logging
import os
import requests
import datetime

from AutoProject.common.PostgreSQL import connect_postgres
from .common.message import MessageGroup
from django.db.models import Count, When, Case, Max, Min, Avg

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

__author__ = ""
__version__ = ""


#
# def mail_task():
#     data = []
#     try:
#         if Weekdays(1) is True:
#             title = data.title
#             Html = html(data.test_version, data.cns_version)
#             if data.receiver == 'QualityControl':  # 测试邮件
#                 receiver = ['hang.yin@biomind.ai', 'yinhang@bishijie.com']
#                 email_cc = ['yinhang@bishijie.com', 'yinhang@bishijie.com']
#             else:  # 正式邮件
#                 receiver = ['tech@bishijie.com', 'product@bishijie.com', 'op@bishijie.com',
#                             'yunwei@bishijie.com', 'qa.list@bishijie.com']
#                 email_cc = ['tan@bishijie.com', 'zhaoyan@bishijie.com', 'limingzhu@bishijie.com']
#             # 附件
#             # attach_xlsx = 'C:/Users/Hvte/Desktop/coinness1.6 行情测试用例.xlsx'
#             # attach_jpg = 'D:/360Downloads/wey.png'
#             try:
#                 [settings.MAIL_USER, receiver, email_cc, title, Html]
#             except Exception as e:
#                 logger.info('[Error] ' + e)
#         else:
#             logger.info('[ 休息时间] ' + datetime.datetime.now())
#     except Exception as e:
#         logger.error('[Error] ' + e)


# 同步持续化数据结果
def DurationSyTask():
    infos = {}
    obj = duration_record.objects.filter(sec=None, error__isnull=True)
    Psqlobj = dictionary.objects.get(key='durationP', status=True, type='sql')
    try:
        for i in obj:
            if i.Host_id in ["192.168.1.200"]:
                continue
            elif infos.__contains__(i.Host_id) is False:
                infos[i.Host_id] = '\'' + str(i.studyinstanceuid) + '\''
            else:
                infos[i.Host_id] = infos[i.Host_id] + ',\'' + str(i.studyinstanceuid) + '\''
        logger.info("持续化数据 模型结果同步定时任务启动！~~")
        for k, v in infos.items():
            Psql = Psqlobj.value.format(v)
            try:
                _result = connect_postgres(host=k, sql=Psql, database="orthanc")
                _dict = _result.to_dict(orient='records')
                for j in _dict:
                    obj = duration_record.objects.filter(studyinstanceuid=j["studyuid"])
                    for i in obj:
                        i.sec = j["sec"]
                        i.model = j["model"]
                        i.start = j["start"]
                        i.end = j["end"]
                        i.save()
            except Exception as e:
                logger.error('[Schedule DurationSyTask Error]: error '.format(e))
                continue
    except Exception as e:
        logger.error('[Schedule Synchronization Task Error]:{}'.format(e))


# 同步 job 时间
def JobSyTask():
    infos = {}
    obj = duration_record.objects.filter(job_sec=None)
    sqlobj = dictionary.objects.get(key='duration', status=True, type='sql')
    try:
        for i in obj:
            if infos.__contains__(i.Host_id) is False:
                infos[i.Host_id] = '\'' + str(i.studyinstanceuid) + '\''
            else:
                infos[i.Host_id] = infos[i.Host_id] + ',\'' + str(i.studyinstanceuid) + '\''
        logger.info("持续化数据 Job结果同步定时任务启动！~~")
        for k, v in infos.items():
            sql = sqlobj.value.format(v)
            try:
                result = connect_postgres(host=k, sql=sql, database="orthanc")
                resultdict = result.to_dict(orient='records')
                for j in resultdict:
                    obj = duration_record.objects.filter(studyinstanceuid=j["studyuid"])
                    for i in obj:
                        i.image_receive = j["image_receive"]
                        i.aistatus = j["aistatus"]
                        i.error = j["error"]
                        i.diagnosis = j["diagnosis"]
                        i.job_sec = j["job_sec"]
                        i.job_end = j["job_end"]
                        i.job_start = j["job_start"]
                        i.save()
            except Exception as e:
                logger.error('[Schedule JobSyTask Error]: error '.format(e))
                continue
    except Exception as e:
        logger.error('[Schedule Synchronization JobSyTask Error]:{}'.format(e))


# 持续化定时任务启动
def DurationTask():
    logger.info("持续化定时任务启动！~~")
    obj = duration.objects.filter(status=True, type='2')
    try:
        for i in obj:
            if str(i.end_time) > str(datetime.datetime.today()):
                cmd = f"nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3 /home/biomind/Biomind_Test_Platform/AutoDicom/common/durationTask.py --relation_id {i.id} &"
                logger.info(cmd)
                os.system(cmd)
            else:
                logger.info("持续化定时任务停止{}！".format(i.id))
                i.sendstatus = False
                i.status = False
                i.save()
    except Exception as e:
        logger.error('[Schedule Sustainability Task Error]:{}'.format(e))


def DurationReportTask():
    obj = duration.objects.filter(sendstatus=True, type=2)
    statistics_date = '{} 00:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
    try:
        for i in obj:
            logger.info("持续化报告定时任务启动！~~")
            record = duration_record.objects.filter(relation_id=i.id,
                                                    create_time__lte=statistics_date).values(
                "relation_id").annotate(
                send=Count(Case(When(aistatus__in=[1, 2, 3], then=0))),
                success=Count(Case(When(aistatus__in=[2, 3], then=0))),
                fail=Count(Case(When(aistatus__in=[0, 1], then=0))),
                count=Count('id'))
            version = project_version.objects.get(id=i.version).version
            # 查询发送信息 数据 发送 企业微信
            messObj = message_group.objects.get(type="duration", status=True)
            params = {
                "msgtype": "markdown",
                "markdown": {
                    "content": messObj.content.format(
                        version,
                        i.server,
                        statistics_date,
                        record[0]['count'],
                        record[0]['success'],
                        record[0]['fail'],
                        i.id,
                        i.id)
                    # "mentioned_mobile_list": MessObj.mentioned_mobile_list.split(",")
                }
            }
            logger.info(params)
            MessageGroup(send_url=messObj.send_url, params=params)

    except Exception as e:
        logger.error('[Schedule Sustainability Task Error]:{}'.format(e))


def NightlyReportTask():
    logger.info("持续化报告定时任务启动！~~")
    obj = duration.objects.filter(status=True, type=3)
    for i in obj:
        try:
            record = duration_record.objects.filter(relation_id=i.id).values(
                "relation_id").annotate(
                send=Count(Case(When(aistatus__in=[1, 2, 3], then=0))),
                success=Count(Case(When(aistatus__in=[2, 3], then=0))),
                fail=Count(Case(When(aistatus__in=[0, 1], then=0))),
                count=Count('id'))
            version = project_version.objects.get(id=i.version).version
            # 查询发送信息 数据 发送 企业微信
            messObj = message_group.objects.get(type="durationNightly", status=True)
            params = {
                "msgtype": "markdown",
                "markdown": {
                    "content": messObj.content.format(
                        version,
                        i.server,
                        record[0]['count'],
                        record[0]['success'],
                        record[0]['fail'],
                        i.id,
                        i.id)
                    # "mentioned_mobile_list": MessObj.mentioned_mobile_list.split(",")
                }
            }

            i.status = False
            i.save()
            logger.info(params)
            MessageGroup(send_url=messObj.send_url, params=params)
        except Exception as e:
            logger.error('[Schedule Sustainability Task Error]:{}'.format(e))
            continue
