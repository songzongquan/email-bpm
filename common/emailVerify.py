class MailVerify:
    def mailVerify(self,subject,fromaddr,attachmentname):
        if fromaddr.endswith('bonc.com.cn'):
            if subject.endswith('[bpm]'):

                if attachmentname.startswith('form_') and attachmentname.endswith('.xlsx'):
                    # print("True")
                    return True
                else:
                    # print("Flase")
                    return False



if __name__ == "__main__":
    a=MailVerify()
    a.mailVerify('[bpm]主题','lixiaofan@bonc.com.cn','form_邮箱注册.xlsx')