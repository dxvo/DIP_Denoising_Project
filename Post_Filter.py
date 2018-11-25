from tkinter import *
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import cv2
import numpy as np
import os

class After_Analysis(tk.Tk):
    def __init__(self,path):
        super().__init__(path)
        self.path = path #this is path of restore
        split_path = self.path.split(os.sep)
        self.image_name  = split_path[1].split(".")[0] #this should give image name noise/gaussian.pnb - gaussan

        #self.noise_type = noise_type
        self.cropped_path = None
        self.before_hist_path = "histogram/" + "Cropped_" + self.image_name + ".png"
        self.degraded_path = "Noise/" + self.image_name + ".png"

        self.after_hist_path = None
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

        self.button1 = Button(self.frame, text = "Click to Crop Region", relief = "sunken", command = self.crop, font = (" ", 25),fg = "blue")
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
        #image_path = "Noise/Gaussian_Noise.png"
        self.im = Image.open(self.path)
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
        image_path = self.path
        #image_path = "Noise/Gaussian_Noise.png"
        self.PIL_image = Image.open(image_path)
        self.image_noise = ImageTk.PhotoImage(self.PIL_image)
        noise_image_label = Label(self, image=self.image_noise)
        noise_image_label.pack(side=LEFT)

        #crop and save the region
        cropped = self.PIL_image.crop(self.area)
        self.cropped_path = "Cropped/"+ self.image_name + "_cropped" + ".png" #this is the cropped path
        #cropped.save('Cropped/Cropped_Gaussian_Image.png')
        cropped.save(self.cropped_path)

        #display it
        #cropped_path = "Cropped/Cropped_Gaussian_Image.png"
        self.PIL_cropped = Image.open(self.cropped_path)
        self.cropped_image = ImageTk.PhotoImage(self.PIL_cropped )
        cropped_image_label = Label(self, image=self.cropped_image)
        cropped_image_label.pack(side=LEFT)

        self.button2 = Button(self.frame, text="Compute Restored Histogram", relief="sunken", command=self.compute_statistic, font=(" ", 25),fg = "blue")
        self.button2.pack(side = LEFT)

        #self.quit()

    def compute_statistic(self):
        self.button2.destroy()
        self.title("Noise_Region_Histogram")
        img = cv2.imread(self.cropped_path, 0)
        h = np.histogram(img, bins=np.arange(256), density=True)

        mean_value = 0
        var_value = 0
        for pixel in range(255):
            mean_value += pixel * h[0][pixel]
        for pixel in range(255):
            var_value += np.square(pixel - mean_value) * h[0][pixel]

        var_value = np.sqrt(var_value)
        imean = mean_value.astype(int)
        ivar = var_value.astype(int)
        print(imean, ivar)

        f = Figure(figsize=(4, 3.5), dpi=100)
        ax = f.add_subplot(111)  # this is the plot element

        ax.set_xlim([mean_value - 1.1 * var_value, mean_value + 1.1 * var_value])
        #if(self.image_name == "Salt_Noise"):
            #ax.set_xlim([mean_value , 260 ])
        #elif(self.image_name == "Peppers_Noise"):
            #ax.set_xlim([0, mean_value - 10])
        #else:
            #ax.set_xlim([mean_value - 1.1 * var_value, mean_value + 1.1 * var_value])
        #ax.set_xlim([0,257])
        ax.set_title("Restored Histogram", fontsize=16)

        x_axes = np.arange(imean - ivar, imean + ivar, (2 * ivar) / len(h[0]))
        y_axes = np.arange(0, np.amax(h[0]))
        rects1 = ax.plot(x_axes, h[0], y_axes)

        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.after_hist_path = "histogram/" + "Restored_" + self.image_name + ".png"
        f.savefig(self.after_hist_path)

        #tk.mainloop()
        self.button3 = Button(self.frame, text="Quit/Restart", relief="sunken", command=self.restart_program,font=(" ", 25),fg = "red")
        self.button3.pack(side = RIGHT)

        self.button4 = Button(self.frame, text="Compare Histogram", relief="sunken", command=self.compare_histogram,font=(" ", 25), fg="blue")
        self.button4.pack(side=RIGHT)

        self.button5 = Button(self.frame, text="Undo", relief="sunken", command=self.undo,font=(" ", 25), fg="blue")
        self.button5.pack(side=LEFT)


    def compare_histogram(self):
        self.compare_window = tk.Toplevel()

        #This is for image
        self.degraded = Image.open(self.degraded_path)
        self.restored = Image.open(self.path)
        self.degraded = self.degraded.resize((330, 330), Image.ANTIALIAS)
        self.restored= self.restored.resize((330, 330), Image.ANTIALIAS)

        self.degraded_img = ImageTk.PhotoImage(self.degraded)
        self.restored_img = ImageTk.PhotoImage(self.restored)

        degraded_img_label = Label(self.compare_window, image=self.degraded_img )
        #degraded_img_label.pack(side=LEFT)
        degraded_img_label.grid(row = 0, column = 0)

        restored_img_label = Label(self.compare_window, image=self.restored_img)
        #restored_img_label.pack(side=LEFT)
        restored_img_label.grid(row=1, column=0)

        #this is histogram
        self.before = Image.open(self.before_hist_path)
        self.after = Image.open(self.after_hist_path)
        #self.before = self.before.resize((300, 300))
        #self.afte = self.afte.resize((300, 300))

        self.before_hist_img = ImageTk.PhotoImage(self.before)
        self.after_hist_img = ImageTk.PhotoImage(self.after )

        before_hist_label = Label(self.compare_window, image=self.before_hist_img)
        #before_hist_label.pack(side=LEFT)
        before_hist_label.grid(row = 0, column = 1)

        after_hist_label = Label(self.compare_window, image=self.after_hist_img)
        #after_hist_label.pack(side=LEFT)
        after_hist_label.grid(row=1, column=1)

        self.button6 = Button(self.compare_window, text="Undo", relief="sunken", command=self.undo, font=(" ", 25), fg="blue")
        #self.button6.pack(side=BOTTOM)
        self.button6.grid(row=2, column=1)

        self.button7 = Button(self.compare_window, text="Quit/Restart", relief="sunken", command=self.restart_program,font=(" ", 25),fg = "red")
        #self.button7.pack(side = BOTTOM)
        self.button7.grid(row=3, column=1)

    def undo(self):
        self.destroy()
        After_Analysis(self.path)

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


