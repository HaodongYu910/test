# coding=utf-8
'''
作用：
把文件夹中的所有study，匿名成不同的uid，持续发到storescp中。
参数说明：
1，CONFIG.local：本storescu的信息，包括ae title
2，CONFIG.server：storescp的信息，包括ae title、ip、port
3，CONFIG.keyword：发送文件匿名tags（patientID, patientName）的前缀关键词
4，CONFIG.folderid：需要发送dicom文件的所在目录id
'''

import getopt
import sys
import pymysql
import copy
import os
import pydicom
import logging
import subprocess as sp
import datetime
import random
import math
import socket
import requests
import time
import queue
import threading

# 链接mysql数据库
def sqlDB(sql, data, type):
    conn = pymysql.connect(host='192.168.1.121', user='root', passwd='P@ssw0rd2o8', db='auto_test',
                           charset="utf8");  # 连接数据库
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if type == 'select':
        try:
            # 查询数据
            cr = cur.execute(sql)  # 查询
            data = cur.fetchmany(cr)
            conn.commit()
        except Exception as e:
            conn.rollback()
    else:
        try:
            logging.info("sql:{0},data:{1}".format(sql, data))
            cur.execute(sql, data)
            conn.commit()
        except Exception as e:
            conn.rollback()
    cur.close()
    conn.close()
    return data


def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y%m%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H%M%S", localtime))


def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 16) - 1)
    return str(time.time())


def Myinster(dicomList):
    diseasesDict = {}
    for i in dicomList:
        try:
            if diseasesDict.__contains__(i["diseases"]) is True:
                dicomlist = dicomlist[i["diseases"]]
                diseasesDict[i["diseases"]] = dicomlist.append(i)
            else:
                diseasesDict[i["diseases"]] = [i]
        except:
            continue


    diseasesDict = dict(sorted(diseasesDict.items(), key=lambda i: -len(i[1])))
    listsum = []
    l = 0
    start = 0
    step = 2
    for key, value in diseasesDict.items():
        if start == 0:
            listsum = list(value)
            start = start + 1
            continue
        for i in value:
            # print((start + step * l))
            listsum.insert((start + step * l), i)
            l = l + 1
        # print(listsum)
        start = start + 1
        step = step + 1
        l = 0
    return listsum


def copylist(listsum, count):
    while len(listsum) < count:
        listA = copy.deepcopy(listsum)
        listsum = listA + listsum
    return listsum[:count]


def grouping(dictsum, dicom):
    if dictsum.get(dicom.diseases) is None:
        sum = set()
        sum.add(dicom)
    else:
        sum = dictsum.get(dicom.diseases)
        sum.add(dicom)
    dictsum[dicom.diseases] = sum


