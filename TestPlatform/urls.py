from django.conf.urls import url
from rest_framework import routers

from .api import ApiDoc, automationCase as Case, member, dynamic, user, VisitorRecord
from .api import automationReport as Report
from .api.DDSapi import *
from .api.projectList import *
from .api.global_parameter import *
from .api.projectTitle import ProjectInfo
from .api.Jiradata import *
from .api.Sendmail import *
from .api.basedata import *
from .api.test_report import *
from .api.apiDuration import *
from .api.apiStress import *
from .api.user_permission import *
from .api.apiDicom import *
from .api.apiSmoke import *
from .api.apiDictionary import *
from .api.apiUpload import *
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
    url(r'global/host_total', HostTotal.as_view()),
    url(r'global/add_host', AddHost.as_view()),
    url(r'global/update_host', UpdateHost.as_view()),
    url(r'global/del_host', DelHost.as_view()),
    url(r'global/disable_host', DisableHost.as_view()),
    url(r'global/enable_host', EnableHost.as_view()),
    url(r'global/disable_protocol', DisableProtocol.as_view()),
    url(r'global/enable_protocol', EnableProtocol.as_view()),
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
    url(r'base/getdata', getBase.as_view()),
    url(r'base/addData', AddbaseData.as_view()),
    url(r'base/updateData', UpdatebaseData.as_view()),
    url(r'base/disablebase', Disablebase.as_view()),
    url(r'base/enablebase', Enablebase.as_view()),
    url(r'base/delbasedata', Delbasedata.as_view()),
    url(r'base/dicom', getDicomfile.as_view()),
    url(r'send', sendmail.as_view()),
    url(r'addupload', AddUpload.as_view()),# 文件上传
    url(r'delupload', DelUpload.as_view()),# 文件上传
    url(r'stress/version', stressversion.as_view()),
    url(r'stress/tool', stressRun.as_view()),
    url(r'stress/Detail', stressDetail.as_view()),
    url(r'stress/result', stressResult.as_view()),
    url(r'stress/figure', reportfigure.as_view()),
    url(r'stress/save', stressResultsave.as_view()),
    url(r'stress/list', stressList.as_view()),
    url(r'stress/add', addStress.as_view()),
    url(r'stress/update', updateStress.as_view()),
    url(r'stress/del', delStress.as_view()),
    url(r'stress/disable', DisableStress.as_view()),
    url(r'stress/enable', EnableStress.as_view()),
    url(r'stress/StressDataAdd', AddStressData.as_view()),
    url(r'stress/StressDataDel', DelStressData.as_view()),
    url(r'stress/SynchroStressData',SynchroStressData.as_view()),
    url(r'stress/disableData', DisableData.as_view()),
    url(r'stress/enableData', EnableData.as_view()),
    url(r'stress/disablebenchmarkstatus', DisableBenchmarkStatus.as_view()),
    url(r'stress/enablebenchmarkstatus', EnableBenchmarkStatus.as_view()),
    url(r'stress/Data', stressData.as_view()),
    url(r'dicom/dicomData', dicomData.as_view()),
    url(r'dicom/dicomdetail', dicomDetail.as_view()),
    url(r'dicom/add_dicomData', adddicomdata.as_view()),
    url(r'dicom/update', dicomUpdate.as_view()),
    url(r'dicom/del_dicomData', deldicomdata.as_view()),
    url(r'dicom/dicomcsv', dicomcsv.as_view()),
    url(r'dicom/dicomSend', dicomSend.as_view()),
    url(r'dicom/delreport', deldicomResult.as_view()),
    url(r'dicom/delete_patients', delete_patients.as_view()),
    url(r'duration/durationData', durationData.as_view()),
    url(r'duration/getduration', getDuration.as_view()),
    url(r'duration/add_duration', add_duration.as_view()),
    url(r'duration/update_duration', update_duration.as_view()),
    url(r'duration/del_duration', del_duration.as_view()),
    url(r'duration/duration_verify', duration_verify.as_view()),
    url(r'duration/disable_duration', DisableDuration.as_view()),
    url(r'duration/enable_duration', EnableDuration.as_view()),
    url(r'dictionary/list', Dictionary.as_view()),
    url(r'dictionary/add', AddDictionary.as_view()),
    url(r'dictionary/update', UpdateDictionary.as_view()),
    url(r'dictionary/del', DelDictionary.as_view()),
    url(r'dictionary/disable', DisableDictionary.as_view()),
    url(r'dictionary/enable', EnableDictionary.as_view()),
    url(r'smoke/addsmoke', AddSmoke.as_view()),
    url(r'smoke/updatesmoke', UpdateSmoke.as_view()),
    url(r'smoke/delsmoke', DelSmoke.as_view()),
    url(r'smoke/disablesmoke', DisableSmoke.as_view()),
    url(r'smoke/enablesmoke', EnableSmoke.as_view()),
    url(r'smoke/record', smokeRecord.as_view()),
    url(r'smoke/test', smokeTest.as_view()),
    url(r'smoke/figure', smokefigure.as_view()),
    url(r'smoke/smokelist', getSmoke.as_view()),
    url(r'updatedata', Updatedata.as_view()),
    url(r'todo', todo.as_view()),
    url(r'dicomurl',dicomUrl.as_view()),
    url(r'tool/anonymization', anonymizationAPI_2nd.as_view()),      # 匿名化数据
    # url(r'tool/sync_dds_data', sync_dds_data.as_view())
]
