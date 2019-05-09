from configparser import ConfigParser
import os,sys

def getMainEmailInfo():
    ''' 获取主程序的邮箱配置信息'''
    path = '/flowControler/conf/email-bpm.ini'
    base = os.getcwd()
    path = base+path
    print(path)
    info = getEmailInfo(path)

    return info


def getAgentEmailInfo():
    '''得到执行代理的邮件配置信息'''
    path = '/executeAgent/conf/agent.ini'
    base = os.getcwd()
    path = base+path
    info = getEmailInfo(path)
    return info


def getEmailInfo(path):
    '''通用的读邮件账号配置的信息 '''

    config =  ConfigParser()
    try:
        
        config.read(path)
    except IOError:
        print("error: file not found ")

    s = config.sections()
    print(s)
    address =  config.get('email','address')
    account = config.get('email','account')
    password = config.get('email','password')
    imap =  config.get('email','imap')
    imap_port =  config.get('email','imap_port')
    stmp = config.get('email','stmp')
    stmp_port = config.get('email','stmp_port')

    info = {}
  
    info['address'] = address
    info['account'] = account
    info['password'] = password
    info['imap'] = imap
    info['imap_port'] = imap_port
    info['stmp'] = stmp
    info['stmp_port'] = stmp_port

    return info

if __name__ == '__main__':

    info = getMainEmailInfo()
    print(info)
