# coding=utf-8
import logging
from django.db.models import Count, When, Case, Max, Min, Avg
import time, datetime
import random
import math
import time

import threading

from ..common.duration_verify import *
from ..serializers import duration_record_Serializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y%m%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H%M%S", localtime))


class ReportThread(threading.Thread):
    def __init__(self, **kwargs):
        self.obj = duration.objects.get(id=kwargs["id"])
        self.server = self.obj.Host.host
        self.statistics_date = '{} 00:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
        self.diseases = kwargs["diseases"]

    # 生成报告数据
    def report(self):
        durationData = []
        diseases = []
        try:
            record = duration_record.objects.filter(duration_id=self.obj.id,
                                                    create_time__lte=self.statistics_date).values(
                "duration_id").annotate(
                send=Count(Case(When(aistatus__in=[1, 2, 3], then=0))),
                success=Count(Case(When(aistatus__in=[2, 3], then=0))),
                fail=Count(Case(When(aistatus__in=[0, 1], then=0))),
                count=Count('id'))

            basedata = {
                "version": self.obj.version,
                "server": self.obj.server,
                "sendcount": record[0]['count'],
                "AICount": record[0]['send'],
                "AISuccess": record[0]['success'],
                "AIFail": record[0]['fail'],
                "start_date": self.obj.start_time,
                "statistics_date": self.statistics_date,
                "end_date": self.obj.end_time
            }

            recordDetail = duration_record.objects.filter(duration_id=self.obj.id, create_time__lte=self.statistics_date).values(
                "diseases").annotate(
                ModelAvg=Avg('time'),
                ModelMax=Max('time'),
                ModelMin=Min('time'),
                success=Count(Case(When(aistatus__in=[2, 3], then=0))),
                fail=Count(Case(When(aistatus__in=[0, 1], then=0))),
                count=Count('id'))

            for i in recordDetail:
                try:
                    diseases.append(i["diseases"])
                    rate = '%.2f' % float(int(i["success"])/(int(i["success"])+int(i["fail"]))*100)
                    durationData.append({
                        "diseases": i["diseases"],
                        "ModelAvg":  '%.2f' % (float(i["ModelAvg"])),
                        "ModelMax": i["ModelMax"],
                        "ModelMin": i["ModelMin"],
                        "success": i["success"],
                        "fail": i["fail"],
                        "count": i["count"],
                        "rate": rate,
                    })
                except Exception as e:
                    logger.error("recordDetail 查询数据错误{}".format(e))
                    continue

            data = {
                "basedata": basedata,
                "durationLineData": self.durationLine(diseases=diseases),
                "durationData": durationData,
                "diseases": diseases,
                "model": ['date', self.diseases]
            }
            return data
        except Exception as e:
            logger.error("队列生成失败：{0}".format(e))

    def durationLine(self, diseases):
        try:
            durationLineData = []
            recordDetail = duration_record.objects.filter(duration_id=self.obj.id, diseases=self.diseases, aistatus__in=[2, 3]).order_by("sendtime")

            for i in recordDetail:
                datedata = {}
                datedata["date"] = i.sendtime[5:]
                for j in diseases:
                    if str(j) == str(i.diseases):
                        datedata[j] = i.time
                    elif str(j) == 'date':
                        continue
                    else:
                        datedata[i.diseases] = 0
                durationLineData.append(datedata)
            return durationLineData
        except Exception as e:
            logger.error("预测趋势数据生成失败：{0}".format(e))



    #     datalist = durationtotal(durationid)
    #     datalist['all'] = obi.count()
    #     datalist['sent'] = int(datalist['all']) - int(datalist['notsent'])
    #     avg = duration_record.objects.filter(duration_id=durationid).aggregate(Avg("time"))
    #     datalist['avg'] = 1 / avg['time__avg']

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
