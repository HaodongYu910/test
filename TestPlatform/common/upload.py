from django.shortcuts import render
from django.http import HttpResponse
import os

# Create your views here.
def upload_file(File,url):
    # 请求方法为POST时，进行处理

            # print(os.path.exists('/temp_file/'))
            with open("./test01app/temp_file/%s" % File.name, 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)
            return HttpResponse("UPload over!")


