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
Dialog used for user's preferences. See config_dict.py for the DS that stores these
	preferences.
"""



import unittest
import pygtk
pygtk.require('2.0')
import gtk
import consts
import config_dict
import log_utils
import tidy_opt_utils
import opts_dlg



class dlg(gtk.Dialog):
	def __init__(self, parent):
		title = 'HTML-Tidy Plugin Configuration'
		buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)

		super(dlg, self).__init__(title, parent, 0, buttons)
		        
		self._make_tidy_opts_vbox()

		self._make_mime_types_vbox()


	def reset(self, config_dict):
		self._config_dict = config_dict.copy()
		        
		self._init_from_config_dict()
		
		self._on_opts_changed(None)
		
		self._on_types_changed(None)
		
		
	def get_config_dict(self):
		return self._config_dict

				
	def _init_from_config_dict(self):
		v = self._config_dict[consts.tidy_opts_config_category]
		
		self._use_default_opts.set_active(v == consts.default_tidy_opts_config)
		self._from_file_opts.set_active(v == consts.from_file_tidy_opts_config)
		self._use_custom_opts.set_active(v == consts.custom_tidy_opts_config)
		
		v = self._config_dict[consts.opt_file_name_category]
		
		self._file_entry.set_text(v)

		v = self._config_dict[consts.type_config_category]

		self._mime_types.set_active(v == consts.mime_type_config)
		self._ext_types.set_active(v == consts.ext_type_config)
		self._all_types.set_active(v == consts.all_type_config)
		
		v = self._config_dict[consts.type_ext_category]
		
		self._ext_entry.set_text(v)

		        
	def _make_tidy_opts_vbox(self):
		frame = gtk.Frame('HTML Tidy Options')
		
		table = gtk.Table(3, 3, False)
		
		self._use_default_opts = gtk.RadioButton(label =  '_Default')
		self._from_file_opts = gtk.RadioButton(group = self._use_default_opts, label = 'From _File')
		self._use_custom_opts = gtk.RadioButton(group = self._use_default_opts, label = '_Custom')
		
		self._use_default_opts.connect('toggled', self._on_opts_changed)
		self._from_file_opts.connect('toggled', self._on_opts_changed)
		self._use_custom_opts.connect('toggled', self._on_opts_changed)
		
		table.attach(self._use_default_opts, 0, 1, 0, 1, xoptions = gtk.SHRINK | gtk.FILL)
		table.attach(self._from_file_opts, 0, 1, 1, 2, xoptions = gtk.SHRINK | gtk.FILL)
		table.attach(self._use_custom_opts, 0, 1, 2, 3, xoptions = gtk.SHRINK | gtk.FILL)
		
		self._view_default_opts = gtk.Button('View...')
		self._view_file_opts = gtk.Button('View...')
		self._edit_custom_opts = gtk.Button('Edit...')

		self._view_default_opts.connect('clicked', self._on_view_default_opts)
		self._view_file_opts.connect('clicked', self._on_view_file_opts)
		self._edit_custom_opts.connect('clicked', self._on_edit_custom_opts)

		table.attach(self._view_default_opts, 1, 2, 0, 1, xoptions = gtk.SHRINK | gtk.FILL)
		table.attach(self._view_file_opts, 1, 2, 1, 2, xoptions = gtk.SHRINK | gtk.FILL)
		table.attach(self._edit_custom_opts, 1, 2, 2, 3, xoptions = gtk.SHRINK | gtk.FILL)
		
		self._file_label = gtk.Label('File')
		
		self._file_entry = gtk.Entry()
		self._file_entry.connect('changed', self._on_file_entry_changed)
		self._choose_file = gtk.Button('Choose')
				
		hbox = gtk.HBox(False, 2)
		hbox.pack_start(self._file_label, False, False, 2)
		hbox.pack_start(self._file_entry, True, True, 2)
		hbox.pack_start(self._choose_file, False, False, 2)
		
		table.attach(hbox, 2, 3, 1, 2)

		self._choose_file.connect('clicked', self._on_choose_file)

		frame.add(table)
		        
		self.vbox.pack_start(frame, True, False, 2)


	def _make_mime_types_vbox(self):
		frame = gtk.Frame('File Types')
		
		table = gtk.Table(3, 3, False)		
		
		self._mime_types = gtk.RadioButton(label = 'Mime Types (HTML, _XHTML, and XML)')
		self._ext_types = gtk.RadioButton(group = self._mime_types, label =  'By _Extension')
		self._all_types = gtk.RadioButton(group = self._mime_types, label =  '_All')

		self._mime_types.connect('toggled', self._on_types_changed)
		self._ext_types.connect('toggled', self._on_types_changed)
		self._all_types.connect('toggled', self._on_types_changed)

		table.attach(self._mime_types, 0, 1, 0, 1, xoptions = gtk.SHRINK | gtk.FILL)
		table.attach(self._ext_types, 0, 1, 1, 2, xoptions = gtk.SHRINK | gtk.FILL)
		table.attach(self._all_types, 0, 1, 2, 3, xoptions = gtk.SHRINK | gtk.FILL)

		self._ext_label = gtk.Label('Extensions')

		self._ext_entry = gtk.Entry()
		self._ext_entry.connect('changed', self._on_ext_entry_changed)

		hbox = gtk.HBox(False, 2)
		hbox.pack_start(self._ext_label, False, False, 2)
		hbox.pack_start(self._ext_entry, True, True, 2)
		
		table.attach(hbox, 2, 3, 1, 2)

		frame.add(table)
		        
		self.vbox.pack_start(frame, True, False, 2)
		
		
	def _on_opts_changed(self, widget):
		use_default = self._use_default_opts.get_active()
		from_file = self._from_file_opts.get_active()
		custom_opts = self._use_custom_opts.get_active()		
		
		k = consts.tidy_opts_config_category
		
		if use_default:
			self._config_dict[k] = consts.default_tidy_opts_config
		elif from_file:
			self._config_dict[k] = consts.from_file_tidy_opts_config
		elif custom_opts:
			self._config_dict[k] = consts.custom_tidy_opts_config
		else:
			assert False
		
		self._view_default_opts.set_sensitive(use_default)
		
		self._view_file_opts.set_sensitive(from_file and self._file_entry.get_text() != '')
		self._file_label.set_sensitive(from_file)
		self._file_entry.set_sensitive(from_file)
		self._choose_file.set_sensitive(from_file)
		
		self._edit_custom_opts.set_sensitive(custom_opts)


	def _on_types_changed(self, widget):
		mime = self._mime_types.get_active()
		ext = self._ext_types.get_active()
		all = self._all_types.get_active()		
		
		k = consts.type_config_category
		
		if mime:
			self._config_dict[k] = consts.mime_type_config 
		elif ext:
			self._config_dict[k] = consts.ext_type_config
		elif all:
			self._config_dict[k] = consts.all_type_config
		else:
			assert False

		self._ext_label.set_sensitive(ext)
		self._ext_entry.set_sensitive(ext)
		
	
	def _on_file_entry_changed(self, w):
		t = self._file_entry.get_text()
		
		self._config_dict[consts.opt_file_name_category] = t

		self._view_file_opts.set_sensitive(self._file_entry.get_text() != '')


	def _on_ext_entry_changed(self, w):
		t = self._ext_entry.get_text()
		
		self._config_dict[consts.type_ext_category] = t
		

	def _on_view_default_opts(self, w):
		tabs = tidy_opt_utils.default_opts_names_dicts()
	
		d = opts_dlg.dlg(self, tabs, False)
		
		d.show_all()
		
		d.run()
		
		d.destroy()
		
		
	def _on_view_file_opts(self, w):
		f_name = self._file_entry.get_text()
		
		try:
			f_dict = tidy_opt_utils.read_dict(f_name)
		except Exception, inst:
			parent = self
			flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
			type_ = gtk.MESSAGE_WARNING
			buttons = gtk.BUTTONS_OK
			log_utils.warn('can\'t view opts file')
			log_utils.warn(inst)
			msg = 'Couldn\'t read or parse file'
			
			d = gtk.MessageDialog(parent, flags, type_, buttons, msg)
			
			d.run()
			
			d.destroy()
			
			return
		
		tabs = tidy_opt_utils.dict_to_names_dicts(f_dict)
	
		d = opts_dlg.dlg(self, tabs, False)
		
		d.show_all()
		
		d.run()
		
		d.destroy()

		
	def _on_edit_custom_opts(self, w):	
		tabs = self._config_dict[consts.custom_opts_names_dicts_category] 
		
		d = opts_dlg.dlg(self, tabs, True)
		
		d.show_all()
		
		rep = d.run()
		
		if rep == gtk.RESPONSE_OK:
			log_utils.debug('updating custom opts')
			
			self._config_dict[consts.custom_opts_names_dicts_category] = d.names_dicts()
			
			log_utils.debug('updated custom opts')
			
		d.destroy()
		

	def _on_choose_file(self, w):
		title = 'Choose...'
		flags = gtk.FILE_CHOOSER_ACTION_OPEN	
		buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
		
		s = gtk.FileChooserDialog(title, None, flags, buttons)
		   			
		f_name = None
   		if s.run() == gtk.RESPONSE_OK:
   			t = s.get_filename()
   			
   			self._file_entry.set_text(t)
   		
   		s.destroy()



class test(unittest.TestCase):		
	def test_dlg_0(self):		
		o = dlg(None)
		
		o.reset(config_dict.read_config_dict())
		
		o.show_all()

		rep = o.run()
		
		if rep == gtk.RESPONSE_OK:
			config_dict.write_config_dict(o.get_config_dict())
		


def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()


