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
Some logging utilities.
"""



import logging



_l = logging.getLogger("gedit-html-tidy.log")
_l.setLevel(logging.WARN)

_ch = logging.StreamHandler()
######
# Set here the logging level.
######
_ch.setLevel(logging.WARN)

_fmt = logging.Formatter("%(levelname)s -  %(message)s")
_ch.setFormatter(_fmt)

_l.addHandler(_ch)



def debug(msg):
	"""
	Logs a debug level message.
	
	Keyword arguments:
    msg -- The message (text).
	"""
	_l.debug(msg)



def info(msg):
	"""
	Logs an info level message.
	
	Keyword arguments:
    msg -- The message (text).
	"""
	_l.info(msg)



def warn(msg):
	"""
	Logs a warn level message.
	
	Keyword arguments:
    msg -- The message (text).
	"""
	_l.warn(msg)



def error(msg):
	"""
	Logs an error level message.
	
	Keyword arguments:
    msg -- The message (text).
	"""
	_l.error(msg)



def critical(msg):
	"""
	Logs a critical level message.
	
	Keyword arguments:
    msg -- The message (text).
	"""
	_l.critical(msg)
