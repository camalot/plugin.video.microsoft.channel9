#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import httplib
import HTMLParser
import re
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from ms_channel9_utils import HTTPCommunicator

#
# Constants
# 
__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString
rootDir = __settings__.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)


#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):
        # Constants
        self.DEBUG = False
        self.IMAGES_PATH = xbmc.translatePath(os.path.join(rootDir, 'resources', 'images'))

        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.current_page = int(params.get("page", "1"))

        #
        # Get the videos...
        #
        self.get_authors()

    #
    # Get videos...
    #
    def get_authors(self):

        http_communicator = HTTPCommunicator()
        url = "https://channel9.msdn.com/Browse/Authors?direction=desc&sort=atoz&page=%u&lang=en" % self.current_page
        html_data = http_communicator.get(url)
        html_parser = HTMLParser.HTMLParser()

        soup_strainer = SoupStrainer("ul", {"class": "authors"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)


        li_entries = beautiful_soup.findAll("li")
        for li_entry in li_entries:
            div_author_image = li_entry.find("img", {"class": "avatar"})

            if div_author_image is None:
                continue

            author_thumb = div_author_image['src']
            author_a = li_entry.find("a", {"class": "button"})
            author_link = author_a['href']

            span_name = li_entry.find("span", {"class": "name"})
            author_name = html_parser.unescape(span_name.string)
            span_count = li_entry.find("span", {"class": "count"})

            list_item = xbmcgui.ListItem(author_name, iconImage="DefaultFolder.png", thumbnailImage=author_thumb)
            folder_item = '%s?action=list-author&author-url=%s' % (sys.argv[0], urllib.quote_plus(author_link))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=folder_item, listitem=list_item, isFolder=True)

        # Next page entry...
        listitem = xbmcgui.ListItem(__language__(30503), iconImage="DefaultFolder.png",
                                    thumbnailImage=os.path.join(self.IMAGES_PATH, 'next-page.png'))
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                    url="%s?action=browse-authors&page=%i" % (sys.argv[0], self.current_page + 1),
                                    listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)

        # End of directory...
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
