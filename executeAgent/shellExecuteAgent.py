# coding=utf-8
import subprocess,time
from common.emailClient import *
from common.excelReadWriter import *
from common.config  import *

emailclient = EmailClient('lixiaofan@bonc.com.cn','Lixiaofan123','mail.bonc.com.cn','993','mail.bonc.com.cn','25')
class ShellExecuteAgent():
    '''shell执行代理：收取邮件，得到附件，解析出内容，按内容里的参数，调用对应shell脚本执行，执行完成，更改附件的状态信息，回复邮件到 cloudiip_ops。'''
    def main(self):
        while True:#五分钟循环一次
            getmail = emailclient.getOldestMessage()# 收取邮件
            id = getmail.get('id')# 获取邮件id，为获取附件做准备
            attachmentlist=emailclient.getAttachements(id)# 以列表形式输出邮件中的所有附件
            for attachment in attachmentlist:
                '''for循环，输出邮件中的所有附件'''
                attachmentname = attachment['attachementname']# 从附件列表的字典中获取附件名称
                # print(attachmentname)
                downloadpath = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+"/Attachments/")
                # 获取下载附件的路径，最后一定要加上"/"
                emailclient.downloadAttachement(id,attachmentname,downloadpath)# 利用获取的附件名称，调用下载附件函数下载附件到指定路径,不包括附件名称
                filename=os.path.join(downloadpath+attachmentname)# 精确到附件名称的路径
                print(filename)
                excelparse = ExcelReadWriter(filename)# 实例化表格解析函数
                command = excelparse.read("script").split(" ")#从附件的sheet2中获取执行什么脚本，需要什么参数
                script=['bash']
                script.extend(command)#列表拼接，例['bash','脚本名','参数1’,'参数2',……]
                if ".sh" in script:
                    executescript = " ".join(script)#执行shell脚本需要将上方的列表准换成字符串
                    status = subprocess.Popen(executescript,stdout=subprocess.PIPE,shell=True,cwd=os.getcwd()+"/script/").communicate()
                    #获取shell脚本传回来的参数。通过subprocess.Popen()方法调用命令后执行的结果，stdout表示程序的标准输出；shell=True表示指定的命令将通过shell执行，cwd表示子进程的工作目录，即脚本所在目录，communicate返回标准输出。
                    excelparse.write("执行结果", status[0])#将脚本返回来的结果写入附件中
                    excelparse.write("执行者", "auto")
                    executetime = time.strftime('%Y.%m.%d', time.localtime(time.time()))
                    # time.time()获得当前时间的时间戳，time.localtime()格式化时间戳为本地的时间，time.strftime()格式化日期
                    excelparse.write("执行时间", executetime)
                    emailclient.sendMail("cloudiip_ops@bonc.com.cn","域名反向代理执行结果","域名反向代理工作已完成",attachmentname,downloadpath)
                    # mailclient.removeMessage(getmail)  # 删除邮件
                elif ".py" in script:
                    status = subprocess.Popen(script,stdout=subprocess.PIPE,cwd=os.getcwd() + "/script/").communicate()
                    excelparse.write("执行结果", status[0])
                    excelparse.write("执行者", "auto")
                    executetime = time.strftime('%Y.%m.%d', time.localtime(time.time()))
                    excelparse.write("执行时间", executetime)
                    emailclient.sendMail("cloudiip_ops@bonc.com.cn","DNS解析执行结果","DNS解析工作已完成",attachmentname,downloadpath)
                    #mailclient.removeMessage(getmail)  # 删除邮件

                time.sleep(300)

if __name__ == '__main__':
    s=ShellExecuteAgent()
    s.main()