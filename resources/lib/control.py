import sys,os,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs


lang = xbmcaddon.Addon().getLocalizedString

setting = xbmcaddon.Addon().getSetting

addon = xbmcaddon.Addon

addItem = xbmcplugin.addDirectoryItem

item = xbmcgui.ListItem

directory = xbmcplugin.endOfDirectory

sort = xbmcplugin.addSortMethod

content = xbmcplugin.setContent

property = xbmcplugin.setProperty

addonInfo = xbmcaddon.Addon().getAddonInfo

infoLabel = xbmc.getInfoLabel

condVisibility = xbmc.getCondVisibility

jsonrpc = xbmc.executeJSONRPC

window = xbmcgui.Window(10000)

dialog = xbmcgui.Dialog()

progressDialog = xbmcgui.DialogProgress()

windowDialog = xbmcgui.WindowDialog()

button = xbmcgui.ControlButton

image = xbmcgui.ControlImage

keyboard = xbmc.Keyboard

sleep = xbmc.sleep

execute = xbmc.executebuiltin

skin = xbmc.getSkinDir()

player = xbmc.Player()

playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

resolve = xbmcplugin.setResolvedUrl

openFile = xbmcvfs.File

makeFile = xbmcvfs.mkdir

deleteFile = xbmcvfs.delete

listDir = xbmcvfs.listdir

transPath = xbmc.translatePath

skinPath = xbmc.translatePath('special://skin/')

addonPath = xbmc.translatePath(addonInfo('path'))

dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')

imagesPath = xbmc.translatePath(os.path.join(addonPath, 'resources', 'images'))

libPath = xbmc.translatePath(os.path.join(addonPath, 'resources', 'lib'))

settingsFile = os.path.join(dataPath, 'settings.xml')

databaseFile = os.path.join(dataPath, 'settings.db')

favouritesFile = os.path.join(dataPath, 'favourites.db')

sourcescacheFile = os.path.join(dataPath, 'sources.db')

cachemetaFile = os.path.join(dataPath, 'metacache.db')

libcacheFile = os.path.join(dataPath, 'library.db')

metacacheFile = os.path.join(dataPath, 'meta.db')

cacheFile = os.path.join(dataPath, 'cache.db')

openSettings = addon().openSettings

def directory_end():
    set_view_thumbnail()
    directory(handle=int(sys.argv[1]), succeeded=True)

def set_view_thumbnail():
    if skin == 'skin.confluence':
        execute('Container.SetViewMode(500)')
    elif skin == 'skin.aeon.nox':
        execute('Container.SetViewMode(511)')
    else:
        execute('Container.SetViewMode(500)')


