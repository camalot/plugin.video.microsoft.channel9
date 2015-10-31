# recent: sort=recent
# mostviewed: sort=viewed
# toprated: sort: rating

import os
import sys
import urllib
import HTMLParser

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from HTTPCommunicator import HTTPCommunicator
import control
import utils


class Main:
    def __init__(self):
        # Constants
        self.DEBUG = False
        self.IMAGES_PATH = control.imagesPath

        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.current_page = int(params.get("page", "1"))
        self.sort_method = urllib.unquote_plus(params.get("sort", "NONE"))
        self.url = "https://channel9.msdn.com/Browse/AllContent?sort=%s&page=%i&%s"

        utils.set_no_sort()

        if self.sort_method == control.lang(30701):  # recent
            self.sort = "recent"
            self.get_entries()
        elif self.sort_method == control.lang(30702):  # viewed
            self.sort = "viewed"
            self.get_entries()
        elif self.sort_method == control.lang(30703):  # rating
            self.sort = "rating"
            self.get_entries()
        else:
            self.browse()

    def browse(self):
        # recent
        utils.add_directory(control.lang(30701), "DefaultFolder.png", None, "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30701))))
        # viewed
        utils.add_directory(control.lang(30702), "DefaultFolder.png", None, "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30702))))
        # rating
        utils.add_directory(control.lang(30703), "DefaultFolder.png", None, "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30703))))

        control.directory(handle=int(sys.argv[1], succeeded=True))

    def get_entries(self):
        http_communicator = HTTPCommunicator()
        url = self.url % (urllib.quote_plus(self.sort), self.current_page, utils.url_langs)
        html_data = http_communicator.get(url)

        soup_strainer = SoupStrainer("div", {"class": "tab-content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)

        ul_entries = beautiful_soup.find("ul", {"class": "entries"})
        li_entries = ul_entries.findAll("li")
        for li_entry in li_entries:
            utils.add_entry_video(li_entry)

        next_url = "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method))
        utils.add_next_page(self, beautiful_soup, next_url, self.current_page + 1)
        control.directory(handle=int(sys.argv[1], succeeded=True))
