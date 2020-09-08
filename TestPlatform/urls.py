from django.conf.urls import url
from rest_framework import routers
from TestPlatform.api import ApiDoc, automationCase as Case, member, dynamic, user, VisitorRecord

from TestPlatform.api import automationReport as Report
from TestPlatform.api.global_parameter import HostTotal, AddHost, UpdateHost, DelHost, DisableHost, EnableHost
from TestPlatform.api.projectList import *
from TestPlatform.api.projectTitle import ProjectInfo
from TestPlatform.api.Jiradata import *
from TestPlatform.api.Sendmail import *
from TestPlatform.api.basedata import *
from TestPlatform.api.test_report import *
from TestPlatform.api.tool import *
from TestPlatform.api.user_permission import *
# Routers provide an easy way of automatically determining the URL conf.
# 注册
router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'project/project_list', ProjectList.as_view()),
    url(r'project/add_project', AddProject.as_view()),
    url(r'project/update_project', UpdateProject.as_view()),
    url(r'project/del_project', DelProject.as_view()),
    url(r'project/disable_project', DisableProject.as_view()),
    url(r'project/enable_project', EnableProject.as_view()),
    url(r'title/project_info', ProjectInfo.as_view()),
    url(r'global/host_total', HostTotal.as_view()),
    url(r'global/add_host', AddHost.as_view()),
    url(r'global/update_host', UpdateHost.as_view()),
    url(r'global/del_host', DelHost.as_view()),
    url(r'global/disable_host', DisableHost.as_view()),
    url(r'global/enable_host', EnableHost.as_view()),
    url(r'api/group', ApiDoc.Group.as_view()),
    url(r'api/add_group', ApiDoc.AddGroup.as_view()),
    url(r'api/update_name_group', ApiDoc.UpdateNameGroup.as_view()),
    url(r'api/del_group', ApiDoc.DelGroup.as_view()),
    url(r'api/api_list', ApiDoc.ApiList.as_view()),
    url(r'api/add_api', ApiDoc.AddApi.as_view()),
    url(r'api/updateMock', ApiDoc.UpdateApiMockStatus.as_view()),
    url(r'api/lead_swagger', ApiDoc.LeadSwagger.as_view()),
    url(r'api/update_api', ApiDoc.UpdateApi.as_view()),
    url(r'api/del_api', ApiDoc.DelApi.as_view()),
    url(r'api/update_group', ApiDoc.UpdateGroup.as_view()),
    url(r'api/api_info', ApiDoc.ApiInfoDetail.as_view()),
    url(r'api/add_history', ApiDoc.AddHistory.as_view()),
    url(r'api/history_list', ApiDoc.HistoryList.as_view()),
    url(r'api/del_history', ApiDoc.DelHistory.as_view()),
    url(r'api/operation_history', ApiDoc.OperationHistory.as_view()),
    url(r'api/Download', ApiDoc.DownLoad.as_view()),
    url(r'api/download_doc', ApiDoc.download_doc),
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
    url(r'member/project_member', member.ProjectMemberList.as_view()),
    url(r'member/email_config', member.EmailConfig.as_view()),
    url(r'member/del_email', member.DelEmail.as_view()),
    url(r'member/get_email', member.GetEmail.as_view()),
    url(r'dynamic/dynamic', dynamic.Dynamic.as_view()),
    url(r'user/login', user.obtain_auth_token),
    url(r'user/info', userinfo.as_view()),
    url(r'user/VisitorRecord', VisitorRecord.Record.as_view()),
    url(r'addreport',Addreport.as_view()),
    url(r'updatereport',Updatereport.as_view()),
    url(r'delreport',Delreport.as_view()),
    url(r'report',loadReport.as_view()),
    url(r'sendreport',Sendreport.as_view()),
    url(r'risk/add',Add_test_risk.as_view()),
    url(r'risk/update',Updatetest_risk.as_view()),
    url(r'risk/del',DelAutotest_risk.as_view()),
    url(r'risk/disable_risk', DisableRisk.as_view()),
    url(r'risk/enable_riskt', EnableRisk.as_view()),
    url(r'risk',Testrisk.as_view()),
    url(r'jira/list', jiradata.as_view()),
    url(r'jira/figure', jira_figure.as_view()),
    url(r'base/getdata',getBase.as_view()),
    url(r'base/AddData', AddbaseData.as_view()),
    url(r'base/UpdateData', UpdatebaseData.as_view()),
    url(r'send', sendmail.as_view()),
    url(r'download', down_load.as_view()),
    url(r'tool/stressversion', stressversion.as_view()),
    url(r'tool/stresstool', stresstool.as_view()),
    url(r'tool/stressresult', stressResult.as_view()),
    url(r'tool/stressdata', stressData.as_view()),
    url(r'tool/deletepatients', delete_patients.as_view()),
    url(r'tool/durationData', durationData.as_view()),
    url(r'tool/getduration', getDuration.as_view()),
    url(r'tool/add_duration', add_duration.as_view()),
    url(r'tool/update_duration', update_duration.as_view()),
    url(r'tool/del_duration', del_duration.as_view()),
    url(r'tool/duration_verify', duration_verify.as_view()),
    url(r'tool/disable_duration', DisableDuration.as_view()),
    url(r'tool/enable_duration', EnableDuration.as_view()),
    url(r'updatedata', Updatedata.as_view()),
    url(r'todo', todo.as_view()),
]

