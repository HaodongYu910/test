#! /usr/bin/env python
# coding=utf-8
from HtmlTemplate.test_html import html
from AutoTest.common.sendmail import send_mail
from AutoTest.models import test_report, install, dictionary
from django.conf import settings
import logging
import os,re
import shutil
import datetime
from .common.regexUtil import Weekdays
from .common.transport import SSHConnection
from .common.install import InstallThread

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
        logger.error('[Error] '+ e)


def installtask():
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
                obj = install.objects.filter(status=False,crontab='crontab')
                for j in obj:
                    logger.info("安装版本:{}".format(version))
                    logger.info("version:{0}".format(version[:-4]))
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

