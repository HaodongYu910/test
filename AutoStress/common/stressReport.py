from AutoStress.models import stress, stress_result, stress_record
from AutoProject.models import dictionary
from django.db.models import Count, Case, When
from AutoProject.common.message import sendMessage
import datetime
from AutoDicom.common.deletepatients import *
from ..common.stressfigure import stressdataFigure
from ..serializers import stress_result_Deserializer

import json
import logging

logger = logging.getLogger(__name__)


# 性能测试结果
class StressReport:
    def __init__(self, *args):
        self.id = args[0]
        self.obj = stress.objects.get(stressid=self.id)
        self.serverIP = self.obj.Host.host
        self.StressType = args[1]

    def report(self):
        models = {}
        try:
            aiObj = stress_record.objects.filter(
                Stress_id=int(self.id)).values('Stress_id').annotate(
                total=Count(1),
                success=Count(Case(When(aistatus=3, then=0))),
                warn=Count(Case(When(aistatus=2, then=0))),
                fail=Count(Case(When(aistatus=1, then=0))),
            )
            if not aiObj:
                total = 0
                success = 0
                fail = 0
            else:
                total = aiObj[0]["success"] + aiObj[0]["warn"] + aiObj[0]["fail"]
                success = aiObj[0]["success"] + aiObj[0]["warn"]
                fail = aiObj[0]["fail"]

            for j in self.obj.testdata.split(","):
                dictObj = dictionary.objects.get(id=j)
                models[j] = dictObj.key
            data = {
                "basedata": {
                    "version": self.obj.version,
                    "server": self.obj.Host.host,
                    "total": total,
                    "success": success,  # 成功
                    "fail": fail,  # 失败
                    "models": models,
                    "start_date": self.obj.start_date,
                    "end_date": self.obj.end_date,
                    "server": self.obj.Host.host,
                    "benchmark": self.obj.benchmark,
                    "single": self.obj.single,
                    "synchroniz": self.obj.synchroniz,
                    "loop_time": self.obj.loop_time,
                    "serverInfo": self.obj.Host.description,
                    "summary": self.obj.summary
                },
                "goldrows": [
                    {'状态': '预测成功', '数量': 5},
                    {'状态': '预测失败', '数量': 5}
                ],
                "aiResult": [
                    {'状态': '成功', '数量': success},
                    {'状态': '失败', '数量': fail}
                ]
                ,
                "errorData": self.errorData()
            }
        except Exception as e:
            logger.error("数据报错{}".format(e))
            return {}
        return data

    def recordLine(self, modelID):
        try:
            LineData = []
            recordDetail = stress_record.objects.filter(Stress_id=self.obj.stressid,
                                                        modelname=modelID,
                                                        aistatus__in=[2, 3],
                                                        type=self.StressType).order_by("start")
            for i in recordDetail:
                LineData.append({
                    "date": i.start[5:],
                    "Prediction": i.sec,
                    "Job": i.job_time
                })
            return LineData
        except Exception as e:
            logger.error("预测趋势数据生成失败：{0}".format(e))
            return []

    def ChartData(self, model):
        try:
            rows = []
            dictColumns = {}
            # 模型 ID
            models = []
            models.append(model[1])
            # 多选模型 循环 处理
            # for i in diseases:
            #     models.append(i[1])

            # 肺模型数据 按照 层厚 分类处理
            if '9' in models or '12' in models:
                columns = ['version', 'Prediction-1.0', 'Job-1.0', 'Prediction-1.25', 'Job-1.25', 'Prediction-1.5',
                           'Job-1.5',
                           'Prediction-5.0', 'Job-5.0', 'Prediction-10.0', 'Job-10.0']
                obj = stress_result.objects.filter(modelname__in=models,
                                                   type=self.StressType,
                                                   slicenumber__in=['10.0', '1.0', '5.0', '1.25', '1.25']).order_by(
                    "version")
                # 循环 数据 按 版本 层厚分类
                for j in obj:
                    try:
                        if dictColumns.__contains__(j.version) is False:
                            dictColumns[j.version] = {"version": j.version,
                                                      'Prediction-{}'.format(j.slicenumber): j.avg,
                                                      'job-{}'.format(j.slicenumber): j.jobavg
                                                      }
                        else:
                            dictColumns[j.version]['Prediction-{}'.format(j.slicenumber)] = j.avg
                            dictColumns[j.version]['job-{}'.format(j.slicenumber)] = j.jobavg
                    except Exception as e:
                        logger.error(e)
                    # 按版本 取key
                for k, v in dictColumns.items():
                    rows.append(v)
            else:
                # 其他模型数据 处理
                columns = ['version', 'Prediction', 'Job']
                obj = stress_result.objects.filter(modelname__in=models, type=self.StressType).order_by("version")
                # 循环 数据 按 版本分类
                for j in obj:
                    try:
                       dictColumns = {"version": j.version,
                                      "Prediction": j.avg,
                                      "Job": j.jobavg}
                       rows.append(dictColumns)
                    except Exception as e:
                        logger.error(e)

            return {
                "columns": columns,
                "rows": rows
            }
        except Exception as e:
            logger.error("性能数据 生成失败：{}".format(e))
        return {}

    def dataCheck(self, CheckVersion):
        if CheckVersion == self.obj.version:
            dictA = stress_result_Deserializer(
                stress_result.objects.filter(Stress_id=self.obj.stressid,
                                             version=self.obj.version,
                                             type=self.StressType), many=True).data
            for i in dictA:
                obj = dictionary.objects.get(id=i['modelname'])
                i['modelname'] = obj.key
        else:
            # 按版本 查询 性能测试记录
            dictA = stress_result_Deserializer(
                stress_result.objects.filter(version=self.obj.version, type=self.StressType), many=True).data
            dictB = stress_result_Deserializer(
                stress_result.objects.filter(version=CheckVersion, type=self.StressType), many=True).data
            # 比较 性能测试记录 结果
            for i in dictA:
                for j in dictB:
                    if i['slicenumber'] is None:
                        a = i['modelname']
                        b = j['modelname']
                    else:
                        a = i['slicenumber']
                        b = j['slicenumber']
                    if a == b:
                        try:
                            for x in ['avg', 'single', 'median', 'min', 'max', 'coef', 'rate', 'minimages', 'maximages',
                                      'avgimages', 'jobavg', 'jobmedian', 'jobmin', 'jobmax']:
                                if i[x] is None: i[x] = 0.0
                                if j[x] is None: j[x] = 0.0

                                if float(i[x]) > float(j[x]):
                                    i[x] = str(i[x]) + "(+" + str(
                                        '%.2f' % (float(i[x]) - float(j[x]))) + ")"
                                elif float(i[x]) == float(j[x]):
                                    i[x] = str(i[x])
                                else:
                                    i[x] = str(i[x]) + " (" + str(
                                        '%.2f' % (float(i[x]) - float(j[x]))) + ")"
                        except Exception as e:
                            logger.error("error:{0}".format(e))
                            continue
                    else:
                        continue
                obj = dictionary.objects.get(id=i['modelname'])
                i['modelname'] = obj.key
        return dictA

    def errorData(self):
        try:
            recorddata = {}
            errorData = []
            recordDetail = stress_record.objects.filter(Stress_id=self.id, aistatus='1')

            for i in recordDetail:
                try:
                    if i.error is not None and i.error != '[]':
                        error = json.loads(i.error[1:-1])["code"]
                        if recorddata.__contains__(error) is False:
                            recorddata[error] = 1
                        else:
                            recorddata[error] = recorddata[error] + 1
                except Exception as e:
                    logger.error("失败：{0}".format(e))
                    continue
            for k, v in recorddata.items():
                errorData.append({'状态': k, '数量': v})
            return errorData
        except Exception as e:
            logger.error("预测趋势数据生成失败：{0}".format(e))
