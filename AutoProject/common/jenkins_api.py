#! /usr/bin/env python
# coding=utf-8

import jenkins
import time
from django.conf import settings

__author__ = "vte"
__version__ = "0.0.1"


# 链接jenkins
class JenkinsApi:
    def __init__(self, url='http://10.10.10.2:8095/', username='admin', password='hana#ony'):
        """
            链接 Jenkins 服务
            parm：
            url：Jenkins 地址
            username: admin 用户名
            password：密码
        """
        self.JenkinsServer = jenkins.Jenkins(url, username=username, password=password)

    def get_job(self, jobName):
        """
            获取全部job 信息
        """
        job = self.JenkinsServer.get_jobs(jobName)

        return job

    def get_jobs_info(self, name):
        """
        parm name: 构建名称
         查询 job信息
         """

        # 入参 构建版本名称
        # Refer Example #1 for definition of function 'get_server_instance'
        job = self.JenkinsServer.get_job_info(name)
        number = job['builds'][0]["number"]  # 构建版本

        for i in range(int(number)):
            try:
                url = job.__dict__['_data']['builds'][i]["url"]  # 构建url
            except:
                return False
            id = number - i
            # obj = Build(url, id, job)
            # params = obj.get_params()  # 获取参数
            # print(obj.get_status())
            # # if Client =="iOS":
            # #     params_channel=params['CONFIGURATIONS']
            # #     params["PUSH_KEY"] =""
            # # else:
            # #     params_channel = params['CHANNEL']
            # # if channel==params_channel and obj.get_status()=="SUCCESS" :
            #     break
        return [id]

    def build_job(self, job_name, param_dict):
        """
            启动job  入参 job名 参数变量 dict 类型
        """
        self.JenkinsServer.build_job(job_name, param_dict)
        job = self.JenkinsServer.get_job_info(job_name)
        number = job['builds'][0]["number"]
        # Refer Example #1 for definition of function 'get_server_instance'
        # print(server.get_build_info(job_name,48))
        return number

    def stop_job(self, job_name, number):
        """
                   停止job 构建  入参 job名
                """
        self.JenkinsServer.stop_build(job_name, number)

    def buildStatus(self, job_name, number):
        build_state = self.JenkinsServer.get_build_info(job_name, number)['result']
        return build_state

    def speedProgress(self, job_name, number):
        job_info = self.JenkinsServer.get_build_info(job_name, number)
        job_start_time = job_info['timestamp']  # 任务启动时间
        now_timestamp = int(round(time.time() * 1000))  # 当前时间戳
        estimatedDuration = job_info['estimatedDuration']  # 上次构建时间
        building_process = int(((now_timestamp - job_start_time) / estimatedDuration) * 100) if estimatedDuration > -1 else -1  # 如果estimatedDuration是-1，则说明是首次构建
        if building_process >= 100:
            building_process = 99  # 因为是预估，即使超过了100，也位于99
        return building_process


if __name__ == '__main__':
    # 构建参数化job


    # print(a.build_job("install", {"reset": 0,
    #                               "passwd": "biomind",
    #                               "path": "oss://biomind/Radiology/Prod/2.20.10-radiology2.tgz",
    #                               "version": "2.20.10-radiology",
    #                               "package_name": "2.20.10-radiology2.tgz",
    #                               "environment": "187"}))
    pass
