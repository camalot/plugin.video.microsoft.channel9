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
        self.get_videos()

    #
    # Get videos...
    #
    def get_videos(self):
        #
        # Init
        #

        #
        # Get HTML page...
        #
        httpCommunicator = HTTPCommunicator()
        url = "http://channel9.msdn.com/Browse/Series?page=%u&lang=en" % self.current_page
        htmlData = httpCommunicator.get(url)

        #        
        # Parse response...
        #
        soupStrainer = SoupStrainer("ul", {"class": "entries"})
        root_strainer = SoupStrainer("div", {"class": "mainContent"})
        beautifulSoup = BeautifulSoup(htmlData, soupStrainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        root_beautifulsoup = BeautifulSoup(htmlData, root_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        #
        # Parse shows...
        #
        li_entries = beautifulSoup.findAll("li")
        for li_entry in li_entries:
            # Thumbnail...
            div_entry_image = li_entry.find("div", {"class": "entry-image"})
            thumbnail = div_entry_image.find("img", {"class": "thumb"})["src"]

            # Title
            div_entry_meta = li_entry.find("div", {"class": "entry-meta"})
            a_title = div_entry_meta.find("a", {"class": "title"})
            title = a_title.string

            # Series page URL
            series_url = a_title["href"]

            # Plot
            div_description = div_entry_meta.find("div", {"class": "description"})
            plot = div_description.string

            # Add to list...
            listitem = xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
            plugin_list_show = '%s?action=list-series&series-url=%s' % (sys.argv[0], urllib.quote_plus(series_url))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=plugin_list_show, listitem=listitem, isFolder=True)

        # Next page entry...
        ul_paging = root_beautifulsoup.find("ul", {"class": "paging"})
        #if ul_paging:
        #    if ul_paging.find("li", {"class": "next"}):
        listitem = xbmcgui.ListItem(__language__(30503), iconImage="DefaultFolder.png",
            thumbnailImage=os.path.join(self.IMAGES_PATH, 'next-page.png'))
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="%s?action=browse-series&page=%i" % (
            sys.argv[0], self.current_page + 1), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)

        # End of directory...
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
