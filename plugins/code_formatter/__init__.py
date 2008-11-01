# Copyright (C) 2007 - Nando Vieira
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
from gettext import gettext as _
import gtk
import gedit
import re
import os
import subprocess



ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="FormatCode" action="FormatCode"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class CodeFormatterPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = CodeFormatterWindowHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        self._instances[window].update_ui()

class CodeFormatterWindowHelper:
    handlers = {}
    
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin

        # Insert menu items
        self._insert_menu()

    
    def deactivate(self):
        # Remove any installed menu items
        self._remove_menu()

        self._window = None
        self._plugin = None
        self._action_group = None

        
    def _insert_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        self._action_group = gtk.ActionGroup("CodeFormatterPluginActions")
        self._action_group.add_actions([("FormatCode", gtk.STOCK_SELECT_COLOR, _("Format Code"),
                                         '<Control><Alt>f', _("Format the Code"),
                                         self.on_format_code_activate)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def update_ui(self):
        self._action_group.set_sensitive(self._window.get_active_document() != None)

    # Menu activate handlers
    def on_format_code_activate(self, action):
        doc = self._window.get_active_document()
        if not doc:
            return
        formatter_script = os.path.join(os.path.dirname(__file__), "rubybeautifier.rb")
        start, end = doc.get_bounds()
        txt = doc.get_text(start,end)
        proc = subprocess.Popen(["ruby",formatter_script], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write(txt)
        proc.stdin.close()
        out = proc.stdout.read()
        doc.set_text(out)

