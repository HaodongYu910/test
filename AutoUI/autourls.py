from django.conf.urls import url
from rest_framework import routers

from .api.apiUI import *
from .api.apiUiCase import *
from .api.apiUIRecord import *

# Routers provide an easy way of slicenumberally determining the URL conf.
# 注册

router = routers.DefaultRouter()
# router.register(r'account', AccountViewSet)


# Wire up our API using slicenumber URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'auto/addauto', AddAutoUI.as_view()),
    url(r'auto/updateauto', UpdateAutoUI.as_view()),
    url(r'auto/delauto', DelAutoUI.as_view()),
    url(r'auto/disableauto', DisableAutoUI.as_view()),
    url(r'auto/enableauto', EnableAutoUI.as_view()),
    url(r'auto/record', AutoRecord.as_view()),
    url(r'auto/figure', Autofigure.as_view()),
    url(r'auto/autolist', getAutoUI.as_view()),
    url(r'auto/addcase', AddUICase.as_view()),
    url(r'auto/updatecase', UpdateUICase.as_view()),
    url(r'auto/delcase', DelUICase.as_view()),
    url(r'auto/disablecase', DisableUICase.as_view()),
    url(r'auto/enablecase', EnableUICase.as_view()),
    url(r'auto/case', getUICase.as_view()),
]
