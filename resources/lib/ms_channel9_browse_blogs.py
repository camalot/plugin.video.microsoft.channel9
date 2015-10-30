#
# Imports
#
import os
import sys
import urllib
import re

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from HTTPCommunicator import HTTPCommunicator



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
        http_communicator = HTTPCommunicator()
        url = "http://channel9.msdn.com/Browse/Blogs?sort=recent&page=%u&lang=en" % self.current_page
        html_data = http_communicator.get(url)

        #        
        # Parse response...
        #
        soup_strainer = SoupStrainer("ul", {"class": "entries"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)

        #
        # Parse shows...
        #
        li_entries = beautiful_soup.findAll("li")
        for li_entry in li_entries:
            # Thumbnail...
            div_entry_image = li_entry.find("div", {"class": "entry-image"})
            thumbnail = div_entry_image.find("img", {"class": "thumb"})["src"]

            # Title
            div_entry_meta = li_entry.find("div", {"class": "entry-meta"})
            a_title = div_entry_meta.find("a", {"class": "title"})
            title = a_title.string

            # Show page URL
            show_url = a_title["href"]

            # this is to ignore things that are not linked to channel9
            if re.match('^https?:', show_url):
                continue

            print show_url

            # Plot
            div_description = div_entry_meta.find("div", {"class": "description"})
            plot = div_description.string

            # Add to list...
            listitem = xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
            plugin_list_show = '%s?action=list-blog&blog-url=%s' % (sys.argv[0], urllib.quote_plus(show_url))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=plugin_list_show, listitem=listitem, isFolder=True)

        # Next page entry...
        listitem = xbmcgui.ListItem(__language__(30503), iconImage="DefaultFolder.png",
                                    thumbnailImage=os.path.join(self.IMAGES_PATH, 'next-page.png'))
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                    url="%s?action=browse-blog&page=%i" % (sys.argv[0], self.current_page + 1),
                                    listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)

        # End of directory...
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
