#!/usr/bin/python3
#encoding:utf-8

from common.emailClient import EmailClient 
from common.excelReadWriter import ExcelReadWriter

# -*- coding:utf-8 -*-
#!usr/bin/python

import os
import time
import json
from FlowDefineParser import FlowDefineParser




class FlowExecuter():


    """没有流水号的文件添加流水号"""
    current_path = os.path.dirname(__file__)
    excel_path = os.path.join(current_path+"/../data/excels/")
    date_file = os.path.join(current_path+"/../data/date.txt")
    order_file = os.path.join(current_path+"/../data/order.txt")
    current_time = time.strftime("%Y%m%d",time.localtime())
    current_path = os.path.dirname(__file__)
    excel_path = os.path.join(current_path+"/data/excels/")
    instance_path = os.path.join(current_path+"/data/instance/")
    
    def __init__(self,filename):
        self.filename=filename

    def getId(self):
        f = open(self.date_file)
        date = f.read()
        if date == self.current_time:
            f1 = open(self.order_file)
            order = str(int(f1.read())+1)
            newId = self.current_time+"-"+order
            f.close()
            f1.close()
            f2 = open(self.order_file,"w")
            f2.write(order)
            f2.close()
        else:
            f.close()
            f2 = open(self.date_file,"w")
            f2.write(self.current_time)
            f2.close()
            f1 = open(self.order_file,"w")
            f1.write("1")
            f1.close()
            newId = self.current_time+"-"+"1"
        return newId
    
    def excelRename(self,filename,sn):
        
        file_split2 = filename.split(".")
        old_excel = os.path.join(self.excel_path+filename)
        new_excel = os.path.join(self.excel_path+file_split2[0]+"_"+sn+"."+file_split2[1])
        os.rename(old_excel,new_excel)
        

    def createInstance(self):
        #生成序列号
        sn = self.getId()
        #修改附件文件名
        self.excelRename(self.filename,sn)
        
        #初始化流程实例json文件添加内容
        file_split = self.filename.split("_")
        flow_name = file_split[1].split(".")[0]
        flow_json = os.path.join("flow_"+flow_name+".json")
        json_file = os.path.join(instance_path+json_name)

        json_file1 = "flow_"+flow_name+"_"+sn+".json"
        
        #如果找到流程定义文件，加载它
        if os.path.exists(json_file):
            flowDef = flowDefineParser()
            flow = flowDef.parse(json_file)
            self.flowdef = flow
            def_nodes = flow['nodes']
            
            write_json ={}
            nodes = []
            node = {}
            node["id"] = def_nodes[0]['id']
            node["name"] = def_nodes[0]['name']
            node['state']= ''
            node['actor'] = ''
            nodes.append(node)
            write_json['nodes'] = nodes    
            with open(json_file1, 'w',encoding="utf-8") as f:
                json.dump(write_json, f)
                f.close()
        self.instance = write_json
        return write_json
                
    def loadInstance(self):
        """读取实例文件"""
        #文件名解析，得到流程定义文件名
        filename = self.filename
        file_split = filename.split('_')
        flow_name = file_split[1]
        def_file = "flow_"+flow_name+".json"
        #加载流程定义
        flowDef = flowDefineParser()
        flow = flowDef.parse(def_file)
        self.flowdef = flow 
        json_file = os.path.join(instance_path+filename)
        with open(json_file, encoding="utf-8") as f: 
            data = json.load(f)
        f.close()
        self.instance = data
        return data
    
    def getCurrentStep(self):
        """获取当前节点"""
        node = self.instance['nodes'][-1]
        nodeId =  node['id']
        nodes = self.flowdef['nodes']
        for nod in nodes:
            if nod['id'] == nodeId:
                currentNode = nod
                break
        return currentNode
        
    def getNextStep(self,step):
        """获取下一个节点""" 
        
        flowdef = self.flowdef
        route = step['route']
        if route:
            if len(route) > 1:
                for r in route:
                    c = r['condition']
                    cs = c.split("=")
                    left = cs[0]
                    right = cs[1]
                    excelrw = ExcelReadWriter(self.filename)
                    vv = excelrw.read(left)
                    if vv == right:
                        next_step = r['toNode']
                        break
            else:
                next_step = route[0]['toNode']
        else:
            next_step = None
    
    def start(self):
        #文件名解析，看是否有流水号，如果没有，创建实例，如果有，加载实例
        filename = self.filename

        file_split = filename.split("_")
        if len(file_split) == 2:  #没有流水号
            instance = self.createFlowInstance()
            step = self.getCurrentStep(instance)
            self.execute(step)
            #得到下一个节点，并在实例文件中初始化这个节点的结构

        else:
            instance = self.loadFlowInstance()
            step = self.getCurrentStep(instance)
            self.execute(step)
            #得到下个节点，并在实例文件中初始化


    def complete(self,stepId):
        '''通知该节点已完成 '''
        pass
        
            
    def execute(self,step):
        """执行节点:根据流程定义与step,得到流程定义中当前节点的所有信息，然后根据是人工还是自动，如果是人工，则取得actor,给它发邮件，并且将当前附件作为新附件发出
        如果是自动，则取得脚本，调用脚本。调用时将excel中取得的变量都传给脚本，最后把脚本执行后返回值，取到加入到流程变量"""
        instance = self.instance
        stepId = step['id']
        actor = step['actor']
        tasktype = step['type']
 
        if tasktype =='man' or tasktype == 'remote':
            pass
        elif tasktype == 'auto':
            pass
        

  
        


if __name__ == '__main__':
    
    f = flowExecuter()
    f.main()


