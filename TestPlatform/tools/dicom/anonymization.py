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

def onlyDoAnonymization(src_folder,study_infos,diseases,wPN,wPID,anonkey):
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
            onlyDoAnonymization(full_fn,study_infos,diseases,wPN,wPID,anonkey)
            continue
        elif (os.path.splitext(fn)[1] == ".dcm"):
            try:
                ds = pydicom.dcmread(full_fn, force=True)
                study_infos["No"] = study_infos["No"]+1
                try:
                    if wPID:
                        ds.PatientID = norm_string("{0}_{1}".format(anonkey,time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                    elif not wPID:
                        continue

                    if wPN:
                        if ds.StudyInstanceUID in study_infos.keys():
                            ds.PatientName = study_infos[ds.StudyInstanceUID]
                        elif ds.StudyInstanceUID not in study_infos.keys():
                            ds.PatientName = norm_string("{0}_{1}".format(anonkey,time.strftime("%H%M%S", time.localtime(time.time()))), 16)
                            study_infos[ds.StudyInstanceUID] = ds.PatientName
                    elif not wPN:
                        continue

                    # 保存文件匿名化之后的文件到192.168.1.121：/files/QA_FTP/testData/anonymization
                    folder_fake = '/files/anonymization/{0}/{1}'.format(diseases, ds.PatientName)
                    if not os.path.exists(folder_fake):
                        os.makedirs(folder_fake)
                    full_fn_fake = '{0}/{1}.dcm'.format(folder_fake,str(study_infos["No"]))
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
    a = 'success'
    return a