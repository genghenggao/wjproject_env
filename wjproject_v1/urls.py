'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-05 09:46:12
LastEditors: henggao
LastEditTime: 2021-08-19 23:18:23
'''
"""wjproject_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include, re_path
from django.views.generic import TemplateView
import wjproject_app.urls
import wjproject_users.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(wjproject_app.urls)),
    path('api/', include(wjproject_users.urls)),
    path('', TemplateView.as_view(template_name="index.html")),
]
