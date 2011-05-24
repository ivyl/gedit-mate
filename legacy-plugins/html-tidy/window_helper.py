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
The window-specific HTML plugin part.
"""



import gtk
import gedit
from gettext import gettext as _
import gtk_utils
import output_pane
import config_dict
import tidy_utils
import file_types_filter
import log_utils



class window_helper:
	"""
	The window-specific HTML plugin part.
	"""
	def __init__(self, plugin, window):
		log_utils.debug('Creating window helper')
	
		self._window = window
		self._plugin = plugin
	
		self._insert_menu()
		self._insert_configure_menu()
		
		log_utils.debug('Created window helper')
		
		
	def _flash_message(self, msg):
			self._window.get_statusbar().flash_message(112, msg)
			
		
	def deactivate(self):
		self._remove_configure_menu()
		self._remove_menu()
		
		self._window = None
		self._plugin = None
		self._action_group = None
		self._configure_action_group = None
						
	
	def _insert_menu(self):
		ui_str = """
<ui>
	<menubar name="MenuBar">
		<menu name="ToolsMenu" action="Tools">
			<placeholder name="ToolsOps_2">
				<separator/>
				<menuitem name="tidy" action="tidy"/>
				<menuitem name="tidy_check" action="tidy_check"/>
				<separator/>
			</placeholder>
			<placeholder name="ToolsOps_5">
				<menuitem name="configure_tidy" action="configure_tidy"/>
			</placeholder>
		</menu>
	</menubar>
</ui>
"""
	
		self._action_group = gtk.ActionGroup("html_tidy_plugin_actions")
		actions = [
			("tidy", None, _("_Tidy"), None, _("Tidies HTML, XHTML, and XML"),	self.on_tidy),
			("tidy_check", None, _("Tidy _Check"), None, _("Checks HTML, XHTML, and XML"),	self.on_tidy_check)]
		self._action_group.add_actions(actions)
		
		manager = self._window.get_ui_manager()
		
		manager.insert_action_group(self._action_group, -1)
		
		self._ui_id = manager.add_ui_from_string(ui_str)
	
	
	def _insert_configure_menu(self):
		ui_str = """
<ui>
	<menubar name="MenuBar">
		<menu name="ToolsMenu" action="Tools">
			<placeholder name="ToolsOps_5">
				<menuitem name="configure_tidy" action="configure_tidy"/>
			</placeholder>
		</menu>
	</menubar>
</ui>
"""
	
		self._configure_action_group = gtk.ActionGroup("html_tidy_plugin_configure_actions")
		actions = [
			("configure_tidy", None, _("Configure Tidy..."), None, _("Configures HTML, XHTML, and XML Checker"), self._plugin.on_configure)]
		self._configure_action_group.add_actions(actions)
		
		manager = self._window.get_ui_manager()
		
		manager.insert_action_group(self._configure_action_group, -1)
		
		self._configure_ui_id = manager.add_ui_from_string(ui_str)


	def _remove_menu(self):
		manager = self._window.get_ui_manager()
		
		manager.remove_ui(self._ui_id)
		
		smanager.remove_action_group(self._action_group)
		
		manager.ensure_update()
		
		
	def _remove_configure_menu(self):
		manager = self._window.get_ui_manager()
		
		manager.remove_ui(self._configure_ui_id)
		
		smanager.remove_action_group(self._configure_action_group)
		
		manager.ensure_update()


	def _can_tidy(self):
		log_utils.debug('checking if can tidy')
		
		active_doc = self._window.get_active_document()
		
		if active_doc == None:
			log_utils.debug('No doc active - returning False')
			return False
			
		f_name = active_doc.get_uri()
		mime_type = active_doc.get_mime_type()		
		
		log_utils.debug('active doc\'s name is %s' % f_name)
		log_utils.debug('active doc\'s mime type is %s' % mime_type)
		
		return file_types_filter.can_tidy(self._plugin.config_dict, f_name, mime_type)
	
	
	def update_ui(self):
		sensitive = self._can_tidy()
		
		self._action_group.set_sensitive(sensitive)
		
		self._configure_action_group.set_sensitive(True)
		
		
	def on_tidy(self, action):
		self._plugin.output_pane.clear()
		
		log_utils.debug('tidying')
		
		view = self._window.get_active_view()	
		bf = view.get_buffer()
		
		non_white = gtk_utils.num_non_whites_till_cur(bf)
		text = gtk_utils.get_view_text(view)
			
		try:	
			effective_opts_dict = config_dict.effective_opts_dict(self._plugin.config_dict)
			(s, report_items) = tidy_utils.tidy_the_stuff(text, effective_opts_dict)
		except Exception, inst:
			self._flash_message(str(inst))

			return
		
		log_utils.debug('tidy checked; found %s' % len(report_items))
		
		if s == '':
			log_utils.warn('got empty tidied text')
			
			self._flash_message('failed to tidy')
			
			return
		
		doc = self._window.get_active_document()

		doc.set_text(s)
		
		log_utils.debug('set text')
		
		gtk_utils.cursor_to_non_whites(view, non_white)

		log_utils.debug('tidied')
		
		
	def on_tidy_check(self, action):
		self._plugin.output_pane.clear()
		
		log_utils.debug('setting target uri')
		
		uri = self._window.get_active_document().get_uri()
		if uri == None:
			self._flash_message('Please first save your work to some name')
		
			return
			
		self._plugin.output_pane.target_uri = uri
			
		log_utils.debug('set target uri')

		log_utils.debug('tidy checking')
		
		view = self._window.get_active_view()	
		text = gtk_utils.get_view_text(view)
		
		try:	
			effective_opts_dict = config_dict.effective_opts_dict(self._plugin.config_dict)
			(s, report_items) = tidy_utils.tidy_the_stuff(text, effective_opts_dict)
		except Exception, inst:
			self._flash_message(str(inst))

			return

		log_utils.debug('tidy checked; found %s' % len(report_items))
		
		for item in report_items:
			self._plugin.output_pane.append(item.line, item.col, item.type_, item.what)
			
		if len(report_items) > 0:
			log_utils.debug('showing output pane')
			
			self._plugin.output_pane.show()

		log_utils.debug('tidy checked')
		

	def on_output_pane_row_activated(self, line, col, type_, what):
		target_uri = self._plugin.output_pane.target_uri
	
		log_utils.debug('row activated for  %s %s %s %s %s to output box' % (target_uri, line, col, type_, what))
		
		uri = self._window.get_active_document().get_uri()
		
		if uri != target_uri:
			self._flash_message('Please switch to %s' % target_uri)
	
			return
			
		if line == None:
			assert col == None, col
			
			return
			
		assert col != None, col
		
		view = self._window.get_active_view()

		try:
			gtk_utils.scroll_view_to_line_col(view, line, col)
		except Exception, inst:
			log_utils.warn('failed to scroll')
			
			log_utils.warn(inst)
			
			self._flash_message('Huh? Can\'t scroll to this position...')
		
