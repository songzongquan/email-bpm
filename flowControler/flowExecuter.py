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

    
    def __getDataPath(self):

        current_path = os.path.dirname(__file__)
        data_path = os.path.join(current_path+"/../data/")
        return data_path
    
    def __getId(self):
        data_file = os.path.join(__getDataPath()+"date.txt")
        order_file = os.path.join(__getDataPath()+"order.txt")
        f = open(date_file)
        date = f.read()
        if date == self.current_time:
            f1 = open(order_file)
            order = str(int(f1.read())+1)
            current_time =  time.strftime("%Y%m%d",time.localtime())
            newId = current_time+"-"+order
            f.close()
            f1.close()
            f2 = open(order_file,"w")
            f2.write(order)
            f2.close()
        else:
            f.close()
            f2 = open(date_file,"w")
            f2.write(current_time)
            f2.close()
            f1 = open(order_file,"w")
            f1.write("1")
            f1.close()
            newId = current_time+"-"+"1"
        return newId
    
    def excelRename(self,filename,sn):
        
        file_split2 = filename.split(".")
        old_excel = os.path.join(__getDataPath()+filename)
        new_excel = os.path.join(__getDataPath()+file_split2[0]+"_"+sn+"."+file_split2[1])
        os.rename(old_excel,new_excel)
        

    def createInstance(self):
        #生成序列号
        sn = __getId()
        #修改附件文件名
        excelRename(self.filename,sn)
        
        #初始化流程实例json文件添加内容
        file_split = self.filename.split("_")
        flow_name = file_split[1].split(".")[0]
        flow_json = os.path.join("flow_"+flow_name+".json")
        json_file = os.path.join(__getDataPath()+json_name)

        json_file1 = "flow_"+flow_name+"_"+sn+".json"
        #设置流程实例文件名 
        self.instanceFile = json_file1 
        
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
        sn =  file_split[2]
        def_file = "flow_"+flow_name+".json"
        #加载流程定义
        flowDef = flowDefineParser()
        flow = flowDef.parse(def_file)
        self.flowdef = flow 
        json_file = os.path.join(__getDataPath()+filename)
        with open(json_file, encoding="utf-8") as f: 
            data = json.load(f)
        f.close()
        self.instance = data
        self.instanceFile = "flow_"+flow_name+"_"+sn+".json"
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

        else:
            instance = self.loadFlowInstance()
        
        #得到当前节点并执行
        step = self.getCurrentStep(instance)
        self.execute(step)
        #得到下一个节点并执行，如果下一个节点是自动节点，需要继承找到下个节点并执行，如果不是自动节点，则执行后不再找下一个接点去执行
        newNode = step
        while(True):
            if newNode['type'] == 'auto':
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
        如果是自动，则取得脚本，调用脚本。调用时将excel中取得的变量都传给脚本，最后把脚本执行后返回值，取到加入到流程变量"""
        instance = self.instance
        stepId = step['id']
        actor = step['actor']
        tasktype = step['type']
        if tasktype =='man' or tasktype == 'remote':
            email=getEmail(actor)
            info = getMainEmailInfo()
            send_email=info["address"]
            passwd=info["password"]
            flow_name=self.filename.split("_")[1]
            title = "请领导审批"+flow_name
            text = title+\n+"请将审批结果填写至附件中，并发回"+send_email+\n+"本邮件为系统自动发出"
            a=EmailClient(send_email,passwd,'mail.bonc.com.cn','993','mail.bonc.com.cn','25')
            a.sendMail(send_email,passwd,email,title,text,self.filename,self.excel_path)
            os.remove(self.excel_path+self.filename)
        elif tasktype == 'auto'：
            auto_script = step['script']    
            current_system = platform.system()  #返回操作系统类型
            if current_system=="Windows":
                yuyan = "python "
            elif current_system=="Linux":
                yuyan = "python3 "
            script_split = auto_script.split(" ")
            script = script_split[0]
            original = yuyan+self.script_path+script
            vars = []
            for i in script_split:
                if i!=script:
                    aa=excelReadWriter()
                    var = aa.excelReadWriter(i)
                    vars.append(var)
            vars1=[str(i) for i in vars]
            command1=" ".join(vars1)
            command=command+" "+command1
            if current_system == "Windows":
                ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,timeout=30)
            else:
                ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding=encode,timeout=30)            
            if ret.returncode == 0:
                self.flowVars[script]="执行成功"
                back_read = bytes.decode(ret.stdout,encoding=encode)  #返回值是一个字典
                for k,v in back_read.items():
                    self.flowVars[k]=v
            else:
                self.flowVars[script]="执行失败"
        
    def getEmail(self,actor):
        a = flowDefineParser()
        data = a.parse("emailInfo.json")
        for i in data["info"]:
            if i["姓名"]==actor:
                email = i["邮箱"]

    getFlowVarValue(self,varName):
        cc=ExcelReadWriter()
        return cc.read(varName)

    setFlowVarValue(self,varName,value):
        self.flowVars[varName]=value

if __name__ == '__main__':
    
    f = flowExecuter()
    f.main()


