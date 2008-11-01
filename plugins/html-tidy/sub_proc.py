# Copyright (C) 2007 Ami Tavory (atavory@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, 
# Boston, MA 02111-1307, USA.



"""
Wrapper around Python's subprocess.
"""


import unittest
import subprocess
import select
import threading
import os
import log_utils
import copy



_buf_size = 1024



def _to_none_if_empty(text):
	if text == '':
		return None
		
	return text



def _make_select_list(read_txt, err_txt, out_fd, err_fd):
	select_list = []
	
	if read_txt != '':
		select_list.append(out_fd)
	if err_txt != '':
		select_list.append(err_fd)

	return select_list



class proc_dispatch:
	def __init__ (self, args, read_fn, err_fn, done_fn, except_fn):
		self._args = args
		self._read_fn = read_fn
		self._err_fn = err_fn
		self._except_fn = except_fn		
		self._done_fn = done_fn
			
		
	def run(self):
		log_utils.debug('proc_dispatch::run running popen')
	
		self._pr = subprocess.Popen(self._args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
		
		log_utils.debug('proc_dispatch::run ran running popen; running select loop')

		self._select_loop()		
		
		log_utils.debug('proc_dispatch::run left select loop; calling done fn')
		
		self._done_fn()
		
		log_utils.debug('proc_dispatch::run left select loop; called done fn')


	def _select_loop(self):
		out_fd = self._pr.stdout.fileno()
		err_fd = self._pr.stderr.fileno()
		
		read_txt = 'dummy'
		err_txt = 'dummy'

		while True:
			select_list = _make_select_list(read_txt, err_txt, out_fd, err_fd)
			
			if select_list == []:
				return

			read_list, write_list, except_list = select.select(select_list, [], select_list)
			
			assert write_list == [], str(write_list)
			
			assert except_list == []
			
			for fd in except_list:
				log_utils.warn('proc_dispatch::select_loop calling except function')
				self._except_fn()
				
				return
	
			if out_fd in read_list:
				log_utils.debug('proc_dispatch::select_loop calling read function')
				read_txt = os.read(out_fd,  _buf_size)
				self._read_fn(_to_none_if_empty(read_txt))
				
			if	err_fd in read_list:
				log_utils.debug('proc_dispatch::select_loop calling err function')
				err_txt = os.read(err_fd, _buf_size)
				self._err_fn(_to_none_if_empty(err_txt))					
				
				
				
class _on_readline:
	def __init__(self, cb):
		self._cb = cb
		self._text = ''
		self._none_reached = False
		
		
	def on_read(self, text):
		assert self._none_reached == False
		
		if text == None:
			self._none_reached = True
		
			self._cb(_to_none_if_empty(self._text))
			
			return
	
		self._text = self._text + text		
		
		while self._text.find('\n') != -1:
			newline_pos = self._text.find('\n')
		
			self._cb(self._text[0: newline_pos])
			
			self._text = self._text[newline_pos + 1: ]
				
				

def make_on_line_cb(fn):
	return _on_readline(fn).on_read



class _on_done:
	def __init__(self, cb):
		self._cb = cb
		self._text = ''
		self._none_reached = False
		
		
	def on_read(self, text):
		assert self._none_reached == False
		
		if text == None:
			self._none_reached = True
		
			self._cb(_to_none_if_empty(self._text))
			
			return
	
		self._text = self._text + text		
		

				
def make_on_done_cb(fn):
	return _on_done(fn).on_read



class test(unittest.TestCase):		
	class _on_readline_helper:
		def __init__(self):
			self.lines = []
			
			
		def on_readline(self, line):
			if line != None:
				self.lines.append(line)
			
			
	def _test_readline(self, notifications, lines):
		
		assert len(notifications) == len(lines)
		
		h = self._on_readline_helper()		
		f = make_on_line_cb(h.on_readline)
		
		for i in range(1, len(lines)):
			tmp = copy.copy(lines[i - 1])
			tmp.extend(lines[i])
			lines[i] = tmp
			
		for i in range(len(notifications)):					
			f(notifications[i])
		
			self.assertEqual(lines[i], h.lines)
		
		
	def test_readline(self):
		self._test_readline([], [])
		self._test_readline([None], [[]])		
		self._test_readline([''], [[]])
		self._test_readline(['hello'], [[]])
		self._test_readline(['hello\n'], [['hello']])
		self._test_readline(['hello', '\n'], [[], ['hello']])
		self._test_readline(['hello', '\n', 'world\n'], [[], ['hello'], ['world']])
		self._test_readline(['hello', '\n', 'world', None], [[], ['hello'], [], ['world']])
		self._test_readline(['hello', '\n', 'world\nyeah', '\n'], [[], ['hello'], ['world'], ['yeah']])
		self._test_readline(['hello', '\n', 'world\nyeah', '\n', None], [[], ['hello'], ['world'], ['yeah'], []])
		self._test_readline(['hello', '\n', 'world\nyeah\n'], [[], ['hello'], ['world', 'yeah']])
				
		

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()
