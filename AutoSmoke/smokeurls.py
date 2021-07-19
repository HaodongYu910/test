from django.conf.urls import url
from rest_framework import routers
#
# from .api.apiDicom import *
# from .api.apiDuration import *
# from .api.apiDicombase import *
# from .api.apiDurationReport import DurationReport
# from .api.apiGroup import *

# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'dicomData', dicomData.as_view()),
    url(r'smokeTest', smokeTest.as_view()),
]
