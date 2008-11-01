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
A dialog for setting HTML-Tidy options.
"""


import unittest
import pygtk
pygtk.require('2.0')
import gtk
import config_dict
import opts_notebook
import os
import tidy_opt_utils
import consts
import sys, string
import gen_utils
import log_utils
				


class dlg(gtk.Dialog):
	"""
	A dialog for setting HTML-Tidy options.
	"""
	def __init__(self, parent, tabs, sensitive):
		"""
		Keyword arguments:
	    parent -- gtk.Window parent.
	    tabs -- A list of pairs of (logical category name, options dictionary within the category).
	    sensitive -- Wether the options are sensitive (i.e., can be modified).
		"""
		title = 'HTML-Tidy Options'
		flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT	
		if sensitive:
			buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
		else:
			buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK)		      

		super(dlg, self).__init__(title, parent, flags, buttons)
				      
		log_utils.debug('setting up opts dialog')
		
		self._n = opts_notebook.notebook(tabs, sensitive)
		
		self.vbox.pack_start(self._n, True, True)
		
		log_utils.debug('set up opts dialog')
		
		self.show_all()
		
	
	def names_dicts(self):
		"""
		Returns a list of pairs of (logical category name, options dictionary within the category).
		"""
		return self._n.names_dicts()
		


class test(unittest.TestCase):		
	def test_defaults_dlg(self):		
		tabs = tidy_opt_utils.default_names_dicts()
	
		o = dlg(None, tabs, False)

		rep = o.run()
		

	def test_custom_dlg(self):		
		custom_dict = tidy_opt_utils.read_dict(consts.custom_opt_file_name, True)
		tabs = tidy_opt_utils.dict_to_names_dicts(custom_dict)
	
		o = dlg(None, tabs, True)

		rep = o.run()
		
		if rep == gtk.RESPONSE_OK:
			log_utils.debug('updating custom opts')
			
			names_dicts = o.names_dicts()
			custom_dict = tidy_opt_utils.names_dicts_to_dict(names_dicts)
			
			tidy_opt_utils.write_dict(custom_dict, consts.custom_opt_file_name)
			
			log_utils.debug('updated custom opts')



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()


