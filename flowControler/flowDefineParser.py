#-*- coding="utf-8" -*-
import json
import os

class FlowDefineParser:
    '''流程定义文件解析器，读取指定的json文件，得到流程定义信息，返回一个字典数据结构;'''
    def parse(self,filename):
        '''此程序共4个json文件，分别对应4种流程。
           本方法读取filename对应的json文件，将json文件反序列化，返回字典。
        '''
        path1 = os.path.dirname(__file__)           #返回的是__file__所在的路径，是当前方法的绝对路径。
        # print(path1)
        path2 = os.path.join(path1+"/data/"+filename)       #返回路径加文件名
        # print(path2)
        with open(path2,encoding="utf-8") as flow_info:
             flow = json.load(flow_info)
             print(flow)



# x = FlowDefineParser()
#
# x.parse("flow_邮箱注册.json")