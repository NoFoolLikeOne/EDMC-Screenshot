# -*- coding: utf-8 -*-
import sys
import re
import ttk
import Tkinter as tk
import requests
import os
import errno
import glob
import StringIO

from PIL import Image


from config import applongname, appversion
import myNotebook as nb
from config import config



this = sys.modules[__name__]
this.s = None
this.prep = {}

this.debug=False

def debug(d):
	if this.debug==True:
		print '[Screenshot] '+str(d)


def plugin_start():
	"""
	Load Screenshot plugin into EDMC
	"""
	this.bmp_loc = tk.StringVar(value=config.get("BMP"))
	this.png_loc = tk.StringVar(value=config.get("PNG"))
	this.delete_org = tk.StringVar(value=config.get("DelOrg"))
	this.mkdir = tk.StringVar(value=config.get("Mkdir"))
	print("Screenshot loaded!")
	return "Screenshot"

	

def plugin_prefs(parent,cmdr,is_beta):  
	frame = nb.Frame(parent)
	frame.columnconfigure(1, weight=1)

	bmp_label = nb.Label(frame, text="Screenshot Directory")
	bmp_label.grid(padx=10, row=10, sticky=tk.W)

	bmp_entry = nb.Entry(frame, textvariable=this.bmp_loc)
	bmp_entry.grid(padx=10, row=10, column=1, sticky=tk.EW)

	png_label = nb.Label(frame, text="Conversion Directory")
	png_label.grid(padx=10, row=12, sticky=tk.W)

	png_entry = nb.Entry(frame, textvariable=this.png_loc)
	png_entry.grid(padx=10, row=12, column=1, sticky=tk.EW)

	nb.Checkbutton(frame, text="Delete Original File", variable=this.delete_org).grid()
	nb.Checkbutton(frame, text="Group files by system directory", variable=this.mkdir).grid()
	
	return frame

	
def plugin_app(parent):
	this.label = tk.Label(parent, text="Screenshot:")
	this.status = tk.Label(parent, anchor=tk.W, text="Ready")
	
	
	return (label, this.status)

# Log in

# Settings dialog dismissed
def prefs_changed():
	config.set("BMP", this.bmp_loc.get())
	config.set("PNG", this.png_loc.get())
	config.set("DelOrg", this.delete_org.get())
	config.set("Mkdir", this.mkdir.get())
	
	

	
#get the file sequence number from destination	
def get_sq(entry):
	system = entry['System']
	body = entry['Body']
	dir = tk.StringVar(value=config.get("PNG")).get()
	mkdir = tk.StringVar(value=config.get("Mkdir")).get()
	
	if mkdir:
		mask = dir+'/'+system+'/'+'/*'+system+'('+body+')_*.png'
	else:
		mask = dir+'/*'+system+'('+body+')_*.png'	
		
	debug("mask: "+mask)
	files = glob.glob(mask)
	
	n = []
	for elem in files:
		try:
			n.append(int(elem[-9:-4]))
		except:
			debug(elem)
		
	if not n:
		n = [0]
			
	
	sequence = int(max(n))+1
	return format(sequence, "05d")
	
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
	
	
# Detect journal events
def journal_entry(cmdr, system, station, entry):

    if entry['event'] == 'Screenshot':
		this.status['text'] = 'processing...'	
		## get the numeric component from the filename	
		seq = get_sq(entry)
			
		## get the filename
		#f = re.compile('[HighRes|Screen.hot].*_\d+.bmp')
		#bmpfile=f.search(entry['Filename']).group();
		
		#take /ED Pictures/ off the front of the name
		bmpfile=entry['Filename'][13:]
		
		debug("filename "+entry['Filename'])
		debug("filename "+bmpfile)
		debug(bmpfile[0:7])
		
		if bmpfile[0:7] == "HighRes":
			prefix="HighRes_"
		else:
			prefix=""
		
		## Construct the new filename		
		pngfile=prefix+entry['System']+"("+entry['Body']+")_"+seq+".png"
		
		mkdir = tk.StringVar(value=config.get("Mkdir")).get()
		print mkdir
		
		original = tk.StringVar(value=config.get("BMP")).get() + '\\'+ bmpfile
		
		newdir = tk.StringVar(value=config.get("PNG")).get() + '\\'+ system
		
		if mkdir == "1":
			print "With dir " + mkdir
			make_sure_path_exists(newdir)
			converted = newdir + '\\'+ pngfile
			print converted
		else:	
			print "Without dir " + mkdir
			converted = tk.StringVar(value=config.get("PNG")).get() + '\\'+ pngfile
			print converted
			
		im = Image.open(original)
		im.save(converted,"PNG");
		
		delete_original = tk.StringVar(value=config.get("DelOrg")).get()
				
				
		if delete_original:
			os.remove(original)
		
		this.status['text'] = pngfile
