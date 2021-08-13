'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-26 20:54:08
LastEditors: henggao
LastEditTime: 2021-08-09 22:21:10
'''
from django.db.models.fields import CharField
from djongo import models

# Create your models here.


# class UserInfoModel(models.Model):
#     username = CharField(verbose_name="用户名", max_length=100)
#     password = CharField(verbose_name="密码", max_length=100)

#     def __str__(self):
#         return self.username

#     class Meta:
#         verbose_name = '用户信息'
#         verbose_name_plural = verbose_name

# from django.db import models
 
class Status(models.TextChoices):
    UNSTARTED = 'u', "Not started yet"
    ONGOING = 'o', "Ongoing"
    FINISHED = 'f', "Finished"


class Task(models.Model):
    name = models.CharField(verbose_name="Task name", max_length=65, unique=True)
    status = models.CharField(verbose_name="Task status", max_length=1, choices=Status.choices)
    
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"

    def __str__(self):
        return self.name