class DurationThread:
    def __init__(self, **kwargs):
        self.id = kwargs["durationId"]
        try:
            result = sqlDB(f"select * from duration where id ={self.id}", "", "select")[0]
        except Exception as e:
            logging.error(f"error: failed to get select * from duration :{e}")

        self.aec = result["aet"]
        self.server = result["server"]
        self.port = result["port"]
        self.groupIds = result["dicom"]
        self.end = result["sendcount"]
        self.count = 0  # 可用来被外部访问
        self.thread_num = 4
        self.CountData = []

        # 获取计算机名称
        if socket.gethostname() == "biomindqa38":
            self.local_aet = 'QA38'
        else:
            self.local_aet = 'QA120'
        self.full_fn_fake = f'/home/biomind/Biomind_Test_Platform/logs/Duration{self.id}'
        if not os.path.exists(self.full_fn_fake):
            os.makedirs(self.full_fn_fake)
        logging.basicConfig(filename=f"/home/biomind/Biomind_Test_Platform/logs/Duration{self.id}/send.log",
                            filemode='a+',
                            format="%(asctime)s [%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    def anonymization(self, test_data):
        full_fn = test_data[0]
        full_fn_fake = test_data[1]
        info = test_data[2]
        saveID = test_data[3]
        try:
            ds = pydicom.dcmread(full_fn, force=True)
        except Exception as e:
            logging.error('errormsg: failed to read file [{0}]:{1}'.format(full_fn, e))
        try:
            studyolduid = ds.StudyInstanceUID
            acc_number = ds.AccessionNumber
            Seriesinstanceuid = ds.SeriesInstanceUID
            rand_uid = str(info.get("rand_uid"))
            fake_acc_number = self.norm_string("{0}_{1}".format(acc_number, rand_uid), 16)
            cur_date = get_date()
            cur_time = get_time()
        except Exception as e:
            logging.error(
                'failed to fake: file[{0}], error[{1}]'.format(full_fn, e))

        try:
            ds.SeriesInstanceUID = self.norm_string(
                '{0}.{1}'.format(ds.SeriesInstanceUID, rand_uid), 64)

            ds.SOPInstanceUID = self.norm_string(
                '{0}.{1}'.format(ds.SOPInstanceUID, rand_uid), 64)
            ds.StudyInstanceUID = info.get("study_uid")
            ds.PatientID = f"{ds.PatientID}{self.id}"
            ds.PatientName = f"{ds.PatientName}{self.id}"
            ds.AccessionNumber = fake_acc_number
            ds.StudyDate = cur_date
            ds.StudyTime = cur_time
            ds.SeriesDate = cur_date
            ds.SeriesTime = cur_time
        except Exception as e:
            logging.error(
                'failed to anonymous :  error[{}]'.format(e))

        try:
            ds.save_as(full_fn_fake)
        except Exception as e:
            logging.error('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))
        try:
            if int(saveID) == 0:
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                sqlDB(f"INSERT INTO duration_record('id', 'patientid', 'patientname', 'accessionnumber', 'studyinstanceuid', 'studyolduid', 'imagecount', 'imagecount_server', 'aistatus', 'diagnosis', 'sendserver', 'sendtime', 'starttime', 'endtime', 'jobtime', 'error', 'model', 'time', 'duration_id', 'diseases', 'update_time', 'create_time') VALUES (NULL, {ds.PatientID}, {ds.PatientName}, {ds.AccessionNumber}, {ds.StudyInstanceUID}, {studyolduid}, NULL, NULL, NULL, NULL, {self.server}, NULL, NULL, NULL, NULL, NULL, NULL, NULL, {self.id}, {info.get('diseases')}, {create_time}, {create_time});", "", "")
        except Exception as e:
            logging.error('[获取数据失败]： [{0}]'.format(e))
        return Seriesinstanceuid

    def QueData(self):
        q = queue.Queue()
        filecount = 1
        # 查询 所以 dicom ID  优先组数据
        dicomList = sqlDB(
            f"select * from dicom d join dicom_group_detail dgd on d.id = dgd.dicom_id  where dgd.group_id in ({self.groupIds}) and d.status=True",
            "", "select")
        # 变成排好序的数据
        listsum = Myinster(dicomList)
        # 补充数据
        listsum = copylist(listsum, int(self.end))
        logging.info("listsum:{}".format(listsum))
        # 优先查询组
        for j in listsum:
            dcmcount = 0
            src_folder = str(j["route"])
            while src_folder[-1] == '/':
                src_folder = src_folder[0:-1]
            try:
                rand_uid = get_rand_uid()
                info = {
                    "diseases": j["diseases"],
                    "rand_uid": rand_uid,
                    "study_uid": self.norm_string('{0}.{1}'.format(j["studyinstanceuid"], rand_uid), 64),
                }
                file_names = os.listdir(src_folder)
                file_names.sort()
                for fn in file_names:
                    full_fn = os.path.join(src_folder, fn)
                    full_fn_fake = os.path.join(self.full_fn_fake, '{0}{1}'.format(filecount, fn))
                    if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                        continue
                    try:
                        q.put([full_fn, full_fn_fake, info, dcmcount])
                        dcmcount = dcmcount + 1

                    except Exception as e:
                        logging.error("[匿名错误]:{}".format(e))
                        continue
            except Exception as e:
                logging.error("遍历文件：{}".format(e))
        return q

    # 匿名数据队列
    def run(self):
        q = self.QueData()
        if q is None:
            logging.info("没有有效数据发送")
            return False
        threads = []
        try:
            logging.info("duration threading start")
            for i in range(self.thread_num):
                t = threading.Thread(target=self.durationAnony, args=(q,))
                # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
                time.sleep(1)
        except Exception as e:
            logging.error("队列生成失败：{0}".format(e))

    def durationAnony(self, q):
        while not q.empty():
            if not os.path.exists(self.full_fn_fake):
                break
            self.count = self.count + 1
            test_data = q.get()
            # logging.info(testdata)
            full_fn_fake = test_data[1]
            try:
                Seriesinstanceuid=self.anonymization(test_data)
            except Exception as e:
                logging.error("匿名失败:{}".format(e))

            try:
                self.sync_send_file(full_fn_fake, test_data[2]["study_uid"], Seriesinstanceuid)
            except Exception as e:
                logging.error('errormsg: failed to sync_send [{0}]---报错：{1}'.format(q.get()[1], e))
                continue
            try:
                self.delayed()
            except Exception as e:
                logging.error("delayed fail:{}".format(e))

    # 存储 每张发送信息
    def connect_influx(self, data):
        try:
            tamp = int(round(time.time() * 1000000000))
            influxdata = f'test,id={self.id},studyuid={data["studyuid"]},Seriesinstanceuid={data["Seriesinstanceuid"]} value={data["time"]} {tamp}'
            logging.info(f"influx data:{influxdata}")
            requests.post('http://192.168.1.121:8086/write?db=auto_test', data=influxdata)
        except Exception as e:
            logging.error("保存connect_influx数据错误{}".format(e))

    def get_fake_name(self, rand_uid, fake_prefix):
        ts = time.localtime(time.time())
        return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), self.norm_string(rand_uid, 6))

    def sync_send_file(self, file_name, studyuid, Seriesinstanceuid):
        # 发送数据
        try:
            commands = [
                "storescu",
                "-xs",  # 压缩方式
                self.server,
                self.port,
                "-aec", self.aec,
                "-aet", self.local_aet,
                file_name
            ]
            starttime = time.time()
            popen = sp.Popen(commands, stderr=sp.PIPE, stdout=sp.PIPE, shell=False)
            popen.communicate()
            endtime = time.time()
            self.connect_influx({'studyuid': studyuid,
                                 'time': str('%.2f' % (float(endtime - starttime))),
                                 'starttime': starttime,
                                 'endtime': endtime,
                                 'Seriesinstanceuid': Seriesinstanceuid
                                 })
            os.remove(file_name)
        except Exception as e:
            logging.error('send_file error: {0}'.format(e))

    def norm_string(self, str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest

    # 随机等待
    def delayed(self):
        if int(random.randint(1, 100)) > 80:
            hour = int(datetime.datetime.now().strftime("%H"))
            if 18 > hour > 13:
                sleepTime = random.randint(1, 300)
            elif 22 > hour > 18:
                sleepTime = random.randint(1, 10)
            elif hour > 22:
                return True
            else:
                sleepTime = random.randint(100, 600)
            time.sleep(int(sleepTime))

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h",
                                   ["durationid="])

        for opt, arg in opts:
            if opt == '-h':
                sys.exit()
            elif opt in ("--durationid"):
                durationId = arg

        DT = DurationThread(durationId=durationId)
        DT.run()
    except Exception as e:
        logging.error("failed to start:{}".format(e))
