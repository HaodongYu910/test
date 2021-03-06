# coding=utf-8

import os
import pydicom
from tqdm import tqdm
import logging

from AutoProject.models import uploadfile
from ..models import dicom_group, dicom, dicom_relation, dicom_group_detail
from django.db.models import Max

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置。


#
def norm_string(str):
    str_dest = str
    while len(str_dest) > 16 or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest


# 更新文件到 测试目录 安装类型分类重新命名
def updateFolder(custom, src_folder, study_infos, diseases, foldType, id, predictor, history_uid):
    file_names = os.listdir(src_folder)
    file_names.sort()
    dicom_relation_data = {}
    folder_fake = ""  # 最终路径
    temporary_uid = history_uid
    for fn in tqdm(file_names):
        full_fn = os.path.join(src_folder, fn)

        if (os.path.isdir(full_fn)):  # 如果它是个文件夹
            updateFolder(custom, full_fn, study_infos, diseases, foldType, id, predictor, temporary_uid)
            continue
        elif (os.path.splitext(fn)[1] !='.dcm'):
            # 规范化数据时候，不论成功失败都要记录哪个成功，哪个失败
            houzhui = os.path.splitext(fn)[1]
            logger.info(F"发现错误文件后缀。。{houzhui}")
            dicom_relation_data["baseid"] = id
            dicom_relation_data["old_path"] = full_fn
            dicom_relation_data["custom"] = custom
            dicom_relation_data["type"] = foldType
            dicom_relation_data["predictor"] = predictor
            dicom_relation_data["fail_uid"] = "【检查数据】："+str(full_fn)
            relation = dicom_relation.objects.create(**dicom_relation_data)
            logger.info(f"【检查数据】：数据类型可能不正确，请检查{fn}")
            # break

        try:
            ds = pydicom.dcmread(full_fn, force=True)
            study_uid = ds.StudyInstanceUID
            try:
                study_infos["No"] = study_infos["No"] + 1
                if study_infos.__contains__(study_uid) is False:
                    try:
                        # 规范化数据时候，不论成功失败都要记录哪个成功，哪个失败
                        dicom_relation_data["baseid"] = id
                        dicom_relation_data["old_path"] = full_fn
                        dicom_relation_data["custom"] = custom
                        dicom_relation_data["type"] = foldType
                        dicom_relation_data["predictor"] = predictor
                        dicom_relation_data["fail_uid"] = study_uid

                        objdicom = dicom.objects.get(studyinstanceuid=study_uid)
                        # 数据库中已经存在这个检查号
                        if study_uid in temporary_uid:
                            pass
                        else:
                            relation = dicom_relation.objects.create(**dicom_relation_data)
                            temporary_uid.append(study_uid)
                    except:
                        # 数据库中没找到这个检查号
                        obj = dicom.objects.all().aggregate(Max('id'))
                        filename = str(int(obj["id__max"]) + 1)

                        ds.PatientName = norm_string("{0}_{1}".format(diseases, filename))
                        ds.PatientID = norm_string("{0}_{1}".format(custom, filename))
                        filename = "{0}{1}".format(str(ds.PatientName), str(int(obj["id__max"]) + 1))
                        folder_fake = '/files1/dicomTest/{0}/{1}/{2}'.format(foldType, diseases, study_uid)
                        # folder_fake = "C:\D\MRP1" + '/dicomTest/{0}/{1}/{2}'.format(foldType, diseases, study_uid)
                        study_infos[study_uid] = {
                            "patientid": ds.PatientID,
                            "patientname": ds.PatientName,
                            "folder_fake": folder_fake
                        }
                        if not os.path.exists(folder_fake):
                            os.makedirs(folder_fake)
                        data = {
                            "patientid": ds.PatientID,
                            "patientname": ds.PatientName,
                            "studyinstanceuid": study_uid,
                            "diseases": diseases,
                            "type": foldType,
                            "route": folder_fake,
                            "fileid": id,
                            "predictor": predictor,
                            "status": True
                        }
                        # 存入dicom 数据表
                        logger.info("【上传数据】更新dicom表：{}".format(data))
                        objDicom = dicom.objects.create(**data)
                        # 组内添加关联关系
                        dicom_group_detail.objects.create(**{
                            "group_id": int(id),
                            "dicom_id": int(objDicom.id)
                        })
                        logger.info("【上传数据】更新dicom_group_detail表 dicom_id:{}".format(objDicom.id))
                        # 保存上传记录和对应关系和结果
                        dicom_relation_data["fail_uid"] = ""
                        dicom_relation_data["new_path"] = folder_fake
                        dicom_relation_data["success_uid"] = study_uid
                        relation = dicom_relation.objects.create(**dicom_relation_data)

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
    try:
        logger.info(f"【上传数据】：开始遍历数据")
        obj = dicom_group.objects.get(id=id)
        uploadfileResult = uploadfile.objects.filter(fileid=id)
        if uploadfileResult.exists() is False:
            pass
        files = list(uploadfileResult)
        loadfile = files[-1]

        study_infos = {}
        study_infos["No"] = 0

        src_folder = obj.route
        while src_folder[-1] == '/':
            src_folder = src_folder[0:-1]
        updateFolder(
            custom=loadfile.remark,
            src_folder=loadfile.fileurl,
            # src_folder=src_folder,
            study_infos=study_infos,
            diseases=obj.name,
            foldType=obj.type,
            id=id,
            predictor=obj.predictor,
            history_uid=[]
        )
        # 更新数量
        obj.amount = dicom_group_detail.objects.filter(group_id=id).count()
        obj.save()
    except Exception as e:
        logger.error("文件上传更新错误：{}".format(e))
