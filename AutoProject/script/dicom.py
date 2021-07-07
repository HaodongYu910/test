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

import copy
import os
import pydicom
import datetime
import random
import math

import time


def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y%m%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H%M%S", localtime))


def get_rand_uid():
    rand_val = random.randint(1, math.pow(10, 16) - 1)
    return str(time.time())


class DurationThread:
    def __init__(self, route):
        self.route = route
        self.full_fn_fake = f'D:\\download\\lung\\test'
        self.Seriesinstanceuid =''

    def run(self):
        src_folder = self.route
        while src_folder[-1] == '/':
            src_folder = src_folder[0:-1]
        try:
            rand_uid = get_rand_uid()
            file_names = os.listdir(src_folder)
            file_names.sort()
            cur_date = get_date()
            cur_time = get_time()

            for fn in file_names:
                full_fn = os.path.join(src_folder, fn)
                if (os.path.splitext(fn)[1] in ['.dcm'] == False):
                    continue
                try:
                    try:
                        ds = pydicom.dcmread(full_fn, force=True)
                    except Exception as e:
                        print('errormsg: failed to read file [{0}]:{1}'.format(full_fn, e))
                    try:
                        try:
                            SliceThickness = '%.2f' % float(ds.SliceThickness)
                            ds.PatientName = f"{ds.PatientName}{SliceThickness}"
                        except:
                            SliceThickness = '1.2.3'
                            print(1)
                        acc_number = ds.AccessionNumber
                        Seriesinstanceuid = ds.SeriesInstanceUID
                        fake_acc_number = self.norm_string("{0}_{1}".format(acc_number, rand_uid), 16)
                    except Exception as e:
                        print(
                            'failed to fake: file[{0}], error[{1}]'.format(full_fn, e))

                    try:
                        ds.SeriesInstanceUID = self.norm_string(
                            '{0}.{1}'.format(ds.SeriesInstanceUID, rand_uid), 64)

                        ds.SOPInstanceUID = self.norm_string(
                            '{0}.{1}'.format(ds.SOPInstanceUID, rand_uid), 64)
                        ds.StudyInstanceUID = f"{ds.StudyInstanceUID}{SliceThickness}"
                        ds.PatientID = f"{ds.PatientID}{SliceThickness}"

                        ds.AccessionNumber = fake_acc_number
                        ds.StudyDate = cur_date
                        ds.StudyTime = cur_time
                        ds.SeriesDate = cur_date
                        ds.SeriesTime = cur_time
                    except Exception as e:
                        print(
                            'failed to anonymous :  error[{}]'.format(e))
                    try:
                        self.full_fn_fake = f'D:\\download\\lung\\BM_Lung_04\\{Seriesinstanceuid}'
                        if not os.path.exists(self.full_fn_fake):
                            os.makedirs(self.full_fn_fake)
                        full_fn_fake = os.path.join(self.full_fn_fake, fn)
                        ds.save_as(full_fn_fake)
                    except Exception as e:
                        print('errormsg: failed to save file [{0}] --{1}'.format(full_fn_fake, e))

                except Exception as e:
                    print("[匿名错误]:{}".format(e))
        except Exception as e:
            print("遍历文件：{}".format(e))


    def get_fake_name(self, rand_uid, fake_prefix):
        ts = time.localtime(time.time())
        return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), self.norm_string(rand_uid, 6))
    
    
    def norm_string(self, str, len_norm):
        str_dest = str
        while len(str_dest) > len_norm or str_dest[0] == '.':
            str_dest = str_dest[1:]
        return str_dest


if __name__ == '__main__':
    try:
        DT = DurationThread(route="D:\\download\\lung\\BM_Lung_0499")
        DT.run()
    except Exception as e:
        print("failed to start:{}".format(e))
