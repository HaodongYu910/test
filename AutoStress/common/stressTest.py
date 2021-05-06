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
            logger.info("基准测试开始")
            Manual = ManualThread(stressid=self.id)
            Manual.setDaemon(True)
            Manual.run()
            Restart(id=self.obj.Host.id)
            time.sleep(300)
        except Exception as e:
            logger.error("基准测试失败：{}".format(e))

        try:
            if self.Flag is True:
                Single = SingleThread(stressid=self.id)
                Single.setDaemon(True)
                Single.run()

        except Exception as e:
            logger.error("单一测试失败：{}".format(e))

        try:
            # 开始时间
            start = datetime.datetime.now()
            # 结束时间
            end = (datetime.datetime.now() + datetime.timedelta(hours=int(self.obj.duration))).strftime(
                "%Y-%m-%d %H:%M:%S")
            if self.Flag is True:
                logger.info("混合测试开始")
                Hybrid = HybridThread(stressid=self.id)
                Hybrid.setDaemon(True)
                Hybrid.start()
                while str(start) < str(end):
                    start = datetime.datetime.now()
                Restart(id=self.obj.Host.id)
                time.sleep(300)
        except Exception as e:
            logger.error("混合测试失败：{}".format(e))
            # 混合测试

    def setFlag(self, parm):  # 外部停止线程的操作函数
        self.Flag = parm  # boolean

