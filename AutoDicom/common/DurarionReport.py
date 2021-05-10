# coding=utf-8
import logging
from django.db.models import Count, When, Case, Max, Min, Avg, Q
import datetime
from AutoProject.scheduletask import DurationTask
import time
import json
import threading
from ..models import duration, duration_record

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
        self.statistics_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.diseases = kwargs["diseases"]
        self.dis = []
        self.durationData = []

    # 生成报告数据
    def report(self):
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
            self.DetailData()
            data = {
                "basedata": basedata,
                "durationLineData": self.durationLine(),
                "durationData": self.durationData,
                "diseases": self.dis,
                "model": ['date', "{}-Prediction".format(self.diseases), "{}-Job".format(self.diseases)],
                "errorData": self.errorData()
            }
            return data
        except Exception as e:
            logger.error("报告数据：{0}".format(e))

    def DetailData(self):
        recordDetail = duration_record.objects.filter(jobtime__isnull=False, duration_id=self.obj.id,
                                                      create_time__lte=self.statistics_date).values(
            "diseases").annotate(
            ModelAvg=Avg('time'),
            ModelMax=Max('time'),
            ModelMin=Min('time'),
            JobAvg=Avg('jobtime'),
            JobMax=Max('jobtime'),
            JobMin=Min('jobtime'),
            success=Count(Case(When(aistatus__in=[2, 3], then=0))),
            fail=Count(Case(When(aistatus__in=[0, 1], then=0))),
            count=Count('id'))

        # Detailed 数据信息
        for i in recordDetail:
            try:
                info = {}
                obl = duration_record.objects.filter(duration_id=self.obj.id, diseases=i["diseases"], aistatus__in=[1])
                # 按病种 统计 错误 信息
                for jj in obl:
                    error = json.loads(jj.error[1:-1])["code"]
                    if info.__contains__(error) is False:
                        info[error] = 1
                    else:
                        info[error] = info[error] + 1
                if i["ModelAvg"] is None:
                    i["ModelAvg"] = 0
                elif i["ModelMax"] is None:
                    i["ModelMax"] = 0
                elif i["ModelMin"] is None:
                    i["ModelMin"] = 0
                elif i["JobAvg"] is None:
                    i["JobAvg"] = 0
                elif i["JobMax"] is None:
                    i["JobMax"] = 0
                elif i["JobMin"] is None:
                    i["JobMin"] = 0
                self.dis.append(i["diseases"])
                rate = '%.2f' % float(int(i["success"]) / (int(i["success"]) + int(i["fail"])) * 100)
                self.durationData.append({
                    "diseases": i["diseases"],
                    "ModelAvg": '%.2f' % (float(i["ModelAvg"])),
                    "ModelMax": i["ModelMax"],
                    "ModelMin": i["ModelMin"],
                    "JobAvg": '%.2f' % (float(i["JobAvg"])),
                    "JobMax": i["JobMax"],
                    "JobMin": i["JobMin"],
                    "success": i["success"],
                    "fail": i["fail"],
                    "count": i["count"],
                    "rate": rate,
                    "errorinfo": info
                })
            except Exception as e:
                logger.error("recordDetail 查询数据错误{}".format(e))
                continue

    def errorData(self):
        try:
            recorddata = {}
            errorData = []
            recordDetail = duration_record.objects.filter(duration_id=self.obj.id,
                                                          create_time__lte=self.statistics_date)

            for i in recordDetail:
                try:
                    if i.error is not None and i.error != '[]':
                        error = json.loads(i.error[1:-1])
                        if recorddata.__contains__(error["code"]) is False:
                            recorddata[error["code"]] = 1
                        else:
                            recorddata[error["code"]] = recorddata[error["code"]] + 1
                except Exception as e:
                    logger.error("失败：{0}".format(e))
                    continue
            for k, v in recorddata.items():
                errorData.append({'状态': k, '数量': v})

            return errorData
        except Exception as e:
            logger.error("错误分析数据生成失败：{0}".format(e))

    def durationLine(self):
        try:
            durationLineData = []
            recordDetail = duration_record.objects.filter(duration_id=self.obj.id, diseases=self.diseases,
                                                          aistatus__in=[2, 3]).order_by("starttime")
            for i in recordDetail:
                durationLineData.append({
                    "date": i.starttime[5:],
                    "{}-Prediction".format(i.diseases): i.time,
                    "{}-Job".format(i.diseases): i.jobtime
                })
            return durationLineData
        except Exception as e:
            logger.error("预测趋势数据生成失败：{0}".format(e))

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
