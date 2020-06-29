#! /usr/bin/env python
# coding=utf-8

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.build import Build

from django.conf import settings

__author__ = "vte"
__version__ = "0.0.1"

#链接jenkins
def get_server_instance():
    # print(settings.SITE_JENKINURL)
    jenkins_url = settings.SITE_JENKINURL
    server = Jenkins(jenkins_url, username='yinhang', password='123456')
    return server

def getBuild(jobName):
    server = get_server_instance()
    job = server[jobName]
    lgb = job.get_last_good_build()
    return job

#查询 版本信息
def get_job_details(name,channel,Client):
    #入参 构建版本名称
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    job = server.get_job(name)
    number = job.__dict__['_data']['lastBuild']['number']  # 构建版本

    for i in range(int(number)):
        try:
            url = job.__dict__['_data']['builds'][i]["url"] #构建url
        except:
            return False
        id =number-i
        obj = Build(url,id, job)
        params=obj.get_params() #获取参数
        if Client =="iOS":
            params_channel=params['CONFIGURATIONS']
            params["PUSH_KEY"] =""
        else:
            params_channel = params['CHANNEL']
        if channel==params_channel and obj.get_status()=="SUCCESS" :
            break
    return [id,params["PUSH_KEY"],number]



"""启动/关闭 job"""
def disable_job(job_name,param_dict):
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    # print(server.get_build_info(job_name,48))
    param_dict = {"VERSION_NAME": "2.0.0","VERSION_CODE": "200","GREENDAO_CODE": "200","CHANNEL": "Release","PUSH_KEY": "Push_release",'TINKER_ABLE': False,"AGE": "coinness"}
    server.build_job(job_name, params=param_dict)
    return True
#
# if __name__ == '__main__':
#     print(get_job_details("CoinWorld_iOS_Branch_v2.7.0",'Debug','iOS'))
#     param_dict = {"APP_VERSION": "2.0.0", "CONFIGURATIONS": "Release", "UPLOAD_ITUNES_CONNECT": False}
#     # param_dict = {"VERSION_NAME": "2.0.0", "VERSION_CODE": "200", "GREENDAO_CODE": "200", "CHANNEL": "Release",
#     #               "PUSH_KEY": "Push_test", 'TINKER_ABLE': False, "AGE": "coinness"}
#     print((disable_job("CoinWorld_iOS_Branch_v2.7.0",param_dict)))