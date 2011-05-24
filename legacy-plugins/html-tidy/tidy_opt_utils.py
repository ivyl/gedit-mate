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
Utility facade for HTML Tidy - just the dictionary part.
"""



import os
import consts
import unittest
import gen_utils
import log_utils
import opt_stream_utils
import itertools
import string



def orig_to_lib_opt_rep(s):
	""" 
	Translates an option from the form used by Tidy utility to the form used by the Tidy python.
	"""
	if not gen_utils.is_string_type(s):
		return s
		
	if s == 'yes':
		return True
	elif s == 'no':
		return False

	return s
	


def lib_to_orig_opt_rep(s):
	""" 
	Translates an option from the form used by Tidy python to the form used by the Tidy utility.
	"""
	if gen_utils.is_bool_type(s):
		if s:
			return 'yes'

		return 'no'
	
	return s
	


def _opt_stream_to_dict(s):
	d = {}
	
	for (name, val) in opt_stream_utils.opt_stream_to_dict(s).items():
		d[orig_to_lib_opt_rep(name)] = orig_to_lib_opt_rep(val)	
		
	return d
	


def _dict_to_opt_stream(d, s):
	tmp_d = {}
	
	for (name, val) in d.items():
		tmp_d[lib_to_orig_opt_rep(name)] = lib_to_orig_opt_rep(val)
		
	opt_stream_utils.dict_to_opt_stream(tmp_d, s)



def default_names_dicts():
	"""
	Returns a pair-list of Tidy's default options.
	The first item in each pair is the name of the dictionary (e.g., "Diagnostics"); the second
	item in each pair is the dictionary itself.
	"""
	names = [consts.opt_names_to_logical_names[k] for k in consts.opts] 

	data_dir = gen_utils.data_dir()
	
	f_names = [os.path.join(data_dir, consts.opt_names_to_f_names[k]) for k in consts.opts]

	dicts = [_opt_stream_to_dict(open(f_name, 'r')) for f_name in f_names]	
	
	return [p for p in itertools.izip(names, dicts)]
	
	
	
def dict_to_names_dicts(d):
	"""
	Converts an options dictionary to a list of pairs of (logical category name, options dictionary within the category).
	"""
	return [(n_, gen_utils.replace_dict(d_, d)) for (n_, d_) in default_names_dicts()]



def names_dicts_to_dict(names_dicts):
	"""
	Converts a list of pairs of (logical category name, options dictionary within the category) to an options dictionary.
	"""
	return gen_utils.disjoint_dicts_union([d_ for (n_, d_) in names_dicts])



def read_dict(f_name, use_default_on_err = False):
	"""
	Returns an dictionary contained in a file.
	
	Keyword arguments:
	f_name -- File name containing the stuff.
	use_default_on_err (= True) -- Whether to return the default dict in case f_name could not be read/parsed.
	"""
	try:
		f = open(f_name, 'r')
		ret = _opt_stream_to_dict(f)
		f.close()
		
		return ret
	except Exception, inst:
		log_utils.warn(inst)
		
		if use_default_on_err:
			return names_dicts_to_dict(default_names_dicts())
			
		raise inst



def write_dict(d, f_name):
	"""
	Writes an options dictionary to a file
	"""
	f = open(f_name, 'w')
	_dict_to_opt_stream(d, f)	
	f.close()
		
		
		
def dict_to_str(d):
	"""
	Converts a dictionary to the format expected by HTML Tidy's command line utility. 
	"""
	return string.join(['--%s \'%s\'' % (lib_to_orig_opt_rep(k), lib_to_orig_opt_rep(v)) for (k, v) in d.items() if v != ''], ' ')



class test(unittest.TestCase):		
	def test_orig_to_lib_opt_rep(self):		
		self.assertEqual(orig_to_lib_opt_rep('dd'), 'dd')
		self.assertEqual(orig_to_lib_opt_rep(2), 2)
		self.assertEqual(orig_to_lib_opt_rep('yes'), True)
		self.assertEqual(orig_to_lib_opt_rep('no'), False)


	def test_lib_to_orig_opt_rep(self):		
		self.assertEqual(lib_to_orig_opt_rep('dd'), 'dd')
		self.assertEqual(lib_to_orig_opt_rep(2), 2)
		self.assertEqual(lib_to_orig_opt_rep(True), 'yes')
		self.assertEqual(lib_to_orig_opt_rep(False), 'no')


	def test_opt_stream_to_dict(self):
		f_name = os.path.join(gen_utils.data_dir(), consts.opt_names_to_f_names['misc_opts'])
		d = _opt_stream_to_dict(open(f_name, 'r'))
		
		self.assertEqual(len(d), 10)
		self.assertEqual(d['write-back'], False)
		self.assertEqual(gen_utils.is_bool_type(d['write-back']), True)
		self.assertEqual(d['gnu-emacs-file'], '')
		
		
	def test_default_names_dicts(self):
		names_dicts = default_names_dicts()
		
		self.assertEqual(len(names_dicts), len(consts.opts))

	
	def test_dict_to_names_dicts(self):
		names_dicts = default_names_dicts()
		d = names_dicts_to_dict(names_dicts)
		
		self.assertEquals(dict_to_names_dicts(d), names_dicts)
	 	
	 	
	def test_dict_to_str(self):	 	
		self.assertEquals(dict_to_str({'char-encoding': 'utf8'}), '--char-encoding \'utf8\'')
		self.assertEquals(dict_to_str({'char-encoding': 'utf8', 'foo': ''}), '--char-encoding \'utf8\'')
		self.assertEquals(dict_to_str({'wrap-php': True}), '--wrap-php \'yes\'')
		self.assertEquals(dict_to_str({}), '')
		 
		 	
	
def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()
