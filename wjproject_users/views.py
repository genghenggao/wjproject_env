'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 20:54:08
LastEditors: henggao
LastEditTime: 2021-08-12 23:33:52
'''
'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 20:54:08
LastEditors: henggao
LastEditTime: 2021-07-27 09:49:56
'''




from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UsersSerializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import render
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Task
from django.contrib.auth.models import User, Permission, Group
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


# 自定义的登陆视图Token
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

# 登录


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
            # print(response)
            # print("go here now")
            # print(User.objects.filter(username=username).count())
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


def userStatistics(request):
    user_count = User.objects.count()
    task_count = Task.objects.count()

    context = {'user_count': user_count, 'task_count': task_count}
    return render(request, 'userstatistics.html', context)


# 修改密码


class ChangePasswordView(APIView):
    def get(self, request, *args, **kwargs):
        print(request)

        return Response("resposnse success")

    def post(self, request, *args, **kwargs):
        print(request.data)
        username = request.data['username']
        oldPassword = request.data['oldPassword']
        password = request.data['password']
        # 用户登录验证
        query_result = User.objects.filter(Q(username=username))
        # print(query_result)
        # 查询时密码是加密后，校验正确返回用户名，错误返回None
        user_return = auth.authenticate(
            username=query_result[0].username, password=oldPassword)

        # print(user_return)
        res = {}
        if user_return:
            # print("校验正确")
            # print(password)

            # 以后考虑可以后端密码校验
            # if user_return.is_active:
            #     print("验证合法")
            #     user_return.set_password(password)
            #     user_return.save()
            #     res['retCode'] = 1
            # else:
            #     res['retCode'] = 0
            # 设置密码
            user_return.set_password(password)
            user_return.save()
            res = {
                'retCode': 1,
                'retMsg': u"成功 | Success"
            }
        else:
            # print("原密码不正确")
            # 返回错误信息
            res = {
                'retCode': 0,
                'retMsg': u"失败 | fail"
            }

        return Response(res)


# 创建分页


class MyPagination(PageNumberPagination):
    page_size = 10  # 每页显示数据的数量

    max_page_size = 100   # 每页最多可以显示的数据数量

    page_query_param = 'currentPage'  # 获取页码时用的参数,当前页码

    page_size_query_param = 'pageSize'  # 调整每页显示数量的参数名，每页数据大小

    # 指定返回格式，根据需求返回一个总页数，数据存在results字典里返回

    def get_paginated_response(self, data):
        """重写get_paginated_response方法"""

        tpl = {
            'count': self.page.paginator.count,  # 总条数
            'links': {
                'next': self.get_next_link(),  # 下一页
                'previous': self.get_previous_link()  # 上一页
            }
        }
        tpl.update(data)  # 重新定义模板
        res = {
            'data': tpl,
            'retCode': 0,
            'retMsg': u"成功 | Success"
        }
        # 通过渲染器进行返回
        return Response(res)


# 用户信息,权限信息
class UserPermissonView(APIView):
    # 查询权限
    def get(self, request, *args, **kwargs):
        # print(request.GET['username'])
        # 查询所有用户
        query_users = User.objects.all().order_by('id')  # 一定要排序
        print(query_users)
        # 创建分页对象
        page = MyPagination()
        # # 实例化查询，获取分页的数据
        page_chapter = page.paginate_queryset(
            queryset=query_users, request=request, view=self)
        print(page_chapter)
        # 序列化及结果返回，将分页后返回的数据, 进行序列化
        ser = UsersSerializers(instance=page_chapter, many=True)
        data = {'list': ser.data}
        # print(data)

        return page.get_paginated_response(data)

    # 修改权限
    def put(self, request, *args, **kwargs):
        # print(request.data)

        #   获取前端用户名和权限类型
        username = request.data['username']
        admintype = request.data['type']
        # 获取用户
        user = User.objects.get(username=username)
        # user = User.objects.get(username='genghenggao')
        if len(admintype) == 0:
            print("空")
            user.is_staff = False
            user.is_superuser = False
            user.save()
        elif "管理员" in admintype:
            print("高级用户 + 管理员")
            user.is_staff = True
            user.is_superuser = True
            user.save()
        elif "高级用户" in admintype:
            print("高级用户")
            user.is_staff = True
            user.is_superuser = False
            user.save()

        # add_task = Permission.objects.get(codename='add_task')
        # print(add_task)
        # # 查看实例对象所有权限若无任何返回值是空集合set
        # # user.get_all_permissions()
        # print(user.get_all_permissions())
        # # 添加权限,将user的权限设置为当前权限值，之前权限的会自动去掉
        # user.user_permissions.set([add_task])
        # # 查看是否有权限
        # has_permission = user.has_perm('wjproject_users.add_task')
        # print(has_permission)  # True

        # # 通过User对象来查询某个用户有哪些权限
        # per = user.user_permissions.values()
        # print(per)

        # # 创建用户组
        # group_book = Group.objects.get(username='genghenggao')
        # # 添加用户组全权限
        # group_book.permissions.set([add_book])
        # # group_book.permissions.set([add_book,change_book])
        # # 查看哪些用户具有此权限
        # users = User.objects.filter(Q(groups__permissions=add_task) | Q(
        #     user_permissions=add_task)).distinct()
        # print(users)

        return Response("resposnse success")

    # 删除权限

    def delete(self, request, *args, **kwargs):
        print(request.data['username'])

        username = request.data['username']

        deleteResult = User.objects.filter(username=username).delete()
        print(deleteResult)
        return Response("resposnse success")

    # 添加用户

    def post(self, request, *args, **kwargs):
        print("POST方法")
        print(request)
        print(request.data)
        print(request.data['username'])
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        admintype = request.data['type']
        # user = User.objects.create_user('esperyong', 'esperyong@gmail.com', '123456')
        user = User.objects.create_user(username, email, password)
        if len(admintype) == 0:
            print("空")
            user.is_staff = False
            user.is_superuser = False
            user.save()
        elif "管理员" in admintype:
            print("高级用户 + 管理员")
            user.is_staff = True
            user.is_superuser = True
            user.save()
        elif "高级用户" in admintype:
            print("高级用户")
            user.is_staff = True
            user.is_superuser = False
            user.save()
        return Response("resposnse success")


class SearchUserView(APIView):
    # 用户名
    def get(self, request, *args, **kwargs):
        # username = request.GET  # 根据字段搜索
        # print(request)
        # print(request.GET['username'] )
        username = request.GET['username']  # 根据字段搜索
        print(username)

        # 获取用户
        user = User.objects.get(username=username)
        # print(user.username)
        # print(user.email)
        data = [{
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }]

        data = {'list': data}
        print(data)

        # return Response("resposnse success")
        return Response(data)

# 判断用户是否存在


class CheckUserView(APIView):
    # 用户名
    def get(self, request, *args, **kwargs):
        # username = request.GET  # 根据字段搜索
        # print(request)
        # print(request.GET['username'] )
        username = request.GET['username']  # 根据字段搜索
        print(username)

        # 获取用户
        count = User.objects.filter(username=username).count()
        data = {
            "count": count,
            # "password": password,
        }
        print(data)

        # return Response("resposnse success")
        return Response(data)
