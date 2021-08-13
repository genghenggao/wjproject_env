# coding=utf8


'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-05 09:56:53
LastEditors: henggao
LastEditTime: 2021-08-06 17:30:59
'''
from django.template.defaultfilters import length
import zipstream
import zipfile
import json
from django.utils.encoding import escape_uri_path
import re
from bson.json_util import dumps
import base64
import time
import os
from bson.objectid import ObjectId
from django.shortcuts import render
from mongoengine.queryset.transform import update
from rest_framework import response
from .models import TestModel, DataFormModel
from .serializers import TestSerializer, DataFormSerializers
# Create your views here.
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.http.response import FileResponse, HttpResponse, JsonResponse, StreamingHttpResponse
from rest_framework.response import Response


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        # name = request.GET.get("name")
        # print(name)
        # age = request.GET.get("age")
        # count = TestModel.objects.filter(name="henggao").count()
        user = TestModel.objects.all()
        serializer = TestSerializer(user, many=True)
        print(serializer.data)
        print("get")
        # return JsonResponse(context)
        # return HttpResponse("This is get")
        return Response(serializer.data)

    def post(self, request):
        print("post")
        serializer = TestSerializer(data=request.data)
        # 接收前端表单数据,使用Post.get()方法
        # username = request.POST.get('username')
        # name = request.data["name"]
        # age = request.data["age"]
        # TestModel.objects.create(name=name, age=age)
        # return Response(dict(msg="OK", code=10000))
        return HttpResponse("This is post")
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

# wjproject

# 上传


class DataStoreView(APIView):
    def get(self, request, *args, **kwargs):

        dataform = DataFormModel.objects.all().order_by('_id')  # 一定要排序
        # 创建分页对象
        page = MyPagination()
        # 实例化查询，获取分页的数据
        page_chapter = page.paginate_queryset(
            queryset=dataform, request=request, view=self)
        # 序列化及结果返回，将分页后返回的数据, 进行序列化
        ser = DataFormSerializers(instance=page_chapter, many=True)
        data = {'list': ser.data}
        # print('走了一趟这里')
        # print(data)
        return page.get_paginated_response(data)

    def post(self, request, *args, **kwargs):
        fileio = request.FILES.get("file", None)  # 注意比较

        # print(request.FILES)
        # print(request.POST)  # Django只有request.POST、request.GET
        # print(request.data)   # DRF才有request.data

        # print(request.data)
        # print('=================================================')
        # print(fileio)
        # =====================================================

        # 保存到服务器
        if not os.path.exists('tem_data/'):
            os.mkdir('tem_data/')
        with open("./tem_data/%s" % fileio.name, 'wb+') as f:
            for chunk in fileio.chunks():
                f.write(chunk)
            f.close()

        # 数据写入数据库
        dataForm = request.data
        if ('dataName' in dataForm):
            # 字段信息
            write_data = DataFormModel(
                dataName=dataForm['dataName'],
                dataNumber=dataForm['dataNumber'],
                dataFormat=dataForm['dataFormat'],
                dataCompany=dataForm['dataCompany'],
                dataMaker=dataForm['dataMaker'],
                dataMaker2=dataForm['dataMaker2'],
                dataMaker3=dataForm['dataMaker3'],
                dataDate=dataForm['dataDate'],
                dataScale=dataForm['dataScale'],
                dataCoordinate=dataForm['dataCoordinate'],
                dataAdmin=dataForm['dataAdmin'],
                dataReview=dataForm['dataReview'],
                dataStorageCompany=dataForm['dataStorageCompany'],
                dataStorageLocation=dataForm['dataStorageLocation'],
                dataKeyWord1=dataForm['dataKeyWord1'],
                dataKeyWord2=dataForm['dataKeyWord2'],
                dataKeyWord3=dataForm['dataKeyWord3'],
                dataprojectname=dataForm['dataprojectname'],
                dataLeftX=dataForm['dataLeftX'],
                dataLeftY=dataForm['dataLeftY'],
                dataRightX=dataForm['dataRightX'],
                dataRightY=dataForm['dataRightY'],
                # dataLeftX=float(dataForm['dataLeftX']),
                # dataLeftY=float(dataForm['dataLeftY']),
                # dataRightX=float(dataForm['dataRightX']),
                # dataRightY=float(dataForm['dataRightY']),
                dataIntro=dataForm['dataIntro'],
            )
            aliases_name = dataForm['dataName']  # 别名，文件名

            fileListName = dataForm['fileListName']
            carouselImgName = dataForm['carouselImgName']

            # 数据写入数据库
            with open("./tem_data/%s" % fileListName, 'rb') as fs, open("./tem_data/%s" % carouselImgName, 'rb') as fd:
                # 写入GridFS
                # 1.源件
                write_data.fileList.put(
                    fs, content_type=fileListName.split(".")[1], filename=fileListName, aliases=[aliases_name])
                # 附属图
                write_data.imgList.put(
                    fd, content_type=carouselImgName.split(".")[1], filename=carouselImgName, aliases=[aliases_name])

            write_data.save()
        # =====================================================
        return HttpResponse('success')

# 增、删、改、查


class DataStoreDetailView(APIView):
    def get(self, request, *args, **kwargs):
        # 判断是否含有_id,没有则随机
        if not '_id' in request.GET:
            # if request.GET['_id'] == "no_value":
            # 空_id值
            publish_obj = DataFormModel.objects.first()
        else:
            # 有值
            query_id = request.GET['_id']
            print(query_id)
            publish_obj = DataFormModel.objects.filter(
                id=query_id).first()
        # # 序列化及
        result_serialize = DataFormSerializers(publish_obj)  # 序列化
        datainfo = result_serialize.data

        # 判断是Query还是Edit
        if request.GET['type'] == 'QUERY':
            # print("request.GET['type']")
         # 根据附属图
            #  方式一：以Base64发送，速度慢
            # img_obj = publish_obj.imgList.read()
            # datainfo['img_obj'] = img_obj
            # temp_data = base64.b64encode(img_obj)
            #  方式二：从数据库下载到服务器，读取快
            img_name = publish_obj.imgList.filename
            # 获取附属图名
            datainfo['img_name'] = publish_obj.imgList.filename
            # 数据写入服务器
            download_file = publish_obj.imgList.read()
            with open("./media/%s" % img_name, 'wb') as f:
                f.write(download_file)

        if request.GET['type'] == 'EDIT':
            print(request.GET['type'])

        # 返回json数据
        data = dumps(datainfo)
        return Response(data)
        # return Response('success')

    def put(self, request, *args, **kwargs):
        # print(request.data["_id"])
        edit_id = request.data["_id"]
        update_data = request.data["upatate_data"]
        # print(update_data)
        publish_obj = DataFormModel.objects.filter(
            id=edit_id).first()
        # print(publish_obj)
        # 更新字段
        publish_obj.dataName = update_data['dataName']
        publish_obj.dataNumber = update_data['dataNumber']
        publish_obj.dataFormat = update_data['dataFormat']
        publish_obj.dataCompany = update_data['dataCompany']
        publish_obj.dataMaker = update_data['dataMaker']
        publish_obj.dataMaker2 = update_data['dataMaker2']
        publish_obj.dataMaker3 = update_data['dataMaker3']
        publish_obj.dataDate = update_data['dataDate']
        publish_obj.dataScale = update_data['dataScale']
        publish_obj.dataCoordinate = update_data['dataCoordinate']
        publish_obj.dataAdmin = update_data['dataAdmin']
        publish_obj.dataReview = update_data['dataReview']
        publish_obj.dataStorageCompany = update_data['dataStorageCompany']
        publish_obj.dataStorageLocation = update_data['dataStorageLocation']
        publish_obj.dataKeyWord1 = update_data['dataKeyWord1']
        publish_obj.dataKeyWord2 = update_data['dataKeyWord2']
        publish_obj.dataKeyWord3 = update_data['dataKeyWord3']
        publish_obj.dataprojectname = update_data['dataprojectname']
        publish_obj.dataLeftX = update_data['dataLeftX']
        publish_obj.dataLeftY = update_data['dataLeftY']
        publish_obj.dataRightX = update_data['dataRightX']
        publish_obj.dataRightY = update_data['dataRightY']
        publish_obj.dataIntro = update_data['dataIntro']
        publish_obj.save()
        return Response('success')

    def delete(self, request, *args, **kwargs):
        delete_id = request.data['_id']
        publish_obj = DataFormModel.objects.filter(
            id=delete_id).first()
        publish_obj.delete()

        return Response('success')

# 搜索


class SearchDataInfo(APIView):
    # 单个字段检索
    def get(self, request, *args, **kwargs):
        # print('success')
        search_key = request.GET['search_key']  # 根据字段搜索
        # print(search_key)
        search_obj = DataFormModel.objects(
            dataName=re.compile(search_key, re.IGNORECASE)).order_by('_id')  # 一定要排序

        # 创建分页对象
        page = MyPagination()
        # 实例化查询，获取分页的数据
        page_chapter = page.paginate_queryset(
            queryset=search_obj, request=request, view=self)
        # 序列化及结果返回，将分页后返回的数据, 进行序列化
        ser = DataFormSerializers(instance=page_chapter, many=True)
        data = {'list': ser.data}
        return page.get_paginated_response(data)

# 高级搜索


class AdvanceSearch(APIView):
    # 高级检索，多个字段检索
    def get(self, request, *args, **kwargs):
        # print('success')
        # search_key = request.GET['search_key']  # 根据字段搜索
        print(request.GET)
        print(request.GET['data'])
        query_dic = eval(request.GET['data'])
        # print(type(query_dic))
        # for key in query_dic:
        #     if not query_dic[key] == "" and not query_dic[key].isspace() == True:
        #         print(key + ':' + query_dic[key].strip())
        #         query_value = query_dic[key].strip()
        #     # 多字段检索

        #     search_obj = DataFormModel.objects(
        #             dataName=re.compile(query_value, re.IGNORECASE),
        #             dataNumber=re.compile(query_value, re.IGNORECASE),

        #         ).order_by('_id')  # 一定要排序
        dataName = query_dic['dataName'].strip()
        dataNumber = query_dic['dataNumber'].strip()
        dataFormat = query_dic['dataFormat'].strip()
        dataprojectname = query_dic['dataprojectname'].strip()
        dataCompany = query_dic['dataCompany'].strip()
        dataMaker = query_dic['dataMaker'].strip()
        dataMaker2 = query_dic['dataMaker2'].strip()
        dataMaker3 = query_dic['dataMaker3'].strip()
        dataDate = query_dic['dataDate'].strip()
        dataScale = query_dic['dataScale'].strip()
        dataCoordinate = query_dic['dataCoordinate'].strip()
        dataAdmin = query_dic['dataAdmin'].strip()
        dataReview = query_dic['dataReview'].strip()
        dataStorageCompany = query_dic['dataStorageCompany'].strip()
        dataStorageLocation = query_dic['dataStorageLocation'].strip()
        dataKeyWord1 = query_dic['dataKeyWord1'].strip()
        dataKeyWord2 = query_dic['dataKeyWord2'].strip()
        dataKeyWord3 = query_dic['dataKeyWord3'].strip()
        dataLeftX = query_dic['dataLeftX'].strip()
        dataLeftY = query_dic['dataLeftY'].strip()
        dataRightX = query_dic['dataRightX'].strip()
        dataRightY = query_dic['dataRightY'].strip()
        dataIntro = query_dic['dataIntro'].strip()

        search_obj = DataFormModel.objects(
            dataName=re.compile(dataName, re.IGNORECASE),
            dataNumber=re.compile(dataNumber, re.IGNORECASE),
            dataFormat=re.compile(dataFormat, re.IGNORECASE),
            dataprojectname=re.compile(dataprojectname, re.IGNORECASE),
            dataCompany=re.compile(dataCompany, re.IGNORECASE),
            dataMaker=re.compile(dataMaker, re.IGNORECASE),
            dataMaker2=re.compile(dataMaker2, re.IGNORECASE),
            dataMaker3=re.compile(dataMaker3, re.IGNORECASE),
            dataDate=re.compile(dataDate, re.IGNORECASE),
            dataScale=re.compile(dataScale, re.IGNORECASE),
            dataCoordinate=re.compile(dataCoordinate, re.IGNORECASE),
            dataAdmin=re.compile(dataAdmin, re.IGNORECASE),
            dataReview=re.compile(dataReview, re.IGNORECASE),
            dataStorageCompany=re.compile(dataStorageCompany, re.IGNORECASE),
            dataStorageLocation=re.compile(dataStorageLocation, re.IGNORECASE),
            dataKeyWord1=re.compile(dataKeyWord1, re.IGNORECASE),
            dataKeyWord2=re.compile(dataKeyWord2, re.IGNORECASE),
            dataKeyWord3=re.compile(dataKeyWord3, re.IGNORECASE),
            # dataLeftX=re.compile(float(dataLeftX), re.IGNORECASE),
            # dataLeftY=re.compile(float(dataLeftY), re.IGNORECASE),
            # dataRightX=re.compile(float(dataRightX), re.IGNORECASE),
            # dataRightY=re.compile(float(dataRightY), re.IGNORECASE),
            dataLeftX=re.compile(dataLeftX, re.IGNORECASE),
            dataLeftY=re.compile(dataLeftY, re.IGNORECASE),
            dataRightX=re.compile(dataRightX, re.IGNORECASE),
            dataRightY=re.compile(dataRightY, re.IGNORECASE),
            dataIntro=re.compile(dataIntro, re.IGNORECASE),

        ).order_by('_id')  # 一定要排序

        # print(search_obj)
        # 创建分页对象
        page = MyPagination()
        # 实例化查询，获取分页的数据
        page_chapter = page.paginate_queryset(
            queryset=search_obj, request=request, view=self)
        # 序列化及结果返回，将分页后返回的数据, 进行序列化
        ser = DataFormSerializers(instance=page_chapter, many=True)
        data = {'list': ser.data}
        return page.get_paginated_response(data)
        # return Response('success')

# 上、下一条


class PreDataDetailView(APIView):
    # 前一条、后一条数据
    def get(self, request, *args, **kwargs):
        # 判断是否含有_id,没有则随机
        query_id = request.GET['_id']
        collection = DataFormModel._get_collection()

        # 第一条数据
        frist_obj = collection.find({}).limit(1)
        for first_result in frist_obj:
            first_id = first_result['_id']
        # 最后一条数据
        last_obj = collection.find({}).limit(1).sort([('_id', -1)])
        for last_result in last_obj:
            last_id = last_result['_id']

        if request.GET['type'] == 'PREQUERY':
            # 原生Mongodb操作
            # print(ObjectId(query_id) == first_id)
            if ObjectId(query_id) == first_id:
                # 第一一条数据，返回上一条是最后一条数据
                current_obj = collection.find({}).limit(1).sort([('_id', -1)])
            else:
                current_obj = collection.find(
                    {'_id': {"$lt": ObjectId(query_id)}}).limit(1).sort([('_id', -1)])
        if request.GET['type'] == 'NEXTQUERY':
            if ObjectId(query_id) == last_id:
                # 最后一条数据，返回下一条是第一条数据
                current_obj = collection.find({}).limit(1)
            else:
                current_obj = collection.find(
                    {'_id': {"$gt": ObjectId(query_id)}}).limit(1).sort([('_id', 1)])

        # 获取前后一条数据_id
        for result in current_obj:
            pre_id = result['_id']  # 获取前后一条数据的_id

        publish_obj = DataFormModel.objects.filter(
            id=pre_id).first()
        # # 返回结果
        result_serialize = DataFormSerializers(publish_obj)  # 序列化
        datainfo = result_serialize.data

        # 根据关附属图
        # BASE64模式
        # img_obj = publish_obj.imgList.read()
        # datainfo['img_obj'] = img_obj
        # URL模式
        img_name = publish_obj.imgList.filename
        # 获取附属图名
        datainfo['img_name'] = publish_obj.imgList.filename
        # 数据写入服务器
        download_file = publish_obj.imgList.read()
        with open("./media/%s" % img_name, 'wb') as f:
            f.write(download_file)

        # 返回json数据
        data = dumps(datainfo)
        return Response(data)

# 下载


class DownLoadDataView(APIView):
    # 下载
    def get(self, request, *args, **kwargs):
        # 获取下载文件_id
        download_id = request.GET['download_id']
        # 从数据库拿到数据
        download_obj = DataFormModel.objects(id=download_id).first()
        # filename = download_obj.dataName
        filename = download_obj.fileList.filename
        print(filename)
        download_file = download_obj.fileList.read()

        # 数据写入服务器
        with open("./tem_data/%s" % filename, 'wb') as f:
            f.write(download_file)
        print('save success')
        # 拿到数据,返回前端
        readfile = open("./tem_data/%s" % filename, "rb")
        # res = FileResponse(readfile)
        # res["Content-Type"] = "application/octet-stream"  # 注意格式
        # # res["Content-Disposition"] = 'filename="{}"'.format(filename)
        # # res["Content-Disposition"] = 'attachment;filename="{}"'.format(filename)
        # res["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(
        #     escape_uri_path(filename))
        # # res['Content-Disposition'] = 'attachment; filename=' + \
        # #     filename.encode('utf-8').decode('ISO-8859-1')
        # return res
        # response = FileResponse(readfile)
        response = FileResponse(readfile)
        response['Content-Type'] = 'application/octet-stream'  # 让浏览器知道这是一个下载文件
        readfilesize = r"./tem_data/%s" % filename
        # print(os.stat(readfilesize).st_size)
        # 返回文件大小
        response['content-length'] = os.stat(readfilesize).st_size
        # response.block_size(os.stat(readfilesize).st_size)
        # 解决文件下载中文命名出现乱码的情况
        response["Content-Disposition"] = "attachment; filename={0}".format(
            escape_uri_path(filename))
        return response

# 压缩文件


class ZipUtilities:
    zip_file = None

    def __init__(self):
        self.zip_file = zipstream.ZipFile(
            mode='w', compression=zipstream.ZIP_DEFLATED)

    def toZip(self, file, name):
        if os.path.isfile(file):
            self.zip_file.write(file, arcname=os.path.basename(file))
        else:
            self.addFolderToZip(file, name)

    def addFolderToZip(self, folder, name):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                self.zip_file.write(full_path, arcname=os.path.join(
                    name, os.path.basename(full_path)))
            elif os.path.isdir(full_path):
                self.addFolderToZip(full_path, os.path.join(
                    name, os.path.basename(full_path)))

    def close(self):
        if self.zip_file:
            self.zip_file.close()

# 批量下载


class BatchDownLoadDataView(APIView):
    # 批量下载
    def get(self, request, *args, **kwargs):
        #   获取_id数组
        id_arr = request.GET.getlist('datainfo[]')
        # 压缩文件
        utilities = ZipUtilities()
        # 遍历
        # start = time.time()
        fileallsize = 0
        for download_id in id_arr:

            download_obj = DataFormModel.objects(id=download_id).first()
            filename = download_obj.fileList.filename
            download_file = download_obj.fileList.read()
            # 数据写入服务器
            with open("./tem_data/%s" % filename, 'wb') as f:
                f.write(download_file)
            # print(download_id)
            tmp_dl_path = os.path.join("./tem_data", filename)
            # print(tmp_dl_path)
            utilities.toZip(tmp_dl_path, filename)
            # 获取文件大小
            readfilesize = r"./tem_data/%s" % filename
            fileallsize += os.stat(readfilesize).st_size

        response = StreamingHttpResponse(
            utilities.zip_file, content_type='application/zip',)
        response['Content-Disposition'] = 'attachment;filename={0}'.format(
            escape_uri_path("批量下载压缩包.zip"))
        # response['Content-Length'] = str(fileallsize)
        # end = time.time()
        # print('Running time: %s Seconds' % (end-start))
        # print(response.streaming_content)
        # print(utilities.zip_file.paths_to_write)
        return response
        # return Response("success")


# 批量下载信息预览
class BatchDownLoadDataPreView(APIView):
    # 批量下载
    def get(self, request, *args, **kwargs):
        #   获取_id数组
        id_arr = request.GET.getlist('datainfo[]')
        file_len = 0
        file_num = len(id_arr)
        for download_id in id_arr:

            download_obj = DataFormModel.objects(id=download_id).first()
            file_len += download_obj.fileList.length
        data = {
            'file_len': file_len,
            'file_num': file_num
        }
        return Response(data)


# 统计数据库信息
class DataBaseInfoView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取到集合
        collection = DataFormModel._get_collection()
        # print(collection)
        # 获取当前数据库
        mydb = DataFormModel._get_db()
        # 1.获取数据库信息
        # print(mydb.command("dbstats"))
        dbinfo = mydb.command("dbstats")
        # 当前mongodb所在的硬盘已经使用的空间大小
        fsUsedSize = round((dbinfo['fsUsedSize'] / 1024 / 1024), 2)
        # 当前mongodb所在的硬盘总共的空间大小
        fsTotalSize = round((dbinfo['fsTotalSize'] / 1024 / 1024), 2)
        # 当前数据库的数据大小
        dataSize = round((dbinfo['dataSize'] / 1024 / 1024), 2)
        data_percent = round((fsUsedSize / fsTotalSize), 2)

        # 数据总览头部数据信息
        datatop = {
            "fsUsedSize": fsUsedSize,
            "fsTotalSize": fsTotalSize,
            "dataSize": dataSize,
            'data_percent': data_percent
        }
        # print(datatop)
        # 获取集合信息
        # print(mydb.command("collstats","dataform") )

        # 2.查询项目文件.这里查询上传单位
        # test = DataFormModel.objects.sum('dataStorageCompany')
        # pipeline = [
        #     {"$sort": {"dataStorageCompany": -1}},
        #     {"$project": {"_id": 0, "name": "$dataStorageCompany",}}
        # ]
        # data = DataFormModel.objects().aggregate(pipeline)
        # print(data)
        # for i in data:
        #     print(i)
        # 返回的是一个字典，key是字段名，value是该字段出现的次数。
        datanum_tmp = DataFormModel.objects().item_frequencies('dataprojectname')
        # datanum = DataFormModel.objects().item_frequencies('dataName')
        # print(datanum_tmp)
        # print(type(datanum_tmp))
        datanum = []
        cnt = 0  # mongodb数据返回已经排序好了，获取前10个
        for data_key, data_value in datanum_tmp.items():
            cnt += 1
            if cnt > 10:
                break
            # print(data_key, data_value)
            tmp_dic = {
                'name': data_key,
                'value': data_value
            }
            datanum.append(tmp_dic)

        # 数据太多，可以考虑取前十个
        # print(len(datanum))

        # 3.最后10条数据
        dataupload = []
        current_obj = collection.find({}).limit(10).sort([('_id', -1)])
        for result in current_obj:
            query_id = result['_id']  # 获取数据的_id
            data_name = result['dataName']  # 获项目名称
            data_admin = result['dataAdmin']  # 上传人员
            data_projectname = result['dataprojectname']  # 上传人员
            # print(result)
            # print(query_id)
            # print(data_name)
            # print(data_admin)
            publish_obj = DataFormModel.objects.filter(
                id=query_id).first()

            # 获取文件信息
            file_lenght = round((publish_obj.fileList.length / 1024 / 1024), 2)
            # print(file_lenght)
            file_date = publish_obj.fileList.upload_date

            # print(file_date)
            datauploadinfo = {
                'file_date': file_date,
                'data_admin': data_admin,
                'data_name': data_name,
                'file_lenght': file_lenght,
                'data_projectname': data_projectname
            }
            dataupload.append(datauploadinfo)
        # print(dataupload)
        # # 返回结果
        # result_serialize = DataFormSerializers(publish_obj)  # 序列化
        # datainfo = result_serialize.data

        # 4.查询文件分布信息
        # 数据分类
        dataNameList = ["图", '报告', '表', "柱状图", '剖面图', '平面图']
        # 数据统计信息
        dataview = []
        # 数据总量
        fileallsize = 0
        for dataName in dataNameList:
            search_obj = DataFormModel.objects(
                dataName=re.compile(dataName, re.IGNORECASE),).order_by('_id')  # 一定要排序

            # 统计数目
            # print(len(search_obj))
            # filenum = len(search_obj)
            # print(search_obj.count())
            filenum = search_obj.count()  # 官方说这比len(search_obj)快

            # 统计数据量
            filesize = 0
            if filenum != 0:
                for obj in search_obj:
                    # print(obj.fileList.length)
                    filesize += obj.fileList.length
            # 类别数据统计
            filesize = round((filesize / 1024 / 1024), 2)   # B --> KB --> MB
            # 整个数据统计
            fileallsize += filesize
            # 序列化及结果返回
            # ser = DataFormSerializers(instance=search_obj, many=True)
            # print(ser.data)
            # 统计数目
            # print(len(ser.data))
            # print(dataName + ":" + search_obj.count())
            datainfo = {
                'datatype': dataName,
                'filesize': filesize,
                "filenum": filenum,
            }

            dataview.append(datainfo)
        # print(dataview)
        # print(fileallsize)

        # # 5. # 数据分类
        # dataImgList = ["柱状图", '剖面图', '平面图']
        # # 图数据统计
        # dataimgview = []
        # for dataImg in dataImgList:
        #     search_obj = DataFormModel.objects(
        #         dataName=re.compile(dataImg, re.IGNORECASE),).order_by('_id')

        #     # 统计数目
        #     # print(len(search_obj))
        #     # imgnum = len(search_obj)
        #     imgnum = search_obj.count()  # 官方说这比len(search_obj)快

        #     # 统计数据量
        #     imgsize = 0
        #     if imgnum != 0:
        #         for obj in search_obj:
        #             # print(obj.fileList.length)
        #             imgsize += obj.fileList.length
        #     # 类别数据统计
        #     imgsize = imgsize / 1024 / 1024   # B --> KB --> MB

        #     dataimginfo = {
        #         'datatype': dataImg,
        #         'imgsize': imgsize,
        #         "imgnum": imgnum,
        #     }
        #     dataimgview.append(dataimginfo)
        # # print(dataimgview)

        # 统计信息
        res_data = {
            'datatop': datatop,
            'datanum': datanum,
            'dataupload': dataupload,
            'dataview': dataview,
        }

        # print(res_data)

        return Response(res_data)
