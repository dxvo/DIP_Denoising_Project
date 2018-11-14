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

        #displaying current image
        label = Label(noise_window, image=self.img) #this is to display image
        label.pack()

        noise_frame = Frame(noise_window, bg="gray")
        noise_frame.pack(side=LEFT, fill=Y, padx=2, pady=2)

        Gaussian_noise_button = Button(noise_frame, text="Gaussian Noise", fg="blue", height=5)
        Gaussian_noise_button.pack(pady=3, padx=3, fill = X)

        salt_noise_button = Button(noise_frame, text="Salt Noise", fg="Green", height=5)
        salt_noise_button.pack(pady=3, padx=3, fill=X)

        peppers_noise_button = Button(noise_frame, text="Salt Noise", fg="Green", height=5)
        peppers_noise_button.pack(pady=3, padx=3, fill=X)


if __name__ == "__main__":
    application = Application()
    application.mainloop()