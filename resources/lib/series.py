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
import xbmc


class Main:
    def __init__(self):
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.current_page = int(params.get("page", "1"))
        self.action = params.get("action", None)
        # self.sort_method = params.get("sort", control.infoLabel("Container.SortMethod"))
        self.sort_method = urllib.unquote_plus(params.get("sort", "NONE"))
        self.series_url = urllib.unquote_plus(params.get("series-url", ""))
        self.browse_url = "%s/Browse/Series?sort=%s&page=%i&%s"

        utils.set_no_sort()

        if self.action is None or self.action == "browse-series":
            if self.sort_method == control.lang(30701):  # recent
                self.sort = "recent"
            elif self.sort_method == control.lang(30704):  # AtoZ
                self.sort = "atoz"
            else:
                self.show_sort()
                return
            self.browse()
        elif self.action == "list-series" and self.series_url != "":
            if self.sort_method == control.lang(30701):  # recent
                self.sort = "recent"
            elif self.sort_method == control.lang(30702):  # viewed
                self.sort = "viewed"
            elif self.sort_method == control.lang(30703):  # rating
                self.sort = "rating"
            elif self.sort_method == control.lang(30706):  # sequential
                self.sort = ""
            else:
                self.show_list_sort()
                return
            self.list()
        print "fail: action=%s&series-url=%s" % (self.action, self.series_url)
        return

    def show_sort(self):
        # recent
        utils.add_directory(control.lang(30701), utils.icon_folder, None, "%s?action=browse-series&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30701))))
        # A to Z
        utils.add_directory(control.lang(30704), utils.icon_folder, None, "%s?action=browse-series&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30704))))
        control.directory_end()
        return

    def show_list_sort(self):
        # sequential
        utils.add_directory(control.lang(30706), utils.icon_folder, None,
                            "%s?action=list-series&page=%i&sort=%s&series-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30706)),
                                urllib.quote_plus(self.series_url)))
        # recent
        utils.add_directory(control.lang(30701), utils.icon_folder, None,
                            "%s?action=list-series&page=%i&sort=%s&series-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30701)),
                                urllib.quote_plus(self.series_url)))
        # viewed
        utils.add_directory(control.lang(30702), utils.icon_folder, None,
                            "%s?action=list-series&page=%i&sort=%s&series-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30702)),
                                urllib.quote_plus(self.series_url)))
        # rating
        utils.add_directory(control.lang(30703), utils.icon_folder, None,
                            "%s?action=list-series&page=%i&sort=%s&series-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30703)),
                                urllib.quote_plus(self.series_url)))
        control.directory_end()
        return

    def browse(self):
        url = self.browse_url % (utils.url_root, urllib.quote_plus(self.sort), self.current_page, utils.selected_languages())
        html_data = http_request.get(url)
        soup_strainer = SoupStrainer("main")
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        articles = beautiful_soup.findAll("article")
        for article in articles:
            action_url = ("%s?action=list-series&series-url=" % (sys.argv[0])) + "%s"
            utils.add_show_directory(article, action_url)

        next_url = "%s?action=browse-series&page=%i&sort=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()
        return

    def list(self):
        url = "%s%s?sort=%s&page=%i&%s" % (
            utils.url_root, self.series_url, self.sort, self.current_page, utils.selected_languages())
        html_data = http_request.get(url)
        print url
        soup_strainer = SoupStrainer("main")
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        articles = beautiful_soup.findAll("article")
        for article in articles:
            utils.add_entry_video(article)

        next_url = "%s?action=list-series&page=%i&sort=%s&series-url=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method), urllib.quote_plus(self.series_url))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()
        return
