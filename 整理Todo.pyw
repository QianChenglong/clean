# coding=utf-8
'''
# =============================================================================
#      FileName: 整理ToDo.py
#        Author: QianChengLong
#         Email: qian_cheng_long@163.com
#      HomePage: www.QianChengLong.com
#       Version: 1.0
#    LastChange: 2013-05-08 18:41:50
#       History:
# =============================================================================
'''

import sqlite3
import os

# 变量定义
db_name = "E:\Programming\Language\Python\Code\my\Todo\My.s3db" # 数据库名称
ToDo_fileName = r"E:\Todo" # 待做事情文件名
ToDo_tableName = "TB_ToDo"

# 事务整理

# 数据库操作
db = sqlite3.connect(db_name)
c = db.cursor()

# 检查文件是否存在
if os.path.isfile(ToDo_fileName) == False :
    exit(-1)

# 读取文件内容
file = open(ToDo_fileName, 'r')
lines = file.readlines()
update_lines = ""

for line in lines :
    line = line.strip('\n')
    fields = line.split()
    if  len(fields) == 3 :
        c.execute("insert into %s values('%s', '%s', '%s', NULL)"
                % (ToDo_tableName, fields[0], fields[1], fields[2]))
    elif len(fields) == 4 :
        c.execute("insert into %s values('%s', '%s', '%s', '%s')"
                % (ToDo_tableName, fields[0], fields[1], fields[2], fields[3]))
    else :
        update_lines += line + '\n'

file.close()
file = open(ToDo_fileName, 'w')
file.writelines(update_lines)
file.close()

db.commit()
db.close()
