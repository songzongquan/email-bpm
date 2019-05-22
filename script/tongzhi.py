#!/usr/bin/python3
#encoding:utf-8
import os,sys

p = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print(p)
sys.path.append(p)

print(sys.path)
from common.emailClient import EmailClient
from common.config import *


def tongzhi(toaddrs, subject, content):
    try:
        info = getMainEmailInfo()
        # print(info)

        mailname = info['address']
        imaphost = info['imap']
        imapport = info['imap_port']
        smtphost = info['smtp']
        smtpport = info['smtp_port']
        password = info['password']

        a=EmailClient(mailname,password,imaphost,imapport,smtphost,smtpport)
        a.sendMail(toaddrs, subject,content,'', '')
        result = {}
        result["status"] = 'success'
        result["message"] = '执行成功'
        print(result)
    except Exception as e:
        result1={}
        result1["status"]='fail'
        result1["message"]=repr(e)
        print(result1)


if __name__ == '__main__':
    import sys
    toaddrs = sys.argv[1]
    subject = sys.argv[2]
    content = sys.argv[3]
    tongzhi(toaddrs, subject, content)
