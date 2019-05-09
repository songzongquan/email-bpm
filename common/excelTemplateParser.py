# encoding:utf-8
import json
import os
class ExcelTempleteParser():
    def parse(templateName):
        a = os.getcwd()
        print(a)
        b = os.path.dirname(a)
        path = os.path.join(b+'/flowControler/data/'+'form_邮箱注册.json')
        print(path)
        with open(path) as form:
            aa = json.load(form, encoding='utf-8')
            print(aa)
e = ExcelTempleteParser()
e.parse()





