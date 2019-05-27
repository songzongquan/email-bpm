#!/usr/bin/python3
#encoding:utf-8

import os
import time
import json
import platform
import subprocess
import re

from flowControler.flowDefineParser import FlowDefineParser
from common.config  import *
from common.emailClient import EmailClient
from common.excelReadWriter import ExcelReadWriter

class FlowExecuter():

    def __init__(self,filename):
        self.filename=filename
        self.instance=None
        self.instanceFile = None
        self.flowdef = None
        self.flowVars ={}
    
    def __getDataPath(self):

        current_path = os.path.dirname(__file__)
        data_path = os.path.join(current_path+"/../data/")
        return data_path
    
    def __getId(self):
        date_file = os.path.join(self.__getDataPath()+"date.txt")
        order_file = os.path.join(self.__getDataPath()+"order.txt")
        f = open(date_file,'r')
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
        old_excel = os.path.join(self.__getDataPath()+"excel/"+filename)
        new_excel = os.path.join(self.__getDataPath()+"excel/"+file_split2[0]+"_"+sn+"."+file_split2[1])
        os.rename(old_excel,new_excel)
        self.filename = file_split2[0]+"_"+sn+"."+file_split2[1]
        

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
        
        #创建实例文件

        write_json ={}
        nodes =[]
        write_json['nodes']=nodes
        f = open(json_file1,'w',encoding='utf-8')
        json.dump(write_json,f)
        f.close()

        #加载流程定义
        flowDef = FlowDefineParser()
        flow = flowDef.parse(flow_json)
        self.flowdef = flow 

        self.instance = write_json
        return write_json
                
    def loadInstance(self):
        """读取实例文件"""

        print("进入了加载实例。")
        #文件名解析，得到流程定义文件名
        filename = self.filename
        file_split = filename.split('_')
        flow_name = file_split[1]
        sn =  file_split[2].split(".")[0]
        def_file = "flow_"+flow_name+".json"

        #加载流程定义
        flowDef = FlowDefineParser()
        flow = flowDef.parse(def_file)
        self.flowdef = flow 
        json_file = os.path.join(self.__getDataPath()+"flow_"+flow_name+"_"+sn+".json")
        with open(json_file, encoding="utf-8") as f: 
            data = json.load(f)
        f.close()
        self.instance = data
        self.instanceFile = self.__getDataPath()+"flow_"+flow_name+"_"+sn+".json"
        return data
    
    def getCurrentStep(self):
        """获取当前节点"""
        print(self.instance)
        currentNode = None

        if len(self.instance['nodes']) == 0:
            #如果当前还没有执行过节点，就从定义中查出一个节点
            currentNode = self.flowdef['nodes'][0]
  

        else:     #否则就取实例中最后一个节点
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
        next_step = None
        nextnode = None
        if route:
            print("判定路由")
            if len(route) > 1:
                for r in route:
                    c = r['condition']
                    if self.evalCondition(c):
                        next_step = r['toNode']
                        break    
            else:
                next_step = route[0]['toNode']
                
            nodes = flowdef['nodes']
            for node in nodes:
                if node['id'] == next_step:
                    nextnode = node
        else:
            nextnode = None

        return nextnode

    
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
        print("当前应该执行的节点："+str(step))
        #当前的实例状态数据的节点
        nodes = self.instance['nodes'] 
        if len(nodes)>0:
            state = self.getStepState(step['id'])
        else:
            state = ''

        #如果状态为没执行过，则执行        
        if state == '': #如果没执行过，则执行
            self.execute(step)
        elif state == 'start' or state == 'complete': #如果已开始执行，则这时应该是完成
            self.complete(step['id'])

            
            #得到下一个节点并执行，如果下一个节点是自动节点，需要继承找到下个节点并执行，如果不是自动节点，则执行后不再找下一个接点去执行
            newNode = step

            while(True):
                newNode = self.getNextStep(newNode)
                print("下一节点："+str(newNode))
                if newNode == None:
                    break
                if newNode['taskType'] == 'auto':
                    self.execute(newNode)
                    continue
                else:
                    self.execute(newNode)
                    break



    def complete(self,stepId):
        '''通知流程引擎该步骤已经完成，即设定为完成状态,并将执行者信息写入实例文件 '''
        self.setStepState(stepId,'complete') 
            
    def execute(self,step):
        """执行节点:根据流程定义与step,得到流程定义中当前节点的所有信息，然后根据是人工还是自动，如果是人工，则取得actor,给它发邮件，并且将当前附件作为新附件发出
        如果是自动，则取得脚本，调用脚本。调用时将excel中取得的变量都传给脚本，最后把脚本执行后返回值，取到加入到流程变量"""
        print("正在执行的节点："+str(step))
        instance = self.instance
        stepId = step['id']
        actor = ''
        tasktype = step['taskType']
        print("正在执行的节点类型 ："+tasktype)
        if tasktype =='man' or tasktype == 'remote':
            if tasktype =='man':
                actor = step['actor']

            print("actor:"+actor)

            email=self.getEmail(actor)
            print("接收人邮箱："+email)
            info = getMainEmailInfo()
            send_email=info["address"]
            passwd=info["password"]
            imap = info["imap"]
            imap_port = info["imap_port"]
            smtp = info["smtp"]
            smtp_port = info["smtp_port"]

            flow_name=self.filename.split("_")[1]
            title = "请领导审批"+flow_name+"[bpm]"
            text = title+"\n请将审批结果填写至附件中，并发回"+send_email+"\n本邮件为系统自动发出"
            a = EmailClient(send_email,passwd,imap,imap_port,smtp,smtp_port)
            a.sendMail(email,title,text,self.filename,self.__getDataPath()+"excel/")
            
            os.remove(self.__getDataPath()+"excel/"+self.filename)

            self.appendNode(step)
            self.setStepState(step['id'],'start') #执行完后状态设为已开始

        elif tasktype == 'auto':
            print("执行自动节点"+str(step))
            auto_script = step['script']  
            encode = 'utf-8'
            current_system = platform.system()  #返回操作系统类型
            if current_system=="Windows":
                yuyan = "python "
                encode='gbk'
            elif current_system=="Linux":
                yuyan = "python3 "
                encode = 'utf-8'
            script_split = auto_script.split(" ")
            script = script_split[0]
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__))+"/script/")
            original = yuyan+script_path+script
            print("将执行的脚本："+original)
            vars = []
            excel_path = os.path.join(self.__getDataPath()+"excel/"+self.filename)
            aa=ExcelReadWriter(excel_path)
            if script!="tongzhi.py":                                               
                for i in script_split:
                    if i!=script: 
                        var = aa.read(i)
                        vars.append(var)
            else:
                to=aa.read(script_split[1])
                vars.append(to)
                title=script_split[2]
                vars.append(title)
                text=script_split[3]
                vars.append(text)
            vars1=[str(i) for i in vars]
            command1=" ".join(vars1)
            command=original+" "+command1

            print("将执行的完整命令是："+command)
            if current_system == "Windows":
                ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,timeout=30)
            else:
                ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding=encode,timeout=30)            
            if ret.returncode == 0:
                self.flowVars["脚本执行结果"]="执行成功"
                print("执行返回的结果是："+ret.stdout)

                back_read = json.loads(ret.stdout) #返回值是一个字典
                for k,v in back_read.items():
                    self.flowVars[k]=v
            else:
                print("脚本执行失败")
                print("执行返回的结果是："+ret.stdout)
                self.flowVars["脚本执行结果"]="执行失败"
            #添加节点，并修改状态为完成 
            self.appendNode(step)
            self.setStepState(step['id'],'complete')


    def appendNode(self,step):
        #在流程实例中添加这个节点的数据
        newnode = {}
        newnode['id']= step['id']
        newnode['name']=step['name']
        newnode['state']=''
        newnode['actor']=''
        self.instance['nodes'].append(newnode)
        f = open(self.instanceFile,'w',encoding='utf-8')
        json.dump(self.instance,f)
        f.close()
        
    def setStepState(self,stepId,state):
        '''设置某节点的执行状态'''
        self.instance = self.loadInstance()
        #找到对应节点，将其状态设为完成
        nodes  = self.instance['nodes']
        for node in nodes:
            if node['id'] == stepId:
                node['state']=state
                break
        #将实例的新状态保存入库
        print("流程实例文件名："+self.instanceFile)         
        f = open(self.instanceFile,'w',encoding='utf-8')
        print("更新过的实例状态："+str(self.instance))
        json.dump(self.instance,f)
        f.close()

    def getStepState(self,stepId):
    
        self.instance = self.loadInstance()
        
        nodes = self.instance['nodes']
        state = None
        for node in nodes:
            if node['id'] == stepId:
                state = node['state']
        return state

    
    
    def getEmail(self,actor):
        a = FlowDefineParser()
        data = a.parse("emailInfo.json")

        for i in data:
            if i["姓名"]==actor:
                email = i["邮箱"]
                return email

    def getFlowVarValue(self,varName):
        cc=ExcelReadWriter(filename)
        return cc.read(varName)

    def setFlowVarValue(self,varName,value):
        self.flowVars[varName]=value
        
    def add1(self,value):
        return "【"+value+"】"
    
    def add2(self,value):
        return '"'+value+'"'

    def evalCondition(self,condition):
        """表达式格式为：【判断值】 条件表达式 【比较值】"，例如：【a】>【b】"""
        condition=condition.replace("=","==")
        p = r"(?<=\【).+?(?=\】)"
        #p1 = r"(?<=\《).+?(?=\》)"
        vars = re.findall(p,condition)
        print("解析出的变量："+str(vars))
        filepath = self.__getDataPath()+"excel/"+self.filename
        print("附件路径："+filepath)
        RW = ExcelReadWriter(filepath)
        for i in vars:
            value=RW.read(i)
            print("解析出的变量值："+str(value))
            if type(value)==int or type(value)==float:
                print("解析的变量是数字")
                new_i=self.add1(i)
                condition = condition.replace(new_i,str(value))
            elif type(value)==str:
                print("解析出的变量是字符串")
                new_i=self.add1(i)
                new_value=self.add2(value)
                condition = condition.replace(new_i,new_value)
            print('最后的条件表达式为：'+condition)
        return eval(condition)

if __name__ == '__main__':
    
    f = FlowExecuter('form_邮箱注册.xlsx')
    f.start()


