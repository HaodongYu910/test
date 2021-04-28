import datetime
import os
import shutil
import threading
import time
from django.conf import settings
from ..models import stress_record, stress_result, stress

from AutoProject.utils.graphql.graphql import *
from AutoProject.common.biomind import Restart
from ..common.manual import ManualThread
from ..common.single import SingleThread
from ..common.hybrid import HybridThread
from ..common.saveResult import ResultThread

logger = logging.getLogger(__name__)



# 全部的性能测试
class StressThread(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.Flag = True  # 停止标志位
        # self.count = kwargs["count"]  # 可用来被外部访问的
        # 性能测试id
        self.id = kwargs["stressid"]
        self.obj = stress.objects.get(stressid=self.id)

    def run(self):
        try:
            self.obj.teststatus = "基准测试"
            self.obj.status = True
            self.obj.save()
            logger.info("基准测试开始")
            Manual = ManualThread(stressid=self.id)
            Manual.setDaemon(True)
            Manual.run()
            Restart(id=self.obj.Host.id)
            time.sleep(300)
        except Exception as e:
            logger.error("基准测试失败：{}".format(e))

        try:
            self.obj.teststatus = "混合测试"
            self.obj.status = True
            # 开始时间
            start = datetime.datetime.now()
            # 结束时间
            end = (datetime.datetime.now() + datetime.timedelta(hours=int(self.obj.duration))).strftime(
                "%Y-%m-%d %H:%M:%S")
            self.obj.start_date = start
            self.obj.end_date = end

                while str(start) < str(end):
                    start = datetime.datetime.now()
                Restart(id=self.obj.Host.id)
                time.sleep(300)
        except Exception as e:
            logger.error("混合测试失败：{}".format(e))
            # 混合测试

        try:
            self.obj.teststatus = "单一测试"
            self.obj.status = True
            self.obj.save()
            if self.Flag is True:
                Single = SingleThread(stressid=self.id)
                Single.setDaemon(True)
                Single.run()
        except Exception as e:
            logger.error("单一测试失败：{}".format(e))
            # 混合测试

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

    def setParm(self, parm):  # 外部修改内部信息函数
        self.Parm = parm

    def getParm(self):  # 外部获得内部信息函数
        return self.parm
