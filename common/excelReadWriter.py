# encoding:utf-8
import os,openpyxl
from common.excelTemplateParser import ExcelTempleteParser

class ExcelReadWriter():
    '''excel读写器,实现excel附件的业务数据的读取和写入'''

    def __init__(self,filename):
        '''根据模板名称来加载指定的模板excel以及其定义的json文件。'''

        self.filename = filename  #带路径的附件
        attachmentFileName = self.filename.split('/')[-1]
        attachmentFileName1 = attachmentFileName.split('.')[0]
        print(attachmentFileName1)
        splitfilename = attachmentFileName1.split('_')  #获得附件对应的模板名称前缀
        name = "_".join(splitfilename[0:2])
        print(name)
        parserFile = ExcelTempleteParser().parse(name + '.json')  #解析出的附件对应的模板信息
        self.parserFile = parserFile
        print(type(self.parserFile))


    def read(self,varName):
        '''读取filname指定的excel文件中的某变量值，varName是模板中定义的变量名，'''

        varCoordinate = self.parserFile.get(varName)  #根据变量名从附件名解析对应的模板中找到变量的位置
        print(varCoordinate)
        sheet = str(varCoordinate.get('sheet')) #获得变量所在表单的工作簿
        row = str(varCoordinate.get('row'))  #获得变量所在表单的某个工作簿中的某行
        col = varCoordinate.get('col')  #获得变量所在表单的某个工作簿中的某列
        workbook = openpyxl.load_workbook(self.filename) #打开附件
        Data_sheet = workbook['Sheet'+sheet]  #获得需要读取的工作表
        cellValue = Data_sheet[col+row].value  #根据变量的位置获取到对应的值
        print(cellValue)
        return cellValue


    def write(self,varName,value):
        '''读取filname指定的excel文件中的某变量坐标，varName是模板中定义的变量名，再将变量值value写入excel中并保存'''

        varCoordinate = self.parserFile.get(varName)  # 根据变量名从附件名解析对应的模板中找到变量的位置
        print(varCoordinate)
        sheet = str(varCoordinate.get('sheet'))  # 获得变量所在表单的工作簿
        row = str(varCoordinate.get('row'))  # 获得变量所在表单的某个工作簿中的某行
        col = varCoordinate.get('col')  # 获得变量所在表单的某个工作簿中的某列
        attachmentFile = openpyxl.load_workbook(self.filename)  # 打开附件
        Data_sheet = attachmentFile['Sheet' + sheet]  # 获得需要读取并写入的工作表
        Data_sheet[col+row].value = value  #将值写入到指定变量的坐标位置
        attachmentFile.save(filename=self.filename)  #保存修改过的附件


if __name__=='__main__':
    ExcelReadWriter = ExcelReadWriter('C:/Users/user/Desktop/form_邮箱注册_20190510.xlsx')
    ExcelReadWriter.read('姓名')
    ExcelReadWriter.write('工号', '0111831')


