#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  meta_crawler.py
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
from bs4 import BeautifulSoup
import requests, re, random, codecs, sys, json

streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)

def soupify(url):
    # Parses html with Beautiful Soup
	try:
		r = requests.get(url)
		soup = BeautifulSoup(r.text)
		return soup
	except ConnectionError:
		input("Could not connect to site. Please enter a new url:")

def randomlink(soup):
    # Finds all links on page and stores them in a list. Picks random link from list and returns it
	anchors = soup.find_all('a')
	#~ print anchors
	links = []
	for anchor in anchors:
		href = anchor.get('href')# .encode
		if not isinstance(href, basestring):
			href = str(href)
		if re.search('http', href) != None:
			links.append(href)
	if len(links) > 1:
		newurl = links[random.randint(0,len(links)-1)]
		print newurl
		return newurl
	elif len(links) > 0:
		newurl = links[0]
		print newurl
		return newurl
	else: 
		print "Dead End."
		newurl = input("Enter new starting url:")
		return newurl
	# TODO: Add Try/Except blocks
	
def store_metas(soup):
    # Finds all meta tags on given page and stores values and attributes to a file in valid JSON format
	meta_count = 0
	metas = soup.find_all('meta')
	meta_num = len(metas)
	if meta_num > 0:
		for meta in metas:
			meta_count += 1
			object_name = ""
			with open("meta_json.txt", "a+b") as f:
				f.write(object_name.join(['"meta', str(meta_count), '":'])) 
			meta_attributes = meta.attrs
			metas_db = json.dumps(meta_attributes, indent=4, separators=(',', ': '))
			with open("meta_json.txt", "a+b") as f:
				f.write(metas_db)
				if meta_count < meta_num:		
					f.write(",")
				else:
					f.write("}")
	else:
		with open("meta_json.txt", "a+b") as f:
			f.write('}')
		
def main(depth=10):
	pagecount = 0
	with open ("meta_json.txt", "w") as f:
		f.write('{')
	page = input("Enter a URL to scrape:")
	with open ("meta_json.txt", "a+b") as f:
		object_name = ""
		f.write(object_name.join(['"', page, '" : {']))
	soup = soupify(page)
	store_metas(soup)
	with open ("meta_json.txt", "a+b") as f:
		f.write(",")
	for i in range(depth):
		pagecount += 1
		newpage = randomlink(soup)
		with open("meta_json.txt", "a+b") as f:
			object_name = ""
			f.write(object_name.join(['"', newpage, '" : {']))
		newsoup = soupify(newpage)
		store_metas(newsoup)
		with open("meta_json.txt", "a+b") as f:
			if pagecount < depth:
				f.write(',')
			else:
				f.write('}')
		soup = newsoup
		page = newpage

if __name__ == '__main__':
	main()

