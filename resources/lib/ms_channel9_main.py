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
    def __init__( self ):
        # Constants
        IMAGES_DIR = xbmc.translatePath( os.path.join( rootDir, 'resources', 'images' ) )        
        
        #
        # All
        #
        listitem = xbmcgui.ListItem( __language__(30401), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=list-all' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        #
        # Tags
        #
        listitem = xbmcgui.ListItem( __language__(30402), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=browse-tags' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        #
        # Shows
        #
        listitem = xbmcgui.ListItem( __language__(30403), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=browse-shows' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        #
        # Series
        #
        listitem = xbmcgui.ListItem( __language__(30404), iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1] ), url = '%s?action=browse-series' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)

        # Disable sorting...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )