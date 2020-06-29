#! /usr/bin/env python
# coding=utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from django.conf import settings
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib import Account, Credentials, Message, Mailbox, FileAttachment
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

# import email.mime.multipart
# import email.mime.text
# from email.mime.image import MIMEImage
# from email.mime.application import MIMEApplication
# from TestPlatform.HTML_template.test_html import html

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")

'''
1.与邮件服务器建立连接,用户名和密码
2.发邮件:发件人\收件人\主题\内容\附件
3.发送
'''


def send_mail(send_list):
    # 图片处理
    # def addimg(src, imgid):
    #     fp = open(src, 'rb')
    #     msgImage = MIMEImage(fp.read())
    #     fp.close()
    #     msgImage.add_header('Content-ID', imgid)
    #     return msgImage

    # msg = email.mime.multipart.MIMEMultipart()  #生成包含多个邮件体的对象
    # msg1 = MIMEMultipart('mixed')  # 创建带附件的实例
    # msg2 = MIMEMultipart('related')  # 创建内嵌资源的实例
    msg = MIMEMultipart('alternatvie')  # 创建纯文本与超文本实例
    msg['from'] = send_list[0]
    msg['Cc'] = ', '.join(send_list[2])
    msg['to'] = ', '.join(send_list[1])
    msg['subject'] = send_list[3]
    mail_msg = send_list[4]
    html_part = MIMEText(mail_msg, 'HTML', 'utf-8')
    html_part.set_charset('utf-8')
    msg.attach(html_part)  # 邮件正文,将文件正文当成附件发送,当正文内容很多时,提高效率

    # # excel附件--固定格式
    # xlsxpart = MIMEApplication(open(attach_xlsx, 'rb').read())
    # xlsxpart.add_header('Content-Disposition', 'attachment', filename='testcase1.xlsx')
    # msg.attach(xlsxpart)

    # # jpg图片附件
    # jpgpart = MIMEApplication(open(attach_jpg, 'rb').read())
    # jpgpart.add_header('Content-Disposition', 'attachment', filename='测试.jpg')
    # msg.attach(jpgpart)

    # 发送邮件
    try:
        smtplib.SMTP().set_debuglevel(1)  # 设置为调试模式，console中显示
        logger.info("样式成功")
        server = smtplib.SMTP_SSL(settings.MAIL_SERVER, port=settings.MAIL_PORT)  # 链接服务器，smtp地址+端口
        logger.info('链接服务成功')
        server.login(settings.MAIL_USER, settings.MAIL_PWD)  # 登录，用户名+密码
        logger.info('用户名成功')
        server.sendmail(send_list[0], send_list[1], str(msg))  # 发送，from+to+内容
        server.close()
        logger.info('发送邮件成功')
    except Exception as e:
        logger.error("send email failed %s" % e)


def exchange_email():
    email = r'hang.yin@biomind.ai'
    password = r'Yh78033521'

    a = Account(email, credentials=Credentials(email, password), autodiscover=True)


        # 此句用来消除ssl证书错误，exchange使用自签证书需加上
    BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
    # 输入你的域账号
    # cred = Credentials(r'hang.yin@biomind.ai', 'Yh78033521')
    #
    # config = Configuration(server='outlook.office365.com', credentials=cred, auth_type=NTLM)
    # a = Account(
    #     primary_smtp_address='hang.yin@biomind.ai)', config=config, autodiscover=False, access_type=DELEGATE
    # )

    # 此处为用来发送html格式邮件的文件路径
    with open(r'/Users/yin/PycharmProjects/Test_platform/TestPlatform/HTML_template/test.html') as f:
        msg = f.read().decode('utf-8')

    m = Message(
        account=a,
        folder=a.sent,
        subject=u'测试邮件',
        body=HTMLBody(msg),
        to_recipients=[Mailbox(email_address='hang.yin@biomind.ai')]
    )
    m.send_and_save()
# exchange_email()

