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
A notebook tab for setting HTML-Tidy options.
"""


import unittest
import pygtk
pygtk.require('2.0')
import gtk
import os
import tidy_opt_utils
import consts
import sys, string
import gen_utils



class tab(gtk.Alignment):
	def __init__(self, opt_dict, sensitive):
		"""
		Keyword arguments:
		dict -- An options dictionary within some HTML-Tidy options category.
	    sensitive -- Wether the options are sensitive (i.e., can be modified).
		"""
		super(tab, self).__init__(0, 0)
		
		self._dict = opt_dict.copy()

		self.set_border_width(10)

		names = self._dict.keys()
		names.sort()
		
		i = 0
		num_vert = 16
		
		hbox = gtk.HBox(True,  4)
			
		while i <= len(names):
			vbox = gtk.VBox(True,  2)

			for name in names[i : min(len(names), i + num_vert)]:
				widget = self._make_widget(name, self._dict[name], sensitive)
				vbox.pack_start(widget, True, False)
			
			vbox.show()
			
			hbox.pack_start(vbox, False, True)

			i = i + num_vert
			
		self.add(hbox)

		self.show()
		

	def opts_dict(self):
		"""
		Returns the options dictionary belonging to (and possibly modified by) this dialog.
		"""
		return self._dict


	def _make_widget(self, name, val, sensitive):
		make_check = gen_utils.is_string_type(val)
		
		name = tidy_opt_utils.lib_to_orig_opt_rep(name)
		
		if make_check:
			val = tidy_opt_utils.lib_to_orig_opt_rep(val)
		
			return self._make_string_widget(name, val, sensitive)

		assert gen_utils.is_bool_type(val), val 

		return self._make_check_widget(name, val, sensitive)


	def _make_string_widget(self, name, val, sensitive):
		h = gtk.HBox(False, 2)
		h.set_sensitive(sensitive)

		l = gtk.Label(name)
		l.set_sensitive(sensitive)
		
		e = gtk.Entry()
		e.connect('changed', self._on_edit_changed, name)
		e.set_text(val)
		
		h.pack_start(l, False, False)
		h.pack_start(e, True, True)

		l.show()
		e.show()
		h.show()
		
		return h


	def _make_check_widget(self, name, val, sensitive):
		b = gtk.CheckButton(name)
		b.set_sensitive(sensitive)
		
		b.connect('toggled', self._on_check, name)
		assert gen_utils.is_bool_type(val), val
		b.set_active(val)		
		
		b.show()
			
		return b
		
		
	def _on_check(self, b, name):
		name = tidy_opt_utils.orig_to_lib_opt_rep(name)
		
		assert self._dict.has_key(name)
		
		self._dict[name] = b.get_active()
		

	def _on_edit_changed(self, e, name):
		name = tidy_opt_utils.orig_to_lib_opt_rep(name)
		
		assert self._dict.has_key(name)
		
		self._dict[name] = e.get_text()
		


class test(unittest.TestCase):		
	def _test_tab(self, sensitive):		
		f_name = os.path.join(gen_utils.data_dir(), consts.opt_names_to_f_names['html_xhtml_xml_opts'])
		opts_dict = tidy_opt_utils.read_dict(f_name)
		
		o = tab(opts_dict, sensitive)

		o.connect('destroy', gtk.main_quit)	

		main_wnd = gtk.Window(gtk.WINDOW_TOPLEVEL)
		main_wnd.set_title('Output');
		main_wnd.add(o)

		main_wnd.show_all()
		gtk.main()


	def test_tab_0(self):		
		self._test_tab(True)


	def test_tab_1(self):		
		self._test_tab(False)



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()


