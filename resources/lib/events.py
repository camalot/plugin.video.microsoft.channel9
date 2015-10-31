# recent: sort=recent
# a-z: sort: atoz

import sys
import urllib
import re
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from HTTPCommunicator import HTTPCommunicator
import control
import utils
import json


class Main:
    def __init__(self):
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.current_page = int(params.get("page", "1"))
        self.action = params.get("action", None)
        self.sort_method = urllib.unquote_plus(params.get("sort", "NONE"))
        self.event_url = urllib.unquote_plus(params.get("event-url", ""))
        self.browse_url = "%s/Browse/Events?sort=%s&page=%i&%s"

        utils.set_no_sort()

        if self.action is None or self.action == "browse-events":
            if self.sort_method == control.lang(30701):  # recent
                self.sort = "recent"
            elif self.sort_method == control.lang(30704):  # atoz
                self.sort = "atoz"
            else:
                self.show_sort()
                return
            self.browse()
            return
        elif self.action == "browse-live":
            self.sort = "current"
            self.live()
            return
        elif self.action == "list-event":
            if self.sort_method == control.lang(30701):  # recent
                self.sort = ""
            elif self.sort_method == control.lang(30702):  # viewed
                self.sort = "viewed"
            elif self.sort_method == control.lang(30703):  # rating
                self.sort = "rating"
                self.sort_dir = "asc"
            else:
                self.show_list_sort()
                return
            self.list()
            return
        print "fail: action=%s&event-url=%s" % (self.action, self.event_url)
        return

    def show_sort(self):
        # recent
        utils.add_directory(control.lang(30701), utils.icon_folder, None, "%s?action=browse-events&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30701))))
        # A to Z
        utils.add_directory(control.lang(30704), utils.icon_folder, None, "%s?action=browse-events&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30704))))
        control.directory_end()
        return

    def show_list_sort(self):
        # recent
        utils.add_directory(control.lang(30701), utils.icon_folder, None,
                            "%s?action=list-event&page=%i&sort=%s&event-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30701)),
                                urllib.quote_plus(self.event_url)))
        # rating
        utils.add_directory(control.lang(30703), utils.icon_folder, None,
                            "%s?action=list-event&page=%i&sort=%s&event-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30703)),
                                urllib.quote_plus(self.event_url)))
        # Most Viewed
        utils.add_directory(control.lang(30702), utils.icon_folder, None,
                            "%s?action=list-event&page=%i&sort=%s&event-url=%s" % (
                                sys.argv[0], 1, urllib.quote_plus(control.lang(30702)),
                                urllib.quote_plus(self.event_url)))
        control.directory_end()
        return

    def browse(self):
        http_communicator = HTTPCommunicator()
        url = self.browse_url % (utils.url_root, urllib.quote_plus(self.sort), self.current_page, utils.selected_languages())
        html_data = http_communicator.get(url)
        print url
        #
        # Parse response...
        #
        soup_strainer = SoupStrainer("div", {"class": "tab-content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        ul_entries = beautiful_soup.find("ul", {"class": "entries"})
        li_entries = ul_entries.findAll("li")
        for li_entry in li_entries:
            action_url = ("%s?action=list-event&sort=%s&event-url=" % (
                sys.argv[0], urllib.quote_plus(self.sort_method))) + "%s"
            utils.add_show_directory(li_entry, action_url)

        next_url = "%s?action=browse-shows&page=%i&sort=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()
        return

    def live(self):
        http_communicator = HTTPCommunicator()
        url = self.browse_url % (utils.url_root, urllib.quote_plus(self.sort), self.current_page, utils.selected_languages())
        html_data = http_communicator.get(url)
        print url
        soup_strainer = SoupStrainer("div", {"class": "tab-content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        ul_entries = beautiful_soup.find("ul", {"class": "entries"})

        if ul_entries is None:
            # nothing is live
            control.directory_end()
            return

        li_entries = ul_entries.findAll("li")
        for li_entry in li_entries:
            action_url = ("%s?action=list-event&event-url=" % (sys.argv[0])) + "%s"
            utils.add_show_directory(li_entry, action_url)

        next_url = "%s?action=browse-shows&page=%i&sort=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()

        return

    def list(self):
        http_communicator = HTTPCommunicator()
        url = "%s%s?sort=%s&page=%i&%s" % (
            utils.url_root, self.event_url, self.sort, self.current_page, utils.selected_languages())
        print url
        html_data = http_communicator.get(url)

        soup_strainer = SoupStrainer("div", {"class": "tab-content"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        ul_entries = beautiful_soup.find("ul", {"class": "entries sessions sessionList"})
        if ul_entries is None:
            control.directory_end()
            return

        li_entries = ul_entries.findAll("li")
        for li_entry in li_entries:
            utils.add_entry_video(li_entry)

        next_url = "%s?action=list-event&page=%i&sort=%s&event-url=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method), urllib.quote_plus(self.event_url))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)

        control.directory_end()
        return
