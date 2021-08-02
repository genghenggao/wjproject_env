'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-08-01 23:13:46
LastEditors: henggao
LastEditTime: 2021-08-01 23:14:19
'''
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    return render(request, "index.html")