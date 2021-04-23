from AutoTest.common.PostgreSQL import connect_postgres
from AutoTest.utils.keycloak.login_kc import *
from AutoDicom.models import dicom, dicom_base
from AutoTest.models import dictionary, smoke
from AutoTest.utils.graphql.graphql import *
from AutoTest.models import smoke_record, dictionary, pid
from AutoTest.common.message import sendMessage
from AutoDicom.common.deletepatients import delete_patients_duration
from AutoTest.utils.graphql.graphql_ai_status import graphql_ai_status
from AutoDicom.common.dicomBase import checkuid
import queue
from django.db.models import Count, Case, When
import json
import datetime
import time
import threading

logger = logging.getLogger(__name__)


# 比对 studyView 接口返回值
def checkdata(data, kc):
    aidiagnosis = ''
    result = graphql_ai_status(data["studyinstanceuid"], kc)
    if result is False:
        data["result"] = '查询预测结果报错'
    else:
        try:  # 比对结果
            airesult = result['studyView'][0]
            if airesult['aistatus'] in [2, 3]:
                data["status"] = True
                # 判断标准结果是否在本次预测结果 中
                if str(airesult['diagnosis']).find(data["diagnosis"]) >= 0:
                    aidiagnosis = KeyChange(data["diagnosis"])
                # 判断是否正常数据
                elif data["diagnosis"] == 'normal':
                    if len(airesult['diagnosis'][0]) == 0:
                        aidiagnosis = data["diagnosis"]
                    else:
                        for i in airesult['diagnosis'][0]:
                            aidiagnosis = KeyChange(str(i)) + ',' + aidiagnosis
                        data["result"] = '匹配失败'
                # 乳腺数据单独判断
                elif data["diseases"] in ['Breast', 'Breast_new']:
                    for k, v in airesult['diagnosis'][0].item():
                        if v == 1:
                            aidiagnosis = aidiagnosis + KeyChange(str(k))
                            if data["diagnosis"] == k:
                                Breast =True
                        else:
                            data["result"] = '匹配失败'
                    if Breast is False:
                        data["result"] = '匹配失败'
                # 匹配失败数据转换处理
                else:
                    # 循环取结果
                    for i in airesult['diagnosis'][0]:
                        aidiagnosis = KeyChange(str(i)) + ',' + aidiagnosis
                    data["result"] = '匹配失败'
            else:
                data["result"] = str(result)[:500]
        except Exception as e:
            data["result"] = str(e)[:1000]
    data["diagnosis"] = KeyChange(data["diagnosis"])
    data["aidiagnosis"] = aidiagnosis
    data["aistatus"] = airesult["aistatus"]
    smoke_record.objects.create(**data)


# 预测验证记录
def predictionCheck(result, data, error):
    data["aidiagnosis"] = ''
    try:
        ai_biomind = result['ai_biomind']
        try:
            data["result"] = str(ai_biomind['pstatus_code'][0]['code'])
            smoke_record.objects.create(**data)
        except Exception as e:
            return True
    except Exception as e:
        data["result"] = str(error)[:500]
        smoke_record.objects.create(**data)
        logger.error("比对失败:{0},预测结果:{1}".format(e, result))


# 预测结论转换
def KeyChange(key):
    try:
        obj = dictionary.objects.get(key__contains=key, type='diseases')
        return obj.value
    except Exception as e:
        logger.error("无此结果:{1}".format(e, key))
        return key


# 删除dicom报告
def delresult(serverID, ids):
    kc = login_keycloak(serverID)
    # 循环删除数据报告
    for i in ids:
        try:
            obj = dicom.objects.get(id=i)
            graphql_query = 'mutation{ ' \
                            'deleteresult( studyuid:' + str(obj.studyinstanceuid) + ' )' \
                                                                                    'deleteProtocol( studyuid:' + str(
                obj.studyinstanceuid) + ' ) }'
            graphql_Interface(graphql_query, kc)
        except:
            logger.error("删除失败{0}".format(obj.studyinstanceuid))
            continue


# 执行冒烟测试
class GoldThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        self.count = 0  # 用来被外部访问的
        self.id = args[0]
        self.smobj = smoke.objects.get(id=self.id)
        self.smobj.starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.serverIP = self.smobj.Host.host

    def QueData(self):
        q = queue.Queue()
        try:
            for k in self.smobj.diseases.split(","):
                try:
                    dicomobj = dicom.objects.filter(fileid=k.strip(), status=True)
                except Exception as e:
                    logger.error("数据错误")
                    continue
                for i in dicomobj:
                    try:
                        if self.Flag is False:
                            break
                        # 验证数据是否存在
                        checkuid(self.smobj.Host_id, self.serverIP, i.id)
                        # 修改执行进度
                        try:
                            q.put(
                                {"version": self.smobj.version,
                                 "patientid": i.patientid,
                                 "patientname": i.patientname,
                                 "studyinstanceuid": i.studyinstanceuid,
                                 "diseases": i.diseases,
                                 "slicenumber": i.slicenumber,
                                 "diagnosis": i.diagnosis,
                                 "type": "gold",
                                 "status": False,
                                 "smokeid": self.id,
                                 "result": "匹配成功",
                                 "starttime": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                 "graphql": i.graphql
                                 })
                        except Exception as e:
                            logging.error("[错误]:{}".format(e))
                            continue
                    except Exception as e:
                        logger.error("错误：{}".format(e))
            return q
        except Exception as e:
            logger.error("队列错误：{}".format(e))

    def run(self):
        q = self.QueData()
        threads = []
        try:
            for i in range(int(self.smobj.thread)):
                t = threading.Thread(target=self.graphqlRun, args=(q,))
                # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                time.sleep(1)
            self.sendMessage()
        except Exception as e:
            logger.error("队列生成失败：{0}".format(e))

        self.smobj.completiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.smobj.status = False
        self.smobj.progress = self.smobj.count
        self.smobj.save()

    def graphqlRun(self, q):
        # 调用 手动预测接口
        while not q.empty():
            if self.Flag == False:
                break
            testdata = q.get()
            try:
                prediction = graphql_Interface(testdata["graphql"], self.kc)
                del testdata["graphql"]
            except Exception as e:
                predictionCheck(prediction, testdata, e)
                continue
            testdata["completiontime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 断言
            try:
                Check = predictionCheck(prediction, testdata, '')
                if Check is True:
                    checkdata(testdata, self.kc)
            except Exception as e:
                logger.error("error:{0}".format(e))
                testdata["result"] = str(e)[:500]
                smoke_record.objects.create(**testdata)
                continue

    # 金标准测试报告
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
