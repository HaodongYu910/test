#! /usr/bin/env python
# coding=utf-8
from HtmlTemplate.test_html import html
from TestPlatform.common.sendmail import send_mail
from TestPlatform.models import test_report,base_data
from django.conf import settings
from Dicom.common.duration_verify import *

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

__author__ = "vte"
__version__ = "1.0.1"



def mail_task():

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


def clean_task():
    try:
        obj = pid.objects.filter(durationid=data["id"])
        okj = duration.objects.get(id=data["id"])

        for i in obj:
            cmd = 'kill -9 {0}'.format(int(i.pid))
            logger.info(cmd)
            os.system(cmd)
            i.delete()

        okj.sendstatus = False
        okj.save()
        # 删除 文件夹
        folder = "/files/logs/{0}".format(str(okj.keyword))
        if os.path.exists(folder):
            shutil.rmtree(folder)
    except Exception as e:
        logger.error("修改失败" % e)

def duration(durationid):
    try:
        min = 1000
        sumdicom = 0
        obj = duration.objects.get(id=durationid)
        for j in obj.dicom.split(","):
            dicom = base_data.objects.get(remarks=j)
            if dicom.other is None:
                sumdicom = sumdicom
            else:
                if min > int(dicom.other):
                    min = int(dicom.other)
                    mindicom = j
                sumdicom = int(dicom.other) + sumdicom

        imod = divmod(int(obj.sendcount), sumdicom)
        imin = divmod(int(imod[1]), min)
        if int(imin[1]) < (int(imin[1]) / 2):
            mincount = int(imin[0]) + int(imod[0])
        else:
            mincount = int(imin[0]) + int(imod[0]) + 1

        for i in obj.dicom.split(","):
            dicom = base_data.objects.get(remarks=i)
            folder = dicom.content
            if i == mindicom:
                sendcount = mincount
            else:
                sendcount = imod[0]
            cmd = ('nohup /home/biomind/.local/share/virtualenvs/biomind-dvb8lGiB/bin/python3'
                   ' /home/biomind/Biomind_Test_Platform/TestPlatform/install/duration/durationcmd.py '
                   '--ip {0} --aet {1} '
                   '--port {2} '
                   '--keyword {3} '
                   '--dicomfolder {4} '
                   '--durationid {5} '
                   '--diseases {6} '
                   '--end {7} '
                   '--sendcount {8} &').format(obj.server, obj.aet, obj.port, obj.keyword, folder, durationid, i,
                                               obj.end_time, sendcount)
            logger.info(cmd)
            os.system(cmd)
            time.sleep(1)

        obj.sendstatus = True
        obj.save()
    except Exception as e:
        logger.error(e)

