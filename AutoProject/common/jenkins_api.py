#! /usr/bin/env python
# coding=utf-8

import jenkins
from django.conf import settings

__author__ = "vte"
__version__ = "0.0.1"


# 链接jenkins
class JenkinsApi:
    def __init__(self, url='http://10.10.10.2:8095/', username='admin', password='hana#ony'):
        """
                 链接 Jenkins 服务
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
                    # 查询 版本信息
                              """

        # 入参 构建版本名称
        # Refer Example #1 for definition of function 'get_server_instance'
        job = self.JenkinsServer.get_job_info(name)
        number = job['builds'][0]["number"]  # 构建版本
        print(number)

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
        build = self.JenkinsServer.build_job(job_name, param_dict)
        # Refer Example #1 for definition of function 'get_server_instance'
        # print(server.get_build_info(job_name,48))
        return build

    def stop_job(self, job_name):
        """
                   停止job 构建  入参 job名
                """
        while True:
            job = self.JenkinsServer.get_job_info(job_name)
            number = job['builds'][0]["number"]
            print(number)
            stopBuild = self.JenkinsServer.stop_build(job_name, number)



if __name__ == '__main__':
    pass
    # 构建参数化job
    # a = JenkinsApi()
    # print(a.build_job("Radiology_Prod", {"BRANCH" : "2.20-fda-preview"}))



