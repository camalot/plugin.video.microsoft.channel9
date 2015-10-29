##############################################################################
#
# Microsoft Channel 9 - Video addon for Kodi
# http://channel9.msdn.com
#
# Version 2.0
# 
#
# https://github.com/camalot/plugin.video.microsoft.channel9
#
#
# Credits:
#   * Team XBMC                                                         [http://xbmc.org/]
#   * The Channel 9 Team @ Microsoft                                    [http://channel9.msdn.com/About]
#   * Leonard Richardson <leonardr@segfault.org> - BeautifulSoup 3.0.7a [http://www.crummy.com/software/BeautifulSoup/]
#   * Dan Dar3                                                          [http://dandar3.blogspot.com]
#

# 
# Constants
#
__addon__ = "Microsoft Channel 9"
__author__ = "Ryan Conrad"
__url__ = "https://github.com/camalot/plugin.video.microsoft.channel9"
__date__ = "10/27/2015"
__version__ = "2.0"

#
# Imports
#
import os
import sys
import xbmcaddon
import urlparse

__settings__ = xbmcaddon.Addon()
rootDir = __settings__.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)

LIB_DIR = xbmc.translatePath(os.path.join(rootDir, 'resources', 'lib'))
sys.path.append(LIB_DIR)

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))

try:
    action = params['action']
except:
    action = None

if action is None:
    import ms_channel9_main as plugin

if action == 'list-all':
    import ms_channel9_list_all as plugin
elif action == 'browse-authors':
    import ms_channel9_browse_authors as plugin
elif action == 'browse-tags':
    import ms_channel9_browse_tags as plugin
elif action == 'browse-tag-item':
    import ms_channel9_browse_tag_item as plugin
elif action == 'list-tag':
    import ms_channel9_list_tag as plugin
elif action == 'browse-shows':
    import ms_channel9_browse_shows as plugin
elif action == 'list-show':
    import ms_channel9_list_show as plugin
elif action == 'browse-series':
    import ms_channel9_browse_series as plugin
elif action == 'list-series':
    import ms_channel9_list_series as plugin
elif action == 'list-event':
    import ms_channel9_list_events as plugin
elif action == 'browse-event':
    import ms_channel9_browse_events as plugin
elif action == 'browse-live':
    import ms_channel9_browse_live as plugin
elif action == 'list-blog':
    import ms_channel9_list_blogs as plugin
elif action == 'browse-blog':
    import ms_channel9_browse_blogs as plugin
elif action == 'browse-authors':
    import ms_channel9_browse_authors as plugin
elif action == 'list-author':
    import ms_channel9_list_author as plugin
elif action == 'play':
    import ms_channel9_play as plugin
else:
    xbmc.log("[ADDON] %s v%s (%s)" % (__addon__, __version__, __date__), xbmc.LOGNOTICE)
    import ms_channel9_main as plugin

plugin.Main()
