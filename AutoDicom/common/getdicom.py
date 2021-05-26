# coding=utf-8
import os
import random

import paramiko
import pydicom
from tqdm import tqdm
import time
import logging
from AutoDicom.models import *
from AutoProject.common.transport import SSHConnection
logger = logging.getLogger(__name__)


def getDicomServe(PID, destIP, destUSR, destPSW):
    '''
    获取一个patientID，在qa的db中找到这个patientid对应的源数据，并将这个源数据发送给目标服务器
    input：
        PID：待查询的患者id
        destIP：目标服务器ip
        destUSR：目标服务器用户名
        destPSW：目标服务器密码
    output：
        nothing
    '''
    # 获取PID对应路径
    logging.info("start extract dicom file PID:[{0}], route:[{1}], destination:[{2}]")
    tmp1 = duration_record.objects.get(patientname=PID)  # 从duration_record表中读取PID对应行
    UID = tmp1.studyolduid  # 得到PID对应的old studyUID
    tmp2 = dicom.objects.get(studyinstanceuid=UID)  # 利用得到的old studyUID 去dicom表中读取其所在行
    dicom_route = tmp2.route  # 得到该studyUID对应的存储路径
    route_list = dicom_route.rsplit("/", 1)  # 分割路径，得到路径和文件名
    fn_route = route_list[0]  # 路径
    fn = route_list[1]  # 文件名
    # 连接服务器scp数据
    try:
        os.system('cd {0} && zip -r /home/biomind/data.zip {1}'.format(fn_route, fn))  # 打包文件
        dest = SSHConnection(host=destIP, user=destUSR, pwd=destPSW)  # 链接目标服务器
        dest_route = '/home/biomind/data.zip'
        # local_path = 'C:\\Users\\yuhaodong\\Desktop\\train\\data.zip'
        local_path = '/home/biomind/data.zip'
        dest.upload(local_path, dest_route)  # 传输数据
        logging.info("success extract dicom file PID:[{0}], route:[{1}], destination:[{2}]".format(PID, dicom_route, destIP))
        # os.system('cd ~ && rm -rf data.zip')  # 删除文件
    except Exception as e:
        logging.error("scp数据至服务器失败:[{0}]".format(e))

    # s = paramiko.SSHClient()
    # s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 取消安全认证
    # s.connect(hostname='192.168.1.120', username='biomind', password='biomind')  # 连接linux
    # order = 'scp {0} {1}@{2}:/home/biomind'.format(fulder_path,destIP,destUSR)  # 执行命令
    # stdin, stdout, stderr = s.exec_command(order)
    # stdin.write('{0}'.format(destPSW) + '\n')
    # s.close()  # 关闭linux连接

    return

def get_to_local(PID):
    # 获取PID对应路径
    try:
        logging.info("start extract dicom file PID:[{0}] to local Download".format(PID))
        tmp1 = duration_record.objects.filter(patientname=PID)  # 从duration_record表中读取PID对应行
        tmp_UID = ""
        for i in tmp1:
            tmp_UID = i.studyolduid  # 得到PID对应的old studyUID
        logging.info(" we get UID {0}".format(tmp_UID))
        if tmp_UID == "":
            tmp_url = "we dont have this data"
            logging.info("we dont have this data")
            return tmp_url

        tmp2 = dicom.objects.filter(studyinstanceuid=tmp_UID)  # 利用得到的old studyUID 去dicom表中读取其所在行
        dicom_route = ""
        for i in tmp2:
            dicom_route = i.route  # 得到该studyUID对应的存储路径
        logging.info("we get route {0}".format(dicom_route))
        route_list = dicom_route.rsplit("/", 1)  # 分割路径，得到路径和文件名
        fn_route = route_list[0]  # 路径
        fn = route_list[1]  # 文件名
        os.system('cd {0} && zip -r /home/biomind/data.zip {1} && mv /home/biomind/data.zip /home/biomind/Biomind_Test_Platform/static/data.zip'.format(fn_route, fn))  # 打包文件
        logging.info("execute shell command success")
        tmp_url = "/static/data.zip"
    except Exception as e:
        logging.error("error happend {0}".format(e))
    return tmp_url

