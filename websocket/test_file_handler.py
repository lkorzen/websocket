# File handler test module, testable with py.test

import os
import file_handler

def create_file(file_name):
	#helper function that creates a test text file
	try:
		f = open(file_name, 'w')
		f.write('some sample text\nsome second line\nand some third\n')
		f.close()
	except IOError:
		print 'File creating error: ', file_name

def test_load_file():
	create_file('text.txt')
	assert file_handler.load_file('text.txt') == 'some sample text\nsome second line\nand some third\n'
	os.remove('text.txt')
	assert file_handler.load_file('not_exist.txt') == 'No such file or directory: not_exist.txt'

def test_check_for_file():
	assert file_handler.check_for_file('sample text') == None
	assert file_handler.check_for_file('sample text file some') == None
	assert file_handler.check_for_file('sample text file: some text') == None
	assert file_handler.check_for_file('sample text file: file some text') == None
	assert file_handler.check_for_file('sample text file: file. some text') == None
	assert file_handler.check_for_file('sample text file: file.txt some text') == 'file.txt'