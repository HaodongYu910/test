import requests
import json
import datetime
import logging
from ..models import message_group, message_detail, dictionary

logger = logging.getLogger(__name__)

"""
参数示例：
        {
           "touser" : "UserID1|UserID2|UserID3",
           "toparty" : "PartyID1|PartyID2",
           "totag" : "TagID1 | TagID2",
           "msgtype" : "text",
           "agentid" : 1,
           "text" : {
               "content" : "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
           },
           "safe":0,
           "enable_id_trans": 0,
           "enable_duplicate_check": 0,
           "duplicate_check_interval": 1800
        }

参数详解：
        touser	否	指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。
        特殊情况：指定为”@all”，则向该企业应用的全部成员发送
        toparty	否	指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。
        当touser为”@all”时忽略本参数
        totag	否	指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。
        当touser为”@all”时忽略本参数
        msgtype	是	消息类型，此时固定为：text
        agentid	是	企业应用的id，整型。企业内部开发，可在应用的设置页面查看；第三方服务商，可通过接口 获取企业授权信息 获取该参数值
        content	是	消息内容，最长不超过2048个字节，超过将截断（支持id转译）
        safe	否	表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        enable_id_trans	否	表示是否开启id转译，0表示否，1表示是，默认0。仅第三方应用需要用到，企业自建应用可以忽略。
        enable_duplicate_check	否	表示是否开启重复消息检查，0表示否，1表示是，默认0
        duplicate_check_interval	否	表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时

注：QA部门ID是132，如果需要其他部门可以联系CIT 张子轩。

"""
"""
msgtype	是	消息类型，此时固定为text
content	是	文本内容，最长不超过2048个字节，必须是utf8编码
mentioned_list	否	userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
mentioned_mobile_list	否	手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
目前支持的markdown语法是如下的子集：

标题 （支持1至6级标题，注意#与文字中间要有空格）
# 标题一
## 标题二
### 标题三
#### 标题四
##### 标题五
###### 标题六
加粗
**bold**
链接
[这是一个链接](http://work.weixin.qq.com/api/doc)
行内代码段（暂不支持跨行）
`code`
引用
> 引用文字
字体颜色(只支持3种内置颜色)
<font color="info">绿色</font>
<font color="comment">灰色</font>
<font color="warning">橙红色</font>
图片类型

{
    "msgtype": "image",
    "image": {
        "base64": "DATA",
        "md5": "MD5"
    }
}
参数	是否必填	说明
msgtype	是	消息类型，此时固定为image
base64	是	图片内容的base64编码
md5	是	图片内容（base64编码前）的md5值
注：图片（base64编码前）最大不能超过2M，支持JPG,PNG格式


图文类型

{
    "msgtype": "news",
    "news": {
       "articles" : [
           {
               "title" : "中秋节礼品领取",
               "description" : "今年中秋节公司有豪礼相送",
               "url" : "www.qq.com",
               "picurl" : "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }
        ]
    }
}
参数	是否必填	说明
msgtype	是	消息类型，此时固定为news
articles	是	图文消息，一个图文消息支持1到8条图文
title	是	标题，不超过128个字节，超过会自动截断
description	否	描述，不超过512个字节，超过会自动截断
url	是	点击后跳转的链接。
picurl	否	图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。


文件类型

{
    "msgtype": "file",
    "file": {
         "media_id": "3a8asd892asd8asd"
    }
}
参数	是否必填	说明
msgtype	是	消息类型，此时固定为file
media_id	是	文件id，通过下文的文件上传接口获取

"""

def MessageGroup(send_url, params):
    # """
    # 发送消息
    # """
    try:
        requests.post(send_url, data=json.dumps(params))
    except Exception as e:
        logger.error("send Message fail :{}".format(e))



def sendMessage(touser='',toparty='',message='Message'):
    """
    固定参数:corpid,appsecret，agentid
    """
    corpid = 'wwa15f77b69def1486'
    appsecret = 'yH9BHMQMpqlppA8Np-K1_sTnw7hSxo872FPGYQibGSk'
    agentid = 1000014

    """
    固定:获取token
    """
    token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(corpid, appsecret)
    req = requests.get(token_url)
    accesstoken = req.json()['access_token']

    """
    固定：发消息API  post请求
    """
    msgsend_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(accesstoken)

    params = {
        "touser": touser,
        "toparty": toparty,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": message
        },
        "safe": 0
    }

    """
    发送消息
    """
    try:
        requests.post(msgsend_url, data=json.dumps(params))
    except Exception as e:
        logger.error("send Message fail :{}".format(e))

# Ansible 消息推送
def AnsibleMessage(**kwargs):
    obj = message_group.objects.get(type='ansible', status=True)
    data = kwargs["data"]
    if data["status"] == "fail":
        if data["channel"] == "#production_build_radiology":
            #obj.send_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cd8a05b4-37b9-49e6-925a-a3aa6cc87d6c'
            params = {
                "msgtype": "text",
                "text": {
                    "content": "【{0} Production Build Radiology Fail】 \n Job_Name: {1} \n JobURL: {2} \n ArtifactURL {3} \n {4}".format(
                        data["version"], data["job_name"], data["AWXURL"], data["ArtifactURL"], data["msg"]),
                    "mentioned_list": ["@yinhang"]
                }
            }
        else:
            params = {
                "msgtype": "text",
                "text": {
                    "content": "【Nightly Build {0} Fail】 \n Job_Name: {1} \n JobURL: {2} \n ArtifactURL {3} \n {4}".format(
                        data["version"], data["job_name"], data["AWXURL"], data["ArtifactURL"], data["msg"]),
                    "mentioned_list": ["@all"]
                }
            }
    else:
        if data["channel"] == "#production_build_radiology":
            params = {
                "msgtype": "text",
                "text": {
                    "content": "{} 版本构建成功！".format(data["version"]),
                }
            }
        else:
            params = {
                "msgtype": "text",
                "text": {
                    "content": "Nightly Build {} Success".format(data["version"])
                }
            }
    try:
        MessageGroup(obj.send_url, params)
    except Exception as e:
        logger.error("send Message fail :{}".format(e))


