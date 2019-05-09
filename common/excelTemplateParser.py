# coding:utf-8
import json
class ExcelTempleteParser():
    def parse(templateName):
        d = json.load(open('/tmp/result.txt','r'))
        print(d)
