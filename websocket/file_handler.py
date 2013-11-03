# Module that opens a file and passes its content

import re

def load_file(file_name):
	try:
		f = open(file_name, 'r')
		message = f.read()
		f.close()
	except IOError:
		message = 'No such file or directory: ' + file_name
	return message

def check_for_file(message):
	file_name = re.search(r'file: (\w+\.\w+)', message)
	if file_name:
		return file_name.group(1)
	else:
		return None