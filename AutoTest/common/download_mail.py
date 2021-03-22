# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import poplib
import logging
import email
import datetime,time
import os
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from django.conf import settings


logger = logging.getLogger(__name__) # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。

poplib._MAXLINE=20480

def decode_str(s):  # 字符编码转换
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def get_att(msg, name):
    attachment_files = []
    #上级路径
    dir_path = os.path.abspath(os.path.join(os.getcwd()))
    date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # 格式化收件时间
    excel_date = time.strftime("%Y%m%d", date1)

    for part in msg.walk():
        file_name = part.get_filename()  # 获取附件名称类型
        contType = part.get_content_type()

        if file_name:
            h = email.header.Header(file_name)
            dh = email.header.decode_header(h)  # 对附件名称进行解码
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))  # 将附件名称可读化
                # filename = filename.encode("utf-8")

            data = part.get_payload(decode=True)  # 下载附件
            if name[7:]=='-Coinness&nbsp;International--崩溃信息日报':
                excel_name = '-Coinness_International--崩溃信息日报'
            else:
                excel_name = name[7:]
            logger.info("下载地址"+dir_path)
            att_file = open('/usr/project_env/platform/logs/{1}{2}.xls'.format(dir_path,excel_date,excel_name), 'wb') # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            attachment_files.append(filename)
            att_file.write(data)  # 保存附件
            att_file.close()
    return attachment_files


def get_email_headers(msg):
    headers = {}
    for header in ['From', 'To', 'Cc', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            if header == 'Date':
                headers['Date'] = value
            if header == 'Subject':
                subject = decode_str(value)
                headers['Subject'] = subject
            if header == 'From':
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                from_addr = u'%s <%s>' % (name, addr)
                headers['From'] = from_addr
            if header == 'To':
                all_cc = value.split(',')
                to = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    to_addr = u'%s <%s>' % (name, addr)
                    to.append(to_addr)
                headers['To'] = ','.join(to)
            if header == 'Cc':
                all_cc = value.split(',')
                cc = []
                for x in all_cc:
                    hdr, addr = parseaddr(x)
                    name = decode_str(hdr)
                    cc_addr = u'%s <%s>' % (name, addr)
                    cc.append(to_addr)
                headers['Cc'] = ','.join(cc)
    return headers



def download(get_starttime,get_endtime):
    # 连接到POP3服务器,有些邮箱服务器需要ssl加密，对于不需要加密的服务器可以使用poplib.POP3()
    server = poplib.POP3_SSL(settings.MAIL_SERVER)
    server.set_debuglevel(1)
    # 打印POP3服务器的欢迎文字:
    logger.info(server.getwelcome().decode('utf-8'))
    # 身份认证:
    server.user(settings.MAIL_USER)
    server.pass_(settings.MAIL_PWD)
    # 返回邮件数量和占用空间:
    logger.info('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]

    index = len(mails)

    for i in range(index, 0, -1):
        # 倒序遍历邮件
        resp, lines, octets = server.retr(i)
        # lines存储了邮件的原始文本的每一行,
        # 邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('GB2312')
        # 解析邮件:
        msg = Parser().parsestr(msg_content)
        headers = get_email_headers(msg)
        # logger.info('subject:', headers['Subject'])
        # logger.info('from:', headers['From'])
        # logger.info('to:', headers['To'])
        # logger.info('date:', headers['Date'])

        now_time = datetime.datetime.today()
        # 获取邮件时间
        date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # 格式化收件时间
        date2 = time.strftime("%Y%m%d %H:%M:%S", date1)  # 邮件时间格式转换

        if len(get_starttime)>0:
            start_time = get_starttime + " 00:00:00"
        else:
            start_time = now_time.strftime("%Y%m%d ") + "00:00:00"

        if  len(get_endtime)>0:
            end_time = get_endtime + " 00:00:00"
        else:
            end_time = now_time.strftime("%Y%m%d ") + "23:59:59"

        if (date2 < start_time ) | (date2 > end_time):
            continue
        f_list = get_att(msg, headers['Subject'])  # 获取附件

    server.quit()

