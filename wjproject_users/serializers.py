'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 21:13:19
LastEditors: henggao
LastEditTime: 2021-08-12 09:43:21
'''
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# 1、如果自定义了用户表，那么就要使用这个方法来获取用户模型
# 2、没有自定义的话可以使用以下方式加载用户模型:
# from django.contrib.auth.models import User
# 3、不过这种是万能的
User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        """
        此方法往token的有效负载 payload 里面添加数据
        例如自定义了用户表结构，可以在这里面添加用户邮箱，头像图片地址，性别，年龄等可以公开的信息
        这部分放在token里面是可以被解析的，所以不要放比较私密的信息

        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        # 添加个人信息
        token['name'] = user.username
        return token

    def validate(self, attrs):
        # data是个字典
        # 其结构为：{'refresh': '用于刷新token的令牌', 'access': '用于身份验证的Token值'}
        data = super().validate(attrs)
        # print(data)
        # 获取Token对象
        refresh = self.get_token(self.user)
        # 令牌到期时间
        data['expire'] = refresh.access_token.payload['exp']  # 有效期
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # 用户名
        data['username'] = self.user.username  # 自定义返回
        data['user_id'] = self.user.id  # 自定义返回
        data['is_staff'] = self.user.is_staff  # 权限
        data['is_superuser'] = self.user.is_superuser  # 超级权限
        data['code'] = 200  # 自定义状态码，前端判断
        return data

# 序列化用户


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('username', 'email', 'date_joined', 'is_staff',
                  'is_superuser')  # 只序列化指定的字段
