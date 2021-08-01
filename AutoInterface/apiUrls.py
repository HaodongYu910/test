from django.conf.urls import url
from rest_framework import routers

from .api.apiGold import *
from .api import ApiDoc, ApiGroup, ApiScene, automationCase as Case

from .api import automationReport as Report
from .api.apiSmoke import *
# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'Interface/group', ApiGroup.Group.as_view()),
    url(r'Interface/add_group', ApiGroup.AddGroup.as_view()),
    url(r'Interface/update_name_group', ApiGroup.UpdateNameGroup.as_view()),
    url(r'Interface/del_group', ApiGroup.DelGroup.as_view()),
    url(r'Interface/api_list', ApiDoc.ApiList.as_view()),
    url(r'Interface/add_api', ApiDoc.AddApi.as_view()),
    url(r'scene/list', Case.CaseList.as_view()),
    url(r'scene/Detail', ApiScene.ApiSceneDetail.as_view()),
    url(r'Interface/updateMock', ApiDoc.UpdateApiMockStatus.as_view()),
    url(r'Interface/lead_swagger', ApiDoc.LeadSwagger.as_view()),
    url(r'Interface/update_api', ApiDoc.UpdateApi.as_view()),
    url(r'Interface/del_api', ApiDoc.DelApi.as_view()),
    url(r'Interface/update_group', ApiDoc.UpdateGroup.as_view()),
    url(r'Interface/api_info', ApiDoc.ApiInfoDetail.as_view()),
    url(r'Interface/add_history', ApiDoc.AddHistory.as_view()),
    url(r'Interface/history_list', ApiDoc.HistoryList.as_view()),
    url(r'Interface/del_history', ApiDoc.DelHistory.as_view()),
    url(r'Interface/operation_history', ApiDoc.OperationHistory.as_view()),
    url(r'Interface/Download', ApiDoc.DownLoad.as_view()),
    url(r'Interface/download_doc', ApiDoc.download_doc),
    url(r'automation/group', Case.Group.as_view()),
    url(r'automation/add_group', Case.AddGroup.as_view()),
    url(r'automation/del_group', Case.DelGroup.as_view()),
    url(r'automation/update_name_group', Case.UpdateNameGroup.as_view()),
    url(r'automation/update_case_group', Case.UpdateGroup.as_view()),
    url(r'automation/case_list', Case.CaseList.as_view()),
    url(r'automation/add_case', Case.AddCase.as_view()),
    url(r'automation/update_case', Case.UpdateCase.as_view()),
    url(r'automation/del_case', Case.DelCase.as_view()),
    url(r'automation/DownloadCase', Case.DownLoadCase.as_view()),
    url(r'automation/api_list', Case.ApiList.as_view()),
    url(r'automation/api_info', Case.CaseApiInfo.as_view()),
    url(r'automation/add_new_api', Case.AddNewApi.as_view()),
    url(r'automation/get_correlation_response', Case.GetCorrelationResponse.as_view()),
    url(r'automation/add_old_api', Case.AddOldApi.as_view()),
    url(r'automation/update_api', Case.UpdateApi.as_view()),
    url(r'automation/del_api', Case.DelApi.as_view()),
    url(r'automation/start_test', Case.StartTest.as_view()),
    url(r'automation/add_time_task', Case.AddTimeTask.as_view()),
    url(r'automation/get_time_task', Case.GetTask.as_view()),
    url(r'automation/del_task', Case.DelTask.as_view()),
    url(r'automation/look_result', Case.LookResult.as_view()),
    url(r'automation/test_report', Case.TestReport.as_view()),
    url(r'report/auto_test_report', Report.AutoTestReport.as_view()),
    url(r'report/test_time', Report.TestTime.as_view()),
    url(r'report/lately_ten', Report.AutoLatelyTenTime.as_view()),
    url(r'gold/addsmoke', AddSmoke.as_view()),
    url(r'gold/updatesmoke', UpdateSmoke.as_view()),
    url(r'gold/delsmoke', DelSmoke.as_view()),
    url(r'gold/disablesmoke', DisableSmoke.as_view()),
    url(r'gold/enablesmoke', EnableSmoke.as_view()),
    url(r'gold/record', smokeRecord.as_view()),
    url(r'gold/figure', smokefigure.as_view()),
    url(r'gold/smokelist', getSmoke.as_view()),
    url(r'gold/GoldReport', getGoldReport.as_view()),
    url(r'smoketest', Smoketest.as_view()),
]
