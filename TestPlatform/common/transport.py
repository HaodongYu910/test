# coding:utf-8
import paramiko
import logging
import uuid

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class SSHConnection:
    # 初始化连接创建Transport通道
    def __init__(self, host='192.168.1.172', port=22, user='biomind', pwd='biomind'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.__transport = paramiko.Transport((self.host, self.port))
        self.__transport.connect(username=self.user, password=self.pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.__transport)

    # 关闭通道
    def close(self):
        self.sftp.close()
        self.__transport.close()

    # 上传文件到远程主机
    def upload(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    # 从远程主机下载文件到本地
    def download(self, local_path, remote_path):
        self.sftp.get(remote_path, local_path)

    # 在远程主机上创建目录
    def mkdir(self, target_path, mode='0777'):
        self.sftp.mkdir(target_path, mode)

    # 删除远程主机上的目录
    def rmdir(self, target_path):
        self.sftp.rmdir(target_path)

    # 查看目录下文件以及子目录（如果需要更加细粒度的文件信息建议使用listdir_attr）
    def listdir(self, target_path):
        return self.sftp.listdir(target_path)

    # 删除文件
    def remove(self, target_path):
        self.sftp.remove(target_path)

    # 查看目录下文件以及子目录的详细信息（包含内容和参考os.stat返回一个FSTPAttributes对象，对象的具体属性请用__dict__查看）
    def listdirattr(self, target_path):
        try:
            list = self.sftp.listdir_attr(target_path)
        except BaseException as e:
            print(e)
        return list

    # 获取文件详情
    def stat(self, remote_path):
        return self.sftp.stat(remote_path)

    # SSHClient输入命令远程操作主机
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        print(str(result,encoding='utf-8'))
        return result

# import os
# name = '2.18.1-radiology'
# ssh = SSHConnection(host='192.168.1.208',pwd='biomind')
# # ssh.cmd("unzip {}.zip".format(name))
# BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))
# path = os.path.join(BASE_DIR, 'logs')
# with open("{}/test.sh".format(path), "w",encoding='utf-8') as f:
#     f.writelines(['cd {}'.format(name),"\nsshpass -p {} bash setup_engine.sh".format('biomind')])
#
# ssh.upload("{}/test.sh".format(path), '/home/biomind/test.sh')
# ssh.cmd("sh test.sh")
# ssh.cmd("ls")
# ssh.cmd("sshpass -p {} bash 2.17.5/setup_engine.sh".format('biomind'))
# ssh.cmd("sshpass -p {} biomind restart".format('biomind'))
# ssh.cmd("unzip {}".format('zipname'))
# ssh.cmd("sshpass -p {} bash /home/biomind/{}/".format('zipname'))
# ssh.cmd("sshpass -p {} biomind restart".format('biomind'))
# ssh.cmd("echo biomind|sudo -S -u biomind restart")
# ssh.cmd("zip -r /home/biomind/pm.zip /home/biomind/.biomind/lib/versions/2.18.0-radiology/logs/pm2")
# # ssh.upload('C:\\Users\\yinhang\\Desktop\\logs\\win.txt', '/home/biomind/win.txt')
# ssh.download('C:\\Users\\yinhang\\Desktop\\logs\\pm.zip', '/lfs/nextcloud/data/hang.yin@biomind.ai/files/src.zip')
# ssh.close()
