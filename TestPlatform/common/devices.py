import jpush

from TestPlatform.common.regexUtil import *

class JpushDevice():
    def __init__(self,key,secret):
        self.create_jpush_device_by_env(key,secret)

    def create_jpush_device_by_env(self, key,secret):
        _jpush = jpush.JPush(key,secret)
        self.__device=_jpush.create_device()

    def is_exist_rid(self,rid):
        try:
            self.__device.get_deviceinfo(rid)
            return (True,'')
        except Exception as e:
            return (False,e.error['message'])

    def get_device(self,rid):
        is_exist,msg = self.is_exist_rid(rid)
        if is_exist:
            msg=self.__device.get_deviceinfo(rid).payload
        return is_exist,msg

    def get_device_status(self,rid):
        is_exist, msg = self.is_exist_rid(rid)
        if is_exist:
            msg = self.__device.get_device_status(rid).payload
        return is_exist,msg

    def get_remote_tags(self,rid):
        is_exist, msg = self.is_exist_rid(rid)
        if is_exist:
            msg = self.__device.get_deviceinfo(rid).payload['tags']
        return is_exist, msg

    def check_tag(self,rid,*tag):
        is_exist, msg = self.is_exist_rid(rid)
        if is_exist:
            msg = {tag:self.__device.check_taguserexist(tag,rid).payload['result'] for tag in tag}
        return is_exist, msg

    def add_tags(self,rid,*tags):
        is_exist, msg = self.is_exist_rid(rid)
        if is_exist and tags:
            entity = jpush.device_tag(jpush.add(*tags))
            msg = self.__device.set_devicemobile(rid, entity).payload
        return is_exist, msg

    def delete_tags(self,rid,*tags):
        is_exist, msg = self.is_exist_rid(rid)
        if is_exist and tags:
            entity = jpush.device_tag(jpush.remove(*tags))
            msg = self.__device.set_devicemobile(rid, entity).payload
        return is_exist, msg

    def set_tags(self,rid,*tags):
        is_exist, msg = self.is_exist_rid(rid)
        if is_exist and tags:
            is_exist,remote_tags = self.get_remote_tags(rid)
            if isinstance(remote_tags,list):
                remote_tags=list(set(remote_tags)-set(tags))
            if remote_tags and isinstance(remote_tags,list):
                entity = jpush.device_tag(jpush.remove(*remote_tags),jpush.add(*tags))
            else:
                entity = jpush.device_tag(jpush.add(*tags))
            msg = self.__device.set_devicemobile(rid, entity).payload
        return is_exist,msg

    def all_tag_list(self):
        return self.__device.get_taglist().payload

    def clear_tags(self,rid):
        is_exist,tags = self.get_remote_tags(rid)
        if is_exist and tags and isinstance(tags,list):
            entity = jpush.device_tag(jpush.remove(*tags))
            tags = self.__device.set_devicemobile(rid,entity).payload
        return is_exist,tags

def tag(system,tag_type,rid,set_tag):
    appKey=AppKey(system)
    device = JpushDevice(**{'key': appKey[0], 'secret': appKey[1]})
    if tag_type == 'select':
        try:
            res=device.get_remote_tags(rid)
            return res
        except:
            return False

    elif tag_type=='add':
        tag = device.get_remote_tags(rid)
        for i in set_tag:
            if str(i) in tag[1]:
                continue
            else:
                device.add_tags(rid,i)
                return (device.get_remote_tags(rid))
    elif tag_type=='del':
        settag=[]
        tag=device.get_remote_tags(rid)
        for i in tag[1]:
            if i != set_tag:
                settag.append(i)
        device.set_tags(rid,*settag)
        return(device.get_remote_tags(rid))
    elif tag_type=='set':
        device.set_tags(rid,*set_tag)
        return(device.get_remote_tags(rid))

# print(tag('Autotest','add', '1a0018970af17bc9fc2','coinness_zh_cn'))
# print(tag('test_online','add', '101d85590909752e54d','bishijie_zh_cn'))
# print(tag('coinness_online','add', '161a3797c84c60d9158','jpush'))
# print(tag('coinness_online','add', '161a3797c84c60d9158','coinness_en_gb'))
# print(tag('cns_test','select', '18071adc0344ee6823f',['shendu','jpush','coinness_tr_tr']))
#
