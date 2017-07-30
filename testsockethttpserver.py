#!/usr/bin/env python
# -*- coding:utf-8 -*-

#服务器端

import sys
import socket   #socket模块

BUF_SIZE = 1024  #设置缓冲区大小
server_addr = ('127.0.0.1', 8888)  #IP和端口构成表示地址
try :
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #生成一个新的socket对象
except socket.error, msg :
    print "Creating Socket Failure. Error Code : " + str(msg[0]) + " Message : " + msg[1]
    sys.exit()
print "Socket Created!"
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #设置地址复用
try : 
    server.bind(server_addr)  #绑定地址
except socket.error, msg :
  print "Binding Failure. Error Code : " + str(msg[0]) + " Message : " + msg[1]
  sys.exit()
print "Socket Bind!"
server.listen(5)  #监听, 最大监听数为5
print "Socket listening"

i = 0;

while True:
	
	client, client_addr = server.accept()  #接收TCP连接, 并返回新的套接字和地址, 阻塞函数
	print 'Connected by', client_addr
	
	while True:
		data = client.recv(BUF_SIZE)
		print data
		if((not data) or len(data) < BUF_SIZE):
			break
	
	response_body_raw ='''
<html>
<body>
	<h1>request info</h1>
	<hr/>
	%s
</body>
</html>
''' % data.replace('\n','<br/>')
	
	response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(response_body_raw),
            'Connection': 'close',
        }

	response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                                response_headers.iteritems())

	# Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
	response_proto = 'HTTP/1.1'
	response_status = '200'
	response_status_text = 'OK' # this can be random

	# sending all this stuff
	client.send('%s %s %s' % (response_proto, response_status, \
													response_status_text))
	client.send(response_headers_raw)
	client.send('\n') # to separate headers from body
	client.send(response_body_raw)
	
	client.close()
server.close()