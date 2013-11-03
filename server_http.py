#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import threading
import signal
from websocket.server_websocket import start_websocket_server

def start_http_server():
	PORT = 8000
	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), handler)
	print "Serving HTTP at port", PORT
	while keep_running():
		httpd.handle_request()

KEEP_RUNNING = True

def signal_handler(signal, frame):
	print 'Ctrl+C pressed. Stopping HTTP Server'
	global KEEP_RUNNING
	KEEP_RUNNING = False

def keep_running():
    return KEEP_RUNNING

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	threading.Thread(target=start_http_server).start()
	start_websocket_server()