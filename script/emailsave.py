#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json

def emailsave(name,mail):
    path=os.path.abspath(os.path.join(os.getcwd(), ".."))+'\\data\\emailInfo.json'
    # print(path)
    #打开json文件，读取里面的内容
    with open(path, encoding='utf-8') as form_info:
        list = json.load(form_info)
        # print(list)
    #再list的最后一行，添加字典
    dict={}
    dict["姓名"]=name
    dict["邮箱"]=mail
    list.append(dict)
    # print(list)
    #将最新的list写入到json文件中
    with open(path,'w',encoding='utf-8') as f:
        f.write(json.dumps(list,ensure_ascii=False))




if __name__ == '__main__':
    emailsave("商华蓝","shanghualan@bonc.com.cn")
