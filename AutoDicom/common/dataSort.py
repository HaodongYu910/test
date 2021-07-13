import copy
import time
import random
import math

def get_date():
    localtime = time.localtime(time.time())
    return time.strftime("%Y%m%d", localtime)

def get_time():
    localtime = time.localtime(time.time())
    return time.strftime("%H%M%S", localtime)

def Myinster(dicta):
    dicta = dict(sorted(dicta.items(), key=lambda i: -len(i[1])))
    listsum = []
    l = 0
    start = 0
    step = 2
    for key, value in dicta.items():
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


def get_fake_name(rand_uid, fake_prefix):
    ts = time.localtime(time.time())
    return "{0}{1}{2}".format(fake_prefix, time.strftime("%m%d", ts), norm_string(rand_uid, 6))


def norm_string(str, len_norm):
    str_dest = str
    while len(str_dest) > len_norm or str_dest[0] == '.':
        str_dest = str_dest[1:]
    return str_dest
