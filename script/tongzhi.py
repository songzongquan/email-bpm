#!/usr/bin/python3
#encoding:utf-8
import os,sys
import json

p = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#print(p)
sys.path.append(p)

#print(sys.path)

from common.emailClient import EmailClient
from common.config import *


def tongzhi(name, subject, content):
    try:
        path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # print(path1)
        path = os.path.join(path1, 'data/emailInfo.json')
        # print(path)
        # 打开json文件，读取里面的内容
        with open(path, encoding='utf-8') as form_info:
            list = json.load(form_info)
            # print(list)
            # 查找姓名在列表中的对应的邮箱
            count = len(list)
            # print(count)
            list1=[]
            for i in range(count):
                if name == list[i]['姓名']:
                    # print(list[i]['邮箱'])
                    list1.append(list[i]['邮箱'])
            # print(list1)
            mail=list1[0]

        info = getMainEmailInfo()
        # print(info)

        mailname = info['address']
        imaphost = info['imap']
        imapport = info['imap_port']
        smtphost = info['smtp']
        smtpport = info['smtp_port']
        password = info['password']

        a=EmailClient(mailname,password,imaphost,imapport,smtphost,smtpport)
        a.sendMail(mail, subject,content,'', '')
        result = {}
        result["status"] = 'success'
        result["message"] = '执行成功'
        r = json.dumps(result,ensure_ascii=False)
        print(r,end="")#去掉print的空行
    except Exception as e:
        result1={}
        result1["status"]='fail'
        result1["message"]=repr(e)
        r = json.dumps(result1,ensure_ascii=False)
        print(r)


if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    subject = sys.argv[2]
    content = sys.argv[3]
    tongzhi(name, subject, content)
    # tongzhi('李晓范','测试一下修改为姓名的情况','发送邮件的内容')
