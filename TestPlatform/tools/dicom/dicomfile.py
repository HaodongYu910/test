# coding=utf-8

import os
import pydicom
from tqdm import tqdm
import logging
from TestPlatform.models import base_data, dicom
from django.db.models import Max
import shutil
import time

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置。


#

def norm_string(str):
    str_dest = str
    while len(str_dest) > 16 or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


# 更新文件到 测试目录 安装类型分类重新命名
def updateFolder(src_folder, study_infos, diseases, type, id):
    file_names = os.listdir(src_folder)
    file_names.sort()
    for fn in tqdm(file_names):
        full_fn = os.path.join(src_folder, fn)
        if (os.path.splitext(fn)[1] in ['.dcm'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            updateFolder(full_fn, study_infos, diseases, type, id)
            continue

        try:
            ds = pydicom.dcmread(full_fn, force=True)
            study_uid = ds.StudyInstanceUID
            try:
                study_infos["No"] = study_infos["No"] + 1
                if study_infos.__contains__(study_uid) is False:
                    try:
                        objdicom = dicom.objects.get(studyinstanceuid=study_uid, fileid=id)
                        if not os.path.exists(objdicom.route):
                            os.mkdir(objdicom.route)
                        else:
                            shutil.rmtree(objdicom.route)
                            time.sleep(2)
                            os.mkdir(objdicom.route)
                        study_infos[study_uid] = {
                            "patientid": objdicom.patientid,
                            "patientname": objdicom.patientname,
                            "folder_fake": objdicom.route
                        }
                        # logger.info('---更新：{}----'.format(study_infos[study_uid]))
                    except Exception as e:
                        obj = dicom.objects.all().aggregate(Max('id'))
                        filename = str(int(obj["id__max"]) + 1)
                        if ds.PatientName:
                            patientname = ds.PatientName
                        else:
                            patientname = norm_string("BM_{0}_{1}".format(diseases, filename))
                            ds.PatientName = patientname
                        if ds.PatientID:
                            patientid = ds.PatientID
                        else:
                            patientid = patientname
                            ds.PatientID = patientid
                        filename = "{0}{1}".format(str(patientname), str(int(obj["id__max"]) + 1))
                        folder_fake = '/files1/dicomTest/{0}/{1}/{2}'.format(type, diseases, filename)
                        study_infos[study_uid] = {
                            "patientid": patientid,
                            "patientname": patientname,
                            "folder_fake": folder_fake
                        }
                        if not os.path.exists(folder_fake):
                            os.makedirs(folder_fake)
                        data = {
                            "patientid": patientid,
                            "patientname": patientname,
                            "studyinstanceuid": study_uid,
                            "diseases": diseases,
                            "type": type,
                            "route": folder_fake,
                            "fileid": id,
                            "status": True
                        }
                        dicom.objects.create(**data)

                ds.PatientName = str(study_infos[study_uid]["patientname"])
                ds.PatientID = str(study_infos[study_uid]["patientid"])
                full_fn_fake = '{0}/{1}.dcm'.format(str(study_infos[study_uid]["folder_fake"]), str(study_infos["No"]))
                # logger.info("添加数据{}".format(data))
                ds.save_as(full_fn_fake)
            except Exception as e:
                logger.error('errormsg: failed to save_as [{0}]---[{1}]'.format(study_infos[study_uid], e))
                continue
        except Exception as e:
            logger.error('errormsg: failed to dcmread [{0}]'.format(e))
            continue


# 更新文件
def fileUpdate(id):
    obj = base_data.objects.get(id=id)
    study_infos = {}
    study_infos["No"] = 0
    src_folder = obj.content
    while src_folder[-1] == '/':
        src_folder = src_folder[0:-1]
    updateFolder(
        src_folder=src_folder,
        study_infos=study_infos,
        diseases=obj.remarks,
        type=obj.type,
        id=id
    )
    obj.other = int(len(study_infos)) - 1
    obj.save()
