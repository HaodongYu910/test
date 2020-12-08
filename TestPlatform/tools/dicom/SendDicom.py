# coding=utf-8
'''
作用：
把文件夹中的所有study持续发到storescp中。
'''

import os
import logging
import subprocess as sp
from ...models import GlobalHost,dicom

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def sync_send_file(server_ip,file_name):
    obj = GlobalHost.objects.get(host=server_ip)
    local_aet='QA38'
    # logging.info('send file: [{0}]'.format(file_name))
    commands = [
        "storescu",
        server_ip,
        "4242",
        "-aec", "ORTHANC208",
        "-aet", local_aet,
        file_name
    ]
    try:
        logger.info(commands)
        popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
        popen.communicate()
    except Exception as e:
        logger.error('send_file error: {0}'.format(e))


def fake_folder(server_ip,folder):
    file_names = os.listdir(folder)
    file_names.sort()

    for fn in file_names:
        full_fn = os.path.join(folder, fn)

        if (os.path.splitext(fn)[1] in  ['.dcm'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            fake_folder(server_ip,full_fn)
            continue
        try:
            logger.info(server_ip,full_fn)
            sync_send_file(server_ip,full_fn)
        except Exception as e:
            logging.error('errormsg: failed to sync_send file [{0}][[1]]'.format(full_fn,e))
            continue



def Send(server_ip,route):
    try:
        src_folder = route
        while src_folder[-1] == '/':
            src_folder = src_folder[0:-1]
        fake_folder(server_ip,src_folder)
    except Exception as e:
        logging.error("error: failed to send", e)

