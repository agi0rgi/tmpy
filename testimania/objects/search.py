#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# https://stackoverflow.com/a/17388505
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class TestimaniaSearch():
	"""
	Class responsible for the research of a
	specific song/artist/album on Testimania.com
	"""

	def __init__(self):
		self.__limit = 5
		self.__offset = 1

		self._search_query = ""
		self._lastresults = []
		self._base_url = "http://www.testimania.com/"
		self._search_url = self._base_url+"searchesp.php"

	def _query(self):
		"""
		Type: Protected

		Makes a request to the testimania search
		page with the query and passes
		the result page content to _parse()
		"""

		headers = {"Host": "www.testimania.com",
		"Connection": "keep-alive",
		"Referer": "www.testimania.com/searchesp.php",
		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
		"Upgrade-Insecure-Requests": "1",
		}
		response = requests.post(self._search_url, headers=headers, data={
		                         'keyword': self._search_query})
		content = response.content
		page = BeautifulSoup(content, "html.parser")
		self._parse(page)

	def _parse(self, page):
		"""
		Type: Protected

		Scrapes information from the given page aka
		Song title, Song artist, and the lyrics link
		then build a dict containing those infos and
		append it to the results list
		"""

		if self._lastresults:
			self._lastresults = []
		data = page.find("ul", attrs={"class": "search-list"})
		if not data:
		    return
		songs = data.findAll("li", limit=self.__limit)
		for song in songs:
			title_artist = song.find("a").text.split(" - ")
			url = song.find("a")['href']
			artist = title_artist[0]
			title = title_artist[1]
			self._lastresults.append({"artist": artist, "title": title, "url": self._base_url+url})


	def _reliable_results(self, query):
		"""
		Type: Protected

		Analyze the results and if atleast one matches,
		or its highly similar to the query then leave the
		results unchanged, otherwise delete them
		"""
		# check if at least one result fits the query at least at the 60%
		for result in self._lastresults:
			titleonly = result["title"]
			artistonly = result["artist"]
			titleandartist = result["title"] + " "+result["artist"]
			artistandtitle = result["artist"] + " "+result["title"]
			if similar(artistonly, query) >= 0.6:
				return True
			if similar(titleonly, query) >= 0.6:
				return True
			if similar(titleandartist, query) >= 0.6:
				return True
			if similar(artistandtitle, query) >= 0.6:
				return True

				
		# no valid results found, setting em to none
		self._lastresults = None

	def search(self,query,limit=5,checkreliability=False):
		"""
		Type: Public
	
		Parasm:	Query text (String)
				Limit of results (Integer)

		Set a couple of attributes and
		calls _query method, than return the list
		containing the results
		"""
		# check if query is valid ( must be at least 3 chars long )
		if len(query)<3:
			return
			
		if limit <= 10:
			self.__limit = limit
		else:
			self.__limit = 10
			
			
		self._search_query=query
		self._query()
		
	    # check the reliability of the results if parameter is true
		if checkreliability:
		    if self._reliable_results(query):
		        return self._lastresults
		    return
		return self._lastresults
