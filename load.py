# -*- coding: utf-8 -*-
import key
from sys import platform
import myNotebook as nb
from config import applongname, appversion
import io

import collections
import ctypes
import errno
import glob
import json
import os
import re
import requests
import sys

import sys


if sys.version_info >= (3, 10, 2):
    from Libs.PIL310 import Image
elif sys.version_info >= (3, 9, 5):
    from Libs.PIL39 import Image
else:
    from Libs.PIL3 import Image


import tkinter as tk
import tkinter.ttk
from config import config
from ctypes.wintypes import *
from ttkHyperlinkLabel import HyperlinkLabel
from datetime import datetime

TARGET_PANEL = 2
COMMS_PANEL = 3
ROLE_PANEL = 4
SYSTEMS_PANEL = 1
SYSTEM_MAP = 7
GALMAP = 6


VK_F10 = 0x79
VK_LEFTALT = 0xA4
VK_F11 = 0x7A
WM_KEYDOWN = 0x0100

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)

CloseHandle = ctypes.windll.kernel32.CloseHandle

GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowText.argtypes = [HWND, LPWSTR, ctypes.c_int]
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow

GetProcessHandleFromHwnd = ctypes.windll.oleacc.GetProcessHandleFromHwnd
FindWindow = ctypes.windll.user32.FindWindowW

this = sys.modules[__name__]
this.s = None
this.prep = {}

this.version = "5.1.0"
this.version_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSy9ij93j2qbwD-1_bXlI5IfO4EUD4ozNX2GJ2Do5tZNl-udWIqBHxYbtmcMRwvF6favzay3zY2LpH5/pub?gid=0&single=true&output=tsv"

this.delete_queue = collections.deque()


def checkVersion():
    versions = requests.get(this.version_url)

    getnews = True
    for line in versions.content.decode("ascii").split("\r\n"):
        rec = line.split("\t")
        if rec[0] == 'EDMC-Screenshot':
            this.status_url = rec[2]
            if rec[1] != this.version:
                this.status_text = "Upgrade to version " + rec[1]
            else:
                this.status_text = "Ready"


def debug(d):
    if this.vdebug.get() == "1":
        print(('[Screenshot] ' + str(d)))


def plugin_start3(plugin_dir):
    return plugin_start(plugin_dir)


def plugin_start(plugin_dir):
    """
    Load Screenshot plugin into EDMC
    """
    this.bmp_loc = tk.StringVar(value=config.get_str("BMP"))
    this.png_loc = tk.StringVar(value=config.get_str("PNG"))
    this.delete_org = tk.StringVar(value=config.get_str("DelOrg"))
    this.mkdir = tk.StringVar(value=config.get_str("Mkdir"))
    this.hideui = tk.StringVar(value=config.get_str("HideUI"))
    this.timer = tk.StringVar(value=config.get_str("Timer"))
    this.scanshot = tk.StringVar(value=config.get_str("Scanshot"))
    this.vdebug = tk.StringVar(value=config.get_str("Debug"))
    this.gamemode = "None"
    if config.get_str("Mask"):
        this.mask = tk.StringVar(value=config.get_str("Mask"))
    else:
        this.mask = tk.StringVar(value="SYSTEM(BODY)_NNNNN.png")

    debug("plugin_start" + this.mask.get())
    checkVersion()

    debug("plugin_start")
    return "Screenshot"


# Settings dialog dismissed
def prefs_changed(cmdr, is_beta):
    debug("prefs_changed")
    config.set("BMP", this.bmp_loc.get())
    config.set("PNG", this.png_loc.get())
    config.set("DelOrg", this.delete_org.get())
    config.set("Mkdir", this.mkdir.get())
    config.set("HideUI", this.hideui.get())
    config.set("Timer", this.timer.get())
    config.set("Scanshot", this.scanshot.get())
    config.set("Debug", this.vdebug.get())
    config.set("Mask", this.maskVar.get())
    debug("PREF: " + this.mask.get())
    debug("PREF: " + this.mask.get())
    debug_settings()
    display()


