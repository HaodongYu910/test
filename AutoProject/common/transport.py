# coding:utf-8
import paramiko
import logging
import uuid
import time

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置

'''
SSH 链接 发送文件
执行 cmd 
host： 链接 IP
user：用户名
pwd：密码

'''


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
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        # while not stdout.channel.exit_status_ready():
        #     result = stdout.readline()
        #     print(result)
        #     # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
        #     if stdout.channel.exit_status_ready():
        #         a = stdout.readlines()
        #         print(a)
        #         break
        logger.debug(stdout)
        result = stdout.read()
        return result

    # SSHClient输入命令远程操作主机
    def shcmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command, timeout=10)
        stdin.write("yes\n")
        out, err = stdout.read(), stderr.read()
        logger.debug(stdout)
        result = stdout.read()

        return result

    def configure(self, host, PROTOCOL):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command('biomind configure', timeout=10)
        stdin.write("{}\n".format(host))
        stdin.write("\n")
        stdin.write("{}\n".format(PROTOCOL))
        stdin.write("eno1\n")
        out, err = stdout.read(), stderr.read()
        logger.debug(stdout)
        result = stdout.read()
        return result

    def command(self, cmd, result_print=None, nohup=False):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host, port=self.port, username=self.user,
                    password=self.pwd)
        if nohup:
            cmd += ' & \n '
            invoke = ssh.invoke_shell()
            invoke.send(cmd)
            # 等待命令执行完成
            time.sleep(2)
        else:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            if result_print:
                lines = result
                for line in lines:
                    print(line)

#
# if __name__ == '__main__':
#
#     ssh = SSHConnection()
#     a = ssh.command("nohup unzip -o QaInstall.zip > zz.log 2>&1 &")
#     print(bytes.decode(a))
#
#     ssh.close()


# # ssh.upload("{}/test.sh".format(path), '/home/biomind/test.sh')
# print(ssh.bashcmd("cd 2.18.1-radiology;sshpass -p biomind biomind restart;"))
# ssh.cmd("sshpass -p {} bash 2.17.5/setup_engine.sh".format('biomind'))
# ssh.cmd("sshpass -p {} biomind restart".format('biomind'))
# ssh.cmd("unzip {}".format('zipname'))
# ssh.cmd("sshpass -p {} bash /home/biomind/{}/".format('zipname'))
# ssh.cmd("sshpass -p {} biomind restart".format('biomind'))
