import sys
import os
import cv2
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import numpy as np
from numpy import *
from Gaussian_Noise_Filter import Gaussian
from Salt_Noise_Filter import Salt
from Peppers_Noise_Filter import Peppers
from Uniform_Noise_Filter import Uniform
from Rayleigh_Noise_Filter import Rayleigh
from Gamma_Noise_Filter import Gamma

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IMAGE RESTORATION")
        #self.geometry("550x550")
        self.configure(background='black')

        self.button1 = Button(self,text ="Restart", font = (" ", 20), highlightbackground='blue', command = self.restart_program)
        self.button1.pack(side = BOTTOM)
        #Load image button
        self.load_image_button = Button(self,text = "\n\n\tCLICK TO LOAD IMAGE\t\n\n",fg = "black", highlightbackground='gray',
                                        font=("Helvetica",40), command =self.load_image)
        self.load_image_button.pack(side = BOTTOM, fill = X)


    def load_image(self):
        try:
            #delete load_image_button
            #add add_noise_button
            self.load_image_button.destroy()
            self.add_noise_button = Button(self,text = "CLICK TO ADD NOISE",fg = "black", font=("", 30), command =self.add_noise)
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

        self.uniform_noise_button = Button(self, text="ADD UNIFORM NOISE", highlightbackground='gray',fg="Black", font=("", 20),command = self.Uniform_Noise)
        self.uniform_noise_button.pack(side = BOTTOM, fill = X)

        self.rayleigh_noise_button = Button(self, text="ADD RAYLEIGH NOISE", highlightbackground='gray',fg="Purple", font=("", 20),command = self.Rayleigh_Noise)
        self.rayleigh_noise_button.pack(side = BOTTOM, fill = X)

        self.gamma_noise_button = Button(self, text="ADD GAMMA NOISE", highlightbackground='gray',fg="deep pink", font=("", 20),command = self.Gamma_Noise)
        self.gamma_noise_button.pack(side = BOTTOM, fill = X)

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

    def Uniform_Noise(self):
        self.noise_window = tk.Toplevel()
        self.noise_window.title("Uniform Noise Image")

        np.random.seed(1)
        rows = self.img.width()
        cols = self.img.height()

        input_image = self.pilImage

        noise_uniform = np.random.randint(-10, 10, (rows, cols))
        noise_uniform.astype("float")
        input_image_added_noise = input_image + noise_uniform
        input_image_added_noise = np.uint8(np.where(input_image_added_noise < 0, 0, np.where(input_image_added_noise > 255, 255, input_image_added_noise)))

        output_dir = 'Noise/'
        Uniform_noise_image = output_dir + 'Uniform_Noise' + ".png"
        cv2.imwrite(Uniform_noise_image, input_image_added_noise)

        uniform_image_path = "Noise/Uniform_Noise.png"
        uniform_PIL_image = Image.open(uniform_image_path)
        image_add_uniform_noise = ImageTk.PhotoImage(uniform_PIL_image)

        original_image_label = Label(self.noise_window, image=self.img)
        original_image_label.pack(side=LEFT)

        uniform_noise_image_label = Label(self.noise_window, image=image_add_uniform_noise)
        uniform_noise_image_label.image = image_add_uniform_noise  # to keep reference
        uniform_noise_image_label.pack(side=LEFT)



        Go_Back_Button = Button(self.noise_window, text="UNDO", fg="red", font=("", 20), highlightbackground='gray',command=self.noise_window.destroy)
        Go_Back_Button.pack(side=BOTTOM, fill=BOTH)
        Filter_Button = Button(self.noise_window, text="Select Filter", fg="blue", font=("", 20), command=self.uniform)
        Filter_Button.pack(side=TOP, fill=BOTH)

    def Rayleigh_Noise(self):
        self.noise_window = tk.Toplevel()
        self.noise_window.title("Rayleigh Noise Image")

        np.random.seed(1)
        rows = self.img.width()
        cols = self.img.height()
        input_image = self.pilImage

        a = -19  # mean=a+sqrt(pi*b/4)=0, variance=b*(4-pi)/4=pow(20,2), a=-38, b=1864
        b = 466  # mean=0, variance=10, a=-19, b=466
        noise_rayleigh = a + np.power((-b * np.log(1 - np.random.rand(rows, cols))), 0.5)

        input_image_added_noise = input_image + noise_rayleigh
        input_image_added_noise = np.uint8(np.where(input_image_added_noise < 0, 0, np.where(input_image_added_noise > 255, 255, input_image_added_noise)))


        output_dir = 'Noise/'
        Rayleigh_noise_image = output_dir + 'Rayleigh_Noise' + ".png"
        cv2.imwrite(Rayleigh_noise_image, input_image_added_noise)

        uniform_image_path = "Noise/Rayleigh_Noise.png"
        uniform_PIL_image = Image.open(uniform_image_path)
        image_add_rayleigh_noise = ImageTk.PhotoImage(uniform_PIL_image)

        original_image_label = Label(self.noise_window, image=self.img)
        original_image_label.pack(side=LEFT)

        Rayleigh_noise_image_label = Label(self.noise_window, image=image_add_rayleigh_noise)
        Rayleigh_noise_image_label.image = image_add_rayleigh_noise  # to keep reference
        Rayleigh_noise_image_label.pack(side=LEFT)

        Go_Back_Button = Button(self.noise_window, text="UNDO", fg="red", font=("", 20), highlightbackground='gray',command=self.noise_window.destroy)
        Go_Back_Button.pack(side=BOTTOM, fill=BOTH)

        Filter_Button = Button(self.noise_window, text="Select Filter", fg="blue", font=("", 20), command=self.rayleigh)
        Filter_Button.pack(side=TOP, fill=BOTH)

    def Gamma_Noise(self):
        self.noise_window = tk.Toplevel()
        self.noise_window.title("Gamma Noise Image")

        np.random.seed(1)
        rows = self.img.width()
        cols = self.img.height()
        input_image = self.pilImage

        a = 0.1  # mean=b/a=50, variance=sqrt(b/pow(a,2))=22.3
        b = 5

        noise_gamma = np.zeros((rows, cols))
        for j in range(b):
            noise_gamma = noise_gamma + (-1 / a) * np.log(1 - np.random.rand(rows, cols))

        input_image_added_noise = input_image + noise_gamma
        input_image_added_noise = np.uint8(np.where(input_image_added_noise < 0, 0, np.where(input_image_added_noise > 255, 255, input_image_added_noise)))


        output_dir = 'Noise/'
        Gamma_noise_image = output_dir + 'Gamma_Noise' + ".png"
        cv2.imwrite(Gamma_noise_image, input_image_added_noise)

        gamma_image_path = "Noise/Gamma_Noise.png"
        uniform_PIL_image = Image.open(gamma_image_path)
        image_add_gamma_noise = ImageTk.PhotoImage(uniform_PIL_image)

        original_image_label = Label(self.noise_window, image=self.img)
        original_image_label.pack(side=LEFT)

        Gamma_noise_image_label = Label(self.noise_window, image=image_add_gamma_noise)
        Gamma_noise_image_label.image = image_add_gamma_noise  # to keep reference
        Gamma_noise_image_label.pack(side=LEFT)

        Go_Back_Button = Button(self.noise_window, text="UNDO", fg="red", font=("", 20), highlightbackground='gray',
                                command=self.noise_window.destroy)
        Go_Back_Button.pack(side=BOTTOM, fill=BOTH)

        Filter_Button = Button(self.noise_window, text="Select Filter", fg="blue", font=("", 20), command=self.gamma)
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

    def uniform(self):
        self.noise_window.destroy()
        self.destroy()
        Uniform()

    def rayleigh(self):
        self.noise_window.destroy()
        self.destroy()
        Rayleigh()

    def gamma(self):
        self.noise_window.destroy()
        self.destroy()
        Gamma()


    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    application = Application()
    application.mainloop()