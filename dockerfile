FROM centos:latest
FROM python:3.6

WORKDIR /usr/src
COPY ./requirements.txt ./

RUN pip3 install -r ./requirements.txt
# RUN apt-get update
# RUN apt-get install -y git

# # 创建ssh文件夹
# RUN mkdir /root/.ssh/
# # 复制私key
# ADD ./ssh/* /root/.ssh/
# # 创建 known_hosts文件
# RUN touch /root/.ssh/known_hosts
# # 添加key
# RUN ssh-keyscan git.biomind.com.cn >> /root/.ssh/known_hosts
# # clone仓库
# RUN git clone git@git.biomind.com.cn:QA/Biomind_Test_Platform.git /usr/src/Biomind_test_platform
CMD bash /usr/src/Biomind_Test_Platform/start.sh
