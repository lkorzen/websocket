#!/usr/bin/env python

import socket, struct, threading, cgi
import handshake

def decode_char (data, data_length):
	#turn byte data into string
	byte_array = [ord(character) for character in data]
	index_first_mask = 2 
	if data_length >= 126 and data_length <= 65535:
		index_first_mask = 4
	elif data_length > 65535:
		index_first_mask = 10
	masks = [m for m in byte_array[index_first_mask : index_first_mask + 4]]
	index_first_data = index_first_mask + 4
	decoded_chars = []
	i = index_first_data
	j = 0
	while i < len(byte_array):
		decoded_chars.append( chr(byte_array[i] ^ masks[j % 4]) )
		i += 1
		j += 1
	return ''.join(decoded_chars)

def determine_length (data):
	#determine message length from first bytes
	byte_array = []
	byte_array = [ord(d) for d in data[:10]]
	data_length = byte_array[1] & 127
	if data_length == 126:
		data_length = (byte_array[2] & 255) * 2**8
		data_length += byte_array[3] & 255
	elif data_length == 127:
		data_length = (byte_array[2] & 255) * 2**56
		data_length += (byte_array[3] & 255) * 2**48
		data_length += (byte_array[4] & 255) * 2**40
		data_length += (byte_array[5] & 255) * 2**32
		data_length += (byte_array[6] & 255) * 2**24
		data_length += (byte_array[7] & 255) * 2**16
		data_length += (byte_array[8] & 255) * 2**8
		data_length += byte_array[9] & 255
	return data_length

def recv_data (client, length):
	#receive data from websocket
	#print "xxxxxx before recv"
	data = client.recv(length)
	#print "xxxxxx after recv"	
	if not data: return data
	#print "xxxxxxbefore data_length"
	data_length = determine_length(data)
	#print "xxxxxx data_length", data_length
	while data_length > length:
		data += client.recv(length)
		data_length -= length
		#print "data_length", data_length
	#print "xxxxxx after data_length"
	#print "xxxxxx before decode_char"
	message = decode_char(data, data_length)
	#print "xxxxxx after decode_char"
	print "Message received:", message
	return message

def send_data (client, data):
	#send data through websocket
	message = encode_char(data)
	print "Message sent:", data
	return client.send(message)

def encode_char (string):
	#turn string values into opererable numeric byte values
	#print "xxxxxx encode char"
	byte_array = [ord(character) for character in string]
	#print "byte_array", byte_array
	data_length = len(byte_array)
	#print "data_length", data_length
	bytes_formatted = []
	bytes_formatted.append(129)
	if data_length <= 125:
		bytes_formatted.append(data_length)
	elif data_length >= 126 and data_length <= 65535:
		bytes_formatted.append(126)
		bytes_formatted.append( (data_length >> 8) & 255)
		bytes_formatted.append( data_length & 255)
	else:
		bytes_formatted.append(127)
		bytes_formatted.append( (data_length >> 56) & 255)
		bytes_formatted.append( (data_length >> 48) & 255)
		bytes_formatted.append( (data_length >> 40) & 255)
		bytes_formatted.append( (data_length >> 32) & 255)
		bytes_formatted.append( (data_length >> 24) & 255)
		bytes_formatted.append( (data_length >> 16) & 255)
		bytes_formatted.append( (data_length >> 8) & 255)
		bytes_formatted.append( data_length & 255)
	bytes_formatted.extend(byte_array)
	#print "bytes_formatted", bytes_formatted
	return struct.pack('B'*len(bytes_formatted), *bytes_formatted)

def handle (client, addr):
	#handle websocket connection
	handshake.handshake(client)
	lock = threading.Lock()
	while 1:
		#data = recv_data(client, 128)
		data = recv_data(client, 4096)
		if not data: break
		data = cgi.escape(data)
		lock.acquire()
		[send_data(c, data) for c in clients]
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

#######################################
def test_determine_length(data):
	#test function that tests determine_length function
	data_length = data[1] & 127
	if data_length == 126:
		data_length = (data[2] & 255) * 2**8
		data_length += data[3] & 255
	elif data_length == 127:
		data_length = (data[2] & 255) * 2**56
		data_length += (data[3] & 255) * 2**48
		data_length += (data[4] & 255) * 2**40
		data_length += (data[5] & 255) * 2**32
		data_length += (data[6] & 255) * 2**24
		data_length += (data[7] & 255) * 2**16
		data_length += (data[8] & 255) * 2**8
		data_length += data[9] & 255
	return data_length

def create_table(number):
	#helper test function that creates websocket first bytes
	array = []
	array.append(129)
	if number <= 125:
		array.append(number)
	elif number >= 126 and number <= 65535:
		array.append(126)
		array.append( (number >> 8) & 255)
		array.append( number & 255)
	else:
		array.append(127)
		array.append( (number >> 56) & 255)
		array.append( (number >> 48) & 255)
		array.append( (number >> 40) & 255)
		array.append( (number >> 32) & 255)
		array.append( (number >> 24) & 255)
		array.append( (number >> 16) & 255)
		array.append( (number >> 8) & 255)
		array.append( number & 255)
	return array

def test():
	#test function
	x = create_table(100)
	print "100", x, test_determine_length(x)
	x = create_table(160)
	print "160", x, test_determine_length(x)
	x = create_table(300)
	print "300", x, test_determine_length(x)
	x = create_table(600)
	print "600", x, test_determine_length(x)
	x = create_table(2000)
	print "2000", x, test_determine_length(x)
	x = create_table(20000)
	print "20000", x, test_determine_length(x)
	x = create_table(200000)
	print "200000", x, test_determine_length(x)
	x = create_table(2000000)
	print "2000000", x, test_determine_length(x)
	x = create_table(20000000)
	print "20000000", x, test_determine_length(x)
	x = create_table(200000000)
	print "200000000", x, test_determine_length(x)
	x = create_table(2000000000)
	print "2000000000", x, test_determine_length(x)
	x = create_table(20000000000)
	print "20000000000", x, test_determine_length(x)
	x = create_table(200000000000)
	print "200000000000", x, test_determine_length(x)
	x = create_table(2000000000000)
	print "2000000000000", x, test_determine_length(x)
	x = create_table(20000000000000)
	print "20000000000000", x, test_determine_length(x)
	x = create_table(200000000000000)
	print "200000000000000", x, test_determine_length(x)
	x = create_table(2000000000000000)
	print "2000000000000000", x, test_determine_length(x)
	x = create_table(20000000000000000)
	print "20000000000000000", x, test_determine_length(x)
	x = create_table(200000000000000000)
	print "200000000000000000", x, test_determine_length(x)
	x = create_table(2000000000000000000)
	print "2000000000000000000", x, test_determine_length(x)
	pass

test()