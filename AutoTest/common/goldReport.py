from AutoTest.utils.keycloak.login_kc import *
from AutoDicom.models import dicom, dicom_base
from AutoTest.models import dictionary, smoke
from AutoTest.utils.graphql.graphql import *
from AutoTest.models import smoke_record, dictionary, pid
from AutoTest.utils.graphql.graphql_ai_status import graphql_ai_status
from AutoDicom.common.dicomBase import checkuid
import queue
from django.db.models import Count, Case, When
from ..common.message import sendMessage
import datetime
import time
import threading

logger = logging.getLogger(__name__)



# 执行冒烟测试
class GoldReportThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.id = args[0]
        self.smobj = smoke.objects.get(id=self.id)
        self.smobj.starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.serverIP = self.smobj.Host.host

    def report(self):
        result = []
        goldData = []
        try:
            smokediseases = smoke_record.objects.filter(smokeid=self.id).values('diseases').annotate(
                total=Count('smokeid'),
                success=Count(Case(When(result='匹配成功', then=0))), fail=Count(Case(When(result='匹配失败', then=0))),
                count=Count('diseases'))

            for j in smokediseases:
                errorInfo = {}
                failInfo = ""
                obl = smoke_record.objects.filter(smokeid=self.id, diseases=j["diseases"])
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
                smobj = smoke_record.objects.filter(smokeid=self.id, result__contains=k)
                result.append(smobj.count())
            smerror = int(smoke_record.objects.filter(smokeid=self.id).count()) - int(result[0]) - int(
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

    def sendMessage(self):
        result = []
        for k in ['成功', '失败']:
            smobj = smoke_record.objects.filter(smokeid=self.id, result__contains=k)
            result.append(smobj.count())
        smerror = int(smoke_record.objects.filter(smokeid=self.id).count()) - int(result[0]) - int(
            result[1])
        total = int(result[0]) + int(result[1]) + int(smerror)
        sendMessage(touser='', toparty='132',
                    message='【Nightly Build -金标准测试】 \n 测试版本：{0} \n 测试服务：{1}  \n 共计预测：{2} \n 预测成功：{3}  预测失败：{4}  \n 匹配成功：{5}  匹配失败：{6}  \n 详细报告查看：http:192.168.1.121/#/report/goldid={7}'.format(
                        self.smobj.version, self.smobj.Host.host, total,
                        int(result[0]) + int(result[1]), result[0], result[1], smerror, self.smobj.id

                    ))

    def errorData(self):
        try:
            recorddata = {}
            errorData = []
            recordDetail = smoke_record.objects.filter(smokeid=self.id)

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
    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.count