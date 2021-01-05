# coding=utf-8

import os
import pydicom
from tqdm import tqdm
import logging
from TestPlatform.models import base_data,dicom
from django.db.models import Max

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置。

#

def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest

#
def fake_folder(src_folder,study_infos,diseases,type,uidInfos,id):
    file_names = os.listdir(src_folder)
    file_names.sort()
    for fn in tqdm(file_names):
        full_fn = os.path.join(src_folder, fn)
        if (os.path.splitext(fn)[1] in ['.dcm'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn,study_infos,diseases,type,uidInfos,id)
            continue
        try:
            ds = pydicom.dcmread(full_fn, force=True)
            study_uid = ds.StudyInstanceUID
            study_infos["No"] = study_infos["No"]+1
            if uidInfos.get(study_uid):
                continue
            try:
                if study_infos.__contains__(study_uid) is False:
                    obj = dicom.objects.all().aggregate(Max('id'))
                    study_infos["filename"] = int(obj["id__max"]) + 1
                if ds.PatientName:
                    patientname = ds.PatientName
                else:
                    if study_infos.get(study_uid):
                        patientname = study_infos[study_uid]
                    else:
                        patientname = norm_string("BM_{0}_{1}".format(diseases,str(study_infos["filename"])))
                    ds.PatientName = patientname
                if ds.PatientID:
                    patientid = ds.PatientID
                else:
                    patientid = patientname
                    ds.PatientID = patientid
                folder_fake = '/files/dicomTest/{0}/{1}/{2}'.format(type,diseases, str(patientname) + str(study_infos["filename"]))
                if not os.path.exists(folder_fake):
                    os.makedirs(folder_fake)
                full_fn_fake = '{0}/{1}.dcm'.format(folder_fake,str(study_infos["No"]))
                ds.save_as(full_fn_fake)
            except Exception as e:
                logger.error(
                    'failed to : file[{0}], error[{1}]'.format(full_fn, e))
                continue

            data = {
                "patientid": patientid,
                "patientname": patientname,
                "studyinstanceuid": study_uid,
                "diseases": diseases,
                "type": type,
                "route": folder_fake,
                "fileid": id
            }
            try:
                if study_infos.get(study_uid):
                    continue
                else:
                    study_infos[study_uid] = patientid
                    dicom.objects.create(**data)
            except Exception as e:
                logger.error('errormsg: failed to sql [{0}]'.format(e))
                continue

        except Exception as e:
            logger.error('errormsg: failed to read file [{0}]'.format(full_fn))
            continue

def fileSave(id,type):
    global filename
    obj= base_data.objects.get(id=id)
    uids =dicom.objects.filter(diseases=obj.remarks)
    uidInfos = {}
    study_infos ={}
    study_infos["No"] = 0
    src_folder = obj.content
    if type =='update':
        for i in uids:
            uidInfos[i.studyinstanceuid]=i.studyinstanceuid
            src_folder = obj.content
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]
    fake_folder(
        src_folder=src_folder,
        study_infos=study_infos,
        diseases=obj.remarks,
        type=obj.type,
        uidInfos=uidInfos,
        id=id
    )
    obj.other =int(len(study_infos))-1
    obj.save()




