from django.conf.urls import url
from rest_framework import routers

from .api.projectList import *
from .api.projectTitle import ProjectInfo
from .api import user
from .api.global_parameter import *
from .api.Jiradata import *
from .api.user_permission import *
from .api.apiDictionary import *
from .api.apiUpload import *
from .api.apInstall import *
from .api.api import test
from .api import dynamic
from .api import member
# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)

# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'project_list', ProjectList.as_view()),
    url(r'add_project', AddProject.as_view()),
    url(r'update_project', UpdateProject.as_view()),
    url(r'del_project', DelProject.as_view()),
    url(r'disable_project', DisableProject.as_view()),
    url(r'enable_project', EnableProject.as_view()),
    url(r'title/project_info', ProjectInfo.as_view()),
    url(r'member/del_email', member.DelEmail.as_view()),
    url(r'member/get_email', member.GetEmail.as_view()),
    url(r'dynamic/dynamic', dynamic.Dynamic.as_view()),
    url(r'dynamic/dynamic', dynamic.Dynamic.as_view()),
    url(r'global/host_total', HostTotal.as_view()),
    url(r'global/add_host', AddHost.as_view()),
    url(r'global/update_host', UpdateHost.as_view()),
    url(r'global/del_host', DelHost.as_view()),
    url(r'global/disable_host', DisableHost.as_view()),
    url(r'global/enable_host', EnableHost.as_view()),
    url(r'global/disable_protocol', DisableProtocol.as_view()),
    url(r'global/enable_protocol', EnableProtocol.as_view()),
    url(r'user/login', user.obtain_auth_token),
    url(r'user/info', userinfo.as_view()),
    url(r'jira/list', jiradata.as_view()),
    url(r'jira/figure', jira_figure.as_view()),
    url(r'addupload', AddUpload.as_view()),  # 文件上传
    url(r'delupload', DelUpload.as_view()),  # 文件上传
    url(r'upload', getUpload.as_view()),  # 文件列表
    url(r'dictionary/list', Dictionary.as_view()),
    url(r'dictionary/add', AddDictionary.as_view()),
    url(r'dictionary/update', UpdateDictionary.as_view()),
    url(r'dictionary/del', DelDictionary.as_view()),
    url(r'dictionary/disable', DisableDictionary.as_view()),
    url(r'dictionary/enable', EnableDictionary.as_view()),
    url(r'install/add', AddInstall.as_view()),
    url(r'install/update', UpdateInstall.as_view()),
    url(r'install/del', DelInstall.as_view()),
    url(r'install/disable', DisableInstall.as_view()),
    url(r'install/enable', EnableInstall.as_view()),
    url(r'install/journal', getJournal.as_view()),
    url(r'install/getReport', getInstallReport.as_view()),
    url(r'install/list', getInstall.as_view()),
    url(r'install/version', getInstallVersion.as_view()),
    url(r'deploy', Install.as_view()),
    url(r'createRestart', getRestart.as_view()),
    url(r'totest', test.as_view()),
]
