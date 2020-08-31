#! /usr/bin/env python
# coding=utf-8

import logging
import datetime
from TestPlatform.HTML_template.test_html import html
from TestPlatform.common.download_mail import download
from TestPlatform.common.sendmail import send_mail
from TestPlatform.models import test_report
from TestPlatform.common.regexUtil import *
from django.conf import settings
from TestPlatform.tools.duration_verify import *

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

__author__ = "vte"
__version__ = "0.0.1"





def job1_task():

    data = test_report.objects.get(type=1)

    try:
        if Weekdays(1) is True:
            title = data.title
            Html = html(data.test_version, data.cns_version)
            if data.receiver == 'Autotest':  # 测试邮件
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


def job2_task():
    try:
        verify()
    except Exception as e:
        logger.error("失败" % e)


