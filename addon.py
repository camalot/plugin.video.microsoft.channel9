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
#   * Team Kodi                                                         [http://kodi.tv/]
#   * The Channel 9 Team @ Microsoft                                    [http://channel9.msdn.com/About]
#   * Leonard Richardson <leonardr@segfault.org> - BeautifulSoup 3.0.7a [http://www.crummy.com/software/BeautifulSoup/]
#   * Dan Dar3                                                          [http://dandar3.blogspot.com]
#

__addon__ = "Microsoft Channel 9"
__author__ = "Ryan Conrad"
__url__ = "https://github.com/camalot/plugin.video.microsoft.channel9"
__date__ = "10/27/2015"
__version__ = "2.0"

import os
import sys
import urlparse
import xbmc
import xbmcaddon

addon_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path'))
lib_path = xbmc.translatePath(os.path.join(addon_path, 'resources', 'lib'))
sys.path.append(lib_path)

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))

try:
    action = params['action']
except:
    action = None

if action is None:
    import home as plugin

if action == 'list-all':
    import all_content as plugin
elif action == 'browse-authors':
    import authors as plugin
elif action == 'search-authors':
    import authors as plugin
elif action == 'list-author':
    import authors as plugin
elif action == 'browse-tags':
    import tags as plugin
elif action == 'browse-tag-item':
    import tags as plugin
elif action == 'list-tag':
    import tags as plugin
elif action == 'browse-shows':
    import shows as plugin
elif action == 'list-show':
    import shows as plugin
elif action == 'browse-series':
    import series as plugin
elif action == 'list-series':
    import series as plugin
elif action == 'list-event':
    import events as plugin
elif action == 'browse-events':
    import events as plugin
elif action == 'browse-live':
    import events as plugin
elif action == 'list-blog':
    import blogs as plugin
elif action == 'browse-blogs':
    import blogs as plugin
elif action == 'search':
    import search as plugin
elif action == 'play':
    import play as plugin
elif action == 'settings':
    import settings as plugin
else:
    import home as plugin

plugin.Main()