def debug_settings():
    debug("debug_settings")
    if this.vdebug.get() == "1":
        print(("Source Directory " + this.bmp_loc.get()))
        print(("Target Directory " + this.png_loc.get()))
        print(("Delete Originals " + this.delete_org.get()))
        print(("Make System Directory " + this.mkdir.get()))
        print(("HideUI " + this.hideui.get()))
        print(("Timer " + this.timer.get()))
        print(("Scanshot " + this.scanshot.get()))
        print(("Debug " + this.vdebug.get()))


def plugin_prefs(parent, cmdr, is_beta):
    debug("plugin_prefs")
    frame = nb.Frame(parent)
    frame.columnconfigure(3, weight=1)

    bmp_label = nb.Label(frame, text="Screenshot Directory")
    bmp_label.grid(padx=10, row=0, column=0, sticky=tk.W)

    bmp_entry = nb.Entry(frame, textvariable=this.bmp_loc)
    bmp_entry.grid(padx=10, row=0, column=1, columnspan=2, sticky=tk.W)

    png_label = nb.Label(frame, text="Conversion Directory")
    png_label.grid(padx=10, row=1, column=0, sticky=tk.W)

    png_entry = nb.Entry(frame, textvariable=this.png_loc)
    png_entry.grid(padx=10, row=1, column=1, columnspan=2, sticky=tk.W)

    nb.Checkbutton(frame, text="Delete Original File", variable=this.delete_org).grid(padx=10, row=2, column=0,
                                                                                      sticky=tk.W)
    nb.Checkbutton(frame, text="Group files by system directory", variable=this.mkdir).grid(padx=10, row=3, column=0,
                                                                                            sticky=tk.W)
    nb.Checkbutton(frame, text="Hide The User Interface", variable=this.hideui).grid(padx=10, row=4, column=0,
                                                                                     sticky=tk.W)
    nb.Checkbutton(frame, text="Take high resolution shots on the timer", variable=this.timer).grid(padx=10, row=5,
                                                                                                    column=0,
                                                                                                    sticky=tk.W)
    nb.Checkbutton(frame, text="Take screenshot when scanning a Thargoid", variable=this.scanshot).grid(padx=10, row=5,
                                                                                                        column=0,
                                                                                                        sticky=tk.W)

    Masks = [
        "SYSTEM(BODY)_NNNNN.png",
        "SYSTEM(BODY)_DATE.png",
        "SYSTEM(CMDR)_NNNNN.png",
        "SYSTEM(CMDR)_DATE.png",
        "BODY(CMDR)_NNNNN.png",
        "BODY(CMDR)_DATE.png",
        "SYSTEM_(BODY)_CMDR_NNNNN.png",
        "SYSTEM_(BODY)_CMDR_DATE.png",
        "SYSTEM BODY (CMDR) NNNNN.png",
        "SYSTEM BODY (CMDR) DATE.png",
        "DATE_SYSTEM_BODY.png",
        "DATE_SYSTEM_CMDR.png",
        "DATE_SYSTEM_BODY_CMDR.png"
    ]

    this.maskVar = tk.StringVar(frame)
    if this.mask.get():
        this.maskVar.set(this.mask.get())  # default value
    else:
        this.maskVar.set(Masks[0])

    popLabel = nb.Label(frame, text="File Mask")
    popupTypes = tk.OptionMenu(frame, this.maskVar, *Masks)
    maskVar.trace('w', change_mask)
    popupTypes.grid(row=6, column=1, columnspan=2, sticky=tk.W)
    popLabel.grid(padx=10, row=6, column=0, sticky=tk.W)
    nb.Checkbutton(frame, text="Enable Debugging", variable=this.vdebug).grid(
        padx=10, row=7, column=0, sticky=tk.EW)

    return frame


def change_mask(*args):
    this.mask.set(this.maskVar.get())


