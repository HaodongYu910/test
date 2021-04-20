from .transport import SSHConnection
from ..models import dictionary
import os

import logging

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def backup(**kwargs):
    downssh = SSHConnection(host='192.168.2.111', pwd='P@ssw0rd2111')
    version = kwargs["version"]
    dObj = dictionary.objects.get(type='install', key='oldversion')
    oldversion = dObj.value.split(',')
    try:
        if version:
            downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{0}.zip'.format(version)
            path = '/files/History_version/{0}'.format(version)
            if not os.path.exists(path):
                os.makedirs(path)
            logger.info("下载备份最新安装包{0}.zip".format(version))
            localpath = '/files/History_version/{0}/{1}'.format(version, version)
            downssh.download(localpath, downpath)
            downssh.close()
            return True
        else:
            filelist = downssh.cmd("ls /lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/")
            for i in str(filelist, encoding="utf-8").split('\n'):
                if i not in oldversion and i:
                    version = i
            downpath = '/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{}'.format(version)
            path = '/files/History_version/{}/'.format(version[:-4])
            if not os.path.exists(path):
                os.makedirs(path)
            localpath = '/files/History_version/{0}/{1}'.format(version[:-4], version)
            logger.info("下载备份最新安装包{0}.zip".format(version[:-4]))
            downssh.download(localpath, downpath)
            downssh.close()
            return True
    except Exception as e:
        logger.error("下载最新版本报错{}".format(e))
        return False
