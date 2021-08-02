'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 20:54:08
LastEditors: henggao
LastEditTime: 2021-07-30 21:56:46
'''
from django.contrib import admin

# Register your models here.
admin.site.site_header = '武甲管理后台'  # 设置header
admin.site.site_title = '武甲管理后台'   # 设置title
admin.site.index_title = '武甲管理后台'

from .models import Task
admin.site.register(Task)
