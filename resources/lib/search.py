import os
import sys

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import control
import urllib
import json
from HTTPCommunicator import HTTPCommunicator
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString
rootDir = __settings__.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]
rootDir = xbmc.translatePath(rootDir)


class Main:
    def __init__(self):
        # Constants
        self.DEBUG = False
        self.IMAGES_PATH = xbmc.translatePath(os.path.join(rootDir, 'resources', 'images'))

        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.search_query = params.get("query", None)
        self.search()

    def search(self):
        if self.search_query is None:
            t = control.lang(30201).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            self.search_query = k.getText() if k.isConfirmed() else None

        if self.search_query is None or self.search_query == '':
            return

        print "query: %s" % self.search_query

        base_url = "https://c9search.azurewebsites.net/content/search?text=%s&$top=25&$skip=0&$inlinecount=allpages" % (
            urllib.quote_plus(self.search_query))
        http_communicator = HTTPCommunicator()
        data = http_communicator.get(base_url)

        start_index = data.index('"documents":') + 12
        if start_index <= 12:
            return

        json_data = data[start_index:-3]
        json_media = json.loads(json_data)

        for media in json_media:
            title = media["title"]
            url = media["permalink"]
            genre = media["published"]
            thumbnail = media["previewImage"]
            plot = media["summaryBody"]

            list_item = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
            list_item.setInfo("video", {"Title": title, "Studio": "Microsoft Channel 9", "Plot": plot, "Genre": genre})
            plugin_play_url = '%s?action=play&video_page_url=%s' % (sys.argv[0], urllib.quote_plus(url))
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item,
                                        isFolder=False)

        # Disable sorting...
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
        # End of directory...
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
