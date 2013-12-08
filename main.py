#! /bin/env python2
# coding=utf-8

import sys
import ConfigParser
import platform
import md5
import os
import logging

config_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(config_dir)

import clean

configfile = os.path.join(config_dir, "clean.ini")
db_name = os.path.join(config_dir, "clean.db")
todo_tablename = "TB_Todo"
question_tablename = 'TB_Question'


def getFilenames():
    '功能：根据操作系统，读取clean.ini，返回相应待处理的文件名'
    todo = ""
    question = ""

    config = ConfigParser.ConfigParser()
    try:
        config.read(configfile)
    except (IOError, OSError):
        logging.error("Error opening config file " + str(configfile))
        sys.exit(1)

    configSections = config.sections()
    for sec in configSections:
        if platform.system() == sec:
            todo = config.get(sec, 'todo')
            question = config.get(sec, 'question')

    return (todo, question)


def fileWasModified(filename):
    "功能：判断该文件是否修改过，返回真，说明修改过"
    try:
        file = open(filename, 'r')
    except IOError:
        logging.error("open " + filename + " Error")
        sys.exit(1)
    config = ConfigParser.ConfigParser()
    try:
        config.read(configfile)
    except (IOError, OSError):
        logging.error("Error opening config file " + str(configfile))
        sys.exit(1)

    configSections = config.sections()
    for sec in configSections:
        if platform.system() == sec:
            try:
                old_md5 = config.get(
                    sec, filename.replace(':', '>') + '_md5', '1')
            except ConfigParser.NoOptionError:
                old_md5 = '1'

    return md5.new(file.read()).hexdigest() != old_md5


def saveMD5(filename):
    '功能：保存文件md5'
    file = open(filename, 'r')
    config = ConfigParser.ConfigParser()
    # 设置为大小写敏感
    config.optionxform = str
    try:
        config.read(configfile)
    except (IOError, OSError):
        logging.error("Error opening config file " + str(configfile))
        sys.exit(1)
    config.set(platform.system(), filename.replace(':', '>')
               + '_md5', md5.new(file.read()).hexdigest())
    config.write(open(configfile, "w"))


def main():
    # 获得相应平台要处理的文件名
    (todo_filename, question_filename) = getFilenames()
    # 检查文件是否修改过
    if fileWasModified(todo_filename):
        clean.clean(db_name, todo_tablename, todo_filename)
        saveMD5(todo_filename)
        logging.info("clean todo up!")
    else:
        logging.info("todo is clean!")
    if fileWasModified(question_filename):
        clean.clean(db_name, question_tablename, question_filename)
        saveMD5(question_filename)
        logging.info("clean question up!")
    else:
        logging.info("question is clean!")

if __name__ == "__main__":
    logging.basicConfig(filename='clean.log',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    main()
