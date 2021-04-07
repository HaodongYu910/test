# -*- coding: utf-8 -*-
"""
# @File    : keycloak_admin.py
# @Time    : 2020/5/28 6:17 下午
"""
import logging
import urllib3
from keycloak import KeycloakAdmin as KcAdmin
from keycloak.urls_patterns import URL_ADMIN_USERS
from keycloak.exceptions import raise_error_from_response, KeycloakGetError
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('urllib3.util.retry').setLevel(logging.WARNING)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('requests.packages.urllib3.util.retry').setLevel(logging.WARNING)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class KeycloakApi(KcAdmin):

    def get_users(self, query=None):
        params_path = {"realm-name": self.realm_name}
        url = URL_ADMIN_USERS.format(**params_path)

        if not query:
            return super().get_users(query)
        else:
            query = {
                'first': query.get('first', 0),
                'max': query.get('max', self.PAGE_SIZE),
                'briefRepresentation': query.get('briefRepresentation', True),
                'search': query.get('search', '')
            }
            return raise_error_from_response(
                self.raw_get(url, **query),
                KeycloakGetError)

    def users_count_with_filter(self, query=None):
        return len(super().get_users(query))

    def refresh_token(self):
        refresh_token = self.token.get('refresh_token')
        try:
            self.token = self.keycloak_openid.refresh_token(refresh_token)
        except KeycloakGetError as e:
            if e.response_code == 400 and (b'Refresh token expired' in e.response_body
                                           or b'Session not active' in e.response_body
                                           or b'Stale token' in e.response_body
                                           or b'Token is not active' in e.response_body):
                self.get_token()
            else:
                raise
        self.connection.add_param_headers(
            'Authorization', 'Bearer ' + self.token.get('access_token'))


class KeycloakAdmin:
    kc_admin = KeycloakApi(
        server_url=f"https://192.168.1.172:443/auth/",
        username='test',
        password='Asd@123456',
        realm_name="biomind",
        auto_refresh_token=[
            'get',
            'put',
            'post',
            'delete'],
        verify=False)

    @classmethod
    def get_all_users(cls, query=None):
        def get_user_group(user):
            group = cls.kc_admin.get_user_groups(user.get("id", None))
            user['rolenames'] = [x.get('name', None) for x in group]

        users = cls.kc_admin.get_users(query)

        # 线程池加速实时获取user
        executor = ThreadPoolExecutor(max_workers=8)
        all_task = [executor.submit(get_user_group, user) for user in users]

        for future in as_completed(all_task):
            future.result()

        return users

    @classmethod
    def get_user(cls, user_id):
        return cls.kc_admin.get_user(user_id)

    @classmethod
    def get_groups(cls):
        return cls.kc_admin.get_groups()

    @classmethod
    def users_count(cls):
        return cls.kc_admin.users_count()

    @classmethod
    def users_count_with_filter(cls, query=None):
        return cls.kc_admin.users_count_with_filter(query)

    @classmethod
    def set_password_groups(cls, user_id, password, group_ids):
        if password:
            cls.kc_admin.set_user_password(user_id, password, False)

        if group_ids:
            # 创建一个用户后，有一个默认的角色分组，需要删除默认的分组
            groups = cls.kc_admin.get_user_groups(user_id)
            for group in groups:
                group_id = group['id']
                cls.kc_admin.group_user_remove(user_id, group_id)

            for group_id in group_ids:
                cls.kc_admin.group_user_add(user_id, group_id)

    @classmethod
    def create_user(cls, username, password, group_ids, firstname, lastname):
        user_id = cls.kc_admin.create_user({
            'username': username,
            "enabled": True,
            "firstName": firstname,
            "lastName": lastname,
            "credentials": [{
                "value": password,
                "type": "password"
            }]
        })
        cls.set_password_groups(user_id, None, group_ids)

    @classmethod
    def delete_user(cls, user_id):
        cls.kc_admin.delete_user(user_id)

    @classmethod
    def update_user(
            cls,
            user_id,
            username,
            firstname,
            lastname,
            password,
            group_ids):
        # 确保user是存在的
        user = cls.kc_admin.get_user(user_id)
        cls.kc_admin.update_user(user['id'],
                                 {'username': username,
                                  'firstName': firstname,
                                  'lastName': lastname
                                  }
                                 )
        cls.set_password_groups(user_id, password, group_ids)


if __name__ == '__main__':
    print(KeycloakAdmin.get_all_users())
    print(KeycloakAdmin.get_all_users({
        'briefRepresentation': False,
        'max': 10,
        'first': 0
    }))  # 获得用户ID

    groups = KeycloakAdmin.get_groups()
    KeycloakAdmin.create_user(
        'test1', 'Asd@123456', [
            x['id'] for x in groups],'test','test')  # 获得角色(分组)ID