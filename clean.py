#! /usr/bin/env python
# coding=utf-8

import sqlite3
import os


def clean(db_name, table_name, filename, delimiter='|'):
    """ clean file up to table of database

        db_name，保存的数据库
        table_name, 表名
        filename, 要整理的文件名
    """

    # 检查文件是否存在
    if not os.path.isfile(filename):
        exit(-1)

    # 数据库操作
    db = sqlite3.connect(db_name)
    c = db.cursor()

    # 读取文件内容
    file = open(filename, 'rb')
    lines = file.readlines()
    update_lines = ""

    for line in lines:
        line = line.strip('\n')
        fields = line.split(delimiter)
        if len(fields) == 3:
            c.execute("insert into %s values('%s', '%s', '%s', NULL)"
                      % (table_name, fields[0], fields[1], fields[2]))
        elif len(fields) == 4:
            c.execute("insert into %s values('%s', '%s', '%s', '%s')"
                      % (table_name, fields[0], fields[1], fields[2],
                         fields[3]))
        else:
            update_lines += line + '\n'

    file.close()
    file = open(filename, 'wb')
    file.writelines(update_lines)
    file.close()

    db.commit()
    db.close()
