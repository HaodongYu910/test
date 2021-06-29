import copy
import time
import random
import math

def get_date():
    localtime = time.localtime(time.time())
    return (time.strftime("%Y%m%d", localtime))


def get_time():
    localtime = time.localtime(time.time())
    return (time.strftime("%H%M%S", localtime))


def get_rand_uid():
    # rand_val = random.randint(1, math.pow(10, 16) - 1)
    # return "%08d" % rand_val
    return str(time.time())



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


