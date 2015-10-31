import sys

import control
import urllib
import utils
import json
from HTTPCommunicator import HTTPCommunicator


class Main:
    def __init__(self):
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.search_query = params.get("query", None)
        self.search()

        utils.set_no_sort()
        return

    def search(self):
        if self.search_query is None:
            t = control.lang(30201).encode('utf-8')
            k = control.keyboard('', t)
            k.doModal()
            self.search_query = k.getText() if k.isConfirmed() else None

        if self.search_query is None or self.search_query == '':
            return

        base_url = "https://c9search.azurewebsites.net/content/search?text=%s&$top=100&$skip=0&$inlinecount=allpages" \
                   % (urllib.quote_plus(self.search_query))
        http_communicator = HTTPCommunicator()
        data = http_communicator.get(base_url)
        print base_url
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

            list_item = control.item(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
            list_item.setInfo("video", {"Title": title, "Studio": "Microsoft Channel 9", "Plot": plot, "Genre": genre})
            plugin_play_url = '%s?action=play&video_page_url=%s' % (sys.argv[0], urllib.quote_plus(url))
            control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item, isFolder=False)

        # End of directory...
        control.directory_end()
        return
