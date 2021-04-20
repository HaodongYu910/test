import urllib3
from keycloak import KeycloakAdmin
import logging
logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class KeycloakAdm:
    def __init__(self, orthanc_ip=None, url=None, user=None, passwd=None, realm=None, change_realm=None, verify=False):
        """
        The administrator logs in to keycloak and can perform user creation and modification
        :param url: keycloak server ip; eg. https://192.168.2.39/auth/
        :param user: admin username
        :param passwd: admin password
        :param realm: realm name
        :param change_realm: new realm name
        :param verify: True if want check connection SSL
        """
        self.kc_adm = KeycloakAdmin(
            server_url=url or '{0}/auth/'.format(orthanc_ip),
            username=user or 'admin',
            password=passwd or 'secret',
            realm_name=realm or 'master',
            verify=verify
        )
        self.kc_adm.realm_name = change_realm or 'biomind'

    def create_update_user(self, query):
        """
        Create or add users
        :param query: user info eg. {"username": "biomind3d","enabled": True}
        :return: user id
        """
        user_id = self.kc_adm.get_user_id(query.get('username'))
        if user_id:
            self.kc_adm.update_user(user_id, query)
        else:
            user_id = self.kc_adm.create_user(query)

        return user_id

    def user_add_group(self, username, group_name):
        """
        add group in user
        :param username: username
        :param group_name: group name
        """
        user_id = self.kc_adm.get_user_id(username)
        if not user_id:
            logger.warning('please create user, no such account')
        group = self.kc_adm.get_group_by_path(f'/{group_name}')
        if not group:
            logger.warning("Can't find the corresponding group, please add")
        self.kc_adm.group_user_add(user_id, group.get('id'))

    def user_add_all_groups(self, username):
        """
        add all groups in user
        :param username: username
        """
        user_id = self.kc_adm.get_user_id(username)
        if not user_id:
            logger.warning('please create user, no such account')
        groups = self.kc_adm.get_groups()
        for group in groups:
            self.kc_adm.group_user_add(user_id, group.get('id'))

    def update_user_add_group(self, query, group_name):
        """
        create or update user and add group
        :param query: user info
        :param group_name: group name
        """
        user_id = self.kc_adm.get_user_id(query.get('username'))
        if user_id:
            self.kc_adm.update_user(user_id, query)
        else:
            user_id = self.kc_adm.create_user(query)
        group = self.kc_adm.get_group_by_path(f'/{group_name}')
        if not group:
            logger.warning("Can't find the corresponding group, please add")
        self.kc_adm.group_user_add(user_id, group.get('id'))

    def create_update_user_add_all_group(self, query):
        """
        create or update user and add all groups
        :param query: user info
        """
        user_id = self.kc_adm.get_user_id(query.get('username'))
        if user_id:
            self.kc_adm.update_user(user_id, query)
        else:
            user_id = self.kc_adm.create_user(query)
        groups = self.kc_adm.get_groups()
        if user_id:
            for group in groups:
                self.kc_adm.group_user_add(user_id, group.get('id'))


if __name__ == '__main__':
    user_info = {"username": "test", "enabled": True,
                 "credentials": [{"value": "1", "type": "password", }]}
    kc_adm = KeycloakAdm(orthanc_ip='{0}://{1}'.format("https", "192.168."))
    # kc_adm.update_user_add_group(user_info, 'admins')
    kc_adm.create_update_user_add_all_group(user_info)
    pass
    # user_info = {"username": "biomind3d", "enabled": True, "credentials": [{"value": "engine3D.", "type": "password", }]}
    # kc_adm = KeycloakAdm(orthanc_ip='https://192.168.2.103')
    # # kc_adm.update_user_add_group(user_info, 'admins')
    # kc_adm.create_update_user_add_all_group(user_info)
