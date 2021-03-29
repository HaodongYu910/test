#! /usr/bin/env python
# coding=utf-8
from HtmlTemplate.test_html import html
from AutoTest.common.sendmail import send_mail
from AutoTest.models import test_report, install, dictionary
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
from AutoTest.common.PostgreSQL import connect_postgres
from django.db import transaction

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

__author__ = ""
__version__ = ""


def mail_task():
    data = test_report.objects.get(type=1)

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
                send_mail([settings.MAIL_USER, receiver, email_cc, title, Html])
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
                obj = install.objects.filter(status=False, crontab='crontab')
                downssh = SSHConnection(host='192.168.2.111', pwd='P@ssw0rd2111')
                downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{0}'.format(version)
                path = '/files/History_version/{0}'.format(version[:-4])
                if not os.path.exists(path):
                    os.makedirs(path)
                    logger.info("Installation定时：创建备份文件夹{}".format(version[:-4]))
                localpath = '/files/History_version/{0}/{1}'.format(version[:-4], version)
                logger.info("Installation{定时}：下载备份最新安装包{}.zip".format(version))
                downssh.download(localpath, downpath)
                logger.info("Installation{定时}：下载备份最新安装包{}.zip 完成".format(version))
                downssh.close()
                for j in obj:
                    logger.info("Installation 安装版本:{}".format(version))
                    logger.info("Installation version:{0}".format(version[:-4]))
                    j.version = version[:-4]
                    j.save()
                    testThread = InstallThread(id=j.id)
                    testThread.setDaemon(True)
                    # 开始线程
                    testThread.start()
                if len(version) > 4:
                    dobj.value = '{},{}'.format(str(dobj.value), version)
                    dobj.save()

    except Exception as e:
        logger.error(e)

# 同步持续化数据结果
def DurationTask():
    obj = duration.objects.filter(type="持续化", status=True)
    sqlobj = dictionary.objects.get(key='duration', status=True, type='sql')
    try:
        for i in obj:
            record = duration_record.objects.filter(duration_id=i.id, aistatus=None)
            for j in record:
                sql = sqlobj.value.format(j.studyinstanceuid)
                result = connect_postgres(host=i.Host.host, sql=sql)
                _dict = result.to_dict(orient='records')
                if len(_dict) == 0:
                    continue
                else:
                    try:
                        serializer = duration_record_Deserializer(data=_dict[0])
                        with transaction.atomic():
                            if serializer.is_valid():
                                # 修改数据
                                serializer.update(instance=j, validated_data=_dict[0])
                    except Exception as e:
                        logger.error('[Schedule Task Error]:serializer.is_valid fail '.format(e))
    except Exception as e:
        logger.error('[Schedule Task Error]:{}'.format(e))
