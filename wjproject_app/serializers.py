'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-06 16:34:40
LastEditors: henggao
LastEditTime: 2021-07-26 20:56:02
'''
from .models import TestModel, DataFormModel
from rest_framework_mongoengine.serializers import DocumentSerializer


class TestSerializer(DocumentSerializer):
    class Meta:
        model = TestModel
        fields = "__all__"


class DataFormSerializers(DocumentSerializer):
    class Meta:
        model = DataFormModel
        fields = "__all__"
