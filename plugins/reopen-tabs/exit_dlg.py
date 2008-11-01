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
import gedit
import ConfigParser
import os

class save_dlg(gtk.Dialog):
    def __init__(self, parent, config):
        # Create config diaog window
        title = _("Reopen Tabs Plugin")
        buttons = (gtk.STOCK_NO, gtk.RESPONSE_NO, gtk.STOCK_YES, gtk.RESPONSE_YES)

        super(save_dlg, self).__init__(title, parent, 0, buttons)
        
        # Create diaog items
        self._msg = gtk.Label(_("Restore opened tabs on next run?"))
        self.vbox.pack_start(self._msg, True, True, 10)
        
        self._chk_save = gtk.CheckButton(_("Don't ask again (always save)"))
        self._chk_save.connect("toggled", self._on_chk_save_toggled)
        self.vbox.pack_start(self._chk_save, True, True, 10)

        self.show_all()
        
        # Setup configuration dictionary
        self._config = config
    
    def _on_chk_save_toggled(self, chk): # Reacts on checkbox toggle        
        if chk.get_active() == True:
            val = "off"
        else:
            val = "on"
        
        self._config.set("common", "save_prompt", val)
        
# ex:ts=4:et:
