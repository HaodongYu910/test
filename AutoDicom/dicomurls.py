from django.conf.urls import url
from rest_framework import routers

from .api.apiDicom import *
from .api.apiDuration import *
from .api.apiDicombase import *
from .api.apiDurationReport import DurationReport
from .api.apiGroup import *

# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'dicomData', dicomData.as_view()),
    url(r'dicomdetail', dicomDetail.as_view()),
    url(r'detail/Disable', DetailDisable.as_view()),
    url(r'update', dicomUpdate.as_view()),
    url(r'delDDD', deldicomdata.as_view()),
    url(r'dicomcsv', dicomcsv.as_view()),
    url(r'dicomSend', dicomSend.as_view()),
    url(r'delete_patients', deletePatients.as_view()),
    url(r'disabledicom', DisableDicom.as_view()),
    url(r'enabledicom', EnableDicom.as_view()),
    url(r'duration/durationData', durationData.as_view()),
    url(r'duration/add', addDuration.as_view()),
    url(r'duration/up', updateDuration.as_view()),
    url(r'duration/del', delDuration.as_view()),
    url(r'duration/disable_duration', DisableDuration.as_view()),
    url(r'duration/enable_duration', EnableDuration.as_view()),
    url(r'duration/getduration', getDuration.as_view()),
    url(r'duration/source', getdurationsource.as_view()), # 获取持续 源数据
    url(r'dicomurl', dicomUrl.as_view()),
    url(r'tool/anonymization', anonymizationAPI_2nd.as_view()),      # 匿名化数据
    url(r'base/getdata', getBase.as_view()),
    url(r'base/getResult', getResult.as_view()),
    url(r'base/dicom', getDicomfile.as_view()),
    url(r'group/dicomadd', DicomAdd.as_view()),
    url(r'group/groupadd', AddGroup.as_view()),
    url(r'group/groupup', UpdateGroup.as_view()),
    url(r'group/disablegroup', DisableGroup.as_view()),
    url(r'group/enablegroup', EnableGroup.as_view()),
    url(r'group/delgroup', DelGroup.as_view()),
    url(r'group/getgroup', getGroup.as_view()),
    url(r'group/getinfo', GroupInfo.as_view()),
    url(r'group/groupbase', getGroupBase.as_view()),
    url(r'updatedata', Updatedata.as_view()),
    url(r'tool/search_data', ddsDataVerifyAPI.as_view()),
    url(r'report/durationreport', DurationReport.as_view()),
    url(r'verify', getDurationTB.as_view()),
    url(r'tool/get_dicom', get_dicomAPI_2nd.as_view()),
]
