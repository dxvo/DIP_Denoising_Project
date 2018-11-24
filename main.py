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
from crop import Cropping
from Filtering import Filter

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.path = None
        self.noise_prob = None
        self.a = None
        self.b = None
        #self.noise_type = None
        self.variance = None
        self.upper = None

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
            self.load_image_button.destroy()
            self.add_noise_button = Button(self,text = "CLICK TO ADD NOISE",fg = "black", font=("", 30), command =self.add_noise)
            self.add_noise_button.pack(side = BOTTOM, fill = X)

            #Get image path and display
            File = fd.askopenfilename()  # return the path
            self.pilImage = Image.open(File).convert('L')  # display image from path and covert to L
            self.pilImage = self.pilImage.resize((512, 512), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.pilImage)
            self.input_image_label = Label(self, image=self.img)
            self.input_image_label.pack(side = LEFT)
        except:
            ms.showerror("Loading Error")

    def add_noise(self):
        self.add_noise_button.destroy()

        self.Gaussian_noise_button = Button(self, text="ADD GAUSIAN NOISE", highlightbackground='gray',fg="blue", font=("", 20),
                                            command=lambda: self.plus_noise("Gaussian_Noise"))
        self.Gaussian_noise_button.pack(side = BOTTOM, fill = X)

        self.Salt_noise_button = Button(self, text="ADD SALT NOISE", fg="green", highlightbackground='gray',font=("", 20),
                                        command=lambda: self.plus_noise("Salt_Noise"))
        self.Salt_noise_button.pack(side = BOTTOM, fill = X)

        self.Peppers_noise_button = Button(self, text="ADD PEPPERS NOISE", highlightbackground='gray',fg="red", font=("", 20),
                                           command=lambda: self.plus_noise("Peppers_Noise"))
        self.Peppers_noise_button.pack(side = BOTTOM, fill = X)

        self.uniform_noise_button = Button(self, text="ADD UNIFORM NOISE", highlightbackground='gray',fg="Black", font=("", 20),
                                           command=lambda: self.plus_noise("Uniform_Noise"))
        self.uniform_noise_button.pack(side = BOTTOM, fill = X)

        self.rayleigh_noise_button = Button(self, text="ADD RAYLEIGH NOISE", highlightbackground='gray',fg="Purple", font=("", 20),
                                            command=lambda: self.plus_noise("Rayleigh_Noise"))
        self.rayleigh_noise_button.pack(side = BOTTOM, fill = X)

        self.gamma_noise_button = Button(self, text="ADD GAMMA NOISE", highlightbackground='gray',fg="deep pink", font=("", 20),
                                         command=lambda: self.plus_noise("Gamma_Noise"))
        self.gamma_noise_button.pack(side = BOTTOM, fill = X)


    def plus_noise(self,noise_type):
        #self.noise_window = tk.Toplevel()
        np.random.seed(1)
        rows = self.img.width()
        cols = self.img.height()
        input_image = self.pilImage
        output_dir = 'Noise/'

        if(noise_type == "Gaussian_Noise"):
            #self.noise_type = "Gaussian_Noise"
            self.get_noise_parameters("Gaussian") #get variance input
            noise_gaussian = np.random.normal(0, self.variance, (rows, cols))
            input_image_added_noise = input_image + noise_gaussian
            input_image_added_noise = np.where(input_image_added_noise > 255, 255, input_image_added_noise)
            input_image_added_noise = np.where(input_image_added_noise < 0, 0, input_image_added_noise)
            self.path = output_dir + 'Gaussian_Noise' + ".png"
            self.noise_window = tk.Toplevel()
            self.noise_window.title("Gaussian Noise Image")

        elif(noise_type == "Salt_Noise"):
            self.get_noise_parameters("salt")
            #self.noise_type = "Salt_Noise"
            noise_salt = np.random.randint(0, 256, (rows, cols))
            noise_salt = np.where(noise_salt < self.noise_prob * 256, 255, 0)
            noise_salt.astype("float")
            input_image_added_noise = input_image + noise_salt
            input_image_added_noise = np.where(input_image_added_noise > 255, 255, input_image_added_noise)
            self.path = output_dir + 'Salt_Noise' + ".png"
            self.noise_window = tk.Toplevel()
            self.noise_window.title("Salt Noise Image")

        elif (noise_type == "Peppers_Noise"):
            self.get_noise_parameters("peppers")
            #self.noise_type = "Peppers_Noise"
            noise_pepper = np.random.randint(0, 256, (rows, cols))
            noise_pepper = np.where(noise_pepper < self.noise_prob * 256, -255, 0)
            noise_pepper.astype("float")
            input_image_added_noise = input_image + noise_pepper
            input_image_added_noise = np.where(input_image_added_noise < 0, 0, input_image_added_noise)
            self.path = output_dir + 'Peppers_Noise' + ".png"
            self.noise_window = tk.Toplevel()
            self.noise_window.title("Peppers Noise Image")

        elif (noise_type == "Uniform_Noise"):
            #self.noise_type = "Uniform_Noise"
            self.get_noise_parameters("Uniform")
            noise_uniform = np.random.randint(-(self.upper), self.upper, (rows, cols))
            noise_uniform.astype("float")
            input_image_added_noise = input_image + noise_uniform
            input_image_added_noise = np.uint8(np.where(input_image_added_noise < 0, 0, np.where(input_image_added_noise > 255, 255, input_image_added_noise)))
            self.path = output_dir + 'Uniform_Noise' + ".png"
            self.noise_window = tk.Toplevel()
            self.noise_window.title("Uniform Noise Image")

        elif (noise_type == "Gamma_Noise"):
            self.get_noise_parameters("gamma")
            #self.noise_type = "Gamma_Noise"
            a = self.a
            b = int(self.b)
            noise_gamma = np.zeros((rows, cols))
            for j in range(b):
                noise_gamma = noise_gamma + (-1 / a) * np.log(1 - np.random.rand(rows, cols))
            input_image_added_noise = input_image + noise_gamma
            input_image_added_noise = np.uint8(np.where(input_image_added_noise < 0, 0,np.where(input_image_added_noise > 255, 255,input_image_added_noise)))
            self.path = output_dir + 'Gamma_Noise' + ".png"
            self.noise_window = tk.Toplevel()
            self.noise_window.title("Gamma Noise Image")

        elif (noise_type == "Rayleigh_Noise"):
            self.get_noise_parameters("rayleigh")
            #self.noise_type = "Rayleigh_Noise"
            a = self.a
            b = self.b
            noise_rayleigh = a + np.power((-b * np.log(1 - np.random.rand(rows, cols))), 0.5)
            input_image_added_noise = input_image + noise_rayleigh
            input_image_added_noise = np.uint8(np.where(input_image_added_noise < 0, 0,np.where(input_image_added_noise > 255, 255,input_image_added_noise)))
            self.path = output_dir + 'Rayleigh_Noise' + ".png"
            self.noise_window = tk.Toplevel()
            self.noise_window.title("Rayleigh Noise Image")


        cv2.imwrite(self.path, input_image_added_noise)
        PIL_image = Image.open(self.path)
        image_add_noise = ImageTk.PhotoImage(PIL_image)

        original_image_label = Label(self.noise_window, image=self.img)
        original_image_label.pack(side=LEFT)

        noise_image_label = Label(self.noise_window, image=image_add_noise)
        noise_image_label.image = image_add_noise  # to keep reference
        noise_image_label.pack(side=LEFT)

        Go_Back_Button = Button(self.noise_window, text="UNDO", fg="blue", font=("", 22),command=self.noise_window.destroy)
        Go_Back_Button.pack(side=BOTTOM, fill=BOTH)

        # button to select noise option
        Image_Cropping_Button = Button(self.noise_window, text="Noise Analysis", fg="Red", font=("", 22),command=lambda: self.noise_analysis(self.path))
        Image_Cropping_Button.pack(side=TOP, fill=BOTH)

        Filter_Button = Button(self.noise_window, text="Filter Selection", fg="blue", font=("", 22), command= self.Filtering)
        Filter_Button.pack(side=TOP, fill=BOTH)


    def get_noise_parameters(self, noise_type):
        self.input_window = tk.Toplevel()
        self.input_window.title("User Noise Input")

        if(noise_type == "salt" or noise_type == "peppers" ):
            label = tk.Label(self.input_window, text=" Noise Parameters", font=(" ", 20))
            label.grid(row=0, column=1)
            probability_density = tk.Label(self.input_window, text="Probability:")
            probability_density.grid(row=1, column=0, sticky=W)
            self.my_prob_entry = tk.Entry(self.input_window)
            self.my_prob_entry.grid(row=1, column=1)

            my_button = tk.Button(self.input_window, text="Submit", command= lambda:self.noise_parameter(noise_type))
            my_button.grid(row=3, column=1)
            self.wait_window(self.input_window)

        elif(noise_type == "Gaussian"):
            label = tk.Label(self.input_window, text=" Gaussian Noise Parameters", font=(" ", 20))
            label.grid(row=0, column=1)
            variance = tk.Label(self.input_window, text="Noise Variance:")
            variance.grid(row=1, column=0, sticky=W)
            self.my_var_entry = tk.Entry(self.input_window)
            self.my_var_entry.grid(row=1, column=1)

            my_button = tk.Button(self.input_window, text="Submit", command= lambda:self.noise_parameter(noise_type))
            my_button.grid(row=3, column=1)
            self.wait_window(self.input_window)

        elif(noise_type == "rayleigh" or noise_type == "gamma" ):
            label = tk.Label(self.input_window, text=" Noise Parameters", font=(" ", 20))
            label.grid(row=0, column=1)
            a_label = tk.Label(self.input_window, text="Displacement a:")
            b_label = tk.Label(self.input_window, text="Displacement b:")
            a_label.grid(row=1, column=0, sticky=W)
            b_label.grid(row=2, column=0, sticky=W)
            self.my_a_entry = tk.Entry(self.input_window)
            self.my_a_entry.grid(row=1, column=1)
            self.my_b_entry = tk.Entry(self.input_window)
            self.my_b_entry.grid(row=2, column=1)
            my_button = tk.Button(self.input_window, text="Submit", command= lambda:self.noise_parameter(noise_type))
            my_button.grid(row=3, column=1)
            self.wait_window(self.input_window)

        elif (noise_type == "Uniform"):
            label = tk.Label(self.input_window, text="Uniform Noise Input", font=(" ", 20))
            label.grid(row=0, column=1)
            upper_range = tk.Label(self.input_window, text="Upper Range Value:")

            upper_range.grid(row=1, column=0, sticky=W)
            self.my_upper_entry = tk.Entry(self.input_window)
            self.my_upper_entry.grid(row=1, column=1)

            my_button = tk.Button(self.input_window, text="Submit", command=lambda: self.noise_parameter(noise_type))
            my_button.grid(row=3, column=1)
            self.wait_window(self.input_window)


    def noise_parameter(self,noise_type):
        if (noise_type == "salt" or noise_type == "peppers"):
            self.noise_prob = float(self.my_prob_entry.get())

        elif (noise_type == "rayleigh" or noise_type == "gamma"):
            self.a = float((self.my_a_entry.get()).replace(',',''))
            self.b = float((self.my_b_entry.get()).replace(',',''))

        elif (noise_type == "Gaussian"):
            self.variance = float(self.my_var_entry.get())

        elif (noise_type == "Uniform"):
            self.upper = float(self.my_upper_entry.get())

        self.update()
        self.input_window.destroy()


    def Filtering(self):
        self.noise_window.destroy()
        self.destroy()
        Filter(self.path)


    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


    #-----------------Noise Analysis----------------------
    def noise_analysis(self, path):
        self.noise_window.destroy()
        self.destroy()
        Cropping(self.path)


if __name__ == "__main__":
    application = Application()
    application.mainloop()

