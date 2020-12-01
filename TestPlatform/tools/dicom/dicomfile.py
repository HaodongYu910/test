# coding=utf-8

import os
import pydicom
from tqdm import tqdm
import time,datetime
import random
import math
import logging
from TestPlatform.models import base_data,dicom,dicom_route

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置。

#

def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest

#
def fake_folder(src_folder,study_infos,diseases,type,uidInfos):

    file_names = os.listdir(src_folder)
    file_names.sort()

    for fn in tqdm(file_names):
        full_fn = os.path.join(src_folder, fn)
        full_fn_fake = os.path.join('/files/dicomTest', fn)

        if (os.path.splitext(fn)[1] in ['.dcm'] == False):
            continue

        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn,study_infos,diseases,type,uidInfos)
            continue
        try:
            ds = pydicom.dcmread(full_fn, force=True)
            study_uid = ds.StudyInstanceUID
            if uidInfos.get(study_uid):
                continue
            try:
                if ds.PatientID:
                    patientid = ds.PatientID
                else:
                    ds.PatientID = norm_string("{0}_{1}".format(diseases,time.strftime("%m%d%H%M%S", time.localtime(time.time()))), 16)
                    patientid = ds.PatientID
                if ds.PatientName:
                    patientname = ds.PatientName
                else:
                    ds.PatientName = norm_string("{0}_{1}".format(diseases,time.strftime("%m%d%H%M%S", time.localtime(time.time()))), 16)
                    patientname = ds.PatientName

            except Exception as e:
                logging.info(
                    'failed to : file[{0}], error[{1}]'.format(full_fn, e))
            try:
                ds.save_as(full_fn_fake)
            except Exception as e:
                logging.error('errormsg: failed to save file [{0}]'.format(full_fn_fake))
                continue
            data={
                "patientname": patientname,
                "patientid": patientid,
                "studyinstanceuid": study_uid,
                "diseases": diseases,
                "type": type,
                "status": True
            }
            route={
                "study_uid": study_uid,
                "route": full_fn_fake
            }
            dicom_route.objects.create(**route)
            try:
                if study_infos.get(study_uid):
                    continue
                else:
                    study_infos[study_uid]=study_uid
                    dicom.objects.create(**data)
            except Exception as e:
                logging.error('errormsg: failed to sql [{0}]'.format(e))


        except Exception as e:
            logger.error('errormsg: failed to read file [{0}]'.format(full_fn))
            continue

def fileUpdate(id):
    obj= base_data.objects.get(id=id)
    uids =dicom.objects.filter(diseases=obj.remarks)
    uidInfos = {}
    study_infos ={}
    for i in uids:
        study_uid=i.studyinstanceuid
        uidInfos[i.studyinstanceuid]=i.studyinstanceuid
        src_folder = obj.content
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]
    fake_folder(src_folder=src_folder,study_infos=study_infos,diseases=obj.remarks,type=obj.type,uidInfos=uidInfos)
    obj.other =len(study_infos)
    obj.save()


def fileSave(id):
    obj= base_data.objects.get(id=id)
    study_infos = {}
    uidInfos = {}
    src_folder = obj.content
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]
    fake_folder(src_folder=src_folder,study_infos=study_infos,diseases=obj.remarks,type=obj.type,uidInfos=uidInfos)
    obj.other =len(study_infos)
    obj.save()






