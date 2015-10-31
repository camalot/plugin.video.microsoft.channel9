# recent: sort=recent
# a-z: sort: atoz

import sys
import urllib

from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from HTTPCommunicator import HTTPCommunicator
import control
import utils


class Main:
    def __init__(self):
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.current_page = int(params.get("page", "1"))
        self.action = params.get("action", None)
        # self.sort_method = params.get("sort", control.infoLabel("Container.SortMethod"))
        self.sort_method = urllib.unquote_plus(params.get("sort", "NONE"))
        self.show_url = urllib.unquote_plus(params.get("show-url", ""))
        self.browse_url = "%s/Browse/Shows?sort=%s&page=%i&%s"

        utils.set_no_sort()

        if self.action is None or self.action == "browse-shows":
            if self.sort_method == control.lang(30701):  # recent
                self.sort = "recent"
            elif self.sort_method == control.lang(30704):  # AtoZ
                self.sort = "atoz"
            else:
                self.show_sort()
                return
            self.browse()
        elif self.action == "list-show" and self.show_url != "":
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
        print "fail: action=%s&show-url=%s" % (self.action, self.show_url)
        return

    def show_sort(self):
        # recent
        utils.add_directory(control.lang(30701), "DefaultFolder.png", None, "%s?action=browse-shows&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30701))))
        # A to Z
        utils.add_directory(control.lang(30704), "DefaultFolder.png", None, "%s?action=browse-shows&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30704))))
        control.directory_end()

    def show_list_sort(self):
        # recent
        utils.add_directory(control.lang(30701), "DefaultFolder.png", None,
                            "%s?action=list-show&page=%i&sort=%s&show-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30701)),
                            urllib.quote_plus(self.show_url)))
        # viewed
        utils.add_directory(control.lang(30702), "DefaultFolder.png", None,
                            "%s?action=list-show&page=%i&sort=%s&show-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30702)),
                            urllib.quote_plus(self.show_url)))
        # rating
        utils.add_directory(control.lang(30703), "DefaultFolder.png", None,
                            "%s?action=list-show&page=%i&sort=%s&show-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30703)),
                            urllib.quote_plus(self.show_url)))
        control.directory_end()

    def browse(self):
        http_communicator = HTTPCommunicator()
        url = self.browse_url % (utils.url_root, urllib.quote_plus(self.sort), self.current_page, utils.url_langs)
        html_data = http_communicator.get(url)

        soup_strainer = SoupStrainer("div", {"class": "tab-content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        ul_entries = beautiful_soup.find("ul", {"class": "entries"})
        li_entries = ul_entries.findAll("li")
        for li_entry in li_entries:
            self.add_show_directory(li_entry)

        next_url = "%s?action=browse-shows&page=%i&sort=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()

    def list(self):
        http_communicator = HTTPCommunicator()
        url = "%s%s?sort=%s&page=%i&%s" % (utils.url_root, self.show_url, self.sort, self.current_page, utils.url_langs)
        html_data = http_communicator.get(url)

        soup_strainer = SoupStrainer("div", {"class": "tab-content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        ul_entries = beautiful_soup.find("ul", {"class": "entries"})
        li_entries = ul_entries.findAll("li")
        for li_entry in li_entries:
            utils.add_entry_video(li_entry)

        next_url = "%s?action=list-show&page=%i&sort=%s&show-url=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method), urllib.quote_plus(self.show_url))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()

    def add_show_directory(self, entry):
        # Thumbnail...
        div_entry_image = entry.find("div", {"class": "entry-image"})
        thumbnail = div_entry_image.find("img", {"class": "thumb"})["src"]

        # Title
        div_entry_meta = entry.find("div", {"class": "entry-meta"})
        a_title = div_entry_meta.find("a", {"class": "title"})
        title = a_title.string

        # Show page URL
        show_url = a_title["href"]

        # Add to list...
        list_item = control.item(title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
        plugin_list_show = '%s?action=list-show&show-url=%s' % (sys.argv[0], urllib.quote_plus(show_url))
        control.addItem(handle=int(sys.argv[1]), url=plugin_list_show, listitem=list_item, isFolder=True)

