#
# Imports
#
import os
import sys

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon


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
        self.get_tags()

    #
    # Get videos...
    #
    def get_tags(self):
        #
        # Init
        #

        tag_list = __language__(30601)
        for tag in tag_list:
            list_item = xbmcgui.ListItem(tag, iconImage="DefaultFolder.png",
                                         thumbnailImage=os.path.join(self.IMAGES_PATH, 'tag.png'))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="%s?action=browse-tag-item&page=%i&tag=%s" % (
                sys.argv[0], self.current_page + 1, tag), listitem=list_item, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)

        # End of directory...
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
