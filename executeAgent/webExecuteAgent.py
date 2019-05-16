# coding=utf-8
import os,time
from common.emailClient import *
from common.excelReadWriter import *
from common.config  import *
import openpyxl


e = EmailClient('lixiaofan@bonc.com.cn','Lixiaofan123','mail.bonc.com.cn','993','mail.bonc.com.cn','25')       #实例化EmailClient类

class WebExecuteAgent():
    '''负责接上工单邮件，解析excel，针对其中的执行业务内容，调用浏览器，完成一些web系统的操作来完成业务处理。'''
    def main(self):
        # while True:
            getmail = e.getOldestMessage()      #调用获得最旧邮件的方法，获得最旧的邮件,形式为字典
            id = getmail.get('id')          #获取该邮件的id
            attachmentlist = e.getAttachements(id)     #调用所有附件的方法，获得该邮件的附件,形式为列表
            for attachement in attachmentlist:
                '''for循环，输出邮件中的所有附件'''
                print(attachement)
                attachementname = attachement['attachementname']     #从附件的列表形式中，获得附件的名称
                print(attachementname)
                abspath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))     #当前文件的绝对路径的上一级
                print(abspath)
                downloadpath = os.path.join(abspath+ "/host_auth_Attachements/")       #确定附件下载的地址
                print(downloadpath)
                downloadatta = e.downloadAttachement(attachementname,downloadpath)    #调用下载附件的方法，下载附件
                print(downloadatta)

                attachementpath = os.path.join(downloadpath + attachementname)        #确定精确到附件名的路径
                print(attachementpath)
                p = ExcelReadWriter(attachementpath)       #实例化ExcelReadWriter类
            #     if "form_堡垒机授权申请" in attachementname:
            #         ip = p.read("内网IP")         # 调用读写附件函数，获取ip和域名
            #         domain = p.read("预申请公网域名")
            #         path = os.path.join(abspath+ '\executeAgent\script\host_auth.py')
            #         os.system("python path%s %s" % (ip, domain))        #执行host_auth.py脚本,并传参数ip和domain
            #         p.write("执行状态","判断是否成功的变量")     #判断是否成功的变量是host_auth.py返回的值
            #         e.sendMail('lixiaofan@bonc.com.cn', 'Lixiaofan123', 'lixiaofan@bonc.com.cn', "[auto]邮箱注册","测试一下发邮件带附件","form_邮箱注册.xlsx","F:/data/")
            #
            #
            #
            # delmail = e.removeMessage(getmail)  # 删除邮件
            # print(delmail)
            # time.sleep(300)     #每5分钟取一次邮件附件

if __name__ == '__main__':
    s=WebExecuteAgent()
    s.main()
