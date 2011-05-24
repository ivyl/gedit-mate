import os
import logging
from xml.etree import ElementTree as ET
from gi.repository import GObject, Gdk, Gtk, Gedit, GdkPixbuf, Gio

logging.basicConfig()
LOG_LEVEL = logging.DEBUG
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ICON_DIR = os.path.join(DATA_DIR, 'icons', '16x16')  
   
class FavoritesPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "FavoritesPlugin"
    window = GObject.property(type=Gedit.Window)
    FAVORITE_ICON = Gtk.STOCK_FILE
    FOLDER_ICON = "favorites-folder" #Gtk.STOCK_DIRECTORY
    
    def __init__(self):
        GObject.Object.__init__(self)
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(LOG_LEVEL)
        self._install_stock_icons()
  
    def _add_favorites_uri(self, parent_iter, uri):
        """ 
        Add a new favorite URI to the treeview under parent_iter. If the URI
        already exists, it will simply be selected.
        """
        exists = self._select_uri_in_treeview(self._store.get_iter_first(), uri)
        if not exists:
            name = os.path.basename(uri)
            self._store.append(parent_iter, (self.FAVORITE_ICON, name, uri, 0))
    
    def _add_favorites_folder(self, parent_iter, name):
        """ Add a new favorites folder to the treeview under parent_iter. """
        new_iter = self._store.append(parent_iter, (self.FOLDER_ICON, 
                                                    name, None, 1))
        return new_iter
        
    def _add_panel(self):
        # create the modal
        self._store = Gtk.TreeStore(GObject.TYPE_STRING,    # icon
                                    GObject.TYPE_STRING,    # name
                                    GObject.TYPE_STRING,    # uri
                                    GObject.TYPE_INT)       # editable 

        # create the treeview
        self._treeview = Gtk.TreeView.new_with_model(self._store)   
        column = Gtk.TreeViewColumn("Favorite")
        cell = Gtk.CellRendererPixbuf()
        column.pack_start(cell, False)
        column.add_attribute(cell, "stock-id", 0)
        cell = Gtk.CellRendererText()
        self._edit_cell = cell
        cell.connect("edited", self.on_cell_edited)
        column.pack_start(cell, True)
        column.add_attribute(cell, "text", 1)
        column.add_attribute(cell, "editable", 3)
        self._treeview.append_column(column)
        self._treeview.set_tooltip_column(2)
        self._treeview.set_headers_visible(False)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self._treeview)
        
        self._panel_widget = Gtk.VBox(homogeneous=False, spacing=2)
        self._panel_widget.pack_start(scrolled, True, True, 0)
        self._panel_widget.show_all()
        self._create_popup_menu()
        
        # add the panel
        filename = os.path.join(ICON_DIR, 'gedit-favorites.png')
        icon = Gtk.Image.new_from_file(filename)
        panel = self.window.get_side_panel()
        panel.add_item(self._panel_widget, "FavoritesPlugin", "Favorites", icon)
        
        # create popup
        
        
        # drag and drop not working in GTK+ 3.0. A patch has been committed.
        self._treeview.set_reorderable(True) 
        """
        targets = [('MY_TREE_MODEL_ROW', Gtk.TargetFlags.SAME_WIDGET, 0),]
        self._treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, 
                                                targets,
                                                Gdk.DragAction.DEFAULT |
                                                Gdk.DragAction.MOVE)
        """
        # connect signals
        self._treeview.connect("row-activated", self.on_row_activated)
        self._treeview.connect("button-press-event", self.on_button_press_event)

    def _add_ui(self):
        """ Merge the 'Project' menu into the Gedit menubar. """
        ui_file = os.path.join(DATA_DIR, 'menu.ui')
        manager = self.window.get_ui_manager()

        self._file_actions = Gtk.ActionGroup("FavoritesFile")
        self._file_actions.add_actions([
            ('AddToFavorites', self.FOLDER_ICON, "A_dd to Favorites", 
                None, "Add document to favorites.", 
                self.on_add_to_favorites_activate),
        ])
        self._file_actions.set_sensitive(False)
        manager.insert_action_group(self._file_actions)       

        self._ui_merge_id = manager.add_ui_from_file(ui_file)
        manager.ensure_update()
    
    def _begin_edit_at_iter(self, tree_iter):
        path = self._store.get_path(tree_iter)
        parent_iter = self._store.iter_parent(tree_iter)
        if parent_iter:
            self._treeview.expand_to_path(path)
        column = self._treeview.get_column(0)
        self._treeview.grab_focus()
        self._treeview.set_cursor_on_cell(path, column, self._edit_cell, True)
        
    def _create_popup_menu(self):
        """ Create the popup menu used by the treeview. """
        manager = Gtk.UIManager()
        self._popup_actions = Gtk.ActionGroup("TreeGlobalActions")
        self._popup_actions.add_actions([
            ('NewFolder', Gtk.STOCK_DIRECTORY, "New _Folder", 
                None, "Add a folder.", 
                self.on_new_folder_activate),
            ('Open', Gtk.STOCK_OPEN, "_Open", 
                None, "Open document.", 
                self.on_open_activate),
            ('Rename', None, "_Rename", 
                None, "Rename the item.", 
                self.on_rename_activate),
            ('Remove', Gtk.STOCK_REMOVE, "Re_move", 
                None, "Remove the item.", 
                self.on_remove_activate),
        ])
        manager.insert_action_group(self._popup_actions)
        ui_file = os.path.join(DATA_DIR, 'popmenu.ui')
        manager.add_ui_from_file(ui_file)
        self._popup = manager.get_widget("/FavoritesPopup")  
        
    def do_activate(self):
        """ Activate plugin. """
        self._add_panel()
        self._add_ui() 
        self.do_update_state()
        self.load_from_xml()

    def do_deactivate(self):
        """ Deactivate plugin. """
        self._remove_panel()
        self._remove_ui()
        self._save_to_xml()

    def do_update_state(self):
        """ Update UI to reflect current state. """
        if self.window.get_active_document():
            self._file_actions.set_sensitive(True)
        else:
            self._file_actions.set_sensitive(False)
    
    def error_dialog(self, message, parent=None):
        """ Display a very basic error dialog """
        self._log.warn(message)
        if not parent:
            parent = self.window
        dialog = Gtk.MessageDialog(parent,
                                   Gtk.DialogFlags.MODAL | 
                                   Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                   Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 
                                   message)
        dialog.set_title("Error")
        dialog.run()
        dialog.destroy()
    
    def _install_stock_icons(self):
        """ 
        Install the favorites folder icon used in the treeview to avoid confusion
        with the filebrowser plugin.
        """
        factory = Gtk.IconFactory()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(ICON_DIR, "favorites-folder.png"))
        iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
        factory.add('favorites-folder', iconset)
        factory.add_default()

    def _load_element(self, parent_iter, element):
        """ Recursive function to add elements from the XML to the treeview. """
        if element.tag == "folder":
            new_iter = self._add_favorites_folder(parent_iter, element.attrib['name'])
            for subelement in element:
                self._load_element(new_iter, subelement)
        elif element.tag == "uri":
            self._add_favorites_uri(parent_iter, element.text)
        
    def load_from_xml(self):
        """ Load the favorites into the treeview from an XML file. """
        self._store.clear()
        filename = os.path.join(DATA_DIR, "favorites.xml")
        xml = ET.parse(filename)
        root = xml.getroot()
        for element in root:
            self._load_element(None, element)

    def on_add_to_favorites_activate(self, action, data=None):
        """ Add the current document to the treeview. """
        document = self.window.get_active_document()
        if document:
            location = document.get_location()
            if location:
                uri = location.get_uri()
                self._add_favorites_uri(None, uri)
    
    def on_button_press_event(self, treeview, event):
        """ Show popup menu. """
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor(path, col, 0)
                tree_iter = self._store.get_iter(path)
                uri = self._store.get_value(tree_iter, 2)
                if uri: 
                    self._popup_actions.get_action("Open").set_sensitive(True)
                    self._popup_actions.get_action("NewFolder").set_sensitive(False)
                    self._popup_actions.get_action("Rename").set_sensitive(False)
                    self._popup_actions.get_action("Remove").set_sensitive(True)
                else:
                    self._popup_actions.get_action("Open").set_sensitive(True)
                    self._popup_actions.get_action("NewFolder").set_sensitive(True)
                    self._popup_actions.get_action("Rename").set_sensitive(True)
                    self._popup_actions.get_action("Remove").set_sensitive(True)
            else:
                treeview.get_selection().unselect_all()
                self._popup_actions.get_action("Open").set_sensitive(False)
                self._popup_actions.get_action("NewFolder").set_sensitive(True)
                self._popup_actions.get_action("Rename").set_sensitive(False)
                self._popup_actions.get_action("Remove").set_sensitive(False)
            self._popup.popup(None, None, None, None, event.button, time)
            return True
    
    def on_cell_edited(self, cell, path, new_text, data=None):
        self._store[path][1] = new_text
        
    def on_remove_activate(self, action, data=None):
        selection = self._treeview.get_selection()
        model, tree_iter = selection.get_selected()
        self._store.remove(tree_iter)
    
    def on_row_inserted(self, model, path, tree_iter, data=None):
        print "on_row_inserted"
        self._store.set_value(tree_iter, 1, "test")
        
    def on_rows_reordered(self, model, path, tree_iter, new_order, data=None):
        print "on_rows_reordered"
        self._store.set_value(tree_iter, 1, "test")
        
    def on_new_folder_activate(self, action, data=None):
        """ Create a new untitled folder. """
        selection = self._treeview.get_selection()
        model, tree_iter = selection.get_selected()
        if tree_iter:
            uri = model.get_value(tree_iter, 2)
            if uri is not None:
                parent_iter = model.iter_parent(tree_iter)
            else:
                parent_iter = tree_iter
        else:
            parent_iter = None
        new_iter = self._add_favorites_folder(parent_iter, "Untitled")
        self._begin_edit_at_iter(new_iter)
        
    def on_open_activate(self, action, data=None):
        selection = self._treeview.get_selection()
        model, tree_iter = selection.get_selected()
        uri = model.get_value(tree_iter, 2)
        if uri:
            self._open_uri(uri)
        else:
            self._open_uris_at_iter(tree_iter)
    
    def on_rename_activate(self, action, data=None):
        selection = self._treeview.get_selection()
        model, tree_iter = selection.get_selected()
        if tree_iter:
            self._begin_edit_at_iter(tree_iter)
        
    def on_row_activated(self, treeview, path, column, data=None):
        model = treeview.get_model()
        tree_iter = model.get_iter(path)
        uri = model.get_value(tree_iter, 2)
        if uri:
            self._open_uri(uri)
   
    def _open_uri(self, uri):
        location = Gio.file_new_for_uri(uri)
        tab = self.window.get_tab_from_location(location)
        if tab:
            self.window.set_active_tab(tab)
        else:
            self.window.create_tab_from_location(location, None, 0, 0, False, True) 
    
    def _open_uris_at_iter(self, tree_iter):
        """ Recursively open all URIs under tree_iter. """
        model = self._store
        while tree_iter:
            uri = model.get_value(tree_iter, 2)
            if uri:
                self._open_uri(uri)
            if model.iter_has_child(tree_iter):
                child_iter = model.iter_children(tree_iter)
                self._open_uris_at_iter(child_iter)
            tree_iter = model.iter_next(tree_iter)
    
    def _remove_panel(self):
        """ Removes the side panel """
        if self._panel_widget:
            panel = self.window.get_side_panel()
            panel.remove_item(self._panel_widget)
        
    def _remove_ui(self):
        """ Remove the 'Project' menu from the Gedit menubar. """
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._file_actions)
        manager.ensure_update()

    def _get_xml_at_iter(self, tree_iter, spaces=2):
        xml = ""
        tabs = " " * spaces
        while tree_iter:
            if self._store.get_value(tree_iter, 2) == None:
                name = self._store.get_value(tree_iter, 1)
                xml += "%s<folder name=\"%s\">\n" % (tabs, name)
                if self._store.iter_has_child(tree_iter):
                    child_iter = self._store.iter_children(tree_iter)
                    xml += self._get_xml_at_iter(child_iter, spaces+2)
                xml += "%s</folder>\n" % tabs
            else:
                uri = self._store.get_value(tree_iter, 2)
                xml += "%s<uri>%s</uri>\n" % (tabs, uri)
                """
                Temporary hack to fix folders dropped on files since we cannot
                implement a custom drag and drop in GTK+ 3.0 (patch committed)
                """
                if self._store.iter_has_child(tree_iter):
                    name = self._store.get_value(tree_iter, 1)
                    xml += "%s<folder name=\"%s\">\n" % (tabs, name)
                    child_iter = self._store.iter_children(tree_iter)
                    xml += self._get_xml_at_iter(child_iter, spaces+2)
                    xml += "%s</folder>\n" % tabs
                    
            tree_iter = self._store.iter_next(tree_iter)
        
        return xml
        
    def _save_to_xml(self):
        """ Save the favorites tree to the XML file. """
        filename = os.path.join(DATA_DIR, "favorites.xml")
        xml =  "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        xml += "<gedit-favorites version=\"1.0\">\n"
        xml += self._get_xml_at_iter(self._store.get_iter_first())
        xml += "</gedit-favorites>\n"
        
        f = open(filename, "w")
        f.write(xml)
        f.close()
    
    def _select_uri_in_treeview(self, tree_iter, uri):
        """ Recursively find URI in treeview and select it or return False. """
        model = self._store
        while tree_iter:
            row_uri = model.get_value(tree_iter, 2)
            if row_uri:
                if row_uri == uri:
                    path = model.get_path(tree_iter)
                    self._treeview.expand_to_path(path)
                    self._treeview.set_cursor(path, None, False)
                    return True
            if model.iter_has_child(tree_iter):
                child_iter = model.iter_children(tree_iter)
                exists = self._select_uri_in_treeview(child_iter, uri)
                if exists:
                    return exists
            tree_iter = model.iter_next(tree_iter)
        return False

    
    
