#! /bin/env python2
# coding=utf-8

import clean
import sys, ConfigParser,platform,md5

configfile = "clean.ini"
db_name = "clean.db"
todo_tablename = "TB_Todo"
question_tablename = 'TB_Question'

# 功能：根据操作系统，读取clean.ini，返回相应待处理的文件名
def getFilenames():
    todo = ""
    question = ""

    config = ConfigParser.ConfigParser()
    try:
        config.read(configfile)
    except (IOError, OSError):
        sys.stderr.write("Error opening config file " + str(configfile))
        sys.exit(1)

    configSections = config.sections()
    for sec in configSections:
        if platform.system() == sec:
            todo = config.get(sec, 'todo')
            question = config.get(sec, 'question')

    return (todo, question)

# 功能：判断该文件是否修改过，返回真，说明修改过
def fileWasModified(filename):
    try:
        file = open(filename, 'r')
    except IOError:
        sys.stderr.write("open " + filename + " Error")
        sys.exit(1)
    config = ConfigParser.ConfigParser()
    try:
        config.read(configfile)
    except (IOError, OSError):
        sys.stderr.write("Error opening config file " + str(configfile))
        sys.exit(1)

    configSections = config.sections()
    for sec in configSections:
        if platform.system() == sec:
            try:
                old_md5 = config.get(sec, filename.replace(':', '>') + '_md5', '1')
            except ConfigParser.NoOptionError:
                old_md5 = '1'

    return md5.new(file.read()).hexdigest() != old_md5

# 功能：保存文件md5
def saveMD5(filename):
    file = open(filename, 'r')
    config = ConfigParser.ConfigParser()
    # 设置为大小写敏感
    config.optionxform = str
    try:
        config.read(configfile)
    except (IOError, OSError):
        sys.stderr.write("Error opening config file " + str(configfile))
        sys.exit(1)
    config.set(platform.system(), filename.replace(':', '>') + '_md5', md5.new(file.read()).hexdigest())
    config.write(open(configfile, "w"))

def main():
    # 获得相应平台要处理的文件名
    (todo_filename, question_filename) = getFilenames()
    # 检查文件是否修改过
    if fileWasModified(todo_filename):
        clean.clean(db_name, todo_tablename, todo_filename)
        saveMD5(todo_filename)
        print("clean todo up!")
    else:
        print("todo is clean!")
    if fileWasModified(question_filename):
        clean.clean(db_name, question_tablename, question_filename)
        saveMD5(question_filename)
        print("clean question up!")
    else:
        print("question is clean!")

if __name__ == "__main__":
    main()
