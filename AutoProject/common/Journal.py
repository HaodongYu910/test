from django.conf import settings
from AutoProject.common.transport import SSHConnection
import logging
import os

import functools
logger = logging.getLogger(__name__)
import datetime

def log(param):
    if callable(param):
        def wrapper(*args, **kw):
            print('%s function()' % (param.__name__,))
            param(*args, **kw)

        return wrapper

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            now = datetime.datetime.now()
            logger.info('%s --参数：%s  方法：%s' % (now, param, func.__name__))
            # path = "{0}/{1}.log".format(settings.LOG_PATH, kw["name"])
            path = "D:\\workspace\\test\\Biomind_Test_Platform\\logs\\test.log"
            with open(path, 'a', encoding='utf-8') as f:
                f.write(kw["content"])
            return func(*args, **kw)

        return wrapper

    return decorator


def AddJournal(**kw):
    # path = "{0}/{1}.log".format(settings.LOG_PATH, kw["name"])
    path = "D:\\workspace\\test\\Biomind_Test_Platform\\logs\\test.log"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(kw["content"])

def readJournal(name):
    full_log = '{0}/{1}.log'.format(settings.LOG_PATH, name)
    #full_log ="D:\\workspace\\test\\Biomind_Test_Platform\\logs\\test.log"
    with open(full_log, 'r', encoding='utf-8') as f:
        strTxt = f.read()  # 将txt文件的所有内容读入到字符串txtstr中
        return strTxt
        # lines = f.readlines()
        # journal = []
        # for line in str(lines).split('\n'):
        #     journal.append(line)
        # print(journal)
