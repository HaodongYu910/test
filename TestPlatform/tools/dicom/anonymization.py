# coding=utf-8
import os
import pydicom
from tqdm import tqdm
import time
import logging

logger = logging.getLogger(__name__)


def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


def onlyDoAnonymization(src_folder, study_infos, diseases, wPN, wPID, anonkey):
    '''
    src_folder: folder need be anonymization
    study_infos: empty dictionary{}
    diseases: input parameter from front
    wPN:boolean值，是否匿名patient name
    wPID:boolean值，是否匿名patient ID
    anonkey:匿名化key值
    '''
    file_names = os.listdir(src_folder)
    file_names.sort()
    time.sleep(0.5)
    for fn in tqdm(file_names):
        full_fn = os.path.join(src_folder, fn)
        if (os.path.isdir(full_fn)):
            onlyDoAnonymization(full_fn, study_infos, diseases, wPN, wPID, anonkey)
            continue
        elif (os.path.splitext(fn)[1] == ".dcm"):
            try:
                # study_infos["No"] = study_infos["No"] + 1
                ds = pydicom.dcmread(full_fn, force=True)
                if ds.StudyInstanceUID not in study_infos.keys():
                    study_infos[ds.StudyInstanceUID] = {"patientID": {}, "patientName": {}}
                try:
                    if wPID:
                        # 判断pID是否有值
                        if study_infos[ds.StudyInstanceUID]["patientID"]:  # has value
                            ds.PatientID = study_infos[ds.StudyInstanceUID]["patientID"]
                        elif not study_infos[ds.StudyInstanceUID]["patientID"]:  # no value
                            ds.PatientID = norm_string("{0}_{1}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                            study_infos[ds.StudyInstanceUID]["patientID"] = ds.PatientID
                    if wPN:
                        if study_infos[ds.StudyInstanceUID]["patientName"]:  # PN有值
                            ds.PatientName = study_infos[ds.StudyInstanceUID]["patientName"]
                        elif not study_infos[ds.StudyInstanceUID]["patientName"]:  # PN没有值
                            ds.PatientName = norm_string("{0}_{1}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                            study_infos[ds.StudyInstanceUID]["patientName"] = ds.PatientName

                    # # 判断要不要进行pid和pn的匿名化
                    # if wPID:
                    #     # 判断字典中UID是否存在
                    #     if ds.StudyInstanceUID in study_infos.keys(): #字典有这个UID
                    #         #判断pID是否有值
                    #         if study_infos[ds.StudyInstanceUID]["patientID"]:
                    #             ds.PatientID = study_infos[ds.StudyInstanceUID]["patientID"]
                    #         elif not study_infos[ds.StudyInstanceUID]["patientID"]:
                    #             ds.PatientID = norm_string("{0}_{1}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                    #             study_infos[ds.StudyInstanceUID]["patientID"] = ds.PatientID
                    #     elif ds.StudyInstanceUID not in study_infos.keys(): #字典没有这个UID
                    #         study_infos[ds.StudyInstanceUID] = {"patientID": {}, "patientName": {}}
                    #         ds.PatientID = norm_string("{0}_{1}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                    #         study_infos[ds.StudyInstanceUID]["patientID"] = ds.PatientID
                    # if wPN:
                    #     if ds.StudyInstanceUID in study_infos.keys(): #字典有这个UID
                    #         # 判断PN是否有值
                    #         if study_infos[ds.StudyInstanceUID]["patientName"]: #PN有值
                    #             ds.PatientName = study_infos[ds.StudyInstanceUID]["patientName"]
                    #         elif not study_infos[ds.StudyInstanceUID]["patientName"]: # PN没有值
                    #             ds.PatientName = norm_string("{0}_{1}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                    #             study_infos[ds.StudyInstanceUID]["patientName"] = ds.PatientName
                    #     elif ds.StudyInstanceUID not in study_infos.keys(): #字典没有这个UID
                    #         study_infos[ds.StudyInstanceUID] = {"patientID": {}, "patientName": {}}
                    #         ds.PatientName = norm_string("{0}_{1}".format(anonkey,time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                    #         study_infos[ds.StudyInstanceUID]["patientName"] = ds.PatientName

                    # 保存文件匿名化之后的文件到192.168.1.121：/files/QA_FTP/testData/anonymization
                    #folder_fake = 'C:\\Users\\yuhaodong\\Desktop\\test\\{0}\\{1}'.format(diseases, ds.PatientName)
                    folder_fake = '/files/QA_FTP/testData/anonymization'.format(diseases, ds.PatientName)
                    if not os.path.exists(folder_fake):
                        logging.info('do not have this path. creating...')
                        os.makedirs(folder_fake)
                        # record into db
                    study_infos["No"] = nextNumber(folder_fake)
                    full_fn_fake = '{0}/{1}.dcm'.format(folder_fake, str(study_infos["No"]))
                    ds.save_as(full_fn_fake)
                except Exception as e:
                    logging.info(
                        'failed to : file[{0}], error[{1}]'.format(full_fn, e))
                    continue

                # data = {
                #     "patientid": patientid,
                #     "studyinstanceuid": study_uid,
                #     "diseases": diseases,
                #     "type": type,
                #     "route": folder_fake,
                #     "fileid":id
                # }

                # link with database
                # try:
                #     if study_infos.get(study_uid):
                #         continue
                #     else:
                #         study_infos[study_uid]=study_uid
                #         dicom.objects.create(**data)
                # except Exception as e:
                #     logging.error('errormsg: failed to sql [{0}]'.format(e))
                #     continue

            except Exception as e:
                logger.error('errormsg: failed to read file [{0}]'.format(full_fn))
                continue


# def nextNumber(addr):
#     files = os.listdir(addr)
#     if files:
#         files.sort(reverse = True)
#         tmp = files[0]
#         tmp = tmp.split('.', 1)[0]
#         tmp = int(tmp) + 1
#     elif not files:
#         tmp = 0
#     return tmp

def nextNumber(addr):
    files = os.listdir(addr)
    if files:
        tmp = list()
        for i in files:
            i = str(i)
            i = i.split(".", 1)[0]
            tmp.append(int(i))
        tmp.sort(reverse=True)
        a = tmp[0] + 1
        return a
    elif not files:
        tmp = 0
        return tmp
