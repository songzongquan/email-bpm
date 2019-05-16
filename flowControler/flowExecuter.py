#!/usr/bin/python3
#encoding:utf-8

from common.emailClient import EmailClient 
from common.excelReadWriter import ExcelReadWriter

# -*- coding:utf-8 -*-
#!usr/bin/python

import os
import time
import json
from flowControler.flowDefineParser import FlowDefineParser




class FlowExecuter():


    
    def __init__(self,filename):
        self.filename=filename
        self.instance=None
        self.instanceFile = None
        self.flowdef = None
    
    def __getDataPath(self):

        current_path = os.path.dirname(__file__)
        data_path = os.path.join(current_path+"/../data/")
        return data_path
    
    def __getId(self):
        date_file = os.path.join(self.__getDataPath()+"date.txt")
        order_file = os.path.join(self.__getDataPath()+"order.txt")
        f = open(date_file,'w+')
        date = f.read()

        current_time =  time.strftime("%Y%m%d",time.localtime())
        if date == current_time:
            f1 = open(order_file)
            order = str(int(f1.read())+1)
            newId = current_time+"-"+order
            f.close()
            f1.close()
            f2 = open(order_file,"w+")
            f2.write(order)
            f2.close()
        else:
            f.close()
            f2 = open(date_file,"w+")
            f2.write(current_time)
            f2.close()
            f1 = open(order_file,"w+")
            f1.write("1")
            f1.close()
            newId = current_time+"-"+"1"
        return newId
    
    def excelRename(self,filename,sn):
        
        file_split2 = filename.split(".")
        old_excel = os.path.join(self.__getDataPath()+filename)
        new_excel = os.path.join(self.__getDataPath()+file_split2[0]+"_"+sn+"."+file_split2[1])
        os.rename(old_excel,new_excel)
        

    def createInstance(self):
        
        print("进入创建实例")
        #生成序列号
        sn = self.__getId()
        #修改附件文件名
        self.excelRename(self.filename,sn)
        
        #初始化流程实例json文件添加内容
        file_split = self.filename.split("_")
        flow_name = file_split[1].split(".")[0]
        flow_json = os.path.join("flow_"+flow_name+".json")
        print("流程定义文件为："+flow_json)

        json_file1 = self.__getDataPath()+"flow_"+flow_name+"_"+sn+".json"
        #设置流程实例文件名 
        self.instanceFile = json_file1 
        
        #如果找到流程定义文件，加载它

        write_json ={}
        

        if os.path.exists(self.__getDataPath()+flow_json):
            flowDef = FlowDefineParser()
            flow = flowDef.parse(flow_json)
            print("流程定义："+str(flow))
            self.flowdef = flow
            def_nodes = flow['nodes']
            print(def_nodes)            
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
            print(write_json)
            self.instance = write_json
        return write_json
                
    def loadInstance(self):
        """读取实例文件"""

        print("进入了加载实例。")
        #文件名解析，得到流程定义文件名
        filename = self.filename
        file_split = filename.split('_')
        flow_name = file_split[1]
        sn =  file_split[2]
        def_file = "flow_"+flow_name+".json"
        #加载流程定义
        flowDef = flowDefineParser()
        flow = flowDef.parse(def_file)
        self.flowdef = flow 
        json_file = os.path.join(self.__getDataPath()+filename)
        with open(json_file, encoding="utf-8") as f: 
            data = json.load(f)
        f.close()
        self.instance = data
        self.instanceFile = "flow_"+flow_name+"_"+sn+".json"
        return data
    
    def getCurrentStep(self):
        """获取当前节点"""
        print(self.instance)
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
            print("没有流水号")
            instance = self.createInstance()

        else:
            print("有流水号")
            instance = self.loadInstance()
        
        #得到当前节点并执行
        step = self.getCurrentStep()
        self.execute(step)
        #得到下一个节点并执行，如果下一个节点是自动节点，需要继承找到下个节点并执行，如果不是自动节点，则执行后不再找下一个接点去执行
        newNode = step
        while(True):
            if newNode['taskType'] == 'auto':
                self.execute(newNode)
                newNode = self.getNextStep(newNode)
            else:
                self.execute(newNode)
                break



    def complete(self,stepId):
        '''通知该节点已完成,此方法只为人工或远程任务才会用，这个需要在这个节点第一次被执行发邮件时把节点id放在附件中，当人回复该邮件后，系统收到时解析这个节点号，来得知当前是哪一个节点被完成了，然后调用此方法'''
        #找到对应节点，将其状态设为完成
        nodes  = self.instance['nodes']
        for node in nodes:
            if node['id'] == setpId:
                node['state']='complete'
                break
        #将实例的新状态保存入库
        
        f = open(self.instanceFile,'w',encoding='utf-8')
        json.dump(self.instance,f)
        f.close()
        
            
    def execute(self,step):
        """执行节点:根据流程定义与step,得到流程定义中当前节点的所有信息，然后根据是人工还是自动，如果是人工，则取得actor,给它发邮件，并且将当前附件作为新附件发出
        如果是自动，则取得脚本，调用脚本。调用时将excel中取得的变量都传给脚本，最后把脚本执行后返回值，取到加入到流程变量
        自动任务执行完后，要列新流程实例数据,自动任务状态直接更新为完成，人工任务设为开始执行或执行中，人工任务只有complete方法才能设为已完成。
        """
        instance = self.instance
        stepId = step['id']
        actor = step['actor']
        tasktype = step['taskType']
 
        if tasktype =='man' or tasktype == 'remote':
            pass
        elif tasktype == 'auto':
            pass
        

  
        


if __name__ == '__main__':
    
    f = flowExecuter()
    f.main()


