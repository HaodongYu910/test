# coding=utf-8
import os
import random

import pydicom
from tqdm import tqdm
import time
import logging

logger = logging.getLogger(__name__)
# code may has efficient issues. I didn't release the memory which is allocated by dic.

def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


def onlyDoAnonymization(src_folder, study_infos, diseases, wPN, wPID, anonkey, ap_addr):
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
    for fn in tqdm(file_names):
        full_fn = os.path.join(src_folder, fn)
        if (os.path.isdir(full_fn)):
            onlyDoAnonymization(full_fn, study_infos, diseases, wPN, wPID, anonkey, ap_addr)
            logging.info('-------------this is a folder,skiping....')
            continue
        else:
            ds = pydicom.dcmread(full_fn, force=True) # 读取该路径文件的dicom信息
            try:
                if ds.StudyInstanceUID and ds.PatientID and ds.PatientName: # 如果该文件存在UID等信息
                    logging.info('1. this is a truly dicom document')
                    if ds.StudyInstanceUID not in study_infos.keys():   # 如果UID没在dic里面
                        study_infos[ds.StudyInstanceUID] = {"patientID": {}, "patientName": {}}  # 在dic里面创建这个UID分支
                        logging.info('2. insert UID in dic')
                    try:
                        if wPID:
                            # 判断pID是否有值
                            if study_infos[ds.StudyInstanceUID]["patientID"]:  # has value
                                ds.PatientID = study_infos[ds.StudyInstanceUID]["patientID"]
                                logging.info('3. has pID [{0}], detect pid from dic'.format(ds.PatientID))
                            elif not study_infos[ds.StudyInstanceUID]["patientID"]:  # no value
                                ds.PatientID = norm_string("{0}_{1}{2}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time())), randomFourNum(4)), 32)
                                study_infos[ds.StudyInstanceUID]["patientID"] = ds.PatientID
                                logging.info('3. do not have pID [{0}], creating ......'.format(ds.PatientID))
                        if wPN:
                            if study_infos[ds.StudyInstanceUID]["patientName"]:  # PN有值
                                ds.PatientName = study_infos[ds.StudyInstanceUID]["patientName"]
                                logging.info('4. has pN [{0}], detect pN from dic'.format(ds.PatientName))
                            elif not study_infos[ds.StudyInstanceUID]["patientName"]:  # PN没有值
                                ds.PatientName = norm_string("{0}_{1}{2}".format(anonkey, time.strftime("%H%M%S", time.localtime(time.time())), randomFourNum(4)), 32)
                                study_infos[ds.StudyInstanceUID]["patientName"] = ds.PatientName
                                logging.info('4. do not has pN [{0}], creating.....'.format(ds.PatientName))

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
                        folder_fake = '{0}/{1}/{2}'.format(ap_addr, diseases, ds.PatientName)
                        if not os.path.exists(folder_fake):
                            logging.info('5. do not have this path. creating...[{0}]'.format(folder_fake))
                            os.makedirs(folder_fake)
                            # record into db
                        else:
                            logging.info('5. path [{0}] is exists, only save'.format(folder_fake))
                        study_infos["No"] = nextNumber(folder_fake)
                        full_fn_fake = '{0}/{1}.dcm'.format(folder_fake, str(study_infos["No"]))
                        ds.save_as(full_fn_fake)
                        logging.info('6. save complete [{0}]'.format(full_fn_fake))
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
                # logger.error('errormsg: failed to read file [{0}]'.format(full_fn))
                continue


# 判断该路径下有多少个文件，并返回n+1
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

# 创建n位随机数
def randomFourNum(n):
    num_str = ''
    i = 0
    while i<n :
        num_str = num_str + str(random.randint(0,9))
        i = i + 1
    return num_str