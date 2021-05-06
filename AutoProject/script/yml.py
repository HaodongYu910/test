import os
import operator
import paramiko
import yaml
import time
import requests
path = "/usr/local/prometheus"
yamlData = open(os.path.join(path, "prometheus.yml"),encoding="UTF-8")
datas = yaml.load(yamlData)
print(datas)

if __name__ == '__main__':
    pass
    # size = get_FileSize("D:\\workspace\\test\\Biomind_Test_Platform\\AutoProject\\Atest.zip")
    # print(size)
