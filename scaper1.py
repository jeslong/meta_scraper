#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2014 utilite <utilite@utilite-ubuntu-desktop>
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
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import urllib2
from HTMLParser import HTMLParser

metacount = 0;
meta_attributes = []
a_count = 0;
a_attributes = []

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	# function to handle an opening tag in the doc
	# this will be called when the closing ">" of the tag is reached
	def handle_starttag(self, tag, attrs):
		global metacount
		global meta_attributes
		global a_count
		global a_attributes
		print "Encountered a start tag:", tag
		if tag == "meta":
			metacount += 1
			meta_attributes.append(attrs)
		if tag == "a":
			a_count += 1
			a_attributes.append(attrs)
		pos = self.getpos() # returns a tuple indication line end character
		print "At line: ", pos[0], " position ", pos[1]
		if attrs.__len__>0:
			print "\tAttributes:"
			for a in attrs:
				print "\t", a[0], "=", a[1]
	
	#function to handle the ending tag
	def handle_endtag(self, tag):
		print "Encountered an end tag:", tag
		pos = self.getpos()
		print "At line: ", pos[0], " position ", pos[1]
		
	#function to handle character and text data (tag contents)
	def handle_data(self,data):
		print "Encountered some data:", data
		pos = self.getpos()
		print "At line: ", pos[0], " position ", pos[1]
	
	#function to handle the processing of HTML comments
	def handle_comment(self, data):
		print "Encountered comment:", data
		pos = self.getpos()
		print "At line: ", pos[0], " position ", pos[1]
		
def main():
	webUrl  = input('Enter a URL to parse: ')
	# open a connection to a URL using urllib2
	website = urllib2.urlopen(webUrl) 
	result_code = str(website.getcode())
	if result_code == '200':
		#instantiate the parser and feed it some HTML
		parser = MyHTMLParser()
	
		# open the sample HTML file and feed it some HTML
		contents = website.read() #read the entire file
		parser.feed(contents)
		
		print "%d meta tags encountered" % metacount
		print "%d anchor tags encountered" % a_count
		print "Meta attributes: "
		for attribute in meta_attributes:
			print attribute
		print "Anchor attributes: "
		for attribute in a_attributes:
			print attribute
		
		
	else:
		print "Invalid URL"

if __name__ == '__main__':
	main()

