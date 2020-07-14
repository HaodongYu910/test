import os
import re
import copy
import requests
import time
import logging
from rx.subjects import Subject
import sys

def stdout_logger(name):
    """
    Use this logger to standardize logs output
    """
    log = logging.getLogger(name)
    log.propagate = False
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    log.handlers = [ stream_handler ]
    log.setLevel(logging.DEBUG)
    return log

log = stdout_logger(__name__)


class KeycloakClient():
    """ Initializes a keycloak gatekeeper client
    Args:
        host:               url of host server (eg. https://192.168.86.53)
        realm_name:         realm of keycloak client (eg. biomind)
        login_callback:     a callback function that will be called when login is required, function should return (username, password) or None to cancel
        error_callback:     a callback function that will be called when an error occurs, message will be passed as the argument

    Returns:
        keycloak http client with get, post, delete, put methods which handles authentications
    """

    def __init__(
            self,
            host,
            realm_name,
            client_id,
            login_callback=None,
            successful_login=None,
            error_callback=None,
            scheduler=None):

        self.reset(
            host,
            realm_name,
            client_id,
            login_callback=login_callback,
            successful_login=successful_login,
            error_callback=error_callback
        )

        self.debounce_refresh = Subject()
        if scheduler:
            self.debounce_refresh \
                .buffer_with_time(5000) \
                .filter(lambda x: len(x) > 0) \
                .subscribe_on(scheduler) \
                .subscribe(lambda x: self.refresh_token())
        else:
            self.debounce_refresh \
                .buffer_with_time(5000) \
                .filter(lambda x: len(x) > 0) \
                .subscribe(lambda x: self.refresh_token())

    def append_auth_header(self, d={}):
        auth_header = {'Authorization': 'Bearer {}'.format(self.raw_token['access_token'])}
        if 'headers' in d:
            d['headers'].update(auth_header)
        else:
            d['headers'] = auth_header
        return d

    def reset(
            self,
            host,
            realm_name,
            client_id,
            login_callback=None,
            successful_login=None,
            error_callback=None):
        log.debug('reset keycloak client ...')

        # logout
        try:
            self.logout()
        except Exception as e:
            pass

        # reset parameters
        self.host = host
        self.realm_name = realm_name
        self.client_id = client_id
        self.login_callback = login_callback
        self.successful_login = successful_login
        self.error_callback = error_callback if error_callback is not None else lambda err: log.error(err)
        self.session = requests.Session()
        self.token = None
        self.raw_token = None

    def login(self, username, password):
        log.debug("logging in ...")
        r = self.session.post(
            "{}/oauth/login".format(self.host),
            data={"username": username, "password": password},
            verify=False,
            timeout=120
        )
        r.raise_for_status()
        self.raw_token = r.json()
        r = self.session.get("{}/oauth/token".format(self.host), verify=False)
        r.raise_for_status()
        self.token = r.json()
        if self.successful_login is not None:
            self.successful_login(username, copy.deepcopy(self.token))

    def logout(self):
        log.debug("logging out ...")
        url = "{}/auth/realms/{}/protocol/openid-connect/logout".format(self.host, self.realm_name)
        r = self.session.post(
            url,
            data={
                'client_id': self.client_id,
                'refresh_token': self.raw_token['refresh_token']
            },
            verify=False,
        )
        r.raise_for_status()
        self.token = None

    def refresh_token(self):
        try:
            log.debug("refreshing token ...")
            r = self.post(
                '/auth/realms/{}/protocol/openid-connect/token'.format(self.realm_name),
                refresh=False,
                data={
                    'client_id': self.client_id,
                    'grant_type': 'refresh_token',
                    'refresh_token': self.raw_token['refresh_token']
                }
            )
            r.raise_for_status()
            self.raw_token = r.json()
            log.debug("token refreshed ...")

        except Exception as e:
            log.debug("failed to refresh token, ({}) ...".format(e))

    def request_login(self):
        """
        Returns:
            False - no login_callback or login_callback returns None
            True - if login_callback exists and returns (username, password)
        """
        try:
            if self.login_callback is None:
                return False
            res = self.login_callback()
            # stop requesting
            if res is None:
                return False
            # request credentials
            else:
                username, pwd = res
                if username is not None:
                    self.login(username, pwd)
                    time.sleep(1)
                    return True

        except Exception as e:
            return self.request_login()

    ####################################################################################################################
    # HELPER METHODS
    ####################################################################################################################

    def get_token(self):
        # login using callback if no token
        if self.token is None:
            log.info('requesting token ...')
            self.request_login()
        return copy.deepcopy(self.token)

    def account_management_url(self):
        return "{}/auth/realms/{}/account".format(self.host, self.realm_name)

    ####################################################################################################################
    # REST METHODS
    ####################################################################################################################

    def get(self, url, refresh=True, **kwargs):
        log.debug('kc.get {} ...'.format(url))
        # login using callback if no token
        if self.token is None:
            if not self.request_login():
                return None
        # update kwargs header with auth
        kwargs = self.append_auth_header(kwargs)
        # request
        res = self.session.get(self.host + url, **kwargs)
        # login if unauthenticated
        if (res.status_code in [400, 401, 415]) or (res.status_code == 200 and res.url != self.host + url):
            if not self.request_login():
                return None
            res = self.session.get(self.host + url, **kwargs)
        # error occured
        if res.status_code != 200 or res.url != self.host + url:
            if res.status_code in [403, 200]:
                self.error_callback("error: unauthorized")
            else:
                self.error_callback("error: {}".format(res.status_code))
        log.debug('kc.get {} done ...'.format(url))
        # refresh token
        if refresh:
            self.debounce_refresh.on_next(True)
        return res

    def post(self, url, refresh=True, **kwargs):
        log.debug('kc.post {} ...'.format(url))
        # login using callback
        if self.token is None:
            if not self.request_login():
                return None
        # update kwargs header with auth
        kwargs = self.append_auth_header(kwargs)
        # request
        res = self.session.post(self.host + url, **kwargs)
        # login if unauthenticated
        if (res.status_code in [400, 401, 415]) or (res.status_code == 200 and res.url != self.host + url):
            if not self.request_login():
                return None
            res = self.session.post(self.host + url, **kwargs)
        # error occured
        if res.status_code != 200 or res.url != self.host + url:
            if res.status_code in [403, 200]:
                self.error_callback("error: unauthorized")
            else:
                self.error_callback("error: {}".format(res.status_code))
        log.debug('kc.post {} done ...'.format(url))
        # refresh token
        if refresh:
            self.debounce_refresh.on_next(True)
        return res

    def delete(self, url, refresh=True, **kwargs):
        log.debug('kc.delete {} ...'.format(url))
        # login using callback
        if self.token is None:
            if not self.request_login():
                return None
        # update kwargs header with auth
        kwargs = self.append_auth_header(kwargs)
        # request
        res = self.session.delete(self.host + url, **kwargs)
        # login if unauthenticated
        if (res.status_code in [400, 401, 415]) or (res.status_code == 200 and res.url != self.host + url):
            if not self.request_login():
                return None
            res = self.session.delete(self.host + url, **kwargs)
        # error occured
        if res.status_code != 200 or res.url != self.host + url:
            if res.status_code in [403, 200]:
                self.error_callback("error: unauthorized")
            else:
                self.error_callback("error: {}".format(res.status_code))
        log.debug('kc.delete {} done ...'.format(url))
        # refresh token
        if refresh:
            self.debounce_refresh.on_next(True)
        return res

    def put(self, url, refresh=True, **kwargs):
        log.debug('kc.put {} ...'.format(url))
        # login using callback
        if self.token is None:
            if not self.request_login():
                return None
        # update kwargs header with auth
        kwargs = self.append_auth_header(kwargs)
        # request
        res = self.session.put(self.host + url, **kwargs)
        # login if unauthenticated
        if (res.status_code in [400, 401, 415]) or (res.status_code == 200 and res.url != self.host + url):
            if not self.request_login():
                return None
            res = self.session.put(self.host + url, **kwargs)
        # error occured
        if res.status_code != 200 or res.url != self.host + url:
            if res.status_code in [403, 200]:
                self.error_callback("error: unauthorized")
            else:
                self.error_callback("error: {}".format(res.status_code))
        log.debug('kc.put {} done ...'.format(url))
        # refresh token
        if refresh:
            self.debounce_refresh.on_next(True)
        return res
