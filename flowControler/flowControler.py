#!/usr/bin/python3
#encoding:utf-8

from common.emailClient import EmailClient 

# -*- coding:utf-8 -*-
#! usr/bin/python

import os
import time
import json
from FlowDefineParser import FlowDefineParser

class rename():
    """没有流水号的文件添加流水号"""
    current_path = os.path.dirname(__file__)
    excel_path = os.path.join(current_path+"/../data/excels/")
    date_file = os.path.join(current_path+"/../data/date.txt")
    order_file = os.path.join(current_path+"/../data/order.txt")
    current_time = time.strftime("%Y%m%d",time.localtime())

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
    
    def excelRename(self,filename):
        
        file_split = filename.split("_")
        if len(file_split) == 2:  #没有流水号
            Id = self.getId()
            file_split2 = filename.split(".")
            old_excel = os.path.join(self.excel_path+filename)
            new_excel = os.path.join(self.excel_path+file_split2[0]+"_"+Id+"."+file_split2[1])
            os.rename(old_excel,new_excel)  #添加流水号
        else:#已有流水号
            pass

class FlowExecuter():
    current_path = os.path.dirname(__file__)
    excel_path = os.path.join(current_path+"/data/excels/")
    instance_path = os.path.join(current_path+"/data/instance/")
    
    """def __init__(self,filrname):
        self.filename=filename
        self.name = ExcelReadWriter.read("姓名")
        self.depart = ExcelReadWriter.read("部门名称")
        file_split = self.filename.split("_")
        self.flow_name = file_split[1].split(".")[0] """

    def createInstance(self,filename):
        """初始的json文件添加内容"""
        file_split = filename.split("_")
        flow_name = file_split[1].split(".")[0]
        flow_json = os.path.join("flow_"+flow_name+".json")
        json_file = os.path.join(instance_path+json_name)
        if os.path.exists(json_file):
            json_read = self.loadInstance(json_file)
            current_step= self.getCurrentStep(json_file)
            next_step = self.getNextStep(flow_json,current_step)
        else:
            applicant_name = ExcelReadWriter.read("姓名")
            applicant_depart = ExcelReadWriter.read("部门名称")
            write_json = {flow_name:{"申请人":applicant_name,"申请人部门":applicant_depart}}
            with open(json_file, 'w',encoding="utf-8") as f:
                json.dump(write_json, f)
            f.close()
            nextStep = "node1"
        return next_step
                
    def loadInstance(self,filename):
        """读取实例文件"""
        with open(json_file, encoding="utf-8") as f: 
            data = json.load(f)
        f.close()
        return data
    
    def getCurrentStep(self,read_data):
        """获取当前节点"""
        currentStep = list(self.read_data.keys())[-1]
        return currentStep
        
    def getNextStep(self,flow_file,current_step):
        """获取下一个节点""" 
        result = ExcelReadWriter.read("审批结果")
        a = FlowDefineParser(flow_file)
        nodes = a.parse(flow_file)
        for i in nodes["nodes"]:
            if i["id"]==current_step:
                if len(i["route"])>0:
                    for j in i["route"]:
                        if j["condition"]:
                            next_step = j["toNode"]
                else:
                    next_step = "none"
        if next_step!="none":
            for i in nodes["nodes"]:
                if i["id"]==next_step:
                    name = i["name"]
        data[next_step]={"name":name}
        with open(json_file, 'w',encoding="utf-8") as f:
                json.dump(write_json, f)
        f.close()
        return next_step

    def execute(self,next_step):
        """执行下一个节点"""
        result = ExcelReadWriter.read("审批结果")
        a = FlowDefineParser()
        nodes = a.parse(flow_file)
        for i in nodes["nodes"]:
            if i["id"]==next_step:
                if i["taskType"]=="man":
                    actor=i["actor"]
                    title = "请领导审批"+self.name+"的"+self.flow_name
                    email_addr="qiaocongcong@bonc.com.cn"
                    text=titel+"\n"+"请在附件中的表格中填写审批意见并发回"+email_addr
                    sendEmail(actor,title,text)
                else:
                    script=actor=i["script"]
                    execute(script) #调用执行代理
        
A=rename()
A.excelRename("flow_反向代理.xlsx")


if __name__ == '__main__':
    f = FlowControler()
    f.main()


