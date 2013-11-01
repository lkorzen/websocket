#!/usr/bin/env python

import socket, threading, cgi
import websocket_messaging
import handshake

def handle (client, addr):
	#handle websocket connection
	handshake.handshake(client)
	lock = threading.Lock()
	while 1:
		data = websocket_messaging.recv_data(client, 4096)
		if not data: break
		data = cgi.escape(data)
		lock.acquire()
		[websocket_messaging.send_data(c, data) for c in clients]
		lock.release()
	print 'Client closed:', addr
	lock.acquire()
	clients.remove(client)
	lock.release()
	client.close()
	
def start_server ():
	print "Server started"
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('', 9876))
	s.listen(5)
	while 1:
		conn, addr = s.accept()
		print 'Connection from:', addr
		clients.append(conn)
		threading.Thread(target = handle, args = (conn, addr)).start()

clients = []
if __name__ == "__main__":
	start_server()