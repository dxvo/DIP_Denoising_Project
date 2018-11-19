from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import noise_estimation as ne

class Gaussian_Cropping(tk.Tk):
    def __init__(self):
        super().__init__()
        self.x = self.y = 0
        self.title("Select A Flat Image Region")
        self.canvas = tk.Canvas(self, width=512, height=512, cursor="cross", bg = "Black", bd = 0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand = True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        #label = Label(self, text = "Use Mouse to select Region", bg = "black", fg = "white")
        #label.pack()

        self.frame = Frame(self, bg = "black", height = 2)
        self.frame.pack(side = BOTTOM)

        self.button1 = Button(self.frame, text = "Click to Crop Region", relief = "sunken", command = self.crop, font = (" ", 25),)
        self.button1.pack()


        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self._display_image()
        self.area = None

    #Display image from copy folder on canvas
    def _display_image(self):

        image_path = "Noise/Gaussian_Noise.png"
        self.im = Image.open(image_path)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        #if not self.rect:
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='white')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)


    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.area = (self.start_x,self.start_y, self.end_x,self.end_y)
        #pass

    def crop(self):
        self.canvas.destroy()
        self.button1.destroy()
        #self.frame.destroy()
        print("Cropped region coordinates are ", self.area)

        #display noise image to window
        image_path = "Noise/Gaussian_Noise.png"
        self.PIL_image = Image.open(image_path)
        self.image_noise = ImageTk.PhotoImage(self.PIL_image)
        noise_image_label = Label(self, image=self.image_noise)
        noise_image_label.pack(side=LEFT)

        #crop and save the region
        cropped = self.PIL_image.crop(self.area)
        cropped.save('Cropped/Cropped_Gaussian_Image.png')

        #display it
        cropped_path = "Cropped/Cropped_Gaussian_Image.png"
        self.PIL_cropped = Image.open(cropped_path)
        self.cropped_image = ImageTk.PhotoImage(self.PIL_cropped )

        cropped_image_label = Label(self, image=self.cropped_image)
        cropped_image_label.pack(side=LEFT)

        self.button2 = Button(self.frame, text="Compute Noise Statistic", relief="sunken", command=self.compute_statistic, font=(" ", 25), )
        self.button2.pack()
        #self.quit()


    def compute_statistic(self):
        region_path = Image.open("Cropped/Cropped_Gaussian_Image.png")
        region_array = np.array(region_path)

        cropped_image_array = np.uint8(np.where(region_array < 0, 0, np.where(region_array > 255, 255, region_array)))
        output_hist, mean_value, var_value = ne.estimating(cropped_image_array)

        print("Mean is {}, Variance is {}".format(mean_value, var_value))
        print("hello")
