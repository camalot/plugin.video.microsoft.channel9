import sys
import os
import urllib
import re
import xbmc
import xbmcgui
import xbmcaddon
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
import http_request
import control
import utils


class Main:
    def __init__(self):
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
        self.video_page_url = urllib.unquote_plus(params["video_page_url"])
        self.video_formats = ("High Quality MP4",
                              "High Quality WMV",
                              "Mid Quality MP4",
                              "Medium Quality MP4"
                              "Medium Quality WMV",
                              "Mid Quality WMV",
                              "Low Quality MP4",
                              "Low Quality WMV",
                              "MP4"
                              "MP3")
        self.play_video()

    def play_video(self):
        # Get current list item details...
        title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")
        studio = unicode(xbmc.getInfoLabel("ListItem.Studio"), "utf-8")
        plot = unicode(xbmc.getInfoLabel("ListItem.Plot"), "utf-8")
        genre = unicode(xbmc.getInfoLabel("ListItem.Genre"), "utf-8")

        # Show wait dialog while parsing data...
        dialog_wait = xbmcgui.DialogProgress()
        dialog_wait.create(control.lang(30504), title)

        # Get video URL and subtitles ...
        video_url, subtitle_urls = self.get_video_url_and_subtitles(self.video_page_url)

        if video_url is None:
            # Close wait dialog...
            dialog_wait.close()
            del dialog_wait

            # Message...
            xbmcgui.Dialog().ok(control.lang(30000), control.lang(30505))
            return

        # Play video...
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()

        list_item = xbmcgui.ListItem(
            title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        list_item.setInfo(
            "video", {"Title": title, "Studio": studio, "Plot": plot, "Genre": genre})
	    list_item.setSubtitles(subtitle_urls)

        playlist.add(video_url, list_item)

        # Close wait dialog...
        dialog_wait.close()
        del dialog_wait

        # Play video...
        xbmc_player = xbmc.Player()
        xbmc_player.play(playlist)
        return

    # Get video URL & subtitles
    def get_video_url_and_subtitles(self, video_page_url):
        # Get HTML page...
        if not re.match('^https?:', self.video_page_url):
            video_page_url = "%s%s" % (utils.url_root, video_page_url)

        html_data = http_request.get(video_page_url)
        # Parse HTML response...
        soup_strainer = SoupStrainer("div", {"class": "download"})
        beautiful_soup = BeautifulSoup(html_data, soup_strainer)

        video_url = None
	    subtitle_urls = []
	    divs = beautiful_soup.findAll("div")
	    li_video_entries = divs[1].findAll("li")

	    if len(divs) > 1:
	        profile = xbmcaddon.Addon().getAddonInfo('profile')
	        tempdir = xbmc.translatePath(os.path.join(profile, "temp/subtiles"))
	        if not os.path.isdir(tempdir):
		        os.makedirs(tempdir)
	        else:
		        for file in os.listdir(tempdir):
    			    filename = os.path.join(tempdir, file)
    			    if os.path.isfile(filename):
			            os.unlink(filename)

	        for li_entry in divs[2].findAll("li"):
	    	    li_entry_a = li_entry.find("a")
	    	    if li_entry_a is not None:
			        subtitle_url = li_entry_a["href"]
			        subtitle_name = li_entry_a["download"].split("_").pop()
			        data = http_request.get(subtitle_url)
			        subtitle_url = os.path.join(tempdir, subtitle_name)
	        	    f = open(subtitle_url, 'w')
                    f.write(data)
                    f.close()
			        subtitle_urls.append(subtitle_url)

        for quality in self.video_formats:
            for li_entry in li_video_entries:
                li_entry_a = li_entry.find("a")
                if li_entry_a is not None:
                    if li_entry_a.string.strip() == quality:
                        video_url = li_entry_a["href"]
                        return video_url, subtitle_urls

        return video_url, subtitle_urls
