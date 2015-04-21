#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  meta_crawler_0.3.py
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
from collections import OrderedDict
from datetime import datetime
from bs4 import BeautifulSoup
import requests, re, random, codecs, sys, json
import couchdb

streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)

def soupify(url):
    # Parses html with Beautiful Soup
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	return soup

def randomlink(soup):
    # Finds all links on page and stores them in a list. Picks random link from list and returns it
	anchors = soup.find_all('a')
	#~ print anchors
	links = []
	for anchor in anchors:
		href = anchor.get('href')# .encode
		#print href
		if not isinstance(href, basestring):
			href = str(href)
		if href.strip().startswith("http"):
			links.append(href)

	if links:
		newurl = random.choice(links)
		print newurl
		return newurl
	else:
		print "Dead End."
		newurl = input("Enter new starting url: ")
		return newurl
	# TODO: Add Try/Except blocks


def build_meta_tags(soup):
    metas = soup.find_all('meta')
    meta_tags = []
    for i, meta in enumerate(metas):
        meta_tags.append(("meta%s" % str(i+1), meta.attrs))
    return OrderedDict(meta_tags)

def build_meta_store(url):
    meta_store = {}
    soup = None
    while len(meta_store) < 10:
        try:
            soup = soupify(url)
        except:
            if soup is None:
                url = input("New url: ")
            else:
                url = randomlink(soup)
            continue
        metas = build_meta_tags(soup)
        meta_store[url] = metas
        url = randomlink(soup)
    return meta_store

def write_meta_store(meta_store):
    meta_json = json.dumps(meta_store, indent=4, separators=(',', ': '))
    with open("%s.json" % datetime.isoformat(datetime.now()), "w") as f:
        f.write(meta_json)


if __name__ == '__main__':
#	main()

    meta_store = build_meta_store(input("Enter a URL to scrape:"))
    write_meta_store(meta_store)
