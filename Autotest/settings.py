"""
Django settings for Autotest project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# import ldap
# from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion, GroupOfNamesType

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u_902ri*_wg9^0_xc0@=fvdi4@o0ci)j34t59p3bw#v-rn1cq2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#服务器

SITE_DBURL = "192.168.1.121"      # 数据库 地址
SITE_JIRAURL = "http://jira.test.com"  #JIRA 地址
SITE_JENKINURL = "http://127.0.0.1:8080"  #JENKINS 地址

#邮箱配置
MAIL_SERVER = "smtp.exmail.qq.com"  #邮箱地址
MAIL_PORT = 465  #端口号
MAIL_USER = "qa@biomind.ai"  #账号
MAIL_PWD = "Autotest@123"  #密码

# Dicom的路径
Dicom_PATH = '/home/biomind/testDatas'

# keycloak 用户名
user ='test'
passwd ='Asd@123456'

# 创建日志的路径
LOG_PATH = os.path.join(BASE_DIR, 'logs')
# 本地

# SITE_DBURL = "rm-2ze7j006i3129ay5vmo.mysql.rds.aliyuncs.com"
# SITE_JIRAURL = "http://jira.bishijie.com"
# SITE_JENKINURL = "http://39.105.135.38:8080"

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        # 简单的日志格式
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            # 'filters': ['special'],
        },
        # 默认的
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "test_info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },# 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "test_error.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门定义一个收集特定信息的日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "test_collect.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'] if DEBUG else ["default"],
            'level': 'ERROR',
            'propagate': False
        },
        '': {
            'handlers': ['default', 'console'] if DEBUG else ["default"],
            'level': 'DEBUG',
            'propagate': False
        },
        'django_auth_ldap': {  # django_auth_ldap模块相关日志打印到console
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,  # 选择关闭继承，不然这个logger继承自默认，日志就会被记录2次了(''一次，自己一次)
        },
    }
}

# #使用LDAP验证
# AUTHENTICATION_BACKENDS = (
#     'django_auth_ldap.backend.LDAPBackend',  #配置为先使用LDAP认证，如通过认证则不再使用后面的认证方式
#     'django.contrib.auth.backends.ModelBackend',
# )
# #ldap的连接基础配置
# AUTH_LDAP_SERVER_URI = 'ldap://ldap.bishijie.com'
# AUTH_LDAP_BASE_DN = 'ou=Users,dc=bishijie,dc=com'
# AUTH_LDAP_BIND_DN = 'cn=RO,dc=bishijie,dc=com'
# AUTH_LDAP_BIND_PASSWORD = 'bishijie'
#
# # 允许认证用户的路径
#
# AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=Users,dc=bishijie,dc=com",
#                                    ldap.SCOPE_SUBTREE, "(&(objectClass=person)(uid=%(user)s))")
#
# # 当ldap用户登录时，从ldap的用户属性对应写到django的user数据库，键为django的属性，值为ldap用户的属性
# AUTH_LDAP_USER_ATTR_MAP = {
#     "username": "uid",
#     "last_name": "sn",
#     "email": "mail"
# }

ALLOWED_HOSTS = ['*',]

AUTH_PROFILE_MODULE = 'djangoadmin.TestPlatform.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TestPlatform',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
]


LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#跨域增加忽略
CORS_ORIGIN_ALLOW_ALL = True

#跨域增加忽略
CORS_ALLOW_CREDENTIALS = True

#设置白名单
CORS_ORIGIN_WHITELIST = (  '*')

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic',
        }
    },
    'USE_SESSION_AUTH': True
}

ROOT_URLCONF = 'Autotest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [os.path.join(BASE_DIR, 'static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

#静态文件主目录
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '/static/'),
)


STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATIC_URL = '/static/'


WSGI_APPLICATION = 'Autotest.wsgi.application'


# Database 服务器环境

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'autotest',
        'USER': 'root',
        'PASSWORD': 'P@ssw0rd2o8',
        'HOST': SITE_DBURL,
        'PORT': '3306',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'test', #数据库名字
#         'USER': 'postgres',
#         "PASSWORD" : 'biomind',
#         "HOST":SITE_DBURL,
#         'PORT':5432,
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#设置时区
LANGUAGE_CODE = 'zh-hans'  #中文

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False   #默认是Ture，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！！

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination',
    ),
    'EXCEPTION_HANDLER': (
            'TestPlatform.common.common.custom_exception_handler'
        # 'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
    )

}

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

#定时配置
CRONJOBS = [
    # 表示每天2：01执行
    #('30 19 * * *', 'TestPlatform.scheduletask.job1_task','>>/home/biomind/Biomind_Test_Platform/logs/last_scheduled_job.logs'),# 每天20：00 执行发送测试邮件 '> /usr/project_env/platform/TestPlatform/logs/job.logs'
    ('*/20 * * * *', 'TestPlatform.scheduletask.job2_task','>>/home/biomind/Biomind_Test_Platform/logs/last_scheduled_job.logs'),# 每天09：30 执行同步听云数据
]


# 30 09 * * *'