import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as ms
from PIL import *
from PIL import Image, ImageTk
import cv2
import numpy as np
from numpy import *
import restart
from crop import *

class Gaussian(tk.Tk):
    def __init__(self):
        super().__init__()
        self.filter_h = None
        self.filter_w = None

        self.title("GAUSSIAN NOISE FILTERING")
        self.configure(background='black')

        self.image_path = "Noise/Gaussian_Noise.png"
        self.PIL_image = Image.open(self.image_path)
        self.image_noise = ImageTk.PhotoImage(self.PIL_image)

        noise_image_label = Label(self, image=self.image_noise)
        noise_image_label.pack(side=LEFT)

        # Order statistic
        self.median_button = Button(self, text="Median Filter", fg="blue", font=("", 20),command=self.print)
        self.median_button.pack(side=TOP, fill=BOTH)

        self.min_button = Button(self, text="Min Filter", fg="blue", font=("", 20), command=self.print)
        self.min_button.pack(side=TOP, fill=BOTH)

        self.max_button = Button(self, text="Max Filter", fg="blue", font=("", 20), command=self.print)
        self.max_button.pack(side=TOP, fill=BOTH)

        self.adaptive_button = Button(self, text="Adaptive Filter", fg="blue", font=("", 20), command=self.print)
        self.adaptive_button.pack(side=TOP, fill=BOTH)

        #mean
        self.arithmetic_button = Button(self, text=" Arithmetic Mean Filter", fg="blue", font=("", 20),command = self.arithmetic_mean)
        self.arithmetic_button.pack(side=TOP, fill=BOTH)

        self.geometric_button = Button(self, text=" Geometric Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.geometric_button.pack(side=TOP, fill=BOTH)

        self.harmonic_button = Button(self, text=" Harmonic Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.harmonic_button.pack(side=TOP, fill=BOTH)

        self.contra_harmonic_button = Button(self, text=" Contraharmonic Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.contra_harmonic_button.pack(side=TOP, fill=BOTH)

        self.trimmed_button = Button(self, text="Alpha Trimmed Mean Filter", fg="blue", font=("", 20), command=self.print)
        self.trimmed_button.pack(side=TOP, fill=BOTH)


        self.restart_button = Button(self, text="Restart Program", fg="RED", font=("", 20), highlightbackground='Yellow', command=self.restart)
        self.restart_button.pack(side=BOTTOM)


    def restart(self):
        restart.restart_program(self)

    def print(self):
        print("hello")
    def arithmetic_mean(self):
        self.filter_h = 10
        self.filter_w = 10
        pad_h = int(1 / 2 * (self.filter_h - 1))  #think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)

        width,height = self.PIL_image.size
        filtered_image = np.zeros((height, width))

        for h in range(height):
            for w in range(width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                filtered_image[h, w] = 1 / (self.filter_h * self.filter_w) * np.sum(image_slice)

        output_dir = 'Filtered_Image/'
        self.filtered_path = output_dir + 'Arithmetic_Result' + str(self.filter_h) + "x" + str(self.filter_w) + ".png"
        #filtered_path = output_dir + 'Arithmetic_Result' + ".png"
        cv2.imwrite(self.filtered_path, filtered_image)

        #------ Now displaying image
        self.result_frame = tk.Toplevel()
        self.result_frame.title("Displaying Result")

        before_filter_image= Image.open(str(self.image_path))
        before_filter_image_tk = ImageTk.PhotoImage(before_filter_image)
        before_filter_label = Label(self.result_frame, image=before_filter_image_tk)
        before_filter_label.img = before_filter_image_tk
        before_filter_label.pack(side=LEFT)

        after_filter_image = Image.open(str(self.filtered_path))
        after_filter_image_tk = ImageTk.PhotoImage(after_filter_image)
        after_filter_label = Label(self.result_frame, image=after_filter_image_tk)
        after_filter_label.img = after_filter_image_tk
        after_filter_label.pack(side=LEFT)

        button1 = Button(self.result_frame, text="Undo", fg="blue", font=("", 20), command=self.result_frame.destroy)
        button1.pack(side=BOTTOM,fill=BOTH)

        button2 = Button(self.result_frame, text="Compute Histogram", fg="blue", font=("", 20), command=self.compute_histogram)
        button2.pack(side=TOP, fill=BOTH)

    def compute_histogram(self):
        print("NOT DONE YET")



