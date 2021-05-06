from AutoInterface.models import gold_record, gold_test
from django.db.models import Count, Case, When
from AutoProject.common.message import sendMessage
import datetime
import logging

logger = logging.getLogger(__name__)



# 执行冒烟测试
class GoldReport:
    def __init__(self, *args):
        self.id = args[0]
        self.smobj = gold_test.objects.get(id=self.id)
        self.smobj.starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.serverIP = self.smobj.Host.host

    def report(self):
        result = []
        goldData = []
        try:
            smokediseases = gold_record.objects.filter(gold_id=self.id).values('diseases').annotate(
                total=Count('gold_id'),
                success=Count(Case(When(result='匹配成功', then=0))), fail=Count(Case(When(result='匹配失败', then=0))),
                count=Count('diseases'))

            for j in smokediseases:
                errorInfo = {}
                failInfo = ""
                obl = gold_record.objects.filter(gold_id=self.id, diseases=j["diseases"])
                # 按病种 统计 错误 信息
                for jj in obl:
                    if jj.result is not None and jj.result not in ['匹配成功', '匹配失败']:
                        if errorInfo.__contains__(jj.result) is False:
                            errorInfo[jj.result] = 1
                        else:
                            errorInfo[jj.result] = errorInfo[jj.result] + 1
                    elif jj.result == '匹配失败':
                       failInfo = failInfo + " <b>{0} -预期：{1} /实际：{2}<b><br/>".format(jj.patientid, jj.diagnosis, jj.aidiagnosis)

                error = int(j["count"]) - int(j["success"]) - int(j["fail"])
                disease = {
                    "diseases": j["diseases"],
                    "total":j["total"],
                    "aisuccess": int(j["success"]) + int(j["fail"]),
                    "success": j["success"],
                    "fail": j["fail"],
                    "error": error,
                    "errorInfo": errorInfo,
                    "failInfo": failInfo
                }
                goldData.append(disease)

            for k in ['成功', '失败']:
                smobj = gold_record.objects.filter(gold_id=self.id, result__contains=k)
                result.append(smobj.count())
            smerror = int(gold_record.objects.filter(gold_id=self.id).count()) - int(result[0]) - int(
                result[1])

            data = {
                "basedata": {
                    "version": self.smobj.version,
                    "server": self.smobj.Host.host,
                    "product": '金标准测试',
                    "total": int(result[0]) + int(result[1]) + int(smerror),
                    "aisuccess": int(result[0]) + int(result[1]), # 预测成功
                    "success": result[0],   # 匹配成功
                    "fail": result[1],      # 匹配失败
                    "error": smerror,       # 报错
                    "start_date": self.smobj.starttime,
                    "end_date": self.smobj.completiontime
                },
                "goldrows": [
                    {'状态': '匹配成功', '数量': result[0]},
                    {'状态': '匹配失败', '数量': result[1]},
                    {'状态': '报错', '数量': smerror}
                ],
                "goldData": goldData
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
            recordDetail = gold_record.objects.filter(gold_id=self.id)

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