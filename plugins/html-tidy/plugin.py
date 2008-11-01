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
Tidy plugin class.
"""



import unittest
import pygtk
pygtk.require('2.0')
import gtk
import sys
import gedit
from gettext import gettext as _
import output_pane
import tidy_opt_utils
import log_utils
import window_helper
import gen_utils
import os
import config_dlg
import config_dict



class html_tidy_plugin(gedit.Plugin):
	"""
	Tidy plugin class.
	"""
	def __init__(self):
		super(html_tidy_plugin, self).__init__()
		self._instances = {}
		self._data_dir = gen_utils.data_dir()
		
		self.config_dict = config_dict.read_config_dict()
		
		
	def activate(self, window):
		"""
		Called to activate a specific gedit window.
		"""
		log_utils.debug('activating plugin')
	
		helper = window_helper.window_helper(self, window)
		self._instances[window] = helper

		self._activate_output_pane(window, helper)
		
		self._config_dlg = config_dlg.dlg(None)
		self._config_dlg.connect('response', self._on_config_dlg_response)

		log_utils.debug('activated plugin')


	def _activate_output_pane(self, window, helper):
		self.output_pane = output_pane.output_pane(helper.on_output_pane_row_activated)
		bottom = window.get_bottom_panel()

		image = gtk.Image()
		image.set_from_icon_name('stock_mark', gtk.ICON_SIZE_MENU)

		bottom.add_item(self.output_pane, _('HTML Tidy'), image)
		

	def deactivate(self, window):
		"""
		Called to deactivate a specific gedit window.
		"""
		log_utils.debug('deactivating plugin')	
	
		self._deactivate_output_pane(window)
	 
		self._instances[window].deactivate()
		del self._instances[window]

		log_utils.debug('deactivated plugin')


	def _deactivate_output_pane(self, window):
		window.get_bottom_panel().remove_item(self.output_pane)
		
			
	def update_ui(self, window):
		"""
		Called to update the user interface of a specific gedit window.
		"""
		self._instances[window].update_ui()
		
		
	def on_configure(self, action):
		dlg = self.create_configure_dialog()
		
		rep = dlg.run()
		
		self._on_config_dlg_response(dlg, rep)
		
		
	def create_configure_dialog(self):
		"""
		Called when configuration is needed. Just returns a configuration dialog (see config_dlg.py), but doesn't run it
			(gedit's framework does that).
		"""
		self._config_dlg.reset(self.config_dict)
	
		self._config_dlg.show_all()
		
		return self._config_dlg 
		
		
	def _on_config_dlg_response(self, dlg, rep):
		"""
		This is given to the configuration dialog as the callback when it gets a response.
		"""
		log_utils.debug('handling config dlg response')
	
		dlg.hide()
	
		if rep == gtk.RESPONSE_OK:
			log_utils.debug('handling OK config dlg response')
		
			self.config_dict = self._config_dlg.get_config_dict().copy()
			
			config_dict.write_config_dict(self.config_dict)
			
		log_utils.debug('handled config dlg response')

		self._config_dlg.reset(self.config_dict)
			
