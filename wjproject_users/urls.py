'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 21:07:31
LastEditors: henggao
LastEditTime: 2021-07-30 22:04:32
'''
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView
from wjproject_users import views    # add
from .views import *
urlpatterns = [
    # 登录验证
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    # modify
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('userinfo/', UserInfoView.as_view(),name="userinfo"),
    path('userlogin/', LoginView.as_view(),name='userlogin'),   # 使用自定义的视图进行登录
     path('tasks/userstatistics/', views.userStatistics, name='userstatistics'),
]
