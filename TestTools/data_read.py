import os
from xlrd import open_workbook
import xlrd
import xlwt
import datetime
import yaml
from xlutils.copy import copy

upPath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
yamlpath = os.path.join(upPath, "TestData", "g_data.yaml")


# 从excel文件中读取测试用例
def get_xls(type,xls_name, sheet_name):
    # get xls file's path
    xlsPath = os.path.join(upPath, "TestData", xls_name)
    # print xlsPath
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    # 判断需要list还是dict的数据返回
    if type == "list":
        cls = []
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'id' and sheet.row_values(i)[0] != u'module' and sheet.row_values(i)[0] != u'name':
                cls.append(sheet.row_values(i))

    elif type == "dict":
        cls = {}
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'id' and sheet.row_values(i)[0] != u'module' and sheet.row_values(i)[0] != u'name':
                cls.setdefault(sheet.row_values(i)[0],sheet.row_values(i)[1])

    if sheet_name == "setup":
        num = cls['num']
        newfile = copy(file)
        newsheet = newfile.get_sheet(0)
        newsheet.write(1, 1, int(int(num) + 1))
        newsheet.write(3, 1, int(int(cls['user_phone']) + 1))

        newfile.save(xlsPath)
        cls = handle_setup_data(cls)

    return cls

def handle_setup_data(cls):
    num = int(cls['num'])
    user_phone = cls['user_phone']
    startDate = datetime.datetime.now().strftime('%Y-%m-%d')
    user_name = "%s%s" % (cls['user_name'], num)
    StartDateTime = "%s %s" % (startDate, cls['StartDateTime'])
    EndDateTime = "%s %s" % (startDate, cls['EndDateTime'])
    cls['num'] = str(num)
    cls['user_name'] = str(user_name)
    cls[u'startDate'] = str(startDate)
    cls[u'endDate'] = str(startDate)
    cls['StartDateTime'] = str(StartDateTime)
    cls['EndDateTime'] = str(EndDateTime)
    cls['user_phone'] = str(int(user_phone))

    return cls


# 从yaml文件中读取数据
def get_yaml():
    f = open(yamlpath, 'r')
    # 读取
    x = yaml.load(f)
    f.close()
    return x


def set_yaml(data):
    # 追加文件
    f = open(yamlpath, 'w')
    # 将data写入到yaml文件中
    yaml.dump(data, f)
    f.close()


# 清除yaml中的数据
def del_yaml():
    f = open(yamlpath, 'w')
    f.truncate()

