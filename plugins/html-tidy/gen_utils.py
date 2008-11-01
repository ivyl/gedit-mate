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
General-purpose utilities.
"""



import consts
import unittest
import os
import log_utils
import ex



_found_data_dir = None



def is_string_type(s):
	"""
	True iff s is a string.
	"""
	return type(s) == type('')
	
	
	
def is_bool_type(s):
	"""
	True iff s is a boolean.
	"""
	return type(s) == type(True)



def disjoint_dicts_union(dicts):
	"""
	Takes a list of dictionaries that have disjoint keys.
	Returns a dictionary that is their union.
	"""
	ret = {}
	
	for d in dicts:
		for k in d.keys():
			assert not ret.has_key(k), k
			
			ret[k] = d[k]
			
	return ret



def replace_dict(d0, d1):
	"""
	Returns a dictionary whose keys are the intersection of d0 and d1, and
	whose values are from d1.
	"""
	ret = {}
	
	for (name, val) in d1.items():
		if name in d0.keys():
				ret[name] = val
		
	return ret



# Idea from snippets plugin, Copyright (C) 2005-2006  Jesse van den Kieboom.
def data_dir():
	"""
	Returns the data directory, i.e., the directory where the plugin's data files reside.
	"""
	global _found_data_dir

	if _found_data_dir != None:
		return _found_data_dir

	base_dirs = [
		os.path.join(os.environ['HOME'], '.gnome2', 'gedit', 'plugins'),
		'/usr/local/share/gedit-2',
		'/usr/share/gedit-2']
		
	for dir in base_dirs:
		_found_data_dir = os.path.join(dir, consts.plugin_name, consts.data_dir)
                        
		if os.path.isdir(_found_data_dir):
			log_utils.debug('found directory %s' % _found_data_dir)
			return _found_data_dir
               
	raise ex.error('can\'t find data directory')	



class test(unittest.TestCase):		
	def test_is_string_type(self):		
		self.assert_(is_string_type(''))
		self.assert_(is_string_type('dd'))
		self.assert_(not is_string_type(2))

		
	def test_is_bool_type(self):		
		self.assert_(is_bool_type(True))
		self.assert_(is_bool_type(False))	
		self.assert_(not is_bool_type(2))


	def test_disjoint_dicts_union(self):
		d = disjoint_dicts_union([{1 : 'a', 2 : 'b'}, {3 : 'c'}])

		self.assert_(len(d), 3)
		
		self.assertEquals(d[1], 'a')
		self.assertEquals(d[2], 'b')
		self.assertEquals(d[3], 'c')
		
		
	def test_replace_dict(self):
		d0 = {'a': 1, 'b': 2}
		
		d1 = {'b': 3, 'f': 8}
		
		d = replace_dict(d0, d1)
		
		self.assertEquals(len(d), 1)

		self.assertEquals(d['b'], 3)

	
	def test_data_dir(self):
		# Tmp Ami
		data_dir()



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		


if __name__ == '__main__':
	unittest.main()
