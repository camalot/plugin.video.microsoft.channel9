# recent: sort=recent
# a-z: sort: atoz

import sys
import urllib
import re
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request
import control
import utils
import json


class Main:
    def __init__(self):
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.current_page = int(params.get("page", "1"))
        self.action = params.get("action", None)
        # self.sort_method = params.get("sort", control.infoLabel("Container.SortMethod"))
        self.sort_method = urllib.unquote_plus(params.get("sort", "NONE"))
        self.tag_url = urllib.unquote_plus(params.get("tag-url", ""))
        self.browse_url = "%s/Browse/Tags/firstLetter/%s/json"
        self.tag = urllib.unquote_plus(params.get("tag", ""))

        if self.tag == '#':
            self.tag = 'more'

        utils.set_no_sort()

        if self.action is None or self.action == "browse-tags":
            self.tags_alpha()
            return
        elif self.action == "browse-tag-item":
            self.browse()
            return
        elif self.action == "list-tag":
            if self.sort_method == control.lang(30701):  # recent
                self.sort = "recent"
            elif self.sort_method == control.lang(30702):  # viewed
                self.sort = "viewed"
            elif self.sort_method == control.lang(30703):  # rating
                self.sort = "rating"
            else:
                self.show_list_sort()
                return
            self.list()
            return
        print "fail: action=%s&tag-url=%s" % (self.action, self.tag_url)
        return

    def tags_alpha(self):
        tag_list = control.lang(30601)
        for tag in tag_list:
            utils.add_directory("[B][COLOR green][UPPERCASE]%s[/UPPERCASE][/COLOR][/B]" % tag,
                                "%s/%s.png" % (control.imagesPath, tag), None,
                                "%s?action=browse-tag-item&&tag=%s" % (sys.argv[0], tag))
        control.directory_end()
        return

    def browse(self):
        url = self.browse_url % (utils.url_root, self.tag)
        json_data = http_request.get(url)
        tags = json.loads(json_data)
        for tag in tags:
            utils.add_directory("%s (%s)" % (tag['name'], tag['entries']), utils.icon_tag, utils.icon_tag,
                                "%s?action=list-tag&tag-url=%s" % (sys.argv[0], tag['href']))
        control.directory_end()
        return

    def show_list_sort(self):
        # recent
        utils.add_directory(control.lang(30701), utils.icon_folder, None,
                            "%s?action=list-tag&page=%i&sort=%s&tag-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30701)),
                                urllib.quote_plus(self.tag_url)))
        # viewed
        utils.add_directory(control.lang(30702), utils.icon_folder, None,
                            "%s?action=list-tag&page=%i&sort=%s&tag-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30702)),
                                urllib.quote_plus(self.tag_url)))
        # rating
        utils.add_directory(control.lang(30703), utils.icon_folder, None,
                            "%s?action=list-tag&page=%i&sort=%s&tag-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30703)),
                                urllib.quote_plus(self.tag_url)))
        control.directory_end()
        return

    def list(self):
        url = "%s%s?sort=%s&page=%i&%s" % (
        utils.url_root, self.tag_url, self.sort, self.current_page, utils.selected_languages())
        html_data = http_request.get(url)

        soup_strainer = SoupStrainer("div", {"class": "tab-content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        ul_entries = beautiful_soup.find("ul", {"class": "entries"})
        if ul_entries is None:
            control.directory_end()
            return
        li_entries = ul_entries.findAll("li")
        for li_entry in li_entries:
            utils.add_entry_video(li_entry)

        next_url = "%s?action=list-show&page=%i&sort=%s&show-url=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method), urllib.quote_plus(self.tag_url))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()
        return
