from django.conf.urls import url
from rest_framework import routers

from .api import user, VisitorRecord
from .api.global_parameter import *
from .api.Jiradata import *
from .api.Sendmail import *
from .api.test_report import *
from .api.user_permission import *
from .api.apiSmoke import *
from .api.apiDictionary import *
from .api.apiUpload import *
from .api.apInstall import *
# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
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
    url(r'user/VisitorRecord', VisitorRecord.Record.as_view()),
    url(r'addreport', Addreport.as_view()),
    url(r'updatereport', Updatereport.as_view()),
    url(r'delreport', Delreport.as_view()),
    url(r'report', loadReport.as_view()),
    url(r'sendreport', Sendreport.as_view()),
    url(r'risk/add', Add_test_risk.as_view()),
    url(r'risk/update', Updatetest_risk.as_view()),
    url(r'risk/del', DelAutoTest_risk.as_view()),
    url(r'risk/disable_risk', DisableRisk.as_view()),
    url(r'risk/enable_riskt', EnableRisk.as_view()),
    url(r'risk', Testrisk.as_view()),
    url(r'jira/list', jiradata.as_view()),
    url(r'jira/figure', jira_figure.as_view()),
    url(r'send', sendmail.as_view()),
    url(r'addupload', AddUpload.as_view()),# 文件上传
    url(r'delupload', DelUpload.as_view()),# 文件上传
    url(r'upload', getUpload.as_view()),  # 文件列表
    url(r'dictionary/list', Dictionary.as_view()),
    url(r'dictionary/add', AddDictionary.as_view()),
    url(r'dictionary/update', UpdateDictionary.as_view()),
    url(r'dictionary/del', DelDictionary.as_view()),
    url(r'dictionary/disable', DisableDictionary.as_view()),
    url(r'dictionary/enable', EnableDictionary.as_view()),
    url(r'gold/addsmoke', AddSmoke.as_view()),
    url(r'gold/updatesmoke', UpdateSmoke.as_view()),
    url(r'gold/delsmoke', DelSmoke.as_view()),
    url(r'gold/disablesmoke', DisableSmoke.as_view()),
    url(r'gold/enablesmoke', EnableSmoke.as_view()),
    url(r'gold/record', smokeRecord.as_view()),
    url(r'gold/figure', smokefigure.as_view()),
    url(r'gold/smokelist', getSmoke.as_view()),
    url(r'install/add', AddInstall.as_view()),
    url(r'install/update', UpdateInstall.as_view()),
    url(r'install/del', DelInstall.as_view()),
    url(r'install/disable', DisableInstall.as_view()),
    url(r'install/enable', EnableInstall.as_view()),
    url(r'install/journal', getJournal.as_view()),
    url(r'install/getReport', getInstallReport.as_view()),
    url(r'install/list', getInstall.as_view()),
    url(r'install/version', getInstallVersion.as_view()),
    url(r'todo', todo.as_view()),
]
