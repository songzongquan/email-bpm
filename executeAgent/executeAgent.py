# coding=utf-8
import os,sys
p = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(p)

import subprocess,time
from common.emailClient import *
from common.excelReadWriter import *
from common.config  import *

class ShellExecuteAgent():
    '''shell执行代理：收取邮件，得到附件，解析出内容，按内容里的参数，调用对应shell脚本执行，执行完成，更改附件的状态信息，回复邮件到 cloudiip_ops。'''
    def main(self):
        info = getAgentEmailInfo()
        mailname = info['address']
        imap = info['imap']
        imapport = info['imap_port']
        smtp = info['smtp']
        smtpport = info['smtp_port']
        password = info['password']
        interval = info['interval']

        #创建邮件客户端
        emailclient = EmailClient(mailname,password,imap,imapport,smtp,smtpport)
        while True:#五分钟循环一次
            getmail = emailclient.getOldestMessage()# 收取邮件
            id = getmail.get('id')# 获取邮件id，为获取附件做准备
            attachmentlist=emailclient.getAttachements(id)# 以列表形式输出邮件中的所有附件
            for attachment in attachmentlist:
                '''for循环，输出邮件中的所有附件'''
                attachmentname = attachment['attachementname']# 从附件列表的字典中获取附件名称
                downloadpath = os.path.join(os.path.abspath(os.path.dirname(__file__))+"/Attachments/")
                # 获取下载附件的路径，最后一定要加上"/"
                emailclient.downloadAttachement(id,attachmentname,downloadpath)# 利用获取的附件名称，调用下载附件函数下载附件到指定路径,不包括附件名称
                filename=os.path.join(downloadpath+attachmentname)# 精确到附件名称的路径
                excelparse = ExcelReadWriter(filename)# 实例化表格解析函数
                command = excelparse.read("script").split(" ")#从附件的sheet2中获取执行什么脚本，需要什么参数

                if "revers_proxy.sh" in command:
                    interpreter1 = ['bash']
                    interpreter1.extend(command)#列表拼接，例['bash','脚本名','参数1’,'参数2',……]
                    executescript1 = " ".join(interpreter1)  # 执行shell脚本需要将上方的列表准换成字符串
                    path = os.path.join(os.path.dirname(__file__),'script')
                    status = subprocess.Popen(executescript1,stdout=subprocess.PIPE,shell=True,cwd=path).communicate() #获取shell脚本传回来的参数。通过subprocess.Popen()方法调用命令后执行的结果，stdout表示程序的标准输出；shell=True表示指定的命令将通过shell执行，cwd表示子进程的工作目录，即脚本所在目录，communicate返回标准输出。
                    status1=str(status[0])
                    status2=status1.split('\\n')
                    excelparse.write("result", status2[1])#将脚本返回来的结果写入附件中
                    excelparse.write("executor", "auto")
                    executetime = time.strftime('%Y.%m.%d', time.localtime(time.time()))
                    # time.time()获得当前时间的时间戳，time.localtime()格式化时间戳为本地的时间，time.strftime()格式化日期
                    excelparse.write("executionTime", executetime)
                    emailclient.sendMail("cloudiip_ops@bonc.com.cn","域名反向代理执行结果","域名反向代理工作已完成",attachmentname,downloadpath)
                    # mailclient.removeMessage(getmail)  # 删除邮件
                elif "host_auth.py" in command:
                    interpreter2 = ['python']
                    interpreter2.extend(command)
                    path = os.path.join(os.path.dirname(__file__),'script')
                    status = subprocess.Popen(interpreter2,stdout=subprocess.PIPE,cwd=path).communicate()
                    status1=str(status[0])
                    status2=status1.split('\\n')
                    excelparse.write("result", status2[1])
                    excelparse.write("executor", "auto")
                    executetime = time.strftime('%Y.%m.%d', time.localtime(time.time()))
                    excelparse.write("executionTime", executetime)
                    emailclient.sendMail("cloudiip_ops@bonc.com.cn","DNS解析执行结果","DNS解析工作已完成",attachmentname,downloadpath)
                    #mailclient.removeMessage(getmail)  # 删除邮件
            print("5 minutes") 
            time.sleep(5)

if __name__ == '__main__':
    s=ShellExecuteAgent()
    s.main()