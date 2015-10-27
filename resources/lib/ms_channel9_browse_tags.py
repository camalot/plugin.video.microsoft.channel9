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
        self.getVideos()

    #
    # Get videos...
    #
    def getVideos(self):
        #
        # Init
        #

        #
        # Get HTML page...
        #
        httpCommunicator = HTTPCommunicator()
        url = "http://channel9.msdn.com/Browse/Tags?page=%u" % self.current_page
        htmlData = httpCommunicator.get(url)

        #        
        # Parse response...
        #
        soupStrainer = SoupStrainer("div", {"class": "tab-content"})
        beautifulSoup = BeautifulSoup(htmlData, soupStrainer, convertEntities=BeautifulSoup.HTML_ENTITIES)

        #
        # Parse tags...
        #
        ul_columns = beautifulSoup.findAll("ul", {"class": "default column"})
        for ul_column in ul_columns:
            li_entries = ul_column.findAll("li")
            for li_entry in li_entries:
                a_tag = li_entry.a

                # Title                                
                title = a_tag.string

                # Tag page URL
                tag_url = a_tag["href"]

                # Add to list...
                listitem = xbmcgui.ListItem(title, iconImage="DefaultFolder.png")
                plugin_list_show = '%s?action=list-tag&tag-url=%s' % (sys.argv[0], urllib.quote_plus(tag_url))
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=plugin_list_show, listitem=listitem,
                                            isFolder=True)

        # Next page entry...
        ul_paging = beautifulSoup.find("ul", {"class": "paging"})
        if ul_paging:
            if ul_paging.find("li", {"class": "next"}):
                listitem = xbmcgui.ListItem(__language__(30503), iconImage="DefaultFolder.png",
                                            thumbnailImage=os.path.join(self.IMAGES_PATH, 'next-page.png'))
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                            url="%s?action=browse-tags&page=%i" % (sys.argv[0], self.current_page + 1),
                                            listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)

        # End of directory...
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