def plugin_app(parent):
    debug("plugin_app")
    this.parent = parent
    this.pcont = tk.Frame(parent)
    this.container = tk.Frame(pcont)
    this.container.columnconfigure(3, weight=1)
    this.label = tk.Label(this.container, text="Screenshot:")
    this.status = HyperlinkLabel(
        this.container, anchor=tk.W, text=this.status_text)
    this.status["url"] = this.status_url
    this.timex = tk.Button(this.container, command=lambda: this.timex.config(text="False", image=this.io_LEDRedOff) if
                           this.timex.config('text')[-1] == 'True' else this.timex.config(text="True", image=this.io_LEDRedOn), anchor=tk.W)
    this.io_LEDRedOn = tk.PhotoImage(
        file=os.path.realpath(os.path.dirname(os.path.realpath(__file__))) + "\\icons\\timer_enabled.gif")
    this.io_LEDRedOff = tk.PhotoImage(
        file=os.path.realpath(os.path.dirname(os.path.realpath(__file__))) + "\\icons\\timer_disabled.gif")
    this.timex.config(text="False", image=io_LEDRedOff)
    this.timex.grid(padx=10, row=0, column=2, sticky=tk.E)
    this.thargoid = False
    this.thargscan = False

    this.images = tk.Frame(this.container)
    this.images.grid(row=1, column=0, columnspan=3, sticky=tk.W)
    this.images.columnconfigure(2, weight=1)

    this.screenshot = tk.Label(this.images, anchor=tk.W)
    this.screenshot.grid(padx=10, row=0, column=0, columnspan=1, sticky=tk.W)
    this.screenshot.grid_remove()
    this.screenshot.bind("<Button-1>", save_screenshot)
    this.cropped = tk.Label(this.images, anchor=tk.W)
    this.cropped.grid(padx=10, row=0, column=1, columnspan=1, sticky=tk.W)
    this.cropped.bind("<Button-1>", save_crop)
    this.cropped.grid_remove()
    this.label.grid(row=0, column=0, sticky=tk.W)
    this.status.grid(padx=10, row=0, column=1, sticky=tk.W)
    debug_settings()
    display()
    this.processing = False
    this.parent.after(1000, sendKeyPress)

    return (this.pcont)


def display():
    debug("display: " + this.hideui.get())
    if this.hideui.get() == "1":
        debug("Hide Display")
        this.container.grid_remove()
        # this.status.grid_remove()
    else:
        # this.label.grid()
        this.container.grid()


def getInputDir():
    debug(this.bmp_loc.get())
    return this.bmp_loc.get()


def getOutputDir(system):
    debug("eh" + this.png_loc.get())

    if this.mkdir.get() == "1" and system:
        make_sure_path_exists(this.png_loc.get() + '/' + system)
        return this.png_loc.get() + '/' + system
    else:
        return this.png_loc.get()


def isHighRes(source):
    if source[0:7] == "HighRes":
        return True
    else:
        return False


