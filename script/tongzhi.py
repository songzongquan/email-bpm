#!/usr/bin/python
# -*- coding: UTF-8 -*-

from common.emailClient import EmailClient

def tongzhi(mailname,password,imaphost,imapport,smtphost,smtpport,toaddrs, subject, content):

    a=EmailClient(mailname,password,imaphost,imapport,smtphost,smtpport)
    a.sendMail(toaddrs, subject,content,'', '')


if __name__ == '__main__':
    tongzhi('lixiaofan@bonc.com.cn', 'Lixiaofan123', 'mail.bonc.com.cn', '993', 'mail.bonc.com.cn', '465','lixiaofan@bonc.com.cn','邮箱注册已经完成','邮箱注册已经完成')
