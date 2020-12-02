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
    # jenkins_url = settings.SITE_JENKINURL
    jenkins_url = 'http://192.168.2.38:8080/'
    server = Jenkins(jenkins_url, username='biomind', password='biomind')
    return server

def getBuild(jobName):
    server = get_server_instance()
    job = server[jobName]
    lgb = job.get_jobs_list()
    return lgb

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
        print(obj.get_status())
        # if Client =="iOS":
        #     params_channel=params['CONFIGURATIONS']
        #     params["PUSH_KEY"] =""
        # else:
        #     params_channel = params['CHANNEL']
        # if channel==params_channel and obj.get_status()=="SUCCESS" :
        #     break
    return [id]



"""启动/关闭 job"""
def disable_job(job_name,param_dict):
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    # print(server.get_build_info(job_name,48))
    param_dict = {"ip": "192.168.1.125","aet": "ORTHANC125","keyword": "duration","duration": "All"}
    server.build_job(job_name, params=param_dict)
    return True

# if __name__ == '__main__':
#     # print(getBuild("Duration_test"))
#     print(get_job_details("Duration_test",'Debug','iOS'))
#     param_dict = {"ip": "192.168.1.125","aet": "ORTHANC125","keyword": "duration","duration": "All"}
#     print((disable_job("Duration_test",param_dict)))