def getFileMask(source, system, body, cmdr):
    # This will be updated to allow different file mask formats
    # selected from teh front end

    sequencemask = "[0123456789][0123456789][0123456789][0123456789][0123456789]"

    mask = this.mask.get()
    if system and body:
        bodyid = body.replace(system, '').strip()
        mask = mask.replace('SYSTEM', system)
        mask = mask.replace('BODY', bodyid)
    elif system and not body:
        mask = mask.replace('SYSTEM', system)
        mask = mask.replace('BODY', 'Unknown')
    else:
        mask = mask.replace('SYSTEM', 'Unknown')
        mask = mask.replace('BODY', 'Unknown')
    mask = mask.replace('CMDR', cmdr)
    mask = mask.replace('NNNNN', sequencemask)
    mask = mask.replace(
        'DATE', datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S'))

    # mask=system+'('+body+')_'+sequencemask+'.png'

    # We want to distinguish high res could make this optional
    if isHighRes(source):
        mask = 'HighRes_' + mask

    return mask


def getFilename(source, system, body, cmdr):
    dir = getOutputDir(system)
    debug("Output Directory: " + dir)
    mask = getFileMask(source, system, body, cmdr)
    debug("Output Mask: " + mask)

    keepcharacters = (' ','.','_','+','-','(',')',',','#','\'','[',']')
    mask = "".join(c for c in mask if c.isalnum() or c in keepcharacters).rstrip()

    files = glob.glob(dir + '/' + mask)

    # This is not very elegant. Is there a better way?
    # counting won't work if there ar gaps in the sequence because of deletions
    n = []
    for elem in files:
        try:
            n.append(int(elem[-9:-4]))
        except:
            debug(elem)

    if not n:
        n = [0]

    sequencemask = "[0123456789][0123456789][0123456789][0123456789][0123456789]"
    sequence = format(int(max(n)) + 1, "05d")

    fname = dir + '/' + mask.replace(sequencemask, sequence)
    debug("getFileMask: " + fname)

    return fname


def getBmpPath(source):
    # remove the ED Screenshot part of the name
    bmpfile = source[13:]
    return this.bmp_loc.get() + "\\" + bmpfile


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def thumbnail(img, size, xy):
    temp = img.copy()

    if xy == "x":
        newwidth = size
        newheight = newwidth * (float(temp.size[0]) / float(temp.size[1]))
    else:
        newheight = size
        newwidth = size * (float(temp.size[0]) / float(temp.size[1]))

    resize = newwidth, newheight

    temp.thumbnail(resize, Image.ANTIALIAS)

    cbuf = io.BytesIO()
    temp.save(cbuf, format='GIF')
    return cbuf.getvalue()


def getGuiFocus():
    status = "{}\status.json".format(config.default_journal_dir)
    debug(status)
    try:
      with open(status) as json_file:
        data = json.load(json_file)
        debug(data["GuiFocus"])
        return data["GuiFocus"]
    except Exception as e:
        debug("Unable to get GuiFocus. {}".format(e))
        return


def save_screenshot(event):
    if this.crop_status:
        this.im.save(this.converted, "PNG")
        this.status['text'] = "Full Screen Saved"


def save_crop(event):
    if this.crop_status:
        this.crop.save(this.converted, "PNG")
        this.status['text'] = "Crop Saved"


# Detect journal events
def journal_entry(cmdr, is_beta, system, station, entry, state):
    # when the outomation is on we need to raise the key
    if this.timer.get() == "1" and this.gamemode == "Solo":
        key.ReleaseKey(VK_LEFTALT)
    key.ReleaseKey(VK_F10)

    display()

    # If we have just scanned a Thargoid force a screenshot and set the Thargoid flag
    if entry.get("event") == "MaterialCollected" and entry.get("Name") in ("tg_shipflightdata", "unknownshipsignature"):
        if this.scanshot.get() == "1":
            key.PressKey(VK_F10)

        this.thargscan = True

    if entry['event'] == 'LoadGame':
        this.gamemode = entry["GameMode"]

    if entry['event'] == 'ShutDown' or entry['event'] == 'Died':
        this.timex.config(text="False", image=this.io_LEDRedOff)
        this.status['text'] = 'Timer Stopped'
        debug("stopping Timer")

    # { "timestamp":"2019-04-28T07:18:00Z", "event":"Music", "MusicTrack":"Unknown_Encounter" }
    if entry.get("event") == "Music":
        if entry.get("MusicTrack") in ("Unknown_Encounter", "Combat_Unknown"):
            this.thargoid = True
        else:
            this.thargoid = False

    if entry['event'] == 'Screenshot':

        if "Body" in entry:
            body = entry['Body']
        else:
            body = station

        this.processing = True
        # we can set status to error because it wont be shown unless we fail
        this.status['text'] = 'error'
        focus = getGuiFocus()

        original = getBmpPath(entry['Filename'])
        converted = getFilename(entry['Filename'][13:], system, body, cmdr)
        this.converted = converted

        # open the image and save it as PNG
        this.im = Image.open(original)
        this.im.save(converted, "PNG")

        # create a thumbnail
        this._IMG_THUMB = tk.PhotoImage(data=thumbnail(this.im, 75, "y"))
        this.screenshot["image"] = this._IMG_THUMB
        this.screenshot.grid()

        crop = True
        if this.thargscan:
            this.thargscan = False
            width = int(entry.get("Width"))
            height = int(entry.get("Height"))
            # box – The crop rectangle, as a (left, upper, right, lower)-tuple.
            this.crop = this.im.crop((0, height / 2, width / 2, height))
        elif focus == TARGET_PANEL:
            debug("TARGET")
            this.crop = this.im.crop((850, 279, 1306, 538))
        elif focus == COMMS_PANEL:
            this.crop = this.im.crop((406, 123, 919, 832))
        elif focus == ROLE_PANEL:
            this.crop = this.im.crop((451, 270, 1460, 837))
        elif focus == SYSTEMS_PANEL:
            this.crop = this.im.crop((451, 270, 1460, 837))
        if this.thargoid:
            this.thargoid = False
            width = int(entry.get("Width"))
            height = int(entry.get("Height"))
            # box – The crop rectangle, as a (left, upper, right, lower)-tuple.
            this.crop = this.im.crop((0, height / 2, width / 2, height))
        else:
            crop = False

        if crop and not isHighRes(entry['Filename'][13:]):
            this.crop_status = True
            debug("Cropping")
            this._IMG_CROP = tk.PhotoImage(data=thumbnail(this.crop, 75, "y"))
            this.cropped["image"] = this._IMG_CROP
            this.cropped.grid()
        else:
            this.crop_status = False
            this.cropped.grid_remove()

        if this.delete_org.get() == "1":
            # append to the delete_queue
            # set a timer to delete it in 30 seconds
            # this will let other plugins work with this one
            grace_period = 1000 * 60
            debug("delete in {} seconds {}".format(
                grace_period / 1000, original))
            this.delete_queue.append(original)
            this.parent.after(grace_period, delete_first)

        this.processing = False
        if len(os.path.basename(converted)) > 30:
            this.status['text'] = os.path.basename(converted)[0:30] + "..."
        else:
            this.status['text'] = os.path.basename(converted)
        this.status["url"] = None


def delete_first():
    original = this.delete_queue.popleft()
    debug("deleting {}".format(original))
    os.remove(original)


def sendKeyPress():
    if game_running():
        running = True

    if this.processing:
        this.status['text'] = "Processing Screenshot"

    if EliteInForeground() and this.timex['text'] == "True" and this.processing == False:
        if this.timer.get() == "1":
            if this.gamemode == "Solo":
                key.PressKey(VK_LEFTALT)
            key.PressKey(VK_F10)
        else:
            key.PressKey(VK_F10)
    elif EliteInForeground() == False and this.timex['text'] == "True":
        this.status['text'] = "Automation Suspended"
    elif this.processing == True and this.timex['text'] == "True":
        this.status['text'] = "Processing"

    this.parent.after(1000, sendKeyPress)


def GetWindowName(h):
    b = ctypes.create_unicode_buffer(255)
    GetWindowText(h, b, 255)
    return b.value


def game_running():
    if platform == 'darwin':
        for app in NSWorkspace.sharedWorkspace().runningApplications():
            if app.bundleIdentifier() == 'uk.co.frontier.EliteDangerous':
                return True
    elif platform == 'win32':

        def WindowTitle(h):
            if h:
                l = GetWindowTextLength(h) + 1
                buf = ctypes.create_unicode_buffer(l)
                if GetWindowText(h, buf, l):
                    return buf.value
                return None

        def callback(hWnd, lParam):
            name = WindowTitle(hWnd)
            if name and name.startswith('Elite - Dangerous'):
                handle = GetProcessHandleFromHwnd(hWnd)
                if handle:  # If GetProcessHandleFromHwnd succeeds then the app is already running as this user
                    CloseHandle(handle)
                    this.game = hWnd
                    return False  # stop enumeration
            return True

        return not EnumWindows(EnumWindowsProc(callback), 0)

    return False


def EliteInForeground():
    active = GetForegroundWindow()
    name = GetWindowName(active)
    if name and name.startswith('Elite - Dangerous'):
        return True
    return False
