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
import json
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
        self.tag = urllib.unquote_plus(params.get("tag"))

        if self.tag == '#':
            self.tag = 'more'

        #
        # Get the videos...
        #
        self.get_tags()

    #
    # Get videos...
    #
    def get_tags(self):
        #
        # Init
        #

        http_communicator = HTTPCommunicator()
        url = "https://channel9.msdn.com/Browse/Tags/firstLetter/%s/json" % self.tag
        json_data = http_communicator.get(url)

        tags = json.loads(json_data)

        for tag in tags:
            list_item = xbmcgui.ListItem("%s (%s)" % (tag['name'], tag['entries']), iconImage="DefaultFolder.png",
                                         thumbnailImage=os.path.join(self.IMAGES_PATH, 'tag.png'))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="%s?action=list-tag&tag=%s" % (
                sys.argv[0], tag['name']), listitem=list_item, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)

        # End of directory...
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
