import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import cv2
import numpy as np
from numpy import *
import restart

class Salt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SALT NOISE FILTERING")
        self.configure(background='black')

        image_path = "Noise/Salt_Noise.png"
        self.PIL_image = Image.open(image_path)
        self.image_noise = ImageTk.PhotoImage(self.PIL_image)

        noise_image_label = Label(self, image=self.image_noise)
        noise_image_label.pack(side=LEFT)

        # Order statistic
        self.median_button = Button(self, text="Median Filter", fg="blue", font=("", 20), command=self.print)
        self.median_button.pack(side=TOP, fill=BOTH)

        self.min_button = Button(self, text="Min Filter", fg="blue", font=("", 20), command=self.print)
        self.min_button.pack(side=TOP, fill=BOTH)

        self.max_button = Button(self, text="Max Filter", fg="blue", font=("", 20), command=self.print)
        self.max_button.pack(side=TOP, fill=BOTH)

        self.adaptive_button = Button(self, text="Adaptive Filter", fg="blue", font=("", 20), command=self.print)
        self.adaptive_button.pack(side=TOP, fill=BOTH)

        # mean
        self.arithmetic_button = Button(self, text=" Arithmetic Mean Filter", fg="blue", font=("", 20),
                                        command=self.print)
        self.arithmetic_button.pack(side=TOP, fill=BOTH)

        self.geometric_button = Button(self, text=" Geometric Mean Filter", fg="blue", font=("", 20),
                                       command=self.print)
        self.geometric_button.pack(side=TOP, fill=BOTH)

        self.harmonic_button = Button(self, text=" Harmonic Mean Filter", fg="blue", font=("", 20), command=self.print)
        self.harmonic_button.pack(side=TOP, fill=BOTH)

        self.contra_harmonic_button = Button(self, text=" Contraharmonic Mean Filter", fg="blue", font=("", 20),
                                             command=self.print)
        self.contra_harmonic_button.pack(side=TOP, fill=BOTH)

        self.trimmed_button = Button(self, text="Alpha Trimmed Mean Filter", fg="blue", font=("", 20),
                                     command=self.print)
        self.trimmed_button.pack(side=TOP, fill=BOTH)

        self.restart_button = Button(self, text="Restart Program", fg="RED", font=("", 20), highlightbackground='Yellow', command=self.restart)
        self.restart_button.pack(side=BOTTOM)

    def restart(self):
        restart.restart_program(self)

    def print(self):
        print("Hello")