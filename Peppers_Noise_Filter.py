import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import cv2
import numpy as np
from numpy import *

class Peppers(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FILTERING")

        gaussian_image_path = "Noise/Peppers_Noise.png"
        self.PIL_image = Image.open(gaussian_image_path)
        self.image_add_gaussian_noise = ImageTk.PhotoImage(self.PIL_image)

        gaussian_noise_image_label = Label(self, image=self.image_add_gaussian_noise)
        gaussian_noise_image_label.pack(side=LEFT)

        self.arithmetic_button = Button(self, text=" Arithmetic Mean Filter", fg="blue", font=("", 20),command = self.print)
        self.arithmetic_button.pack(side=TOP)

        self.geometric_button = Button(self, text=" Geometric Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.geometric_button.pack(side=TOP)

        self.harmonic_button = Button(self, text=" Harmonic Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.harmonic_button.pack(side=TOP)

        self.contra_harmonic_button = Button(self, text=" Contraharmonic Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.contra_harmonic_button.pack(side=TOP)

        # Order statistic
        self.median_button = Button(self, text="Median Filter", fg="blue", font=("", 20),command=self.print)
        self.median_button.pack(side=TOP)

        self.min_button = Button(self, text="Min Filter", fg="blue", font=("", 20), command=self.print)
        self.min_button.pack(side=TOP)

        self.max_button = Button(self, text="Max Filter", fg="blue", font=("", 20), command=self.print)
        self.max_button.pack(side=TOP, fill=BOTH)

        self.trimmed_button = Button(self, text="Alpha Trimmed Mean Filter", fg="blue", font=("", 20), command=self.print)
        self.trimmed_button.pack(side=TOP)

        self.adaptive_button = Button(self, text="Adaptive Filter", fg="blue", font=("", 20), command=self.print)
        self.adaptive_button.pack(side=TOP)


    def print(self):
        print("Hello")