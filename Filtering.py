from tkinter import *
import tkinter as tk
from PIL import *
from PIL import Image, ImageTk
import cv2
import numpy as np
from numpy import *
import restart
import os
from Post_Filter import After_Analysis

class Filter(tk.Tk):
    def __init__(self,path):
        super().__init__(path)
        self.path = path  # this is the original image path
        split_path = self.path.split(os.sep)
        self.image_name = split_path[1].split(".")[0]  # this should give image name noise/gaussian.pnb - gaussan

        self.filter_image_path = None
        self.filter_h = None
        self.filter_w = None
        self.res = None

        self.title("IMAGE FILTERING")
        self.configure(background='black')

        #self.image_path = "Noise/Gaussian_Noise.png"

        #This is to display degraded_image
        self.PIL_image = Image.open(self.path)
        self.image_noise = ImageTk.PhotoImage(self.PIL_image)
        noise_image_label = Label(self, image=self.image_noise)
        noise_image_label.pack(side=LEFT)

        # List of all Filter
        self.arithmetic_button = Button(self, text=" Arithmetic Mean Filter", fg="blue", font=("", 20), command=self.arithmetic_mean)
        self.arithmetic_button.pack(side=TOP, fill=BOTH)

        self.median_button = Button(self, text="Median Filter", fg="blue", font=("", 20), command=self.print)
        self.median_button.pack(side=TOP, fill=BOTH)

        self.min_button = Button(self, text="Min Filter", fg="blue", font=("", 20), command=self.print)
        self.min_button.pack(side=TOP, fill=BOTH)

        self.max_button = Button(self, text="Max Filter", fg="blue", font=("", 20), command=self.print)
        self.max_button.pack(side=TOP, fill=BOTH)

        self.adaptive_button = Button(self, text="Adaptive Filter", fg="blue", font=("", 20), command=self.print)
        self.adaptive_button.pack(side=TOP, fill=BOTH)

        # mean
        self.geometric_button = Button(self, text=" Geometric Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.geometric_button.pack(side=TOP, fill=BOTH)

        self.harmonic_button = Button(self, text=" Harmonic Mean Filter", fg="blue", font=("", 20), command=self.print)
        self.harmonic_button.pack(side=TOP, fill=BOTH)

        self.contra_harmonic_button = Button(self, text=" Contraharmonic Mean Filter", fg="blue", font=("", 20),command=self.print)
        self.contra_harmonic_button.pack(side=TOP, fill=BOTH)

        self.trimmed_button = Button(self, text="Alpha Trimmed Mean Filter", fg="blue", font=("", 20), command=self.print)
        self.trimmed_button.pack(side=TOP, fill=BOTH)

        self.restart_button = Button(self, text="Restart Program", fg="RED", font=("", 20), highlightbackground='Yellow', command=self.restart)
        self.restart_button.pack(side=BOTTOM)


    def print(self):
        print("hello")


    def arithmetic_mean(self):
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)
        width, height = self.PIL_image.size
        filtered_image = np.zeros((height, width))
        for h in range(height):
            for w in range(width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                filtered_image[h, w] = 1 / (self.filter_h * self.filter_w) * np.sum(image_slice)

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)

        self.save_image()
        self.display_image()

    def compute_histogram(self):
        self.destroy()
        After_Analysis(self.filter_image_path)

    def display_image(self):
        self.result_frame = tk.Toplevel()
        self.result_frame.title("Restored Image")

        #before_filter_image = Image.open(str(self.image_path))
        before_filter_image = Image.open(self.path)
        before_filter_image_tk = ImageTk.PhotoImage(before_filter_image)
        before_filter_label = Label(self.result_frame, image=before_filter_image_tk)
        before_filter_label.img = before_filter_image_tk
        before_filter_label.pack(side=LEFT)

        #after_filter_image = Image.open(str(self.filtered_path))
        after_filter_image = Image.open(self.filter_image_path)
        after_filter_image_tk = ImageTk.PhotoImage(after_filter_image)
        after_filter_label = Label(self.result_frame, image=after_filter_image_tk)
        after_filter_label.img = after_filter_image_tk
        after_filter_label.pack(side=LEFT)

        button1 = Button(self.result_frame, text="Undo", fg="blue", font=("", 20), command=self.result_frame.destroy)
        button1.pack(side=BOTTOM, fill=BOTH)

        button2 = Button(self.result_frame, text="Compute Histogram", fg="blue", font=("", 20),command=self.compute_histogram)
        button2.pack(side=TOP, fill=BOTH)

    def get_hw(self):
        self.filter_h = int(self.my_entry_h.get())
        self.filter_w = int(self.my_entry_w.get())
        self.update()
        self.input_window.destroy()
        # print("H and W saved" )
    def full_contrast_stretch(self, image):
        min_pixel = np.min(image)
        max_pixel = np.max(image)
        image = np.uint8(255 / (max_pixel - min_pixel) * (image - min_pixel) + 0.5)
        return image

    # This will update height and width of filter
    def get_filter_size(self):
        # This is getting user input
        self.input_window = tk.Toplevel()
        self.input_window.title("Filter Size")

        label = tk.Label(self.input_window, text="Filter Dimension", font=(" ", 20))
        label.grid(row=0, column=1)

        height = tk.Label(self.input_window, text="Height:")
        width = tk.Label(self.input_window, text="weight:")
        height.grid(row=1, column=0, sticky=W)
        width.grid(row=2, column=0, sticky=W)

        self.my_entry_h = tk.Entry(self.input_window)
        self.my_entry_w = tk.Entry(self.input_window)

        self.my_entry_h.grid(row=1, column=1)
        self.my_entry_w.grid(row=2, column=1)
        my_button = tk.Button(self.input_window, text="Submit", command=self.get_hw)
        my_button.grid(row=3, column=1)
        self.wait_window(self.input_window)

    def save_image(self):
        output_dir = 'Restored/'
        # self.filter_image_path = output_dir + 'Arithmetic_Result' + str(self.filter_h) + "x" + str(self.filter_w) + ".png"
        self.filter_image_path = output_dir + self.image_name + ".png"
        # filtered_path = output_dir + 'Arithmetic_Result' + ".png"
        cv2.imwrite(self.filter_image_path, self.filtered_image_result)

    def restart(self):
        restart.restart_program(self)
