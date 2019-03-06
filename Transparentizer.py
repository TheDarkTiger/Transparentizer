#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GUI to convert one color to transparent
# Thx https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent?noredirect=1&lq=1

from PIL import Image, ImageDraw
import Tkinter as Tk
import tkFileDialog
import tkColorChooser

ALPHA_COLOR = "#FF00FF"

def changeAlphaColor():
	global ALPHA_COLOR
	
	color = tkColorChooser.askcolor()
	ALPHA_COLOR = color[1]
	b_color.configure( background=ALPHA_COLOR )
	print ALPHA_COLOR
	

def inputFileChoose ():
	filename = tkFileDialog.askopenfilename()
	if len(filename) > 0:
		print(filename)
		inputFile.set(filename)

def transparentize() :
	global ALPHA_COLOR
	
	# Default : pink
	replacement = [ [255,0,255], (255, 0, 255, 0) ]
	
	# Load the asked color
	replacement[0][0] = int( ALPHA_COLOR[1:3], 16 )
	replacement[0][1] = int( ALPHA_COLOR[3:5], 16 )
	replacement[0][2] = int( ALPHA_COLOR[5:7], 16 )
	
	replacement[1] = ( replacement[0][0], replacement[0][1], replacement[0][2], 0 )
	
	print replacement
	
	
	imageName = inputFile.get()
	print inputFile.get()
	
	
	# Input image
	img = Image.open(imageName)
	img = img.convert("RGBA")
	
	
	# Color switch
	datas = img.getdata()
	
	newdata = []
	for item in datas :
		if item[0] == replacement[0][0] and item[1] == replacement[0][1] and item[2] == replacement[0][2] :
			newdata.append( replacement[1] )
		else :
			newdata.append( item )
		
	
	# Save
	img.putdata(newdata)
	if toGif.get() == False :
		img.save(imageName+"_Alpha.png", 'PNG')
	else :
		print img.getpalette()
		img.save(imageName+"_Alpha.gif", 'GIF', transparency=0)
	

#===============================================================================
# GUI

window = Tk.Tk()
print "Main"
p_main = Tk.PanedWindow(window, orient="vertical")
p_main.pack(side="top", expand="yes", fill="both", padx=2, pady=2)


# Container for the file
lf_files = Tk.LabelFrame(p_main, text="Files", padx=2, pady=2)
p_main.add(lf_files)

inputFile = Tk.StringVar()
inputFile.set("C:\\")
Tk.Label(lf_files, text="Input file").grid(row=1, column=1)
i_inputFile = Tk.Entry(lf_files, textvariable=inputFile)
i_inputFile.grid(row=1, column=2)
b_inputBrowse = Tk.Button(lf_files, text="...", command=inputFileChoose)
b_inputBrowse.grid(row=1, column=3)



# Options frame
lf_options = Tk.LabelFrame(p_main, text="Get alpha channel from", padx=2, pady=2)
p_main.add(lf_options)

# Radiobutton group : way to get alpha
alphaMode = Tk.IntVar()
alphaMode.set( 1 )

rb_fromColor = Tk.Radiobutton( lf_options, text="color", variable=alphaMode, value=1 )
rb_fromColor.grid(row=1, column=1)
b_fromBottomLeft = Tk.Button( lf_options, text="Get bottom left pixel color" )
b_fromBottomLeft.grid(row=1, column=2)
b_color = Tk.Button( lf_options, relief="sunken", bg=ALPHA_COLOR, command=changeAlphaColor )
b_color.grid(row=1, column=3)


rb_fromfile = Tk.Radiobutton( lf_options, text="file", variable=alphaMode, value=2 )
rb_fromfile.grid(row=2, column=1)
alphaFile = Tk.StringVar()
alphaFile.set("C:\\")
i_alphaFile = Tk.Entry(lf_options, textvariable=alphaFile)
i_alphaFile.grid(row=2, column=2)
b_alphaBrowse = Tk.Button(lf_options, text="...", command=inputFileChoose)
b_alphaBrowse.grid(row=2, column=3)


# Checkbox : to gif (soon to be obsolette)
toGif = Tk.IntVar()
ck_toGif = Tk.Checkbutton(window, text="To GIF instead", variable=toGif)
ck_toGif.pack()


Tk.Button(window, text="Transparentize", command=transparentize).pack()

window.mainloop()
