from configparser import ConfigParser
import os,sys

def getMainEmailInfo():
    ''' 获取主程序的邮箱配置信息'''
    path = os.path.join('..','flowControler','conf','email-bpm.ini')
    
    configfilepath = getAbsPath(path)    
    info = getEmailInfo(configfilepath)

    return info


def getAbsPath(oldpath):
    ''' 根据相对路径计算对路径 '''

    filepath = os.path.abspath(__file__)
    #print(filepath)

    fatherpath = os.path.abspath(os.path.dirname(filepath))
    print(fatherpath)
    configfilepath = os.path.join(fatherpath,oldpath)
    #print(configfilepath)
    return configfilepath


def getAgentEmailInfo():
    '''得到执行代理的邮件配置信息'''
    path = os.path.join('..','executeAgent','conf','email-bpm.ini')
    print(path)
    configfilepath = getAbsPath(path)
    print("最后路径："+configfilepath)
    info = getEmailInfo(configfilepath)
    return info


def getEmailInfo(path):
    '''通用的读邮件账号配置的信息 '''

    config =  ConfigParser()
    try:
        
        config.read(path,encoding='utf-8')
    except IOError:
        print("error: file not found ")

    s = config.sections()
    #print(s)
    address =  config.get('email','address')
    account = config.get('email','account')
    password = config.get('email','password')
    imap =  config.get('email','imap')
    imap_port =  config.get('email','imap_port')
    smtp = config.get('email','smtp')
    smtp_port = config.get('email','smtp_port')
    interval = config.get('email','interval')

    info = {}
  
    info['address'] = address
    info['account'] = account
    info['password'] = password
    info['imap'] = imap
    info['imap_port'] = imap_port
    info['smtp'] = smtp
    info['smtp_port'] = smtp_port
    info['interval'] = interval

    return info

if __name__ == '__main__':

    info = getMainEmailInfo()
    print(info)