class MailVerify:
    def mailVerify(self,subject,fromaddr):
        if fromaddr.endswith('bonc.com.cn'):
            if subject.startswith('[bpm]'):
                print("True")
                return True
            else:
                print("False")
                return False
        else:
            print("False")
            return False



if __name__ == "__main__":
    a=MailVerify()
    a.mailVerify('[bpm]主题','lixiaofan@bonc.com.cn')