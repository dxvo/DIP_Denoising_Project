from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
import PIL
from PIL import Image, ImageTk

class load_image:
    def __init__(self,master):
        self.master = master
        self.c_size = (700,500)
        self.setup_gui(self.c_size)
        #self.img = None
        #self.canvas = None
        #self.wt = None

    def setup_gui(self,size):
        Label(self.master, text = "Image Restoration", pady = 5, bg = "white", font = ("",30)).pack()
        #can be scaled
        self.canvas = Canvas(self.master, height=size[1],width= size[0],bd=10,bg='black',relief = "ridge")
        #self.canvas2 = Canvas(self.master, height=size[1]/2, width=size[0]/2, bd=10, bg='black', relief="ridge")

        #self.canvas2.pack()
        self.canvas.pack()
        txt = ""
        self.wt = self.canvas.create_text(size[0]/2-270,size[1]/2,text =txt, font =("",30),fill = "white")
        f = Frame(self.master,bg = "white",padx = 10, pady = 10)
        Button(f,text = "Load Input Image", bd = 2,fg = "red", bg = "black", font = ("", 20),command = self.display_image).pack(side = LEFT)
        f.pack()

        self.status = Label(self.master, text = "Current Image: None", bg = "gray", font = (" ", 15),relief = "sunken",bd = 2, fg = "black", anchor = W)
        self.status.pack(side = BOTTOM,fill = X)

    def display_image(self):
        try:
            File = fd.askopenfilename() #return the path
            self.pilImage = Image.open(File).convert('LA') #display image from path and covert to LA
            #img.save('greyscale.png') //this is to save the image
            #resize = self.pilImage.resize((700,500),Image.ANTIALIAS)#scale it to window size
            self.img = ImageTk.PhotoImage(self.pilImage)
            self.canvas.delete(ALL)
            self.canvas.create_image(self.c_size[0]/2+10,self.c_size[1]/2+10,anchor = CENTER, image = self.img)
            self.status['text'] = "Current Image: " + File
        except:
            ms.showerror("Error", "File is noto supported")

class MenuBar:
    def __init__(self, parent):
        self.menubar = Menu(parent)

        self.Create()
    def Create(self):
        root.config(menu = self.menubar)

    def add_menu(self, menuname, commands):
        menu = Menu(self.menubar, tearoff = 0)

        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            if command[2]:
                menu.add_separator()

        self.menubar.add_cascade(label=menuname, menu=menu)

def onExit():
    import sys
    sys.exit()

def onOpen():
    print ('Open')

root  = Tk()
root.title("DIP-FIRST ROW")
menubar = MenuBar(root)
fileMenu = menubar.add_menu("File", commands = [("Open", onOpen, True), ("Exit", onExit, False)])


#root.resizable(0,0)
load_image(root)
root.mainloop()

