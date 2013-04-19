#!/usr/bin/python

############################
# Application: pylatexpng.py
# Author: Ashley DaSilva
# Date: 2009, May 30
# Version: 0.1
'''Copyright 2009 Ashley DaSilva

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

from Tkinter import *
import os
import ImageTk
import tkMessageBox


class AppLatexConvert:
    '''Application to convert latex math-mode code to a .png file.

This python application will convert LaTeX (math-mode) code to a png image file.
It depends on the ImageTk package (not included in standard python distribution). Other python dependencies (os, Tkinter) are included in a standard python distribution, so the user need not worry about these.

The script takes input from the user via a text box. The input is already enclosed by math-mode tags, and includes {amsmath,amssymb,amsthm} in the preamble. To move to a new line, use '\\'.

The script will crop your text appropriately, but cannot handle more than 1 page. Its main limitation is the platform dependence: the 'latex' command (line 102) works in linux, but not windows. It also depends on the dvipng package (only available for linux) to convert the .dvi file to a .png file.
'''

    def __init__(self, parent=0):  #master?

        self.mainWindow = Frame(parent) #master?
        self.mainWindow.master.title('LaTeX to png')

        # Set up a menu bar with Tools.
        fMenu=Frame(self.mainWindow, relief='groove')

        bTools=Menubutton(fMenu,text='Tools',menu=Menu) #underline=0
        bTools.pack(side='left')

        bTools.mTools=Menu(bTools)
        bTools['menu']=bTools.mTools

        bAbout=Button(fMenu,text='About',command=self.about,relief='flat')
        bAbout.pack(side='left')

        self.dpiLess=IntVar()
        self.dpiLess.set(500) # Default
        bTools.mTools.add_checkbutton(label='Smaller Image', variable=self.dpiLess, onvalue=170, offvalue=500)

        bTools.mTools.add_command(label='Preamble',command=self.addToPreamble)

        fMenu.pack(fill=X)
        # End menu set up.


        # Box for adding to preamble (packed if selected from menu)
        fPreamble=Frame(self.mainWindow)

        lPreamble=Label(fPreamble, text='Preamble:')

        self.tPreamble=Text(fPreamble, bg='white', height='5')
        self.tPreamble.insert(1.0,r'''\usepackage{amssymb,amsmath,amsthm}''')

        fPreamble.pack()


        fTitle=Frame(self.mainWindow)

        lTitle=Label(fTitle, text='Enter LaTeX code:')
        lTitle.pack(side='left',pady=10,padx=10)

        fTitle.pack(fill=X)


        fEntry=Frame(self.mainWindow)

        self.tEntry=Text(fEntry, bg='white', height='5')
        self.tEntry.pack(padx=10)

        fEntry.pack()


        fButtons=Frame(self.mainWindow)

        self.lTexIt=Label(fButtons, text='Enter filename for output:')
        self.lTexIt.pack(side='left',padx=5,pady=10)

        self.eTexIt=Entry(fButtons, bg='white')
        self.eTexIt.insert(0,'temp.png')
        self.eTexIt.pack(side='left',pady=10)

        bTexIt=Button(fButtons, text='Tex It!',command=self.tex)
        bTexIt.pack(side='left', padx=10, pady=10)

        fQuit=Button(fButtons, text='Quit',command=self.mainWindow.quit )
        fQuit.pack(side='right', padx=10, pady=10)

        fButtons.pack(fill=X)


        fPreview=Frame(self.mainWindow)

        self.lPreview=Label(fPreview, width=600) #packed at TexIt button press

        fPreview.pack(fill=X)

        self.mainWindow.pack()


    def tex(self):
        code=self.tEntry.get(1.0,'end')
        output_name=self.eTexIt.get() # .png file name
        preamble=self.tPreamble.get(1.0,'end')

        # Prepare filename for .png output
        if output_name=='':
            output_name='temp.png'
        else:
            pass
        output_name=output_name.rstrip('png')
        output_name=output_name.rstrip('.')

        # Prepare filename for intermediate .tex file
        if os.path.exists('temp.tex')==False:
            filename='temp'
        elif os.path.exists(output_name+'.tex')==False:
            filename=output_name
        else:
            filename=raw_input('%s.tex and %s.tex exist. Enter filename for intermediate .tex file, without extension: ' %(output_name,'temp'))
            filename=str(filename)
            if os.path.exists(filename+'.tex')==True:
                os.remove(filename+'.tex')
            else:
                pass

        temp=open('%s.tex' %filename, 'w')
        temp.write(r'''\documentclass[12pt]{article}
\pagestyle{empty}
''')
        temp.write(preamble)
        temp.write(r'''
\begin{document}
$\displaystyle \\
''')
        temp.write(code)
        temp.write(r'''$
\end{document}''')
        temp.close()

        os.system('latex %s.tex' %filename)

        # Requires package dvipng: converts dvi to png.
        # -D 500 sets resolution to 500 dpi, 
        # -O -1in,-1in sets offset (cut margins),
        # -o %s.png is the output filename
        dpi=str(self.dpiLess.get())
        os.system('dvipng -D %s -o %s.png -O -1in,-1in %s.dvi' %(dpi,output_name,filename))
        os.remove('%s.tex' %filename) # clean-up
        os.remove('%s.aux' %filename)
        os.remove('%s.log' %filename)
        os.remove('%s.dvi' %filename)

        # Requires ImageTk package:
        img=ImageTk.PhotoImage(file=output_name+'.png')

        self.lPreview['image']=img
        self.lPreview.img=img
        self.lPreview.pack(side='left', padx=10,pady=10)
        print "File saved as '%s.png' in current directory." %(output_name)

    def addToPreamble(self):
        self.tPreamble.pack(padx=10,pady=10)

    def about(self):
        tkMessageBox.showinfo("About", "pylatexpng.py Copyright 2009 Ashley DaSilva\n\nThis program comes with ABSOLUTELY NO WARRENTY. \nThis is free software, and you are welcome to redistribute it under certain conditions. See the GNU General Public License for details (http://www.gnu.org/licenses/).") 
    
    def help(self):
        tkMessageBox.showinfo("Help", "If pylatexpng.py is not running at all, please make sure that dvipng is installed. Please also make sure that you have the TkInter and os python modules available.")




#root = Tk()

#app = AppLatexConvert(root)

#root.mainloop()

app=AppLatexConvert()
app.mainWindow.mainloop()
