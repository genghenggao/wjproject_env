'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-06 16:34:50
LastEditors: henggao
LastEditTime: 2021-08-04 10:29:58
'''
from wjproject_v1.settings import BASE_DIR
from django.urls import path
from django.urls.conf import include, re_path
from . import views
from django.views.static import serve
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('test/', TestView.as_view(),
         name='test'),
    # path('testinfo/', views.TestInfo,
    # name="info"),
    path('wjproject/', DataStoreView.as_view(),
         name='wjproject'),  # 上传
    path('wjproject/query/', DataStoreDetailView.as_view(),
         name='query'),  # 查看、修改、删除
    path('wjproject/searchdatainfo/',
         SearchDataInfo.as_view(), name='searchDataInfo'),  # 搜索
    path('wjproject/advancesearch/',
         AdvanceSearch.as_view(), name='advancesearch'),  # 高级检索
    path('wjproject/prequery/', PreDataDetailView.as_view(),
         name='prequery'),  # 查看、修改、删除
    path('wjproject/downloaddata/', DownLoadDataView.as_view(),
         name='downloaddata'),  # 下载
    path('wjproject/batchdownload/', BatchDownLoadDataView.as_view(),
         name='batchdownload'),  # 批量下载
    path('wjproject/batchdownloadpreview/', BatchDownLoadDataPreView.as_view(),
         name='batchdownloadpreview'),  # 批量下载预览
    re_path(r'^wjproject/media/(?P<path>.*)$', serve,
            {'document_root': os.path.join(BASE_DIR, 'media')}), #服务器资源
     path('wjproject/databaseinfo/',DataBaseInfoView.as_view(),name='databaseinfo') # 数据库统计信息
]
