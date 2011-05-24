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
A notebook for setting HTML-Tidy options.
"""


import unittest
import pygtk
pygtk.require('2.0')
import gtk
import opts_tab
import os
import tidy_opt_utils
import consts
import sys, string
import gen_utils
import log_utils
		
		

class notebook(gtk.Notebook):
	"""
	A notebook for setting HTML-Tidy options.
	"""
	def __init__(self, tabs, sensitive):
		"""
		Keyword arguments:
	    tabs -- A list of pairs of (logical category name, options dictionary within the category).
	    sensitive -- Wether the options are sensitive (i.e., can be modified).
		"""
		log_utils.debug('setting up opts notebook')
		
		super(notebook, self).__init__()
		
		for (tab_name, opts_dict) in tabs:
			o = opts_tab.tab(opts_dict, sensitive)			
			self.append_page(o, gtk.Label(tab_name))
				
		log_utils.debug('set up opts notebook')
		
		
	def names_dicts(self):
		"""
		Returns a list of pairs of (logical category name, options dictionary within the category).
		"""
		children = [super(notebook, self).get_nth_page(i) for i in range(super(notebook, self).get_n_pages())]
		
		return [(super(notebook, self).get_tab_label_text(child), child.opts_dict()) for child in children]
		
		

class test(unittest.TestCase):
	def _test_notebook(self, names_dicts, sensitive):
		o = notebook(names_dicts, sensitive)
	
		o.connect("destroy", gtk.main_quit)			

		main_wnd = gtk.Window(gtk.WINDOW_TOPLEVEL)
		main_wnd.set_title('Output');
		main_wnd.add(o)

		main_wnd.show_all()
		gtk.main()


	def test_notebook_0(self):	
		self._test_notebook(tidy_opt_utils.default_names_dicts(), True)


	def test_notebook_1(self):
	 	sample_f_name = os.path.join(gen_utils.data_dir(), consts.sample_tidy_config_f_name)
	 	
	 	sample_dict = tidy_opt_utils.read_dict(sample_f_name)
	 	
		self._test_notebook(tidy_opt_utils.dict_to_names_dicts(sample_dict), False)



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()


