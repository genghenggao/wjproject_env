'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-08-22 16:58:46
LastEditors: henggao
LastEditTime: 2021-08-22 16:58:57
'''
#!/usr/bin/python3
import os
import sys
import time
import datetime


def delDir(dir, t=120):
    # 获取文件夹下所有文件和文件夹
    files = os.listdir(dir)
    for file in files:
        filePath = dir + "/" + file
        # 判断是否是文件
        if os.path.isfile(filePath):
            # 最后一次修改的时间
            last = int(os.stat(filePath).st_mtime)
            # 上一次访问的时间
            #last = int(os.stat(filePath).st_atime)
            # 当前时间
            now = int(time.time())
            # 删除过期文件
            if (now - last >= t):
                os.remove(filePath)
                print(filePath + " was removed!")
        elif os.path.isdir(filePath):
            # 如果是文件夹，继续遍历删除
            delDir(filePath, t)
            # 如果是空文件夹，删除空文件夹
            if not os.listdir(filePath):
                os.rmdir(filePath)
                print(filePath + " was removed!")


if __name__ == '__main__':

    # 获取现在时间
    now_time = datetime.datetime.now()
    print(now_time)
    # 获取明天时间
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天3点时间
    next_time = datetime.datetime.strptime(str(
        next_year)+"-"+str(next_month)+"-"+str(next_day)+" 03:00:00", "%Y-%m-%d %H:%M:%S")
    print(next_time)
    # 获取距离明天3点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    print(timer_start_time)
    # 获取路径
    path = 'tem_data'
    # 获取过期时间
    # t = 20
    t = 3600*24
    # 获取定期清理时间
    ts = timer_start_time
    # ts = 20
    while True:
        delDir(path, t)
        time.sleep(ts)