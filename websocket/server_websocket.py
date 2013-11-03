# Module that starts websocket server

import socket, threading, cgi
import messaging
import handshake
import file_handler

def handle (client, addr):
	#handle websocket connection
	handshake.handshake(client)
	lock = threading.Lock()
	while 1:
		data = messaging.recv_data(client, 4096)
		if not data: break
		data = cgi.escape(data)
		file_name = file_handler.check_for_file(data)
		if file_name:
			data = file_handler.load_file(file_name)
		lock.acquire()
		[messaging.send_data(c, data) for c in clients]
		lock.release()
	print 'Client closed:', addr
	lock.acquire()
	clients.remove(client)
	lock.release()
	client.close()

def start_websocket_server ():
	#start websocket server
	print "Websocket server started"
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('', 9876))
	s.listen(5)
	while 1:
		conn, addr = s.accept()
		print 'Connection from:', addr
		clients.append(conn)
		threading.Thread(target = handle, args = (conn, addr)).start()
	s.close()
	print "Socket closed"

clients = []

if __name__ == "__main__":
	start_websocket_server()