# coding=utf-8
import copy
import os
import logging
import queue

from AutoDicom.models import duration_record, dicom,  dicom_group_detail
from ..common.anonymous import anonymization
from ..common.dataSort import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def dicomSort(dicomlist, sendCount):
    dicomID = []
    # 查询 所以 dicom ID  优先组数据
    for i in dicom_group_detail.objects.filter(group__id__in=dicomlist, status=True):
        dicomID.append(i.dicom_id)
    # 查询发送数据
    obj = dicom.objects.filter(id__in=dicomID, status=True)

    if len(obj):
        dicomList = list(obj)
        # 变成{"病种"：（病人对象，病人对象），"病种"：（病人对象，病人对象，...}
        dictsum = {}
        for i in dicomList:
            grouping(dictsum, i)

        # 变成排好序的数据
        listsum = Myinster(dictsum)

        # 补充数据
        listsum = copylist(listsum, sendCount)
    return listsum


def QueData(relation_id, Host_id, Type, DicomList, full_fn_fake, patientID=None, patientName=None, anonymous=False):
    """
        relation_id ： 关联id
        Host_id ： 服务 id
        Type ： 类型l
        dicomList： 数据list
        full_fn_fake ： 匿名文件夹
        anonymous ： 是否匿名
    """
    if not os.path.exists(full_fn_fake):
        os.makedirs(full_fn_fake)
    q = queue.Queue()
    fileCount = 0
    # 优先查询组
    dcm = 0
    for i in DicomList:
        src_folder = str(i.route)
        while src_folder[-1] == '/':
            src_folder = src_folder[0:-1]
        if not os.path.exists(src_folder):
            logger.info(f"rclone copy oss://qa-test-data/{i.route} {i.route}")
            os.system(f"rclone copy oss://qa-test-data/{i.route} {i.route}")

        # 判断是否匿名 patientID
        if patientID is None:
            patientid = f"{i.patientid}-{dcm}"
        else:
            patientid = f"{patientID}_{i.patientid}_{dcm}"
        # 判断是否匿名 patientName
        if patientName is None:
            patientname = f"{i.diseases}-{dcm}"
        else:
            patientname = f"{patientName}_{i.patientid}_{dcm}"

        try:
            timeStamp = str(time.time())
            info = {
                "studyinstanceuid": f"{timeStamp}.{dcm}",
                "studyolduid": i.studyinstanceuid,
                "patientid": patientid,
                "patientname": patientname,
                "slicenumber": i.slicenumber,
                "image": i.imagecount,
                "diseases": i.diseases,
                "relation_id": relation_id,
                "type": Type,
                "Host_id": Host_id
            }
            try:
                fileID = duration_record.objects.create(**info).id
            except Exception as e:
                logger.error(f"duration create fail {e}")

            file_names = os.listdir(src_folder)
            file_names.sort()
            for fn in file_names:
                full_fn = os.path.join(src_folder, fn)
                full_fake = os.path.join(full_fn_fake, f'{fileCount}.dcm')
                fileCount = fileCount + 1
                if (os.path.splitext(fn)[1] in '.dcm' == False):
                    continue
                elif anonymous is True:
                    anonymization(
                        full_fn=full_fn,
                        full_fn_fake=full_fake,
                        info=info
                    )
                try:
                    data = [full_fn, full_fake, fileID, info]
                    q.put(data)
                    fileID = ""
                except Exception as e:
                    logging.error("[匿名错误]:{}".format(e))
                    continue
        except Exception as e:
            logger.error("遍历文件：{}".format(e))
            continue
        dcm = dcm + 1
    return q
