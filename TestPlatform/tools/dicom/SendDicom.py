# coding=utf-8
'''
作用：
把文件夹中的所有study持续发到storescp中。
'''

import os,gc
import sys, getopt
import pydicom
import logging
from tqdm import tqdm
import subprocess as sp
import threading
from ...models import GlobalHost,dicom_route,base_data

def sync_send_file(server_ip,port,aec,file_name):
    local_aet='QA38'
    # logging.info('send file: [{0}]'.format(file_name))
    commands = [
        "storescu",
        server_ip,
        port,
        "-aec", aec,
        "-aet", local_aet,
        file_name
    ]

    try:
        popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
        popen.communicate()
    except Exception as e:
        logging.error('send_file error: {0}'.format(e))


def fake_folder(server_ip,port,ate,folder):
    folder_fake = folder
    file_names = os.listdir(folder)
    file_names.sort()

    for fn in file_names:
        full_fn = os.path.join(folder, fn)
        full_fn_fake = os.path.join(folder_fake, fn)

        if (os.path.splitext(fn)[1] in  ['.dcm'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(full_fn)
            continue
        try:
            sync_send_file(server_ip,port,ate,full_fn_fake)
        except Exception as e:
            logging.error('errormsg: failed to sync_send file [{0}][[1]]'.format(full_fn,e))
            continue


def Send(server_ip,id,folder_id):
    try:
        obj = GlobalHost.objects.get(host=server_ip)
        if id:
            routeobj =dicom_route.objects.filter(dicomid=id)
            for i in routeobj:
                sync_send_file(server_ip,obj.port,obj.description,i['route'])
        else:
            for j in folder_id:
                folderobj = base_data.objects.get(id=j)
                # 创建线程
                thread_fake_folder = threading.Thread(target=fake_folder, args=(server_ip,obj.port,obj.description,folderobj.content))
                # 启动线程
                thread_fake_folder.start()
    except Exception as e:
        logging.error("error: failed to send", e)

