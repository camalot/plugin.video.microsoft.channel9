# recent: sort=recent
# mostviewed: sort=viewed
# toprated: sort: rating

import sys
import urllib

from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request
import control
import utils


class Main:
    def __init__(self):
        # Parse parameters...
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.current_page = int(params.get("page", "1"))
        self.sort_method = urllib.unquote_plus(params.get("sort", "NONE"))
        self.url = "https://channel9.msdn.com/Browse/AllContent?sort=%s&page=%i&%s"

        utils.set_no_sort()

        if self.sort_method == control.lang(30701):  # recent
            self.sort = "recent"
            self.get_entries()
        elif self.sort_method == control.lang(30702):  # viewed
            self.sort = "viewed"
            self.get_entries()
        elif self.sort_method == control.lang(30703):  # rating
            self.sort = "rating"
            self.get_entries()
        else:
            self.browse()
        return

    def browse(self):
        # recent
        utils.add_directory(control.lang(30701), utils.icon_folder, None, "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30701))))
        # viewed
        utils.add_directory(control.lang(30702), utils.icon_folder, None, "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30702))))
        # rating
        utils.add_directory(control.lang(30703), utils.icon_folder, None, "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], 1, urllib.quote_plus(control.lang(30703))))

        control.directory_end()
        return

    def get_entries(self):
        url = self.url % (urllib.quote_plus(self.sort), self.current_page, utils.selected_languages())
        html_data = http_request.get(url)

        soup_strainer = SoupStrainer("main")
        beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)
        articles = beautiful_soup.findAll("article")
        if articles is None:
            control.directory_end()
            return

        for article in articles:
            utils.add_entry_video(article)

        next_url = "%s?action=list-all&page=%i&sort=%s" % (
            sys.argv[0], self.current_page + 1, urllib.quote_plus(self.sort_method))
        utils.add_next_page(beautiful_soup, next_url, self.current_page + 1)
        control.directory_end()
        return
