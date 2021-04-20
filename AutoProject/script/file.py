import os
import operator
import paramiko
import logging
import time
import requests

log_file = '../info.log'
logging.basicConfig(filename=log_file, filemode='a+',
                    format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)


class SSHConnection:
    # 初始化连接创建Transport通道
    def __init__(self, host='192.168.1.121', port=22, user='biomind', pwd='Ashunyi@122'):
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

    # 在远程主机上创建目录
    def mkdir(self, target_path, mode='0777'):
        self.sftp.mkdir(target_path, mode)

    # 删除远程主机上的目录
    def rmdir(self, target_path):
        self.sftp.rmdir(target_path)

    # 删除文件
    def remove(self, target_path):
        self.sftp.remove(target_path)

    # SSHClient输入命令远程操作主机
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        result = stdout.read()
        return result


path = "/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/"


# 验证文件大小
def get_FileSize(filePath):
    while True:
        size = os.path.getsize(filePath)
        logging.info("文件大小：{}".format(size))
        if int(size) > 10000 * 1024 * 1024:
            time.sleep(40)
            logging.info("文件大小：{}".format(size))
            return True
            break
        time.sleep(10)


# 文件全路径和对应最后修改时间写入到 backup.txt 文档中；
def save_fileinfo():
    with open('backup.txt', 'w') as f:
        f.close()
    for root, dirs, files in os.walk(path):
        for name in files:
            temp_path = os.path.join(root, name)
            file_time = os.stat(temp_path).st_mtime
            with open('backup.txt', 'a') as f:
                f.write(','.join(['%s' % name, '%s\n' % file_time]))
                f.close()


# path 待比较的文件夹路径 返回生成的txt（包含更新或者添加的文件路径）的路径
def CheckVersion():
    myDic = {}
    try:
        # backup.txt文件内容（文件全路径key和最后修改时间value），生成dict
        txt = open('backup.txt', 'r').readlines()
        for row in txt:
            (key, value) = row.split(',')
            myDic[key] = value
    except Exception as e:
        logging.error("读取backup.txt失败 {}".format(e))
        save_fileinfo()
    try:
        # 运行程序时，重新遍历一遍文件全路径和最后修改时间
        for root, dirs, files in os.walk(path):
            for name in files:
                local_path = "/lfs/nextcloud/data/mengyue.he@biomind.ai/files/Version_for_QA/{}".format(name)
                remote_path = "/files/History_version/{0}/{1}".format(str(name)[:-4], name)

                temp_path = os.path.join(root, name)
                time = os.stat(temp_path).st_mtime  # 获取最后修改时间
                file_time = '%s\n' % time  # 加%s\n是为了与out.txt里值完全对应
                if myDic.__contains__(name) is True:
                    if operator.eq(myDic[name], file_time) is False:  # myDic[file_name]旧最后修改时间，file_time新最后修改时间
                        try:
                            logging.info("版本：{} 更新".format(name))
                            get_FileSize(local_path)
                            # 更新121 服务器上的备份文件
                            ssh = SSHConnection()
                            ssh.upload(local_path, remote_path)
                            ssh.close()
                            api(name)
                            save_fileinfo()
                        except Exception as e:
                            logging.error("备份新版本失败：{}".format(e))
                else:
                    try:
                        logging.info("新版本：{}".format(name))
                        get_FileSize(local_path)
                        ssh = SSHConnection()
                        ssh.cmd("mkdir /files/History_version/{};".format(str(name)[:-4]))
                        ssh.upload(local_path, remote_path)
                        ssh.close()
                        api(name)
                        with open("backup.txt", 'a') as f:  # 新增的文件，写入更新日志
                            f.write((','.join(['%s' % name, '%s\n' % file_time])))
                            f.close()
                        logging.info("备份新版本 ：{}".format(name))
                    except Exception as e:
                        logging.error("备份新版本失败：{}".format(e))

    except Exception as e:
        save_fileinfo()
        logging.error("比较文件内容失败：{}".format(e))


def api(version):
    #server_url = "http://localhost:8000/project/deploy?version={}".format(version)
    server_url = "http://192.168.1.121:9000/project/deploy?version={}".format(version)
    data = requests.get(server_url)


if __name__ == '__main__':
    CheckVersion()
    pass
    # size = get_FileSize("D:\\workspace\\test\\Biomind_Test_Platform\\AutoProject\\Atest.zip")
    # print(size)
