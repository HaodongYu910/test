from django.conf.urls import url
from rest_framework import routers

from .api import ApiDoc, automationCase as Case, member, dynamic
from .api import automationReport as Report
from .api.projectList import *
from .api.projectTitle import ProjectInfo
from .api.Sendmail import *

# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'project/project_list', ProjectList.as_view()),
    url(r'project/add_project', AddProject.as_view()),
    url(r'project/update_project', UpdateProject.as_view()),
    url(r'project/del_project', DelProject.as_view()),
    url(r'project/disable_project', DisableProject.as_view()),
    url(r'project/enable_project', EnableProject.as_view()),
    url(r'title/project_info', ProjectInfo.as_view()),
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
<<<<<<< HEAD:AutoInterface/apiurls.py
    url(r'dynamic/dynamic', dynamic.Dynamic.as_view())
=======
    url(r'dynamic/dynamic', dynamic.Dynamic.as_view()),
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
    url(r'risk/del', DelAutotest_risk.as_view()),
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
    url(r'install/getReport', getInstallReport.as_view()),
    url(r'install/list', getInstall.as_view()),
    url(r'install/version', getInstallVersion.as_view()),
    url(r'todo', todo.as_view()),
>>>>>>> 18f7c255eabf9cf10e0ea800287f437aaa127dec:TestPlatform/urls.py
]
