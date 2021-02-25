"""Autotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from TestPlatform import urls
from AutoUI import autourls
from TestPlatform.api.ApiDoc import MockRequest


schema_view = get_schema_view(title='测试平台 API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer]
                              , permission_classes=())
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', schema_view, name="docs"),
    path('admin/', admin.site.urls), #back login
    url(r'^$', TemplateView.as_view(template_name="index.html")), #home api
    url(r'^api/', include(urls)),
    url(r'^ui/', include(autourls)),
    path('mock/<path:test_tool_platformAdr>', MockRequest.as_view()),   #fake backend return   mock js
]


# hou mian shi sha jiu diao na ge
