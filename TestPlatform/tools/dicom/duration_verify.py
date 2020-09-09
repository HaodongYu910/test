# coding = utf-8
from TestPlatform.common.regexUtil import *

from TestPlatform.models import duration_record,duration
from django.db import transaction
from TestPlatform.serializers import duration_record_Deserializer,duration_record_Serializer,duration_Serializer
import logging
logger = logging.getLogger(__name__)

def update_data(data):
    obj = duration_record.objects.get(studyinstanceuid=data["studyinstanceuid"])
    serializer = duration_record_Deserializer(data=data)
    with transaction.atomic():
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)

def ai_result(kc,patientid):
    study_query = " \
                    {{\
                      studyViewFlexible(\
                        filter: [\
                          {{ filter: patientname, value: [\"{0}\"],type: FuzzyMatch,category: PatientInfo }}\
                        ]\
                      ) {{\
                        aistatus,\
                        diagnosis,\
                        instancecount\
                      }}\
                    }}".format(patientid)
    res_study = kc.post(
        url='/graphql',
        json={'query': study_query},
        timeout=120,
        verify=False
    )
    return res_study

def verifyData(id):
    today=str(datetime.date.today()) + ' 00:00:00'
    duration_data = duration_record.objects.filter(create_time__gte=today,studyolduid__isnull=True,duration_id=id)
    obj =duration.objects.filter(id=id)
    if obj.server == "192.168.1.228":
        serverip = "192.168.1.124"
    else:
        serverip = obj.server
    kc = use_keycloak_bmutils(serverip, 'test', 'Asd@123456')
    for i in duration_data:
        data = {'studyinstanceuid':i.studyinstanceuid}
        airesult=ai_result(kc,i.patientid)
        if airesult.json()['data']['studyViewFlexible'] ==[]:
            data['aistatus']= None
            data['diagnosis'] = '--'
            data['instancecount'] = None
        else:
            # text = eval(str(airesult.content, 'utf-8'), globals)
            res_studyView = airesult.json()['data']['studyViewFlexible']
            data['aistatus'] = res_studyView[0].get('aistatus')
            data['diagnosis'] = res_studyView[0].get('diagnosis')
            data['imagecount_server'] = res_studyView[0].get('instancecount')
            if res_studyView[0].get('instancecount') == i.imagecount:
                data['studyolduid']=1
        update_data(data)
    return True

def verify():
    today=str(datetime.date.today()) + ' 00:00:00'
    duration_data = duration_record.objects.filter(create_time__gte=today,studyolduid__isnull=True)

    for i in duration_data:
        data = {'studyinstanceuid':i.studyinstanceuid}
        if i.sendserver=="192.168.1.228":
            serverip="192.168.1.124"
        else:
            serverip=i.sendserver
        kc = use_keycloak_bmutils(serverip, 'test', 'Asd@123456')
        airesult=ai_result(kc,i.patientid)
        if airesult.json()['data']['studyViewFlexible'] ==[]:
            data['aistatus']= None
            data['diagnosis'] = '--'
            data['instancecount'] = None
        else:
            # text = eval(str(airesult.content, 'utf-8'), globals)
            res_studyView = airesult.json()['data']['studyViewFlexible']
            data['aistatus'] = res_studyView[0].get('aistatus')
            data['diagnosis'] = res_studyView[0].get('diagnosis')
            data['imagecount_server'] = res_studyView[0].get('instancecount')
            if res_studyView[0].get('instancecount') == i.imagecount:
                data['studyolduid']=1
        update_data(data)
    return True

# class ImageCount():
#     def __init__(self):
#         self.kc = KeycloakClient('{0}://{1}'.format(
#             CONFIG.get("server").get("http"), CONFIG.get("server").get("ip")), 'biomind',
#             'password')
#         self.kc.login('biomind', 'password')
#
#     def get_one_image_count(self, patient_id):
#         study_query = " \
#         {{\
#           studyViewFlexible(\
#             filter: [\
#               {{ filter: patientname, value: [\"{0}\"],type: FuzzyMatch,category: PatientInfo }}\
#             ]\
#           ) {{\
#             aistatus,\
#             diagnosis,\
#             instancecount\
#           }}\
#         }}".format(patient_id)
#
#         res_study = self.kc.post(
#             url='/graphql',
#             json={'query': study_query},
#             timeout=120,
#             verify=False
#         )
#         globals = {'null': 0}
#
#         if res_study is None:
#             res_studyView=''
#         else:
#             print('------------------------------------------------')
#             text = eval(str(res_study.content, 'utf-8'), globals)
#             res_studyView = text.get("data", {}).get("studyViewFlexible", None)
#         # print(text)
#         result = {}
#
#         if not res_studyView:
#             aistatus = 0
#             diagnosis = 0
#             instancecount = 0
#         else:
#             aistatus = res_studyView[0].get('aistatus')
#             diagnosis = res_studyView[0].get('diagnosis')
#             instancecount = res_studyView[0].get('instancecount')
#         result["aistatus"] = aistatus
#         result["diagnosis"] = diagnosis
#         result["instancecount"] = instancecount
#         # print(result)
#         return result
#
#     def get_all_image_count(self, filename):
#         imagecount_server = []
#         line = 0
#
#         datas = []
#         csv_file = os.path.join(log_path, filename)
#         csvfile = codecs.open(csv_file, 'r+', 'gbk')
#         rows = csv.reader(csvfile)
#         for row in rows:
#             datas.append(row)
#         patientids = [i[3] for i in datas][1:]
#         for patient_id in patientids:
#             result = self.get_one_image_count(patient_id)
#             imagecount_server.append(result)
#
#         csvfile.close()
#
#         csv_name = filename.split(".")[0]
#         writer_path = os.path.join(log_path, csv_name + "_analysis.csv")
#         f = codecs.open(writer_path, 'w+', 'gbk')
#         writer = csv.writer(f)
#         for row in datas:
#             if line == 0:
#                 row.extend(["imagecount_server", "aistatus", "diagnosis"])
#             else:
#                 temp = imagecount_server[line - 1]
#                 row.extend([temp.get("instancecount", 0), temp.get("aistatus", 0), temp.get("diagnosis", 0)])
#             line = line + 1
#             writer.writerow(row)
#         f.close()
#
#
# def un_analysis(folder):
#     send_csv = []
#     analysis_csv = []
#     for eachfile in os.listdir(folder):
#         if os.path.isfile(os.path.join(folder, eachfile)):
#             if (len(eachfile.split("_")) == 2) and (eachfile.split("_", 1)[0] == "records"):
#                 send_csv.append(eachfile)
#             elif len(eachfile.split("_")) == 3:
#                 analysis_csv.append(eachfile)
#     logger.info(send_csv)
#     for eachfile in analysis_csv:
#         if eachfile.rsplit("_", 1)[0] in send_csv:
#             send_csv.remove(eachfile.rsplit("_", 1)[0])
#     return send_csv
#
#
#
# def runVerify(server_ip):
#     global log_path
#     global CONFIG
#     try:
#         CONFIG["server"]["ip"] = server_ip
#     except Exception as e:
#         logger.error("error: failed to get args")
#
#     log_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")),
#                             'logs/{0}'.format(CONFIG["server"]["ip"]))
#     ic = ImageCount()
#     # # ic.get_one_image_count('duration4814428')
#     unanalysis = un_analysis(log_path)
#     for filename in unanalysis:
#         ic.get_all_image_count(filename)
#
#
# runVerify('192.168.1.122')
