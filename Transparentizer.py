#! C:\Python\Python37\python.exe
#! coding: utf-8
#! python3
# Guillaume Viravau 2018-2019
# GUI to convert one color to transparent
# Thx https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent?noredirect=1&lq=1

from PIL import Image, ImageDraw
import tkinter as Tk
import tkinter.filedialog
import tkinter.colorchooser


ALPHA_COLOR = "#FF00FF"


def changeAlphaColor() :
	global ALPHA_COLOR
	
	color = tkinter.colorchooser.askcolor()
	ALPHA_COLOR = color[1]
	b_color.configure( background=ALPHA_COLOR )
	


def inputFileChoose( var="" ) :
	filename = tkinter.filedialog.askopenfilename()
	if len(filename) > 0:
		if isinstance( var, Tk.StringVar ) :
			var.set(filename)
	


def getBLPixelColor( filename="" ) :
	global ALPHA_COLOR
	
	img = Image.open( filename )
	img = img.convert("RGB")
	pix = img.load()
	
	c = pix[0,img.size[1]-1]
	
	ALPHA_COLOR = "#{R:0>2x}{G:0>2x}{B:0>2x}".format(R=c[0], G=c[1], B=c[2])
	b_color.configure( background=ALPHA_COLOR )
	

def transparentize() :
	global ALPHA_COLOR
	
	mode = alphaMode.get()
	imageName = inputFile.get()
	alphaName = alphaFile.get()
	
	
	# Input image
	img = Image.open(imageName)
	img = img.convert("RGBA")
	datas = img.getdata()
	
	
	print( imageName )
	
	# Color key
	if mode == 1 :
		print( "Color key as alpha" )
		
		# Default : pink
		replacement = [ [255,0,255], (255, 0, 255, 0) ]
		
		# Load the asked color
		replacement[0][0] = int( ALPHA_COLOR[1:3], 16 )
		replacement[0][1] = int( ALPHA_COLOR[3:5], 16 )
		replacement[0][2] = int( ALPHA_COLOR[5:7], 16 )
		
		replacement[1] = ( replacement[0][0], replacement[0][1], replacement[0][2], 0 )
		
		# Color keying
		newdata = []
		for item in datas :
			if item[0] == replacement[0][0] and item[1] == replacement[0][1] and item[2] == replacement[0][2] :
				if invertAlpha.get() :
					newdata.append( item )
				else :
					newdata.append( replacement[1] )
			else :
				if invertAlpha.get() :
					newdata.append( replacement[1] )
				else :
					newdata.append( item )
			
		img.putdata(newdata)
		
	
	# Image as alpha source
	elif mode == 2 :
		print( "Alpha from image" )
		
		# Input image
		alpha = Image.open(alphaName)
		alpha = alpha.convert("RGBA")
		apix = alpha.load()
		pix = img.load()
		
		# Alpha from file
		newdata = []
		for y in range( img.size[1] ) :
			for x in range( img.size[0] ) :
				R, G, B, A = pix[x,y]
				
				if (x < alpha.size[0]) and (y < alpha.size[1]) :
					r, g, b, a = apix[x,y]
					A = int( (a/255.) * ((r*0.3) + (g*0.5) + (b*0.2)) )
				else :
					A = 128
				
				if invertAlpha.get() :
					A = 255-A
				
				pix[x,y] = (R,G,B,A)
			
		
	
	# Itself as alpha source
	elif mode == 3 :
		print( "Alpha from itself" )
		
		# Input image
		pix = img.load()
		
		# Alpha from file
		newdata = []
		for y in range( img.size[1] ) :
			for x in range( img.size[0] ) :
				R, G, B, A = pix[x,y]
				A = int( (R*0.3) + (G*0.5) + (B*0.2) )
				
				if invertAlpha.get() :
					A = 255-A
				
				pix[x,y] = (R,G,B,A)
			
		
	
	# Save
	if mode in [1, 2, 3] :
		# TODO : Utiliser une vrai fonction pour avoir le nom du fichier, pas un hack dégueux
		if eraseOriginal.get() :
			saveName = imageName[:-4]
		else :
			saveName = imageName[:-4]+"_Alpha"
		
		if toGif.get() == False :
			img.save(saveName+".png", 'PNG')
		else :
			# TODO : Finir la conversion propre en parcourant la palette pour trouver la couleur clef
			# TODO : Remâcher l'image générée pour remplacer (avec moiré?) la couche alpha par une couleur pure pour la conversion
			print( img.getpalette() )
			img.save(saveName+".gif", 'GIF', transparency=0)
	


#===============================================================================
# GUI

window = Tk.Tk()
print( "Main" )
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
b_inputBrowse = Tk.Button(lf_files, text="...", command=lambda: inputFileChoose(inputFile) )
b_inputBrowse.grid(row=1, column=3)



# Options frame
lf_options = Tk.LabelFrame(p_main, text="Get alpha channel from", padx=2, pady=2)
p_main.add(lf_options)

# Radiobutton group : way to get alpha
alphaMode = Tk.IntVar()
alphaMode.set( 1 )

rb_fromColor = Tk.Radiobutton( lf_options, text="color", variable=alphaMode, value=1 )
rb_fromColor.grid(row=1, column=1)
b_fromBottomLeft = Tk.Button( lf_options, text="Get bottom left pixel color", command=lambda: getBLPixelColor(inputFile.get()) )
b_fromBottomLeft.grid(row=1, column=2)
b_color = Tk.Button( lf_options, relief="sunken", bg=ALPHA_COLOR, command=changeAlphaColor )
b_color.grid(row=1, column=3)


rb_fromfile = Tk.Radiobutton( lf_options, text="file", variable=alphaMode, value=2 )
rb_fromfile.grid(row=2, column=1)
alphaFile = Tk.StringVar()
alphaFile.set("C:\\")
i_alphaFile = Tk.Entry(lf_options, textvariable=alphaFile)
i_alphaFile.grid(row=2, column=2)
b_alphaBrowse = Tk.Button(lf_options, text="...", command=lambda: inputFileChoose(alphaFile))
b_alphaBrowse.grid(row=2, column=3)

rb_fromfile = Tk.Radiobutton( lf_options, text="itself", variable=alphaMode, value=3 )
rb_fromfile.grid(row=3, column=1)
Tk.Label(lf_options, text="(Uses the image greyscale as alpha)").grid(row=3, column=2)


# Checkbox : to gif (soon to be obsolette)
toGif = Tk.IntVar()
ck_toGif = Tk.Checkbutton(window, text="To GIF instead", variable=toGif)
ck_toGif.pack()

# Checkbox : modify the original
eraseOriginal = Tk.IntVar()
ck_eraseOriginal = Tk.Checkbutton(window, text="Modify the original", variable=eraseOriginal)
ck_eraseOriginal.pack()

# Checkbox : invert alpha
invertAlpha = Tk.IntVar()
ck_invertAlpha = Tk.Checkbutton(window, text="Invert alpha", variable=invertAlpha)
ck_invertAlpha.pack()

Tk.Button(window, text="Transparentize", command=transparentize).pack()

window.mainloop()
