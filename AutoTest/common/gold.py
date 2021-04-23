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


# 比对 studyView 接口返回值
def checkdata(data, kc):
    aidiagnosis = ''
    Breast = False
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
                    try:
                        for k, v in airesult['diagnosis'][0].item():
                            if v == 1:
                                aidiagnosis = aidiagnosis + KeyChange(str(k))
                                if data["diagnosis"] == k:
                                    Breast = True
                        if Breast is False:
                            data["result"] = '匹配失败'
                    except Exception as e:
                        logger.error("乳腺数据判断失败:{}".format(e))
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
        self.kc = login_keycloak(self.smobj.Host.id)

    def QueData(self):
        q = queue.Queue()
        try:
            dicomObj = dicom.objects.filter(fileid__in=self.smobj.diseases.split(","), status=True)
            for i in dicomObj:
                if self.Flag is False:
                    break
                try:
                    # 验证数据是否存在
                    checkuid(self.smobj.Host_id, self.serverIP, i.id)
                    # 添加队列
                    q.put({
                        "version": self.smobj.version,
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
                    logger.error("队列生成错误{0}：{1}".format(i.studyinstanceuid,e))
                    continue
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

        except Exception as e:
            logger.error("队列生成失败：{0}".format(e))


        self.smobj.completiontime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.smobj.status = False
        self.smobj.save()
        self.sendMessage()

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

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.count