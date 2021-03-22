import json
import logging
import random
import time
import uuid

import requests

from config.config import *



class graphRequest():
    def __init__(self):
        endts = round(time.time(),3)
        # dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        self.base_url = 'http://192.168.2.22:9090'
        self.api = '/api/v1/query_range?query=container_memory_usage_bytes%7Bname%3D%22280_biomindserver_1%22%7D&start=1589836394.076&end=1589882392.578&step=172&_=1589879583090'
        self.common_params = {
            'query': "container_memory_usage_bytes%7Bname%3D%22280_biomindserver_1%22%7D",
            'start': 1589836394.076,
            'end':1589882392.578,
            'step':172,
            '_':'1589879583090'
        }

    @property
    def graphrequest(self,**kwargs):
        """ 发送请求 """
        headers = {}
        logger.info(f'请求 URL：{self.base_url + self.api}\n请求参数：{self.common_params}')
        try:
            response = requests.get(
                self.base_url + self.api,
                headers=headers)
            # print(self.common_params)
            data=json.loads(response.text)
            print(data["data"]["result"])

        except Exception as e:
            raise e
        return data["data"]["result"]["values"]

if __name__ == '__main__':
    graphRequest().graphrequest()

