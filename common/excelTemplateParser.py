# encoding:utf-8
import json
import os
class ExcelTempleteParser():
    def parse(self,templateName):
        base = os.getcwd()
        print(base)
        b = os.path.dirname(base)
        path = os.path.join(b+'/flowControler/data/'+templateName)
        print(path)
        with open(path) as form:
            aa = json.load(form, encoding='utf-8')
            print(aa)
# e = ExcelTempleteParser()
# e.parse()
if __name__=='__main__':
    e = ExcelTempleteParser()
    e.parse('form_邮箱注册.json')





