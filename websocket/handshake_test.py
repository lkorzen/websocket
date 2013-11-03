# Handshake test module, testable with py.test

import handshake

def test_create_hash():
	assert handshake.create_hash('x3JJHMbDL1EzLkh9GBhXDw==') == 'HSmrc0sMlYUkAGmm5OPpG2HaGWk='
	assert handshake.create_hash('VSk9BY6OLzHFqpv/8P9hAA==') == 'nsPt1+hbmFq/BDb1BufPnmtlslI='

headers = { 'Origin': 'http://localhost:8080', 'Upgrade': 'websocket', 'Sec-WebSocket-Extensions': 'x-webkit-deflate-frame', 'Sec-WebSocket-Version': '13', 'Sec-WebSocket-Protocol': 'myprotocol', 'Host': 'localhost:9876', 'Sec-WebSocket-Key': 'VSk9BY6OLzHFqpv/8P9hAA==', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36', 'Connection': 'Upgrade', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache' }

def test_parse_headers():
	data = 'GET /stuff HTTP/1.1\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nHost: localhost:9876\r\nOrigin: http://localhost:8080\r\nSec-WebSocket-Protocol: myprotocol\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nSec-WebSocket-Key: VSk9BY6OLzHFqpv/8P9hAA==\r\nSec-WebSocket-Version: 13\r\nSec-WebSocket-Extensions: x-webkit-deflate-frame\r\nUser-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36\r\n'
	assert handshake.parse_headers(data) == headers

def test_create_response():
	response = 'HTTP/1.1 101 WebSocket Protocol Handshake\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: nsPt1+hbmFq/BDb1BufPnmtlslI=\r\nSec-WebSocket-Protocol: myprotocol\r\n\r\n'
	assert handshake.create_response(headers) == response