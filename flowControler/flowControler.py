#!/usr/bin/python3
#encoding:utf-8

from common.emailClient import EmailClient 

class FlowControler:
    '''主控类'''
    def main(self):
        ec = EmailClient()
        print(type(ec))

if __name__ == '__main__':
    f = FlowControler()
    f.main()


