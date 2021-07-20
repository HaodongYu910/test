# coding=utf-8

import os
import logging
import subprocess as sp
import socket

import threading
import time
import queue

from AutoStress.models import stress, Server


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


# 发送文件
class SendQueThread:
    def __init__(self, **kwargs):
        self.thread_num = 4
        self.route = kwargs["route"]
        self.hostobj = Server.objects.get(id=kwargs["hostid"])
        self.routelist = []

        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'

    def DicomSend(self):
        try:
            src_folder = self.route
            while src_folder[-1] == '/':
                src_folder = src_folder[0:-1]
            if not os.path.exists(src_folder):
                os.system(f"rclone copy oss://qa-test-data/{src_folder} {src_folder}")
            self.fake_folder(src_folder)
        except Exception as e:
            logging.error("error: failed to send", e)
        # 添加队列
        q = queue.Queue()
        for i in self.routelist:
            commands = [
                "storescu",
                self.hostobj.host,
                self.hostobj.port,
                "-aec", self.hostobj.remarks,
                "-aet", self.local_aet,
                i
            ]
            q.put(commands)  # 往队列里生成消息

        threads = []
        for i in range(self.thread_num):
            t = threading.Thread(target=self.Send, args=(q,))
            # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
            threads.append(t)
        for i in range(self.thread_num):
            threads[i].start()
        for i in range(self.thread_num):
            threads[i].join()

    # 下面来通过多线程来处理Queue里面的任务：
    def Send(self, q):
        while True:
            if q.empty():
                return
            else:
                try:
                    commands = q.get()
                    starttime = time.time()
                    popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
                    popen.communicate()
                    endtime = time.time()
                    # diff = str('%.2f' % (float(endtime - starttime)))
                    # start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starttime))
                    # end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endtime))
                except Exception as e:
                    logging.error('send_file error: {0}'.format(e))

    def fake_folder(self, folder):
        file_names = os.listdir(folder)
        file_names.sort()

        for fn in file_names:
            full_fn = os.path.join(folder, fn)
            if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                continue
            elif (os.path.isdir(full_fn)):
                self.fake_folder(full_fn)
                continue
            try:
                self.routelist.append(full_fn)
            except Exception as e:
                logging.error('errormsg: file [{0}][[1]]'.format(full_fn, e))
                continue

# if __name__ == "__main__":
#     start = time.time()
#     # main()
#     # print('耗时：', time.time() - start)
