from AutoProject.models import Server
from AutoProject.common.transport import SSHConnection
import os
import logging

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


def monitor(operation="restart", host_id=1):
    host = Server.objects.get(id=host_id)
    if operation == "add":
        ssh = SSHConnection(host="", port=22, user=host.user, pwd=host.pwd)
        ssh.download()
        ssh.upload()
        ssh.cmd("docker restart biomind_prometheus")
        ssh.close()
    try:
        ssh = SSHConnection(host=host.host, port=22, user=host.user, pwd=host.pwd)
        path = os.path.abspath(os.path.join(os.getcwd(), ".."))
        logger.info(f"path:{path}")
        ssh.upload(f"{path}/Biomind_Test_Platform/AutoProject/script/monitor_setup.sh", "/home/biomind/")
        ssh.cmd(f"sshpass -p {host.pwd} bash monitor_setup.sh")
        ssh.close()
    except Exception as e:
        logger.error(e)
