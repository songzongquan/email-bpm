#!/usr/bin/python3
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
            #用倒叙倒序循环遍历的方法删除重复的工号对应的dict信息
            count=len(list)
            # print(count)
            for i in range(count-1, -1, -1):
                if '工号'in list[i].keys():
                    if gonghao==list[i]['工号']:
                        # print(list[i]['工号'])
                        list.pop(i)
                        # print(list)


        dict = {}
        dict["姓名"] = name
        dict["邮箱"] = mail
        dict["工号"] = gonghao
        list.append(dict)
            # print(list)
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
    # emailsave("李晓范", 'lixiaofan@bonc.com.cn', '0112203')
    # emailsave("宋宗权", 'songzongquan@bonc.com.cn', '010114')