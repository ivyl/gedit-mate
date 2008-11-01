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
Just some constants used throughout.
"""



plugin_name = 'html-tidy'
data_dir = 'data'



"""
HTML-Tidy's options categories. 
"""
opts = [
	'html_xhtml_xml_opts',
	'diagnostics_opts',	
	'char_encoding_opts',
	'pretty_print_opts',
	'misc_opts'
]



"""
Maps each option category to the name HTML Tidy gives it.
"""
opt_names_to_logical_names = {
	'html_xhtml_xml_opts' : 'HTML, XHTML, and XML',
	'diagnostics_opts' : 'Diagnostics',	
	'char_encoding_opts' : 'Character Encoding',
	'pretty_print_opts' : 'Pretty Printing',
	'misc_opts' : 'Misc.'
}



"""
Maps each option category to the file where its default options are stored.
"""
opt_names_to_f_names = {
	'html_xhtml_xml_opts' : 'html_xhtml_xml_opts.txt',
	'diagnostics_opts' : 'diagnostics_opts.txt',	
	'char_encoding_opts' : 'char_encoding_opts.txt',
	'pretty_print_opts' : 'pretty_print_opts.txt',
	'misc_opts' : 'misc_opts.txt'
}



"""
The gedit MIME types that pertain to this plugins.
"""
gedit_mime_types = [
	'text/html', 
	'application/xml', 
	'application/xhtml+xml'
]



tidy_opts_config_category = 'tidy_opts_config'
default_tidy_opts_config = 'default'
from_file_tidy_opts_config = 'from_file'
custom_tidy_opts_config = 'custom'



opt_file_name_category = 'opt_file'
opt_file_name = ''

custom_opt_file_name = 'custom_opts.txt'
custom_opts_names_dicts_category = 'custom_opts_names_dicts'


type_config_category = 'type_config'
mime_type_config = 'html_xhtml_and_xml_only'
ext_type_config = 'ext'
all_type_config = 'all'
	
	

type_ext_category = 'extensions'
html_xhtml_and_xml_exts = 'html, xhtml, xml'


	
config_f_name = 'config.txt'



sample_tidy_config_f_name = 'sample_tidy_config.txt'



tmp_input_f_name = 'tmp_input'
tmp_output_f_name = 'tmp_output'
