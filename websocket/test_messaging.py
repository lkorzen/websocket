# Websocket messaging test module, testable with py.test

import messaging, struct

def generate_byte_message(length, masked):
	#helper function that generates websocket byte message 'length' long
	#add masks if data is suppose to be received from client to server
	#skip adding masks if data is suppose to be sent from server to client
	array = []
	masks = [30, 140, 144, 6]
	index_first_mask = 2
	array.append(129)
	if length <= 125:
		array.append(length)
	elif length >= 126 and length <= 65535:
		index_first_mask = 4
		array.append(126)
		array.append( (length >> 8) & 255)
		array.append( length & 255)
	else:
		index_first_mask = 10
		array.append(127)
		array.append( (length >> 56) & 255)
		array.append( (length >> 48) & 255)
		array.append( (length >> 40) & 255)
		array.append( (length >> 32) & 255)
		array.append( (length >> 24) & 255)
		array.append( (length >> 16) & 255)
		array.append( (length >> 8) & 255)
		array.append( length & 255)
	index_first_data = index_first_mask + 4
	j = 0
	if masked:
		array.extend(masks)
		i = index_first_data
		k = len(array) + length
		while i < k:
			array.append( ord('a') ^ masks[j % 4])
			i += 1
			j += 1
	else:
		while j < length:
			array.append(ord('a'))
			j += 1
	return struct.pack('B'*len(array), *array)

def generate_string(length):
	#helper function that generates string 'length' long
	array = []
	i = 0
	while i < length:
		array.append('a')
		i += 1
	return ''.join(array)

def test_determine_length():
	assert messaging.determine_length(data1) == 1
	assert messaging.determine_length(data10) == 10
	assert messaging.determine_length(data160) == 160
	assert messaging.determine_length(data500) == 500
	assert messaging.determine_length(data1000) == 1000
	assert messaging.determine_length(data100000) == 100000
	assert messaging.determine_length(data1000000) == 1000000

def test_decode_char():
	assert messaging.decode_char(masked_data1, 1) == string1
	assert messaging.decode_char(masked_data10, 10) == string10
	assert messaging.decode_char(masked_data160, 160) == string160
	assert messaging.decode_char(masked_data500, 500) == string500
	assert messaging.decode_char(masked_data1000, 1000) == string1000
	assert messaging.decode_char(masked_data100000, 100000) == string100000
	assert messaging.decode_char(masked_data1000000, 1000000) == string1000000

def test_encode_char():
	assert messaging.encode_char(string1) == data1
	assert messaging.encode_char(string10) == data10
	assert messaging.encode_char(string160) == data160
	assert messaging.encode_char(string500) == data500
	assert messaging.encode_char(string1000) == data1000
	assert messaging.encode_char(string100000) == data100000
	assert messaging.encode_char(string1000000) == data1000000

#helper data
data1 = generate_byte_message(1, False) # 1 B
masked_data1 = generate_byte_message(1, True)
string1 = generate_string(1)
data10 = generate_byte_message(10, False) # 10 B
masked_data10 = generate_byte_message(10, True)
string10 = generate_string(10)
data160 = generate_byte_message(160, False) # 160 B
masked_data160 = generate_byte_message(160, True)
string160 = generate_string(160)
data500 = generate_byte_message(500, False) # 500 B
masked_data500 = generate_byte_message(500, True)
string500 = generate_string(500)
data1000 = generate_byte_message(1000, False) # 1 KB
masked_data1000 = generate_byte_message(1000, True)
string1000 = generate_string(1000)
data100000 = generate_byte_message(100000, False) # 100 KB
masked_data100000 = generate_byte_message(100000, True)
string100000 = generate_string(100000)
data1000000 = generate_byte_message(1000000, False) # 1 MB
masked_data1000000 = generate_byte_message(1000000, True)
string1000000 = generate_string(1000000)
# data10000000 = generate_byte_message(10000000, False) # 10 MB
# string10000000 = generate_string(10000000)