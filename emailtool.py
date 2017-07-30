#!/usr/bin/python
#coding=utf-8

#@author:dongluan
#@date:2012-06-06
#@version:1.0
#@description: auto sending email with attachment file

import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
import logging
import sys
import datetime
import os

reload(sys)
sys.setdefaultencoding('utf8')

mailDict = {} #邮件配置信息

###################
#日志辅助类
#################
class Logger:
    LOG_RELEASE= 'releae'
    LOG_RELEASE_FILE = '/data/nuomi/pyMail/%s.log' % str(datetime.date.today())

    def __init__(self, log_type):
        self._logger = logging.getLogger(log_type)
        if log_type == Logger.LOG_RELEASE:
            self._logFile = Logger.LOG_RELEASE_FILE
        handler = logging.FileHandler(self._logFile)
        if log_type == Logger.LOG_RELEASE:
            formatter = logging.Formatter('%(asctime)s ********* %(message)s')
        else:
            formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def log(self, msg):
        if self._logger is not None:
            self._logger.info(msg)

MyLogger = Logger(Logger.LOG_RELEASE) #Logger
#初始化邮件配置信息
#参数要是没有value就放空
def initMailConf(msg_dict):
    global mailDict
    
    mailDict['server'] = 'edm.sys.baidu.com:25'
    mailDict['user'] = 'nuomi.no.reply'
    mailDict['password'] = ''
    

    mailDict['from'] = 'nuomi.no.reply'
    mailDict['to'] = msg_dict['to']
    mailDict['subject']  = msg_dict['subject']
    mailDict['text'] = msg_dict['text']
    mailDict['html'] = msg_dict['html']
    mailDict['path'] = msg_dict['path']
    
def sendMail(paramMap):#发送邮件
    smtp = smtplib.SMTP()
    msgRoot = MIMEMultipart('related')
    msgAlternative = MIMEMultipart('alternative')
    if paramMap.has_key('server') and paramMap.has_key('user') and paramMap.has_key('password'):
        try:
            smtp.set_debuglevel(1)
            smtp.connect(paramMap['server'])
            #smtp.login(paramMap['user'], paramMap['password'])
        except Exception, e:
            MyLogger.log('smtp login exception!')
            return False
    else:
        MyLogger.log('Parameters incomplete!')
        return False

    if paramMap.has_key('subject') == False or  paramMap.has_key('from')== False or paramMap.has_key('to') == False:
        MyLogger.log('Parameters incomplete!')
        return False
    msgRoot['subject'] = paramMap['subject']
    msgRoot['from'] = paramMap['from']
    if paramMap.has_key('cc'):
        msgRoot['cc'] = paramMap['cc']
    msgRoot['to'] = paramMap['to']
    msgRoot.preamble = 'This is a multi-part message in MIME format.' 
    msgRoot.attach(msgAlternative)
    TempAddTo = paramMap['to']
    if paramMap.has_key('text') and paramMap['text'] != '':
        msgText = MIMEText(paramMap['text'], 'plain', 'utf-8')
        msgAlternative.attach(msgText)
    if paramMap.has_key('html') and paramMap['html'] != '':
        msgText = MIMEText(paramMap['html'], 'html', 'utf-8')
        msgAlternative.attach(msgText)  
    if paramMap.has_key('image') and paramMap['image'] != '':
        fp = open(paramMap['image'], 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>' )
        msgRoot.attach(msgImage) 
    if paramMap.has_key('cc'):
        TempAddTo = paramMap['to'] + ',' + paramMap['cc']   
    if TempAddTo.find(',') != -1:
        FinallyAdd = TempAddTo.split(',')
    else:
        FinallyAdd = TempAddTo 
        
    #构造附件
    fileName = paramMap['path']
    basename = os.path.basename(fileName)
    if os.path.exists(fileName) and fileName != '': #数据文件存在
        data = open(fileName, 'rb')
        att = MIMEText(data.read(), 'base64', 'gb2312')
        att['Content-Type'] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment; filename="%s"' % basename
        msgRoot.attach(att)
    smtp.sendmail('', FinallyAdd, msgRoot.as_string())
    smtp.quit()  
    return True
     
def process(msg_dict):
    global mailDict
    initMailConf(msg_dict)
    sendMail(mailDict)

def main():
    msg = sys.argv[1]
    msg_dict=eval(msg)
    process(msg_dict)
    
if __name__ == '__main__':
    main()
