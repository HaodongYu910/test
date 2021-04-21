from django.conf.urls import url
from rest_framework import routers

from .api.apiStress import *
from .api.apiResult import *
from .api.apiData import *
from .api.apiReport import *

# Routers provide an easy way of ally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using  URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'version', stressVersion.as_view()),
    url(r'run', stressRun.as_view()),
    url(r'stop', stressStop.as_view()),
    url(r'Detail', stressDetail.as_view()),
    url(r'figure', reportfigure.as_view()),
    url(r'save', stressResultsave.as_view()),
    url(r'list/add', addStress.as_view()),
    url(r'list/update', updateStress.as_view()),
    url(r'list/del', delStress.as_view()),
    url(r'list/disable', DisableStress.as_view()),
    url(r'list/enable', EnableStress.as_view()),
    url(r'list', stressList.as_view()),
    url(r'data/StressDataAdd', AddStressData.as_view()),
    url(r'data/StressDataDel', DelStressData.as_view()),
    url(r'data/SynchroStressData', SynchroStressData.as_view()),
    url(r'data/disablebenchmarkstatus', DisableBenchmarkStatus.as_view()),
    url(r'data/enablebenchmarkstatus', EnableBenchmarkStatus.as_view()),
    url(r'data/Data', stressData.as_view()),
    url(r'stressmodel', StressModel.as_view()),
    url(r'Report', stressReport.as_view()),
    url(r'Analysis', SaveAnalysis.as_view()),

]
