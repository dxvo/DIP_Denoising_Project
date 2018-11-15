import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IMAGE RESTORATION")
        self.geometry("600x400")
        self.configure(background='black')

        # status bar
        self.status = Label(self, text="Current Image: None", bg="gray", font=(" ", 15), bd=2, fg="black", anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        #Load image button
        self.load_image_button = tk.Button(self,text = "Click to Load Image", fg = "red", font=("", 25),command =self.load_image)
        self.load_image_button.pack(side = tk.BOTTOM, fill = tk.X)

        Left_frame = Frame(self,bg = "gray")
        Left_frame.pack(side = LEFT, fill = Y, padx=2, pady=2)

        add_noise_button = Button(Left_frame, text="Add Noise", fg="red", height = 5,command = self.add_noise)
        button2 = Button(Left_frame, text="button 2", fg="red", height = 5)
        add_noise_button.pack(pady = 3,padx = 3, fill = X)
        button2.pack(pady = 3, padx = 3, fill = X)


    def load_image(self):
        try:
            File = fd.askopenfilename() #return the path
            self.pilImage = Image.open(File).convert('LA') #display image from path and covert to LA
            self.img = ImageTk.PhotoImage(self.pilImage)
            label = Label(self, image=self.img)
            label.pack()
            self.status['text'] = "Current Image: " + File
        except:
            ms.showerror("Loading Error")

    def add_noise(self):
        #creating window
        noise_window = tk.Toplevel()
        noise_window.title("ADD NOISE")
        #noise_window.geometry("700x500")


        #displaying current image
        #label = Label(noise_window, image=self.img) #this is to display image
        #label.pack()

        #self.canvas = Canvas(noise_window, height=700,width= 500,bd=10,bg='black',relief = "ridge")

        # create the canvas, size in pixels
        noise_window.canvas = Canvas(noise_window, bg='black')

        # pack the canvas into a frame/form
        noise_window.canvas.pack(expand=TRUE, fill=BOTH)
        #resize = self.pilImage.resize((700, 500), Image.ANTIALIAS)

        noise_window.canvas.create_image(0,0,anchor=NW, image=self.img) #position  NW


        # load the .gif image file
        #gif1 = PhotoImage(file='Lenna.png')
        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        #noise_window.canvas.create_image(50, 10, image=gif1, anchor=NW)

        noise_frame = Frame(noise_window, bg="gray")
        noise_frame.pack(side=BOTTOM, fill=Y, padx=2, pady=2)

        Gaussian_noise_button = Button(noise_frame, text="Gaussian Noise", fg="blue",height = 4)
        #Gaussian_noise_button.pack(pady=3, padx=3, fill = X)
        Gaussian_noise_button.grid(row = 0, column = 0, sticky = W)

        salt_noise_button = Button(noise_frame, text="Salt Noise", fg="Green",height = 4)
        #salt_noise_button.pack(pady=3, padx=3, fill=Y)
        salt_noise_button.grid(row = 0, column = 1, sticky = W)

        peppers_noise_button = Button(noise_frame, text="Peppers Noise", fg="Blue", height = 4)
        #peppers_noise_button.pack(pady=3, padx=3, fill=X)
        peppers_noise_button.grid(row = 0, column = 2)




if __name__ == "__main__":
    application = Application()
    application.mainloop()