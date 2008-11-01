# -*- coding: utf-8 -*-

#  Copyright (C) 2008 - Eugene Khorev
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

import pygtk
pygtk.require("2.0")
import gtk
import gettext
import ConfigParser
import os

class conf_dlg(gtk.Dialog):
    def __init__(self, parent):
        # Create config diaog window
        title = _("Reopen Tabs Plugin Configuration")
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK)

        super(conf_dlg, self).__init__(title, parent, 0, buttons)
        
        # Create configuration items
        self._chk_save = gtk.CheckButton(_("Ask for saving on exit"))
        self._chk_save.connect("toggled", self._on_chk_save_toggled)
        self.vbox.pack_start(self._chk_save, True, True, 10)
        
        # Setup configuration file path
        conf_path = os.path.join(os.path.expanduser("~/.gnome2/gedit/plugins/"), "reopen-tabs/plugin.conf")
        
        # Check if configuration file does not exists
        if not os.path.exists(conf_path):
            # Create configuration file
            conf_file = file(conf_path, "wt")
            conf_file.close()
            
        # Create configuration dictionary
        self.read_config(conf_path)
        
    def read_config(self, conf_path): # Reads configuration from a file
        self._conf_file = file(conf_path, "r+")
        self._conf_dict = ConfigParser.ConfigParser()
        self._conf_dict.readfp(self._conf_file)
        

        # Setup default configuration if needed
        if not self._conf_dict.has_section("common"):
            self._conf_dict.add_section("common")
            
        if not self._conf_dict.has_option("common", "save_prompt"):
            self._conf_dict.set("common", "save_prompt", "on")
                
        if not self._conf_dict.has_option("common", "active_document"):
            self._conf_dict.set("common", "active_document", "")
                
        if not self._conf_dict.has_section("documents"):
            self._conf_dict.add_section("documents")
                
    def write_config(self): # Saves configuration to a file
        self._conf_file.truncate(0)
        self._conf_file.seek(0)

        self._conf_dict.write(self._conf_file)
    
    def get_config(self):
        return self._conf_dict
    
    def load_conf(self): # Loads configuration
        val = self._conf_dict.getboolean("common", "save_prompt")
        
        self._chk_save.set_active(val)
    
    def _on_chk_save_toggled(self, chk): # React on checkbox toggle        
        if chk.get_active() == True:
            val = "on"
        else:
            val = "off"
        
        self._conf_dict.set("common", "save_prompt", val)
        
# ex:ts=4:et:
