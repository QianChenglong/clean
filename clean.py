#! /usr/bin/env python2
# coding=utf-8

import sqlite3
import os

# 变量定义
db_name = "E:\Programming\Language\Python\Code\my\Todo\My.s3db" # 数据库名称
Question_fileName = r"E:\Question" # 待解决文件名
Question_tableName = "TB_Question"
delimiter = '|'

# 参数：db_name，保存的数据库
#       table_name, 表名
#       filename, 要整理的文件名
def clean(db_name, table_name, filename):
    # 检查文件是否存在
    if os.path.isfile(filename) == False :
        exit(-1)

    # 数据库操作
    db = sqlite3.connect(db_name)
    c = db.cursor()

    # 读取文件内容
    file = open(filename, 'r')
    lines = file.readlines()
    update_lines = ""

    for line in lines :
        line = line.strip('\n')
        fields = line.split(delimiter)
        if  len(fields) == 3 :
            c.execute("insert into %s values('%s', '%s', '%s', NULL)"
                    % (table_name, fields[0], fields[1], fields[2]))
        elif len(fields) == 4 :
            c.execute("insert into %s values('%s', '%s', '%s', '%s')"
                    % (table_name, fields[0], fields[1], fields[2], fields[3]))
        else :
            update_lines += line + '\n'

    file.close()
    file = open(filename, 'w')
    file.writelines(update_lines)
    file.close()

    db.commit()
    db.close()
