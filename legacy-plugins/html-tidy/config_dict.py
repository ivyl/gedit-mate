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
Configuration dictionary. This is a dictionary that describes the different user preferences.
"""



import unittest
import gen_utils
import log_utils
import consts
import os
import opt_stream_utils
import tidy_opt_utils



def _default_config_dict():
	"""
	Returns a configuration dictionary with the default choices. Used when can't open
		a file describing these choices.
	"""
	d = {}
	
	d[consts.tidy_opts_config_category] = consts.default_tidy_opts_config
	
	d[consts.type_config_category] = consts.mime_type_config
	
	d[consts.type_ext_category] = consts.html_xhtml_and_xml_exts

	d[consts.opt_file_name_category] = consts.opt_file_name
	
	d[consts.custom_opts_names_dicts_category] = tidy_opt_utils.default_names_dicts()
	
	return d
	


def read_config_dict():
	"""
	Reads the configuration dictionary from a predefined file (defined in consts.py).
	"""
	log_utils.debug('reading config dict')

	data_dir = gen_utils.data_dir()	

	d = _default_config_dict()

	f_name = os.path.join(data_dir, consts.config_f_name)

	try:
		f = open(f_name, 'r')
		d = opt_stream_utils.opt_stream_to_dict(f)					
		f.close()
	except Exception, inst:		
		log_utils.warn(str(inst))
		log_utils.warn('couldn\'t read config dict from %s' % f_name)
		
	custom_dict = tidy_opt_utils.read_dict(consts.custom_opt_file_name, True)
	d[consts.custom_opts_names_dicts_category] = tidy_opt_utils.dict_to_names_dicts(custom_dict)
	
	log_utils.debug('read config dict')
	
	return d
	


def write_config_dict(d):
	"""
	Writes the configuration dictionary to a predefined file (defined in consts.py).
	"""
	log_utils.debug('writing config dict')
					
	custom_dict = tidy_opt_utils.names_dicts_to_dict(d[consts.custom_opts_names_dicts_category])
	tidy_opt_utils.write_dict(custom_dict, consts.custom_opt_file_name)
	
	tmp_d = {}
	
	for k in [k for k in d.keys() if k != consts.custom_opts_names_dicts_category]:
		tmp_d[k] = d[k]

	f_name = os.path.join(gen_utils.data_dir(), consts.config_f_name)

	f = open(f_name, 'w')
	opt_stream_utils.dict_to_opt_stream(tmp_d, f)
	f.close()
		
	log_utils.debug('wrote config dict')			



def effective_opts_dict(d):
	"""
	Given a configuration dictionary, returns the effective HTML-Tidy options dictionary (default, from file, or custom).
	"""
	k = d[consts.tidy_opts_config_category]
	
	if k == consts.default_tidy_opts_config:
		return tidy_opt_utils.names_dicts_to_dict( tidy_opt_utils.default_names_dicts() )
	elif  k == consts.from_file_tidy_opts_config:
		return tidy_opt_utils.read_dict( d[consts.opt_file_name_category] )
	elif  k == consts.custom_tidy_opts_config:
		return tidy_opt_utils.names_dicts_to_dict( d[consts.custom_opts_names_dicts_category] )
	else:
		assert False
		


class test(unittest.TestCase):		
	def test_default_config_dict(self):		
		d = _default_config_dict()

		self.assertEqual(d[consts.tidy_opts_config_category], consts.default_tidy_opts_config)
	
		self.assertEqual(d[consts.type_config_category], consts.mime_type_config)
		
		
	def test_read_config_dict(self):
		read_config_dict()


	def test_write_config_dict(self):
		d = read_config_dict()
		
		write_config_dict(d)



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()
