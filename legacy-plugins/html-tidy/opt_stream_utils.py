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
Utilities for converting between a stream and an options dictionary.
"""


import unittest
import gen_utils
import log_utils
import consts
import string
import os
import StringIO
import ex



def _is_empty_line(line):
	return line.strip() == ''
	
	
	
def _is_comment_line(line):
	stripped_line = line.strip()
	
	if len(stripped_line) < 2:
		return False
		
	return stripped_line[0: 2] == '//'
	

def _is_def_line(line):
	return len(line.split(':')) == 2
	


def _content_lines(lines):
	content_lines = []
	
	for line in lines:
		if not _is_empty_line(line) and not _is_comment_line(line):
			content_lines.append(line)
			
	return content_lines



def _unsplit_lines(lines):
	if len(lines) == 0:
		return []

	unsplit_lines = [lines[0]]

	for line in lines[1: ]:
		if _is_def_line(line):
			unsplit_lines.append(line)
		else:
			unsplit_lines[-1] = unsplit_lines[-1] + ' %s' % line
			
	return unsplit_lines
		
		
		
def _parse_line(line):
	log_utils.debug('parsing %s' % line)
	
	if not _is_def_line(line):
		raise ex.error('cannot parse %s' % line)
	
	split = line.split(':')
	
	assert len(split) == 2, split
		
	(key, val) = (split[0].strip(), split[1].strip())
	
	log_utils.debug('parsed %s->%s' % (key, val))
	
	return (key, val)
	


def opt_stream_to_dict(s):
	"""
	Transforms a stream of lines of the form x: y into a dictionary where x->y.

	Keyword arguments:
    s -- The stream
	"""
	lines = s.readlines()		
		
	content_lines = _content_lines(lines)
	
	unsplit_lines = _unsplit_lines(content_lines)
	
	d = {}
					
	try:		
		for line in unsplit_lines:
			(key, val) = _parse_line(line)
			
			d[key] = val
	except:
		raise ex.error('cannot parse!')
	
	return d
	


def dict_to_opt_stream(d, s):
	"""
	Transforms a dictionary where x->y to a stream of lines of the form x: y.
	
	Keyword arguments:
	d -- The dictionary.
	s -- The stream.
	"""
	for (name, val) in d.items():
		s.write('%s: %s\n' % (name, val))



class test(unittest.TestCase):		
	def test_dict_to_opt_stream(self):
		d = {'a' : 1}
		s = StringIO.StringIO()
		
		dict_to_opt_stream(d, s)
	
		self.assertEquals(s.getvalue(), 'a: 1\n')
		
		
	def test_is_empty_line(self):
		self.assertEquals(_is_empty_line(''), True)
		self.assertEquals(_is_empty_line('\n'), True)
		self.assertEquals(_is_empty_line('\t\n'), True)
		self.assertEquals(_is_empty_line('dd\n'), False)
		
				
	def test_is_comment_line(self):
		self.assertEquals(_is_comment_line('// ddd'), True)
		self.assertEquals(_is_comment_line('// ddd\n'), True)
		self.assertEquals(_is_comment_line('\t\t// ddd'), True)
		self.assertEquals(_is_comment_line('bib// ddd'), False)
		
		
	def test_content_lines(self):
		self.assertEquals(_content_lines(['dd']), ['dd'])
		self.assertEquals(_content_lines(['dd', 'yy']), ['dd', 'yy'])
		self.assertEquals(_content_lines(['', 'dd', 'yy']), ['dd', 'yy'])
		self.assertEquals(_content_lines(['// Testing, testing', 'dd', 'yy']), ['dd', 'yy'])
		
		
	def test_unsplit_lines(self):
		self.assertEquals(_unsplit_lines(['dd: ']), ['dd: '])
		self.assertEquals(_unsplit_lines(['dd: ', 'ff']), ['dd:  ff'])
		
	
	def test_parse_line(self):
		self.assertEquals(_parse_line('dd: ff'), ('dd', 'ff'))
		self.assertEquals(_parse_line('dd: '), ('dd', ''))


	def _test_opt_stream_to_dict(self, f_name, required_num, required_dict):
		f = open(f_name, 'r')
		d = opt_stream_to_dict(f)
		f.close()
		
		self.assertEqual(len(d), required_num)
		
		for (key, val) in required_dict.items():
			self.assert_(d.has_key(key))
			self.assertEqual(d[key], required_dict[key])
	

	def test_opt_stream_to_dict_0(self):
		f_name = os.path.join(gen_utils.data_dir(), consts.opt_names_to_f_names['misc_opts'])
		
		required_dict = {
			'write-back': 'no',
			'gnu-emacs-file': ''}
		
		self._test_opt_stream_to_dict(f_name, 10, required_dict)


	def test_opt_stream_to_dict_1(self):
		f_name = os.path.join(gen_utils.data_dir(), 'sample_tidy_config.txt')
		
		required_dict = {
			'indent': 'auto',
			'indent-spaces': '2',
			'wrap': '72',
			'markup': 'yes',
			'output-xml': 'no',
			'input-xml': 'no',
			'show-warnings': 'yes',
			'numeric-entities': 'yes',
			'quote-marks': 'yes',
			'quote-nbsp': 'yes',
			'quote-ampersand': 'no',
			'break-before-br': 'no',
			'uppercase-tags': 'no',
			'uppercase-attributes': 'no',
			'char-encoding': 'latin1',
			'new-inline-tags': 'cfif, cfelse, math, mroot, \n   mrow, mi, mn, mo, msqrt, mfrac, msubsup, munderover,\n   munder, mover, mmultiscripts, msup, msub, mtext,\n   mprescripts, mtable, mtr, mtd, mth',
			'new-blocklevel-tags': 'cfoutput, cfquery',
			'new-empty-tags': 'cfelse'}
		
		self._test_opt_stream_to_dict(f_name, 18, required_dict)
	
		
	def test_dict_to_opt_stream(self):
		d = {'a' : 1}
		s = StringIO.StringIO()
		
		dict_to_opt_stream(d, s)
	
		self.assertEquals(s.getvalue(), 'a: 1\n')
		
		
		
def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()
