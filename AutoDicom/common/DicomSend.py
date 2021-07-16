# coding=utf-8
import os
import logging
import subprocess as sp
import shutil
import socket
import requests
import queue
import threading
from AutoDicom.models import duration_record
from AutoProject.models import Server
from ..common.dataSort import *
from ..common.anonymous import anonymization

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class SendThread(threading.Thread):
    def __init__(self, q, hostID, full_fn_fake, sleepCount=0, sleepTime=0, series=None, anonymous=False):
        threading.Thread.__init__(self)
        self.obj = Server.objects.get(id=hostID)
        self.q = q
        self.thread_num = 4
        self.count = 0
        self.SeriesInstanceUID = ''
        self.sleepCount = sleepCount
        self.sleepTime = sleepTime
        self.series = series
        self.anonymous = anonymous
        self.full_fn_fake = full_fn_fake
        self.studyID = ''

        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'

    # 匿名数据队列
    def run(self):
        threads = []
        try:
            for i in range(self.thread_num):
                t = threading.Thread(target=self.sync_send_file)
                # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                time.sleep(1)
            self.UpdateStatus([self.studyID, '1'])
            # for i in range(self.thread_num):
            #     threads[i].start()
            # for i in range(self.thread_num):
            #     threads[i].join()
        except Exception as e:
            logger.error("失败：{0}".format(e))

    def sync_send_file(self):
        try:
            while not self.q.empty():
                if not os.path.exists(self.full_fn_fake):
                    logger.info(f"file_name：{self.full_fn_fake} 文件不存在 跳过")
                    break
                file_data = self.q.get()
                file_name = file_data[1]
                info = file_data[3]
                # 判断是否 去匿名
                if self.anonymous is True:
                    anonymization(
                        full_fn=file_data[0],
                        full_fn_fake=file_name,
                        info=info,
                    )
                try:
                    commands = [
                        "storescu",
                        "-xs",  # 压缩方式
                        self.obj.host,
                        self.obj.port,
                        "-aec", self.obj.remarks,
                        "-aet", self.local_aet,
                        file_name
                    ]
                    info["starttime"] = time.time()
                    popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
                    assert (popen.communicate())
                    # 变更 发送状态
                    if file_data[2]:
                        try:
                            self.UpdateStatus([self.studyID, '1'])
                            self.UpdateStatus([file_data[2], '0'])
                            #map(self.UpdateStatus, [[self.studyID, '1'], [file_data[2], '0']])
                            self.studyID = file_data[2]
                        except Exception as e:
                            logger.error(f"duration_record 更新状态失败{e}")

                except Exception as e:
                    logging.error('error msg: failed to sync_send [{0}]---报错：{1}'.format(file_name, e))
                    continue
                try:
                    info["endtime"] = time.time()
                    info["time"] = str('%.2f' % (float(info["endtime"] - info["starttime"])))
                    self.connect_influx(info)
                except Exception as e:
                    logging.error('error msg: failed to connect_influx  [{0}]---报错：{1}'.format(file_name, e))
                    continue
                try:
                    os.remove(file_name)
                except Exception as e:
                    logging.error('error msg: remove failed to [{0}]---报错：{1}'.format(file_name, e))
                    continue
        except Exception as e:
            logging.error('error msg: while failed to [{0}]}'.format(e))

    # 更新 状态
    def UpdateStatus(self, data):
        if data[0]:
            obj = duration_record.objects.get(id=data[0])
            obj.status = data[1]
            obj.save()

    # 存储 每张发送信息
    def connect_influx(self, info):
        try:
            tamp = int(round(time.time() * 1000000000))
            influxdata = f'duration,id={info["relation_id"]},studyuid={info["studyinstanceuid"]},type={info["type"]} value={info["time"]} {tamp}'
            logger.info(f"influx data:{influxdata}")

            requests.post('http://192.168.1.120:8086/write?db=auto_test', data=influxdata)
            self.delayed("")
        except Exception as e:
            logger.error("保存connect_influx数据错误{}".format(e))

    # 判断是否 同一个 Series
    def delayed(self, SeriesID):
        try: 
            if self.series is True:
                if SeriesID != self.SeriesInstanceUID:
                    time.sleep(int(self.sleepTime))
                    self.SeriesInstanceUID = SeriesID
            elif self.sleepTime != 0 and self.sleepCount != 0:
                imod = divmod(int(self.count), int(self.sleepCount))
                if imod[1] == 0:
                    time.sleep(int(self.sleepTime))
            self.count = self.count + 1
        except Exception as e:
            logger.error("delayed:{}".format(e))

    # 停止
    def SendStop(self):
        # 删除 文件夹
        shutil.rmtree(self.full_fn_fake)
