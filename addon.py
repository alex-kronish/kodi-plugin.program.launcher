import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import sys
import urllib.parse
import subprocess
import json


def additems():  # builds the menu
    p = addon.getAddonInfo('path')
    f = open(p + 'resources/data/launchers.json', 'rt+')
    items = json.load(f)
    for i in items:
        name = i['name']
        command = i['command']
        arg = i['arg']
        icon = i['icon']
        li = xbmcgui.ListItem(name)
        params = {  # these are the arguments i want to pass back to this same script for each menu item
            "syscmd": command,
            "mode": "run",
            "arg": arg
        }
        final_url = build_url(params)
        li.setProperty('IsPlayable', 'true')
        li.setArt({"icon": p + icon})
        xbmcplugin.addDirectoryItem(addon_handle, url=final_url, listitem=li, isFolder=True)
        # if you define isFolder=False, even though this is not really a folder, you can't interact with the menu item.
        # This is very stupid.
    # print('done building list')
    f.close()


def build_url(query): # builds the plugin:// url for each menu entry
    string = base_url + '?' + urllib.parse.urlencode(query)
    # print(string)
    return string


def launchproc(executable):  # subprocess is used to generate new windows
    subprocess.call(executable, stdout=None, shell=True)

# entry point for the plugin - this will run no matter what

addon = xbmcaddon.Addon()
addon_id = addon.getAddonInfo('id')
# print(str(sys.argv))
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urllib.parse.parse_qs(sys.argv[2][1:])
mode = args.get('mode')
# print('Mode = ' + str(mode))
if mode is None:  # if there's no parameter named "mode" we should just build the menu
    additems()
    xbmcplugin.endOfDirectory(addon_handle)
if mode is not None and mode[0] == 'run':  # if there is a parameter named mode and its equal to run, execute the program
    # print("mode was found")
    prog = args.get('syscmd')
    arguments = args.get('arg')
    # print(prog)
    exe = [prog, arguments]
    launchproc(prog)
