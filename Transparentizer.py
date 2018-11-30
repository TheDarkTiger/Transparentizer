#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GUI to convert one color to transparent
# Thx https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent?noredirect=1&lq=1

from PIL import Image, ImageDraw
import Tkinter as Tk
import tkFileDialog


def inputFileChoose ():
	filename = tkFileDialog.askopenfilename()
	if len(filename) > 0:
		print(filename)
		inputFile.set(filename)

def transparentize() :
	
	replacement = ( (255,0,255), (255,0,255,0) )
	
	imageName = inputFile.get()
	print inputFile.get()
	
	#------------------------------------------------------------------------------
	# Input image
	
	img = Image.open(imageName)
	img = img.convert("RGBA")
	
	#------------------------------------------------------------------------------
	# Color switch
	
	datas = img.getdata()
	
	newdata = []
	for item in datas :
		if item[0] == replacement[0][0] and item[1] == replacement[0][1] and item[2] == replacement[0][2] :
			newdata.append( replacement[1] )
		else :
			newdata.append( item )
		
	
	img.putdata(newdata)
	if toGif.get() == False :
		img.save(imageName+"_Alpha.png", 'PNG')
	else :
		print img.getpalette()
		img.save(imageName+"_Alpha.gif", 'GIF', transparency=0)
	


window = Tk.Tk()
print "Main"
p_main = Tk.PanedWindow(window, orient="vertical")
p_main.pack(side="top", expand="yes", fill="both", padx=2, pady=2)

#===============================================================================
# Container for the file
print "File container"
lf_files = Tk.LabelFrame(p_main, text="Files", padx=2, pady=2)
p_main.add(lf_files)

inputFile = Tk.StringVar()
inputFile.set("C:\\")
Tk.Label(lf_files, text="Input file").grid(row=1, column=1)
i_inputFile = Tk.Entry(lf_files, textvariable=inputFile)
i_inputFile.grid(row=1, column=2)
b_inputBrowse = Tk.Button(lf_files, text="...", command=inputFileChoose)
b_inputBrowse.grid(row=1, column=3)

#===============================================================================
# Buttons
print "Buttons"
lf_options = Tk.LabelFrame(p_main, text="Options", padx=2, pady=2)
p_main.add(lf_options)

# Checkbox : no sound
toGif = Tk.IntVar()
ck_toGif = Tk.Checkbutton(lf_options, text="To GIF instead", variable=toGif)
ck_toGif.pack()


Tk.Button(lf_options, text="Transparentize", command=transparentize).pack()
Tk.Button(lf_options, text="Quit", command=window.quit).pack()

print "mainloop"
window.mainloop()
