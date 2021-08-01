from django.conf.urls import url
from rest_framework import routers
#
# from .Interface.apiDicom import *
# from .Interface.apiDuration import *
# from .Interface.apiDicombase import *
# from .Interface.apiDurationReport import DurationReport
# from .Interface.apiGroup import *

# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'dicomData', dicomData.as_view()),
    # url(r'smokeTest', smokeTest.as_view()),
]
