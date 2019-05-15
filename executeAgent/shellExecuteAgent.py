# coding=utf-8
import os,time
from common.emailClient import *
from common.excelReadWriter import *
from common.config  import *

info = getMainEmailInfo()
print(info)

emailclient = EmailClient('wangyujia@bonc.com.cn','wyj211421.','mail.bonc.com.cn','993','mail.bonc.com.cn','25')

class ShellExecuteAgent():
    '''shell执行代理：收取邮件，得到附件，解析出内容，按内容里的参数，调用对应shell脚本执行，执行完成，更改附件的状态信息，回复邮件到 cloudiip_ops。'''

    def main(self):
        while True:
            getmail = emailclient.getOldestMessage()# 收取邮件
            id = getmail.get('id')
            attachmentlist = emailclient.getAttachements(id)#获取邮件中的所有附件
            for attachment in attachmentlist:
                '''for循环，输出邮件中的所有附件'''
                print(attachment)
                attachmentname = emailclient.getFileNameOfAttachement(attachment)  # 利用获取的附件列表，获取附件名称
                print(attachmentname)
                downloadpath = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"/reversAttachments")
                print(downloadpath)
                emailclient.downloadAttachement(attachmentname,downloadpath)  # 利用获取的附件名称，调用下载附件的函数下载附件到指定路径
                filename=os.path.join(downloadpath+"/"+attachmentname)
                excelparse = ExcelReadWriter(filename)
                if "form_域名反向代理申请" in attachmentname:
                    ip = excelparse.read("内网IP")  # 调用读写附件函数获取脚本所需参数
                    domain = excelparse.read("预申请公网域名")
                    os.system(os.getcwd() + '/script/revers_proxy.sh '+ ip + ' ' + domain)
                    status = "成功"# shell脚本传回来的参数
                    excelparse.write("执行状态", status)
                elif "form_dns解析申请" in attachmentname:
                    # content=   #调用读写附件函数获取脚本所需参数
                    os.system(os.getcwd() + '\script\\dns.sh')

                emailclient.sendMail("wangyujia@bonc.com.cn","wyj211421.","cloudiip_ops@bonc.com.cn","主题","邮件内容",attachmentname,downloadpath)
                emailclient.removeMessage(getmail)  # 删除邮件

                time.sleep(300)

if __name__ == '__main__':
    s=ShellExecuteAgent()
    s.main()