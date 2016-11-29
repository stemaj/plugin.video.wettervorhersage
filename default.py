#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import re
import sys
import os
import xbmcplugin
import xbmcaddon
import xbmcgui
from n24Core import N24Core

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addonId = 'plugin.video.wettervorhersage'
addon = xbmcaddon.Addon(id=addonId)
addonDir = xbmc.translatePath(addon.getAddonInfo('path'))
fanart = os.path.join(addonDir ,'fanart.jpg')
icon = os.path.join(addonDir ,'icon.png')

def index():


    #addLink("n24", "", 'playWeather', "")
    addLink("wetter.info", "", 'playWeather', "")

    nC = N24Core()
    data = nC.getWeatherComUrls()
    if (len(nC.error) > 0):
        notification(nC.error)
        return
    vid = ()
    for dat in data:
        vid = nC.getWeatherComVid(dat)
        addLink("wetter.com - " + vid[0], vid[1], 'playWeatherCom', "")
    #addLink("n24", "", 'playWeather', "")
    xbmcplugin.endOfDirectory(pluginhandle)

def playWeatherCom(url):

    listitem = xbmcgui.ListItem(path=url, thumbnailImage=icon, iconImage=fanart)
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def playWeather():
    nC = N24Core()
    data = nC.getWeatherData()
    if (len(nC.error) > 0):
        notification(nC.error)
        return
    listitem = xbmcgui.ListItem(path=data, thumbnailImage=icon, iconImage=fanart)
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def addLink(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)+"&name="+urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setProperty("fanart_image", fanart)
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok

def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))

if mode == 'playWeather':
    playWeather()
elif mode == 'playWeatherCom':
    playWeatherCom(url)
else:
    index()
