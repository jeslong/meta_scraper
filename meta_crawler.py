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


def randomlink(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
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
	# TODO: Add Try/Except blocks, Exception ConnectionError
	
def find_meta(page):
	r = requests.get(page)
	soup = BeautifulSoup(r.text)
	for meta in soup.find_all('meta'):
		return meta.attrs
		
def main(depth=100):
	page = input("Enter a URL to scrape:")
	metas = find_meta(page)
	print metas
	metas_db = json.dumps(metas, indent=4, separators=(',', ': '))
	with open("meta_json.txt", "w") as f:
		f.write(metas_db)
	for i in range(depth):
		newpage = randomlink(page)
		metas = find_meta(newpage)
		print metas
		metas_db = json.dumps(metas, indent=4, separators=(',', ': '))
		with open("meta_json.txt", "a+b") as f:
			f.write(metas_db)
		page = newpage

if __name__ == '__main__':
	main()

