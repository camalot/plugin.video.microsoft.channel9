import sys
import urllib
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import control
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request

# url_langs = "lang=id&lang=cs&lang=da&lang=de&lang=et&lang=en&lang=es&lang=fr&lang=hr&lang=it&lang=sw&lang=lv&"
# url_langs += "lang=hu&lang=nl&lang=nb&lang=uz&lang=pl&lang=pt&lang=pt-br&lang=ro&lang=sk&lang=sl&lang=sr-cyrl&"
# url_langs += "lang=fi&lang=sv&lang=vi&lang=tr&lang=el&lang=bg&lang=ru&lang=uk&lang=hy&lang=he&lang=ur&lang=ar&"
# url_langs += "lang=hi&lang=th&lang=ko&lang=ja&lang=zh-cn&lang=zh-tw"

url_root = "https://channel9.msdn.com/"

icon_folder = os.path.join(control.imagesPath, "folder.png")
icon_search = os.path.join(control.imagesPath, "search.png")
icon_next = os.path.join(control.imagesPath, "next-page.png")
icon_tag = os.path.join(control.imagesPath, "tag.png")
icon_cog = os.path.join(control.imagesPath, "cog.png")
icon_user = os.path.join(control.imagesPath, "user.png")
icon_blog = os.path.join(control.imagesPath, "blog.png")
icon_tag = os.path.join(control.imagesPath, "tag.png")
icon_tv = os.path.join(control.imagesPath, "tv.png")
icon_event = os.path.join(control.imagesPath, "event.png")
icon_all = os.path.join(control.imagesPath, "all.png")

action_list_blog = "%s?action=list-blog&page=%i&sort=%s&blog-url=%s"
action_list_blog2 = "%s?action=list-blog&blog-url=%s"


def selected_languages():
    langs = ""
    setting_lang_items = control.lang(30602).split(",")
    for lang_item in setting_lang_items:
        lang_enabled = control.setting(lang_item)
        if lang_enabled == "true":
            langs += "lang=%s&" % lang_item

    if langs == "" or langs is None:
        return "lang=en"

    return langs[:-1]


def add_entry_video(entry):
    # Thumbnail...
    div_entry_image = entry.find("div", {"class": "entry-image"})
    if div_entry_image is None:
        return
    thumbnail = div_entry_image.find("img", {"class": "thumb"})["src"]
    if not re.match("^https?:", thumbnail):
        thumbnail = "%s%s" % (url_root, thumbnail)
    # Title
    div_entry_meta = entry.find("div", {"class": "entry-meta"})
    a_title = div_entry_meta.find("a", {"class": "title"})
    title = a_title.string

    # Video page
    video_page_url = a_title["href"]

    # Genre (date)...
    div_data = div_entry_meta.find("div", {"class": "data"})

    if div_data is None:
        genre = "none"
    else:
        span_class_date = div_data.find("span", {"class": "date"})
        genre = span_class_date.string

    # Plot
    div_description = div_entry_meta.find("div", {"class": "description"})
    plot = div_description.string

    list_item = control.item(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    list_item.setInfo("video", {"Title": title, "Studio": "Microsoft Channel 9", "Plot": plot, "Genre": genre})
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    plugin_play_url = '%s?action=play&video_page_url=%s' % (sys.argv[0], urllib.quote_plus(video_page_url))
    control.addItem(handle=int(sys.argv[1]), url=plugin_play_url, listitem=list_item, isFolder=False)
    return


def add_next_page(bs, item_url, page):
    ul_paging = bs.find("ul", {"class": "paging"})
    if ul_paging is not None:
        list_item = control.item("[B][UPPERCASE][COLOR green]%s[/COLOR][/UPPERCASE][/B]" % control.lang(30503) % page,
                                 iconImage=icon_next, thumbnailImage=icon_next)
        control.addItem(handle=int(sys.argv[1]), url=item_url, listitem=list_item, isFolder=True)
    return


def add_directory(text, icon, thumbnail, url):
    list_item = xbmcgui.ListItem(text, iconImage=icon, thumbnailImage=thumbnail)
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    control.addItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True)


def add_show_directory(entry, action_url):
    # Thumbnail...
    div_entry_image = entry.find("div", {"class": "entry-image"})
    thumbnail = div_entry_image.find("img", {"class": "thumb"})["src"]
    if not re.match("^https?:", thumbnail):
        thumbnail = "%s%s" % (url_root, thumbnail)

    # Title
    div_entry_meta = entry.find("div", {"class": "entry-meta"})
    a_title = div_entry_meta.find("a", {"class": "title"})
    title = a_title.string

    # Show page URL
    show_url = a_title["href"]

    # Add to list...
    list_item = control.item(title, iconImage=icon_folder, thumbnailImage=thumbnail)
    list_item.setArt({"thumb": thumbnail, "fanart": thumbnail, "landscape": thumbnail, "poster": thumbnail})
    control.addItem(handle=int(sys.argv[1]), url=action_url % urllib.quote_plus(show_url), listitem=list_item,
                    isFolder=True)
    return


def set_no_sort():
    control.sort(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)


def get_banner(url):
    html_data = http_request.get(url)
    soup_strainer = SoupStrainer("head")
    beautiful_soup = BeautifulSoup(html_data, soup_strainer, convertEntities=BeautifulSoup.HTML_ENTITIES)

    banner = beautiful_soup.find("meta", {"name": "msapplication-square310x310logo"})
    if banner is not None:
        return banner["content"]
    else:
        return None
