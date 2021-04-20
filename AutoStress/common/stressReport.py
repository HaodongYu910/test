from AutoStress.models import stress, stress_result, stress_record
from django.db.models import Count, Case, When
from AutoProject.common.message import sendMessage
import datetime
import logging


logger = logging.getLogger(__name__)



# 执行冒烟测试
class StressReport:
    def __init__(self, *args):
        self.id = args[0]
        self.obj = stress.objects.get(stressid= self.id)
        self.serverIP = self.obj.Host.host

    def report(self):
        result = []
        StressData = []
        try:
            modelname = stress_record.objects.filter(Stress_id=self.id, type="predictionrecord").values('modelname').annotate(
                total=Count('Stress_id'),
                success=Count(Case(When(aistatus=3, then=0))), fail=Count(Case(When(aistatus='1', then=0))),
                )

            # for j in modelname:
            #     errorInfo = {}
            #     failInfo = ""
            #     obl = stress_record.objects.filter(gold_id=self.id, diseases=j["diseases"])
            #     # 按病种 统计 错误 信息
            #     for jj in obl:
            #         if jj.result is not None and jj.result not in ['匹配成功', '匹配失败']:
            #             if errorInfo.__contains__(jj.result) is False:
            #                 errorInfo[jj.result] = 1
            #             else:
            #                 errorInfo[jj.result] = errorInfo[jj.result] + 1
            #         elif jj.result == '匹配失败':
            #            failInfo = failInfo + " <b>{0} -预期：{1} /实际：{2}<b><br/>".format(jj.patientid, jj.diagnosis, jj.aidiagnosis)
            #
            #     error = int(j["count"]) - int(j["success"]) - int(j["fail"])
            #     modelname = {
            #         "diseases": j["diseases"],
            #         "total":j["total"],
            #         "aisuccess": int(j["success"]) + int(j["fail"]),
            #         "success": j["success"],
            #         "fail": j["fail"],
            #         "error": error,
            #         "errorInfo": errorInfo,
            #         "failInfo": failInfo
            #     }
            #     StressData.append(modelname)

            # obj = stress_record.objects.filter(Stress_id=self.id, result__contains=k)

            data = {
                "basedata": {
                    "version": self.obj.version,
                    "server": self.obj.Host.host,
                    "total": 10,
                    "success": 5,   # 成功
                    "fail": 1,      # 失败
                    "start_date": self.obj.start_date,
                    "end_date": self.obj.end_date,
                    "server": self.obj.Host.host,
                    "serverInfo": self.obj.Host.description,
                },
                "goldrows": [
                    {'状态': '预测成功', '数量': 5},
                    {'状态': '预测失败', '数量': 5}
                ],
                "stressData": StressData
                # ,
                # "errorData": self.errorData()
            }
        except Exception as e:
            logger.error("数据报错{}".format(e))
            return {}
        return data

    def errorData(self):
        try:
            recorddata = {}
            errorData = []
            recordDetail = stress_record.objects.filter(Stress_id=self.id)

            for i in recordDetail:
                if i.result is not None and i.result not in ['匹配成功', '匹配失败']:
                    if recorddata.__contains__(i.result) is False:
                        recorddata[i.result] = 1
                    else:
                        recorddata[i.result] = recorddata[i.result] + 1
            for k, v in recorddata.items():
                errorData.append({'状态': k, '数量': v})

            return errorData
        except Exception as e:
            logger.error("预测趋势数据生成失败：{0}".format(e))