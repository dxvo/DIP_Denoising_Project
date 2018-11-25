from tkinter import *
import tkinter as tk
from PIL import *
from PIL import Image, ImageTk
import cv2
from numpy import *
import numpy as np
import restart
import os
from Post_Filter import After_Analysis
from scipy import ndimage

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
        self.order = None
        self.filter_type = None
        self.sizeMax = None #this is for adaptive median only


        self.title("IMAGE FILTERING")
        self.configure(background='black')

        #self.image_path = "Noise/Gaussian_Noise.png"

        #This is to display degraded_image
        self.PIL_image = Image.open(self.path)
        self.array_image = np.asarray(self.PIL_image)
        self.width, self.height = self.PIL_image.size
        self.variance = ndimage.variance(self.array_image)

        self.image_noise = ImageTk.PhotoImage(self.PIL_image)
        noise_image_label = Label(self, image=self.image_noise)
        noise_image_label.pack(side=LEFT)

        #All Filters
        self.arithmetic_button = Button(self, text=" Arithmetic Mean Filter", fg="blue", font=("", 20), command= lambda: self.arithmetic_mean("arithmetic"))
        self.arithmetic_button.pack(side=TOP, fill=BOTH)

        self.geometric_button = Button(self, text=" Geometric Mean Filter", fg="blue", font=(" ", 20),command=lambda: self.geometric_mean("geometric"))
        self.geometric_button.pack(side=TOP, fill=BOTH)

        self.harmonic_button = Button(self, text=" Harmonic Mean Filter", fg="blue", font=("", 20), command=lambda: self.harmonic_mean("harmonic"))
        self.harmonic_button.pack(side=TOP, fill=BOTH)

        self.contra_harmonic_button = Button(self, text=" Contraharmonic Mean Filter", fg="blue", font=("", 20),
                                             command=lambda: self.contraharmonic_mean("contraharmonic"))
        self.contra_harmonic_button.pack(side=TOP, fill=BOTH)

        self.min_button = Button(self, text="Min Filter", fg="blue", font=("", 20), command=lambda:  self.min_filter("min"))
        self.min_button.pack(side=TOP, fill=BOTH)

        self.max_button = Button(self, text="Max Filter", fg="blue", font=("", 20), command=lambda: self.max_filter("max"))
        self.max_button.pack(side=TOP, fill=BOTH)

        self.median_button = Button(self, text="Median Filter", fg="blue", font=("", 20),command=lambda: self.median_filter("median"))
        self.median_button.pack(side=TOP, fill=BOTH)

        self.trimmed_button = Button(self, text="Alpha Trimmed Filter", fg="blue", font=("", 20),command=lambda: self.alpha_trim("trim"))
        self.trimmed_button.pack(side=TOP, fill=BOTH)


        self.adaptive_Reduc_button = Button(self, text="Adaptive Reduction Filter", fg="blue", font=("", 20),
                                            command=lambda: self.adaptive_reduction("adaptive_reduction"))
        self.adaptive_Reduc_button.pack(side=TOP, fill=BOTH)

        self.adaptive_median_button = Button(self, text="Adaptive Median Filter", fg="blue", font=("", 20),
                                             command=lambda: self.adaptive_median("adaptive_median"))
        self.adaptive_median_button.pack(side=TOP, fill=BOTH)


        self.restart_button = Button(self, text="Restart Program", fg="RED", font=("", 20), highlightbackground='Yellow', command=self.restart)
        self.restart_button.pack(side=BOTTOM)


    def arithmetic_mean(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)
        filtered_image = np.zeros((self.height, self.width))
        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                filtered_image[h, w] = 1 / (self.filter_h * self.filter_w) * np.sum(image_slice)

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def geometric_mean(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)

        filtered_image = np.zeros((self.height, self.width))
        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                continuous_product = 1.0
                for f_h in range(self.filter_h):
                    for f_w in range(self.filter_w):
                        continuous_product *= image_slice[f_h, f_w]
                filtered_image[h, w] = np.power(continuous_product, 1/(self.filter_h * self.filter_w))

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def harmonic_mean(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)

        filtered_image = np.zeros((self.height, self.width))
        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                continuous_inverse_summary = 0
                for f_h in range(self.filter_h):
                    for f_w in range(self.filter_w):
                        if image_slice[f_h, f_w] != 0:
                            continuous_inverse_summary += 1 / image_slice[f_h, f_w]
                filtered_image[h, w] = self.filter_h * self.filter_w / continuous_inverse_summary

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def contraharmonic_mean(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)
        filtered_image = np.zeros((self.height, self.width))

        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                continuous_power_summary1 = 0
                continuous_power_summary2 = 0

                if self.order > 0:
                    for f_h in range(self.filter_h):
                        for f_w in range(self.filter_w):
                            continuous_power_summary1 += np.power(image_slice[f_h, f_w], self.order + 1)
                            continuous_power_summary2 += np.power(image_slice[f_h, f_w], self.order)
                else:
                    for f_h in range(self.filter_h):
                        for f_w in range(self.filter_w):
                            if image_slice[f_h, f_w]:
                                continuous_power_summary1 += np.power(image_slice[f_h, f_w], self.order + 1)
                                continuous_power_summary2 += np.power(image_slice[f_h, f_w], self.order)
                if continuous_power_summary2:
                    filtered_image[h, w] = continuous_power_summary1 / continuous_power_summary2
                else:
                    filtered_image[h, w] = 0

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def min_filter(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)
        filtered_image = np.zeros((self.height, self.width))

        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                filtered_image[h, w] = np.amin(image_slice)

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def max_filter(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)
        filtered_image = np.zeros((self.height, self.width))

        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                filtered_image[h, w] = np.amax(image_slice)

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def median_filter(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)
        filtered_image = np.zeros((self.height, self.width))

        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                filtered_image[h, w] = np.median(image_slice)

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def alpha_trim(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()

        if ((self.filter_h * self.filter_w - self.order) < 0):
            print("Order must be smaller than filter size\n")
            restart.restart_program(self)

        t = self.filter_h * self.filter_w - self.order
        pad_h = int(1 / 2 * (self.filter_h - 1))  # think there should be +.5
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)
        filtered_image = np.zeros((self.height, self.width))

        for h in range(self.height):
            for w in range(self.width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                filtered_image[h, w] = np.uint8(1/t * np.sum(image_slice))

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def adaptive_reduction(self, filter_type):
        self.filter_type = filter_type
        self.get_filter_size() #this will get height and width of filter

        filtered_image = np.zeros(shape=(self.height, self.width))
        pad_h = int(1 / 2 * (self.filter_h - 1))
        pad_w = int(1 / 2 * (self.filter_w - 1))
        image_pad = np.pad(self.PIL_image, ((pad_h, pad_h), (pad_w, pad_w)), 'constant', constant_values=0)

        for h in range(self.height):
            for w in range(self.width):  # check each pixel
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]

                if (self.variance == 0):
                    filtered_image[h, w] = self.array_image[h, w]
                else:
                    local_variance = ndimage.variance(image_slice)  # the local variance of image slice
                    mean = np.sum(image_slice) / (self.filter_h * self.filter_w)   # the mean or average

                    if (self.variance == local_variance):
                        filtered_image[h,w] =  np.uint8(mean)
                    elif (int(local_variance) == 0):
                        filtered_image[h, w] = self.array_image[h, w]
                    else:
                        filtered_image[h, w] = np.uint8(self.array_image[h, w] - (self.variance) / (local_variance * (self.array_image[h, w] - mean)))

        self.filtered_image_result = self.full_contrast_stretch(filtered_image)
        self.save_image()
        self.display_image()

    def adaptive_median(self,filter_type):
        self.filter_type = filter_type
        self.get_filter_size()  # this will get height and width of filter

        filtered_image = np.zeros(shape=(self.height, self.width))
        maxN = int(1 / 2 * (self.sizeMax - 1))
        image_pad = np.pad(self.PIL_image, ((maxN, maxN), (maxN, maxN)), 'constant', constant_values=0)

        for h in range(self.height):
            for w in range(self.width):  # check each pixel
                vert_start = h
                vert_end = h + self.sizeMax
                horiz_start = w
                horiz_end = w + self.sizeMax
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]

                value = self.array_image[h, w]
                filtered_image[h,w] = self.adaptive_median_recursive(image_slice,value,self.filter_h,self.filter_w,self.sizeMax)


    def adaptive_median_recursive(self,slice_image,cur_value,fil_height,fil_width,max):

        windows_vert_start = int(.5 * (max - fil_height))
        windows_horiz_start = int(.5 * (max - fil_width))
        windows_vert_end = int(.5 * (max + fil_height))
        windows_horiz_end = int(.5 * (max + fil_width))

        windowS = slice_image[windows_vert_start:windows_vert_end, windows_horiz_start:windows_horiz_end]
        try:
            zmed = np.median(windowS)

        except ValueError:  # raise if zero-size array is empty
            zmed = 0
        try:
            zmin = np.min(windowS)
        except ValueError:  # raise if zero-size array is empty
            zmin = 0
        try:
            zmax = np.max(windowS)
        except ValueError:
            zmax = 0

            # stage A
        if zmed > zmin and zmed < zmax:
            # stage B
            if cur_value > zmin and cur_value < zmax:  # if zmin<zxy<zmax=> in the range
                return cur_value
            else:
                return zmed
        else:

            if (self.filter_h + 2) > self.sizeMax or (self.filter_w + 2) > self.sizeMax:  # check the limit of windows
                return zmed
            else:
                return self.adaptive_median_recursive(slice_image, cur_value,  fil_height + 2, fil_width + 2, max)


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

    def get_hwo(self):
        self.filter_h = int(self.my_entry_h.get())
        self.filter_w = int(self.my_entry_w.get())

        if(self.filter_type == "contraharmonic" or self.filter_type == "trim"):
            self.order = int(self.my_entry_order.get())

        if (self.filter_type == "adaptive_median"):
            self.sizeMax = int(self.my_entry_maxsize.get())

        self.update()
        self.input_window.destroy()


    def full_contrast_stretch(self, image):
        min_pixel = np.min(image)
        max_pixel = np.max(image)
        image = np.uint8(255 / (max_pixel - min_pixel) * (image - min_pixel) + 0.5)
        return image

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


        if(self.filter_type == "contraharmonic" or self.filter_type == "trim" ):
            order = tk.Label(self.input_window, text="order:")
            order.grid(row=3, column=0, sticky=W)
            self.my_entry_order = tk.Entry(self.input_window)
            self.my_entry_order.grid(row=3, column=1)

        if(self.filter_type == "adaptive_median"):
            maxsize  = tk.Label(self.input_window, text="Max_Size:")
            maxsize.grid(row=3, column=0, sticky=W)
            self.my_entry_maxsize = tk.Entry(self.input_window)
            self.my_entry_maxsize.grid(row=3, column=1)

        my_button = tk.Button(self.input_window, text="Submit", command=self.get_hwo)
        my_button.grid(row=4, column=1)
        self.wait_window(self.input_window)

    def save_image(self):
        output_dir = 'Restored/'
        # self.filter_image_path = output_dir + 'Arithmetic_Result' + str(self.filter_h) + "x" + str(self.filter_w) + ".png"
        self.filter_image_path = output_dir + self.image_name + ".png"
        # filtered_path = output_dir + 'Arithmetic_Result' + ".png"
        cv2.imwrite(self.filter_image_path, self.filtered_image_result)

    def restart(self):
        restart.restart_program(self)
