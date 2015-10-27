#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xml.dom.minidom
import re
import urllib
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup
from ms_channel9_utils import HTTPCommunicator

#
# Constants
# 
__settings__ = xbmcaddon.Addon()
__language__ = __settings__.getLocalizedString


#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):
        #
        # Constants
        #
        self.DEBUG = False

        #
        # Parse parameters...
        #
        params = dict(part.split('=') for part in sys.argv[2][1:].split('&'))

        self.video_page_url = urllib.unquote_plus(params["video_page_url"])

        #
        # Settings
        #
        self.video_format = __settings__.getSetting("video_format")
        self.pref_video_format = ("High Quality",
                                  "Medium Quality",
                                  "Low Quality",
                                  "Best Available")[int(self.video_format)]
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
        #
        # Play video...
        #
        self.playVideo()

    #
    # Play video...
    #
    def playVideo(self):
        if (self.DEBUG):
            print "video_page_url = " + self.video_page_url

        #
        # Get current list item details...
        #
        title = unicode(xbmc.getInfoLabel("ListItem.Title"), "utf-8")
        thumbnail = xbmc.getInfoImage("ListItem.Thumb")
        studio = unicode(xbmc.getInfoLabel("ListItem.Studio"), "utf-8")
        plot = unicode(xbmc.getInfoLabel("ListItem.Plot"), "utf-8")
        genre = unicode(xbmc.getInfoLabel("ListItem.Genre"), "utf-8")

        #
        # Show wait dialog while parsing data...
        #
        dialogWait = xbmcgui.DialogProgress()
        dialogWait.create(__language__(30504), title)

        #
        # Get video URL...
        #
        video_url = self.getVideoUrl(self.video_page_url)

        if video_url == None:
            # Close wait dialog...
            dialogWait.close()
            del dialogWait

            # Message...
            xbmcgui.Dialog().ok(__language__(30000), __language__(30505))
            return

        #
        # Play video...
        #
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()

        listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        listitem.setInfo("video", {"Title": title, "Studio": studio, "Plot": plot, "Genre": genre})
        playlist.add(video_url, listitem)

        # Close wait dialog...
        dialogWait.close()
        del dialogWait

        # Play video...
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)

    #
    # Get video URL
    #
    def getVideoUrl(self, video_page_url):
        # 
        # Get HTML page...
        # 
        video_page_url = "http://channel9.msdn.com%s" % video_page_url
        httpCommunicator = HTTPCommunicator()
        htmlData = httpCommunicator.get(video_page_url)

        #                
        # Parse HTML response...
        #
        soupStrainer = SoupStrainer("ul", {"class": "download"})
        beautifulSoup = BeautifulSoup(htmlData, soupStrainer)

        #
        # Loop through video URLs and pick one...
        #
        video_url = None

        # Preferred format...
        li_entries = beautifulSoup.findAll("li")
        for li_entry in li_entries:
            li_entry_a = li_entry.find("a")
            if li_entry_a != None:
                for quality in self.video_formats:
                    if li_entry_a.string == quality:
                        video_url = li_entry_a["href"]
                        break

        # No preferred format found, pick any available...
        # if video_url == None :
        #    for li_entry in li_entries :
        #        li_entry_a = li_entry.find( "a" )
        #        if li_entry_a != None :
        #            format = li_entry_a.string
        #            if format == __settings__.getLocalizedString(30303) or \
        #               format == __settings__.getLocalizedString(30302) or \
        #               format == __settings__.getLocalizedString(30301) :
        #                video_url = li_entry_a[ "href" ]
        #                break

        #
        # Return value
        #
        return video_url

        #
        # The End
        #
