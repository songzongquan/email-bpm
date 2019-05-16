from common.config  import *
from common.emailClient import *
from common.excelReadWriter import *
from flowControler.flowExecuter import *


import time
#获取邮箱等配置信息
info = getMainEmailInfo()
#print(info)

mailname = info['address']
imap = info['imap']
imapport = info['imap_port']
smtp = info['smtp']
smtpport = info['smtp_port']
password = info['password']
interval = info['interval']

#创建邮件客户端
ec = EmailClient(mailname,password,imap,imapport,smtp,smtpport)
#print(ec)

#每5分钟处理一次
while(True):
    
    time.sleep(5)
    #print("5 second ...")
    #收取最旧的的待处理邮件
    msg = ec.getOldestMessage()
    print(type(msg))
    if msg != None:
        uid = msg['UIDs']
    
        msgtitle = ec.getTitleOfMessage(uid)
        #获取附件并下载
        path = "data"
        attachments = ec.getAttachements(uid)
        filename = attachments[0]['attachementname']
        current_path = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(current_path+"/data/")

        ec.downloadAttachement(uid,filename,path)
    
        #创建相应流程实例，执行流程实例
        executer = FlowExecuter(path+filename)

        executer.start()







