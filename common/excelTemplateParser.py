# encoding:utf-8
import json
import os
class ExcelTempleteParser():
    '''excel模板定义解析器，读取指定的json文件，得到excel模板定义信息，返回一个字典数据结构;'''
    def parse(self,templateName):
        '''此程序共4个json文件，分别对应4种excel模板文件。
            此方法读取templateName对应的json文件，将json文件反序列化，返回字典。
            '''
        base = os.path.dirname(__file__)  #获得__file__所在的路径，是当前方法的绝对路径。
        # print(base)
        base1 = os.path.dirname(base)
        # print(base1)
        path = os.path.join(base1+'/flowControler/data/'+templateName)  #获得路径加json文件名
        # print(path)
        with open(path,encoding='utf-8') as form_info:
            templateDef = json.load(form_info)
            print(templateDef)
            return templateDef
# e = ExcelTempleteParser()
# e.parse()
if __name__=='__main__':
    e = ExcelTempleteParser()
    e.parse('form_邮箱注册.json')
    # e.parse('form_域名反向代理申请.json')





