#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json


def emailsave(name,mail,gonghao):
    try:

        path1=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # print(path1)
        path=os.path.join(path1,'data/emailInfo.json')
        # print(path)
        #打开json文件，读取里面的内容
        with open(path, encoding='utf-8') as form_info:
            list = json.load(form_info)
            # print(list)
        #再list的最后一行，添加字典
        dict={}
        dict["姓名"]=name
        dict["邮箱"]=mail
        dict["工号"]=gonghao
        list.append(dict)
        # print(list)
        #将最新的list写入到json文件中
        with open(path,'w',encoding='utf-8') as f:
            f.write(json.dumps(list,ensure_ascii=False))
        result = {}
        result["status"]='success'
        result["message"]='执行成功'
        r = json.dumps(result,ensure_ascii=False)
        print(r)
    except Exception as e:
        result1={}
        result1["status"]='fail'
        result1["message"]=repr(e)
        r = json.dumps(result1,ensure_ascii=False)
        print(r)




if __name__ == '__main__':
    import sys
    name=sys.argv[1]
    mail=sys.argv[2]
    gonghao=sys.argv[3]
    emailsave(name,mail,gonghao)
