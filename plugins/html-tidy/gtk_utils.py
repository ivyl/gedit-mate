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
GTK utilities.
"""


import string
import unittest
import pygtk
pygtk.require('2.0')
import gtk
import log_utils
import unittest



def get_view_text(view):
	"""
	Retrieves all the text in a gtk.TextView
	
	Keyword arguments:
    view -- The gtk.TextView object.
	"""
	log_utils.debug('retrieving text')
		
	bf = view.get_buffer()

	start = bf.get_start_iter()
	end = bf.get_end_iter()

	text = bf.get_text(start, end)		
	
	log_utils.debug('retrieved text')

	return text
	
	
	
def get_num_cols_at_line(bf, line):
	"""
	Retrieves the number of columns in a given line of a gtk.TextBuffer.
	
	Keyword arguments:
    bf -- The gtk.TextBuffer object.
    line -- The line number.
	"""
	line_start_it = bf.get_iter_at_line(line)

	it = line_start_it
	count = 0

	while not it.is_end() and it.get_char() != '\n':
		count = count + 1

		it.forward_char()
		
	return count
	
	
	
def _scroll_to_it(view, bf, it):
	(start, end) = bf.get_bounds()
	
	bf.place_cursor(it)
	
	view.scroll_to_iter(end, within_margin = 0.25, use_align = False)
	view.scroll_to_iter(it, within_margin = 0.25, use_align = False)
	
	view.grab_focus()
	
	
	
# Taken from the classbrowser plugin code, Copyright (C) 2006 Frederic Back (fredericback@gmail.com)
def scroll_view_to_line_col(view, line, col):
	"""
	Places cursor at some gtk.TextView in some line and column
	
	Keyword arguments:
    view -- The gtk.TextView object.
    line -- The line number.
    col -- The column.
	"""
	log_utils.debug('scrolling to line  = %d col  = %d ' % (line, col))
	
	assert line > 0 and col > 0
	
	line = line - 1
	col = col - 1

	bf = view.get_buffer()
	
	if col < get_num_cols_at_line(bf, line):
		it = bf.get_iter_at_line_offset(line, col)
	else:
		it = bf.get_iter_at_line(line)	

	_scroll_to_it(view, bf, it)
	    
	log_utils.debug('scrolled to line  = %d col  = %d ' % (line, col))
	
	
	
def num_non_whites_till_cur(bf):	
	"""
	Retrieves the number of non whitespace characters in a gtk.TextBuffer
	up to the current insert cursor.
	
	Keyword arguments:
    bf -- gtk.TextBuffer object.
	"""
	log_utils.debug('retrieving text')
	
	it = bf.get_start_iter()
	
	insert_iter = bf.get_iter_at_mark(bf.get_insert())
	
	count = 0
	while not it.equal(insert_iter):
		if not  it.get_char() in string.whitespace:
			count = count + 1
			
		it.forward_char()
		
	log_utils.debug('retrieved text; non_whites = %d' % count)
			
	return count
		
	

def cursor_to_non_whites(view, non_white):
	"""
	Given a gtk.TextView and a number of non-whitespace characters, places the cursor
	and scrolls the view to this number of spaces from the beginning.
	
	Keyword arguments:
    view -- The gtk.TextView object.
    non_white -- The number of non whitespace chars.
	"""
	bf = view.get_buffer()
	
	(start, end) = bf.get_bounds()
	it = start
	
	log_utils.debug('scrolling non_white = %d' % non_white)
	
	count = 0
	while not it.is_end() and count < non_white:
		if not  it.get_char() in string.whitespace:
			count = count + 1
			
		it.forward_char()

	_scroll_to_it(view, bf, it)
	
	log_utils.debug('scrolled')



class test(unittest.TestCase):		
	def _non_whites_on_change(self, bf):
		num_non_whites_till_cur(bf)
		

	def test_non_whites(self):		
		main_box = gtk.VBox(False, 2)
	
		v = gtk.TextView()
		
		bf = v.get_buffer()
		
		v.connect('destroy', gtk.main_quit)	
		
		v.set_size_request(200, 200)
		
		main_box.pack_start(v, True, True, 2)
		
		main_box.pack_start(gtk.HSeparator(), False, False, 2)

		nonwhites_button = gtk.Button('_Check')		
		nonwhites_box = gtk.HBox(False, 2)
		nonwhites_label = gtk.Label('Non-Whites:')
		nonwhites_entry = gtk.Entry()
		nonwhites_box.pack_start(nonwhites_button, False, False, 2)
		nonwhites_box.pack_start(nonwhites_label, False, False, 2)
		nonwhites_box.pack_start(nonwhites_entry, True, True, 2)
		
		main_box.pack_start(nonwhites_box, False, False, 2)

		main_wnd = gtk.Window(gtk.WINDOW_TOPLEVEL)
		main_wnd.set_title('Non-Whites Test');
		main_wnd.add(main_box)
		
		def on_check_non_whites(b):	
			non_white = num_non_whites_till_cur(bf)
				
			nonwhites_entry.set_text(str(non_white))
			
			cursor_to_non_whites(v, non_white)
	
		nonwhites_button.connect('clicked', on_check_non_whites)
		
		main_wnd.show_all()
		gtk.main()



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test)
		
		

if __name__ == '__main__':
	unittest.main()

	
	
	


