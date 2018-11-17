import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import cv2
import numpy as np
from numpy import *
from Gaussian_Noise_Filter import Gaussian
from Salt_Noise_Filter import Salt
from Peppers_Noise_Filter import Peppers
import sys
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IMAGE RESTORATION")
        #self.geometry("550x550")
        self.configure(background='black')

        #Load image button
        self.load_image_button = Button(self,text = "\n\n\tCLICK TO LOAD IMAGE\t\n\n",fg = "blue", highlightbackground='gray',
                                        font=("Helvetica",40), command =self.load_image)
        self.load_image_button.pack(side = BOTTOM, fill = X)

        self.button1 = Button(self,text ="restart", command = self.restart_program)
        self.button1.pack()

    def load_image(self):
        try:
            #delete load_image_button
            #add add_noise_button
            self.load_image_button.destroy()
            self.add_noise_button = Button(self,text = "CLICK TO ADD NOISE",fg = "blue", font=("", 30), command =self.add_noise)
            self.add_noise_button.pack(side = BOTTOM, fill = X)

            #Get image path and display
            File = fd.askopenfilename()  # return the path
            self.pilImage = Image.open(File).convert('L')  # display image from path and covert to L
            self.img = ImageTk.PhotoImage(self.pilImage)
            self.input_image_label = Label(self, image=self.img)
            self.input_image_label.pack(side = LEFT)
        except:
            ms.showerror("Loading Error")


    def add_noise(self):
        self.add_noise_button.destroy()

        self.Gaussian_noise_button = Button(self, text="ADD GAUSIAN NOISE", highlightbackground='gray',fg="blue", font=("", 20), command = self.Gaussian_Noise)
        self.Gaussian_noise_button.pack(side = BOTTOM, fill = X)

        self.Salt_noise_button = Button(self, text="ADD SALT NOISE", fg="green", highlightbackground='gray',font=("", 20),command = self.Salt_Noise)
        self.Salt_noise_button.pack(side = BOTTOM, fill = X)

        self.Peppers_noise_button = Button(self, text="ADD PEPPERS NOISE", highlightbackground='gray',fg="red", font=("", 20),command = self.Peppers_Noise)
        self.Peppers_noise_button.pack(side = BOTTOM, fill = X)


    def Gaussian_Noise(self):
        self.noise_window = tk.Toplevel()
        self.noise_window.title("Gaussian Noise Image")

        np.random.seed(1)
        rows = self.img.width()
        cols = self.img.height()

        input_image = self.pilImage
        noise_gaussian = np.random.normal(0, 20, (rows, cols))

        input_image_added_noise = input_image + noise_gaussian
        input_image_added_noise = np.where(input_image_added_noise > 255, 255, input_image_added_noise)
        input_image_added_noise = np.where(input_image_added_noise < 0, 0, input_image_added_noise)

        output_dir = 'Noise/'
        gaussian_noise_image = output_dir + 'Gaussian_Noise' + ".png"
        cv2.imwrite(gaussian_noise_image, input_image_added_noise)

        gaussian_image_path = "Noise/Gaussian_Noise.png"
        gaussian_PIL_image = Image.open(gaussian_image_path)
        image_add_gaussian_noise = ImageTk.PhotoImage(gaussian_PIL_image)

        original_image_label = Label(self.noise_window, image=self.img)
        original_image_label.pack(side = LEFT)

        gaussian_noise_image_label = Label(self.noise_window, image=image_add_gaussian_noise)
        gaussian_noise_image_label.image = image_add_gaussian_noise  # to keep reference
        gaussian_noise_image_label.pack(side=LEFT)

        Go_Back_Button = Button(self.noise_window, text="UNDO", fg="blue", font=("", 20),command=self.noise_window.destroy)
        Go_Back_Button.pack(side = BOTTOM, fill=BOTH)

        Filter_Button = Button(self.noise_window, text="Select Filter", fg="blue", font=("", 20),command = self.gaussian)
        Filter_Button.pack(side=TOP, fill=BOTH)


    def Salt_Noise(self):
        self.noise_window = tk.Toplevel()
        self.noise_window.title("Salt Noise Image")

        np.random.seed(1)
        rows = self.img.width()
        cols = self.img.height()

        input_image = self.pilImage
        prob = 0.1
        noise_salt = np.random.randint(0, 256, (rows, cols))
        noise_salt = np.where(noise_salt < prob * 256, 255, 0)
        #input_image.astype("float")
        noise_salt.astype("float")

        input_image_added_noise = input_image + noise_salt
        input_image_added_noise = np.where(input_image_added_noise > 255, 255, input_image_added_noise)

        output_dir = 'Noise/'
        salt_noise_image = output_dir + 'Salt_Noise' + ".png"
        cv2.imwrite(salt_noise_image, input_image_added_noise)

        salt_image_path = "Noise/Salt_Noise.png"
        salt_PIL_image = Image.open(salt_image_path)
        image_add_salt_noise = ImageTk.PhotoImage(salt_PIL_image)

        original_image_label = Label(self.noise_window, image=self.img)
        original_image_label.pack(side=LEFT)

        salt_noise_image_label = Label(self.noise_window, image=image_add_salt_noise)
        salt_noise_image_label.image = image_add_salt_noise  # to keep reference
        salt_noise_image_label.pack(side=LEFT)

        Go_Back_Button = Button(self.noise_window, text="UNDO", fg="green", font=("", 20), highlightbackground='gray',command=self.noise_window.destroy)
        Go_Back_Button.pack(side=BOTTOM, fill=BOTH)

        Filter_Button = Button(self.noise_window, text="Select Filter", fg="blue", font=("", 20), command=self.salt)
        Filter_Button.pack(side=TOP, fill=BOTH)

    def Peppers_Noise(self):

        self.noise_window = tk.Toplevel()
        self.noise_window.title("Peppers Noise Image")

        np.random.seed(1)
        rows = self.img.width()
        cols = self.img.height()

        input_image = self.pilImage
        prob = 0.1
        noise_pepper = np.random.randint(0, 256, (rows, cols))
        noise_pepper = np.where(noise_pepper < prob * 256, -255, 0)
        #input_image.astype("float")
        noise_pepper.astype("float")

        input_image_added_noise = input_image + noise_pepper
        input_image_added_noise = np.where(input_image_added_noise < 0, 0, input_image_added_noise)

        output_dir = 'Noise/'
        peppers_noise_image = output_dir + 'Peppers_Noise' + ".png"
        cv2.imwrite(peppers_noise_image, input_image_added_noise)

        peppers_image_path = "Noise/Peppers_Noise.png"
        peppers_PIL_image = Image.open(peppers_image_path)
        image_add_peppers_noise = ImageTk.PhotoImage(peppers_PIL_image)

        original_image_label = Label(self.noise_window, image=self.img)
        original_image_label.pack(side=LEFT)

        peppers_noise_image_label = Label(self.noise_window, image=image_add_peppers_noise)
        peppers_noise_image_label.image = image_add_peppers_noise  # to keep reference
        peppers_noise_image_label.pack(side=LEFT)

        Go_Back_Button = Button(self.noise_window, text="UNDO", fg="red", font=("", 20), highlightbackground='gray',command=self.noise_window.destroy)
        Go_Back_Button.pack(side=BOTTOM, fill=BOTH)

        Filter_Button = Button(self.noise_window, text="Select Filter", fg="blue", font=("", 20), command=self.peppers)
        Filter_Button.pack(side=TOP, fill=BOTH)


    def gaussian(self):
        self.noise_window.destroy()
        self.destroy()
        Gaussian()

    def salt(self):
        self.noise_window.destroy()
        self.destroy()
        Salt()

    def peppers(self):
        self.noise_window.destroy()
        self.destroy()
        Peppers()


    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    application = Application()
    application.mainloop()