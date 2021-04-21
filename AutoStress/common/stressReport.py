from AutoStress.models import stress, stress_result, stress_record
from AutoProject.models import dictionary
from django.db.models import Count, Case, When
from AutoProject.common.message import sendMessage
import datetime
import logging


logger = logging.getLogger(__name__)



# 执行冒烟测试
class StressReport:
    def __init__(self, *args):
        self.id = args[0]
        self.obj = stress.objects.get(stressid=self.id)
        self.serverIP = self.obj.Host.host

    def report(self):
        models = {}
        try:
            aiObj = stress_record.objects.filter(
                Stress_id=int(self.id), type="predictionrecord").values('Stress_id').annotate(
                total=Count(1),
                success=Count(Case(When(aistatus=3, then=0))),
                fail=Count(Case(When(aistatus=1, then=0))),
                )
            if not aiObj:
                total = 0
                success = 0
                fail = 0
            else:
                total = aiObj[0]["total"]
                success = aiObj[0]["success"]
                fail = aiObj[0]["success"]

            for j in self.obj.testdata.split(","):
                dictObj = dictionary.objects.get(id=j)
                models[j] = dictObj.key
            data = {
                "basedata": {
                    "version": self.obj.version,
                    "server": self.obj.Host.host,
                    "total": total,
                    "success": success,   # 成功
                    "fail": fail,      # 失败
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

    def errorData(self):
        try:
            recorddata = {}
            errorData = []
            recordDetail = stress_record.objects.filter(Stress_id=self.id)

            for i in recordDetail:
                try:
                    if i.error is not None:
                        if recorddata.__contains__(i.error) is False:
                            recorddata[i.error] = 1
                        else:
                            recorddata[i.error] = recorddata[i.error] + 1
                except Exception as e:
                    logger.error("失败：{0}".format(e))
                    continue
            for k, v in recorddata.items():
                errorData.append({'状态': k, '数量': v})
            return errorData
        except Exception as e:
            logger.error("预测趋势数据生成失败：{0}".format(e))