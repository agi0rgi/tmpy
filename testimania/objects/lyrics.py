#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup


class Lyrics():
    """
    Class containing every lyrics info
    """

    def __init__(self, artist, text, title, url=None):
        self._artist = artist
        self._title = title
        self._text = text
        self._url = url

    def __iter__(self):
        """
        Just a generator that makes the object iterable
        """
        yield "artist", self._artist
        yield "title", self._title
        yield "text", self._text
        yield "url", self._url

    def lyrics_dict(self):
        """
        Params: None

        Returns: A dict containing every object information
        """
        return dict(self.__iter__())


class TestimaniaParser():
    """
    Class responsible for the parsing of
    the lyrics information
    """

    def __init__(self):
        self._url = ""
        self._lyrics = Lyrics(None, None, None)

    def _query(self):
        """	
        Type: Protected

        Makes a request to the lyrics page, and pass
        the bs object containing the page source
to the _parse function
        """

        headers = {"Host": "www.testimania.com",
                   "Connection": "keep-alive",
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
                   "Upgrade-Insecure-Requests": "1",
                   }

        response = requests.get(self._url, headers=headers)
        content = response.content
        page = BeautifulSoup(content, "html.parser")
        self._parse(page)

    def _parse(self, page):
        """
        Type: Protected

        Params: Page Contet (Bs Object)

        This method scrapes every information
        it finds about the given url's lyrics
        and builds the Lyrics object
        """
        try:
            text = page.find("div", attrs={"id": "lyrics"})
            try:
                [s.extract() for s in text('script')] # clean lyrics from obstrusive scripts
                [s.extract() for s in text('div')] # clean lyrics from obstrusive scripts
                [s.extract() for s in text('br')] # clean lyrics from obstrusive scripts
            except:
                pass
            
            text = text.prettify().replace('<div id="lyrics">',"").replace("</div>","")
        except:
            return
        title = page.find("h1").text.replace("Testo ", "", 1)
        artist = page.find("ul", attrs={"class": "route"})
        artist = artist.find("li").text
        self._lyrics = Lyrics(artist, text, title, self._url)
        #except:
            #pass    # the result could be a ringtone or there still is no text
        
        
        
    def lyrics(self, url):
        """
        Type: Public

        Params: Lyrics Url (String)

        Calls _query method and just 
        returns the Lyrics object after
        processing.
        """
        self._url = url
        self._query()
        return self._lyrics
