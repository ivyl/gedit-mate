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
Output pane for displaying Tidy's output.
"""



import unittest
import pygtk
pygtk.require('2.0')
import gtk
import pango
import sys, string
import log_utils
import tidy_utils



def _make_column(title, num, markup, allow_sort):
	renderer = gtk.CellRendererText()
		
	column = gtk.TreeViewColumn(title, renderer)
	
	if markup:
		column.add_attribute(renderer, 'markup', num)
	else:
		column.add_attribute(renderer, 'text', num)
	
	if allow_sort:
		column.set_sort_column_id(num)

	return column



def _type_to_color(type_):
	assert tidy_utils.is_valid_type(type_)

	if type_ == 'Error':
		return 'red'
	elif type_ == 'Warning':
		return 'orange'
	elif type_ == 'Config':
		return 'purple'
	else:
		return 'black'			
	


def _color_span(color, s):
	return '<span foreground = "%s">%s</span>' %(color, s)

	

def _cond_visible(n):
	if n != None:
		return n
		
	return ''



def _str_to_int(s):
	if s == '':
		return None
		
	return int(s)
	


def _make_str_int_cmp(num):
	def str_int_cmp(model, it0, it1):
		lhs = _str_to_int( model.get_value(it0, num) )
		rhs = _str_to_int( model.get_value(it1, num) )
		
		if lhs == None and rhs == None:
			return 0

		if lhs == None:
			return -1
			
		if rhs == None:
			return 1
			
		if lhs < rhs:
			return -1
		if lhs == rhs:
			return 0
		return 1

	return str_int_cmp
	
	

class _output_box(gtk.TreeView):
	def __init__(self, on_activated):
		self._list_store = gtk.ListStore(str, str, str, str)
		super(_output_box, self).__init__(self._list_store)
		
		self.append_column(_make_column('Line', 0, False, True))			
		self._list_store.set_sort_func(0, _make_str_int_cmp(0))
		
		self.append_column(_make_column('Column', 1, False, False))	
		self._list_store.set_sort_func(1, _make_str_int_cmp(1))
		
		self.append_column(_make_column('Type', 2, True, True))	
		
		self.append_column(_make_column('Message', 3, False, True))	
						
		self.set_headers_clickable(True)
		
		self._on_activated = on_activated
		
		self.connect("row-activated", self._on_row_activated)		
						
		
	def append(self, line, col, type_, what):		
		log_utils.debug('adding  %s %s %s %s to output box' %(line, col, type_, what))
				
		color = _type_to_color(type_)
		
		log_utils.debug('adding  %s %s to output box' %(_color_span(color, type_), what))
			
		self._list_store.append([_cond_visible(line), _cond_visible(col), _color_span(color, type_), what])
		
		log_utils.debug('added to output box')
		
		
	def clear(self):
		log_utils.debug('clearing output box')
	
		self._list_store.clear()
		
		log_utils.debug('cleared output box')
		
		
	def _on_row_activated(self, view, row, column):
		assert self == view
		
		model = view.get_model()
		iter = model.get_iter(row)

		line = _str_to_int( model.get_value(iter, 0) )
		col = _str_to_int( model.get_value(iter, 1) )
		type_ = model.get_value(iter, 2)
		what = model.get_value(iter, 3)
		
		self._on_activated(line, col, type_, what)



class output_pane(gtk.ScrolledWindow):
	"""
	Output pane for displaying Tidy's output.
	"""
	def __init__(self, on_activated):
		"""
		Keyword arguments:
	    on_activated -- Callback for when a row is activated.
		"""
		super(output_pane, self).__init__()
				
		self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC);
		self.set_shadow_type(gtk.SHADOW_IN)
		
		self._box = _output_box(on_activated)
				
		self.add_with_viewport(self._box)
		self._box.show()
		
		self.target_uri = None
		
		
	def append(self, line, col, type_, what):
		"""
		Append another row.
		"""
		self._box.append(line, col, type_, what)
		
	
	def clear(self):
		"""
		Clear all rows.
		"""
		self._box.clear()
		
		self.target_uri = None		



class test(unittest.TestCase):		
	def _print_activated(self, line, col, type_, what):
		print line, col, type_, what
		

	def test_output_pane_0(self):		
		o = output_pane(self._print_activated)

		o.connect("destroy", gtk.main_quit)	

		main_wnd = gtk.Window(gtk.WINDOW_TOPLEVEL)
		main_wnd.set_title('Output');
		main_wnd.add(o)
		
		o.target_uri = 'foo'

		o.append(None, None, 'Info', 'Some info')		
		o.append(1, 2, 'Warning', 'Bad stuff!')
		o.append(10, 2, 'Error', 'unknown tag <boo>')
		o.append(1, 222, 'Warning', 'Also bad stuff!')
		o.append(6, 2, 'Config', 'Just config stuff')
		o.append(None, None, 'Config', 'Just config stuff with no line')		
			
		main_wnd.show_all()
		gtk.main()



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()
