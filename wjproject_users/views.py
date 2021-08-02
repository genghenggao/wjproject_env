'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 20:54:08
LastEditors: henggao
LastEditTime: 2021-07-30 22:27:39
'''
'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 20:54:08
LastEditors: henggao
LastEditTime: 2021-07-27 09:49:56
'''




from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework import status
class MyTokenObtainPairView(TokenObtainPairView):
    """
    自定义得到token username: 账号; password: 密码
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenViewBase):
    """
    自定义刷新token refresh: 刷新token的元素
    """
    serializer_class = TokenRefreshSerializer


# 自定义的登陆视图
class UserInfoView(APIView):
    # permission_classes = [permissions.IsAuthenticated]  # 控制权限

    def get(self, request, *args, **kwargs):
        # 通过request.auth获取用户Token
        print('请求用户Token为：')
        print(request.auth)

        # 通过request.auth.payload可以获取到解析后的payload内容（字典类型）
        print("\n有效荷载信息：")
        print(request.auth.payload)

        return Response("Get information successfully!", status=status.HTTP_200_OK)

    # 手动颁发 token 主要针对用户注册的情况，用户注册完之后直接返回 token。
    # 手动颁发一个 token 并返回。(用户注册同理，即 user 对象为注册后获取的用户)
    # def post(self, request, *args, **kwargs):
    #     refresh = RefreshToken.for_user(request.user)
    #     content = {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token),
    #     }
    #     return Response(content)
    serializer_class = MyTokenObtainPairSerializer   # 使用序列化类
    # post方法对应post请求，登录时post请求在这里处理

    def post(self, request, *args, **kwargs):
        # 使用序列化处理登陆验证及数据响应
        print("这里")
        # print(request.data)
        # serializer = self.get_serializer(data=request.data)
        # try:
        #     serializer.is_valid(raise_exception=True)
        # except Exception:
        #     # raise ValueError(f'验证失败： {e}')
        #     raise serializers.ValidationError({'': '账号没有注册'})

        # return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response('success')


User = get_user_model()


class LoginView(TokenViewBase):

    # permission_classes = [permissions.IsAuthenticated]  # 控制权限
    def get(self, request, *args, **kwargs):
        return Response("Get  successfully!")

    serializer_class = MyTokenObtainPairSerializer   # 使用序列化类
    # post方法对应post请求，登录时post请求在这里处理

    def post(self, request, *args, **kwargs):
        # 使用序列化处理登陆验证及数据响应
        print(request.data)
        username = request.data['username']
        password = request.data['password']
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        try:

            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
            # serializer.is_valid()
        except Exception as e:
            # raise ValueError(f'验证失败： {e}')
            # raise serializers.ValidationError({'': '账号没有注册'})
            response = self.handle_exception(e)
            print(response)
            print("go here now")
            print(User.objects.filter(username=username).count())
            if not User.objects.filter(username=username).count():
                # print('用户不存在')
                response = {"code": 401, 'message': "账户不存在，请重新输入"}
                # raise serializers.ValidationError(
                #     detail={'status': 401,
                #             "msg": "账户不存在，请重新输入"})
            else:
                if not User.objects.filter(password=password).count():
                    # print('用户存在，密码不正确')
                    # 账户存在，校验密码
                    response = {"code": 401, 'message': "密码不正确，请重新输入"}
                    # raise serializers.ValidationError(
                    #     detail={'status': 401,
                    #             "msg": "密码不正确，请重新输入"})
            return Response(response, status=status.HTTP_200_OK)


# 后台用户统计信息
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Task
def userStatistics(request):
     user_count = User.objects.count()
     task_count = Task.objects.count()
 
     context = { 'user_count': user_count, 'task_count': task_count }
     return render(request, 'userstatistics.html',context)