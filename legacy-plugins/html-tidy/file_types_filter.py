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
Filters to decide whether some file type pertains to this plugin.
"""



import unittest
import log_utils
import consts
import os
import os.path



def can_tidy(config_dict, f_name, mime_type):
	"""
	Checks whether some file type pertains to this plugin (i.e., can possibly be tidied).
	
	Keyword arguments:
	
	config_dict -- The configuration dictionary describing the user preferences (see config_dict.py)
	f_name -- File's name
	mime_type -- gedit's MIME type for the content	
	"""
	log_utils.debug('checking if can tidy %s with mime type %s' % (f_name, mime_type))
	
	v = config_dict[consts.type_config_category]
	
	if v == consts.mime_type_config:
		return _can_tidy_mime_type(mime_type)		
	if v == consts.ext_type_config:
		return _can_tidy_ext(config_dict, f_name)
	if v == consts.all_type_config:
		return _can_tidy_all_type()		

	log_utils.warn('can\'t figure out type_config_category %s in config dict' % v)

	assert False

	return True			

	
	
def _can_tidy_mime_type(mime_type):
	log_utils.debug('checking if can tidy mime type %s based on mime type' % mime_type)
	
	can_tidy = mime_type in consts.gedit_mime_types
				
	log_utils.debug('can tidy = %s' % can_tidy)
	
	return can_tidy



def _can_tidy_ext(config_dict, f_name):
	log_utils.debug('checking if can tidy %s based on extension' % f_name)
	
	if f_name == None:
		log_utils.debug('there is no f_name')
		
		return False
	
	exts = [e.strip() for e in config_dict[consts.type_ext_category].split(',')]
	
	log_utils.debug('extensions are %s' % str(exts))
	
	ext = os.path.splitext(f_name)[1][1: ]
	
	log_utils.debug('the extension of %s is %s' % (f_name, ext))
	
	can_tidy = ext in exts
				
	log_utils.debug('can tidy = %s' % can_tidy)
	
	return can_tidy
	


def _can_tidy_all_type():
	log_utils.debug('checking if can tidy based on all type')
	
	can_tidy = True

	log_utils.debug('can tidy = %s' % can_tidy)	
	
	return can_tidy
		
		
		
class test(unittest.TestCase):		
	def test_mime_type(self):		
		config_dict = {
			consts.type_config_category : consts.mime_type_config, 
			consts.type_ext_category : consts.html_xhtml_and_xml_exts
			}
		f_name = 'index.html'

		mime_type = consts.gedit_mime_types[0]
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), True)

		mime_type = 'shrimpy/foo'
		assert not mime_type in consts.html_xhtml_and_xml_exts
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), False)


	def test_ext(self):		
		config_dict = {
			consts.type_config_category : consts.ext_type_config, 
			consts.type_ext_category : consts.html_xhtml_and_xml_exts
			}
		mime_type = consts.gedit_mime_types[0]
		
		f_name = 'index.html'
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), True)

		f_name = 'index.htmls'
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), False)

		f_name = 'index.html.htmls'
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), False)

		f_name = None
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), False)


	def test_all(self):		
		config_dict = {
			consts.type_config_category : consts.all_type_config, 
			consts.type_ext_category : consts.html_xhtml_and_xml_exts
			}
		f_name = 'index.html'
		
		mime_type = consts.gedit_mime_types[0]
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), True)

		mime_type = 'shrimpy/foo'
		assert not mime_type in consts.html_xhtml_and_xml_exts
		self.assertEquals(can_tidy(config_dict, f_name, mime_type), True)


def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()
		
