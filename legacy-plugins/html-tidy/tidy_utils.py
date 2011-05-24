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
Utility facade for HTML Tidy - just the tidying part.
"""



import os
import unittest
import log_utils
import gen_utils
import tidy_opt_utils
import consts
import commands
import re



class tidy_report:
	__slots__ = ['line', 'col', 'type_', 'what']


	def __init__(self, line, col, type_, what):
		self.line = line
		self.col = col
		self.type_ = type_
		self.what = what 



_line_col_report_re = re.compile('line (\d+) column (\d+) - (\w+): (.*)')
_no_line_col_report_re = re.compile('(\w+): (.*)')



def is_valid_type(type_):
	return type_ in ['Info', 'Error', 'Warning', 'Config']

		

def tidy_report_from_line(line):
	m = _line_col_report_re.match(line)
	
	if m:
		line = int(m.group(1))
		col = int(m.group(2))
		type_ = m.group(3)
		what = m.group(4)			
		
		if is_valid_type(type_):
			return tidy_report(line, col, type_, what)
			
	m = _no_line_col_report_re.match(line)
	
	if m:
		type_ = m.group(1)
		what = m.group(2)			
		
		if is_valid_type(type_):
			return tidy_report(None, None, type_, what)
	
	return None
	
	

def tidy_the_stuff(text, tidy_dict):
	tmp_input_f_name = os.path.join(gen_utils.data_dir(), consts.tmp_input_f_name)
	tmp_output_f_name = os.path.join(gen_utils.data_dir(), consts.tmp_output_f_name)

	log_utils.debug('tidying')	
	
	f = open(tmp_input_f_name, 'w')
	f.write(text)
	f.close()
	
	cmd_str = 'tidy %s %s 2> %s' % (tidy_opt_utils.dict_to_str(tidy_dict),
		tmp_input_f_name,
		tmp_output_f_name)
		
	log_utils.debug(cmd_str)
	
	(stat, out) = commands.getstatusoutput(cmd_str)
		
	log_utils.debug('tidied')
	
	log_utils.debug('generating report items')
	
	f = open(tmp_output_f_name, 'r')
	lines = f.readlines()
	f.close()

	errs = [tidy_report_from_line(line) for line in lines]
	errs = [e for e in errs if e != None]
		
	log_utils.debug('generated report items')
	
	return (out, errs)



class test(unittest.TestCase):		
	def _test_tidy_report_from_line(self, line, expected):
		e  = tidy_report_from_line(line)
		
		self.assertEqual(e.line, expected.line)
		self.assertEqual(e.col, expected.col)
		self.assertEqual(e.type_, expected.type_)
		self.assertEqual(e.what, expected.what)


	def test_tidy_report_from_line(self):
		self._test_tidy_report_from_line('line 1 column 1 - Warning: inserting missing \'title\' element', tidy_report(1, 1, 'Warning', 'inserting missing \'title\' element'))
		

	def test_tidy_the_stuff_0(self):
		opts_dict = 	tidy_opt_utils.names_dicts_to_dict(tidy_opt_utils.default_names_dicts())
		
		(d, tidy_reports) = tidy_the_stuff('', opts_dict)
		
		self.assert_(len(tidy_reports) != 0)

		
	def test_tidy_the_stuff_1(self):		
		f_name = os.path.join(gen_utils.data_dir(), 'bad_tidy_config.txt')		
		opts_dict = 	tidy_opt_utils.read_dict(f_name)
		
		(d, tidy_reports) = tidy_the_stuff('', opts_dict)
		
		self.assert_(len(tidy_reports) != 0)
		


def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()
