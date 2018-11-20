#this is to plot the histogram

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import cv2
import numpy as np


root = tk.Tk()
root.title("Noise_Region_Histogram")

img = cv2.imread('gaussian.png',0)
#img = cv2.imread("uniform.png",0)
rows, cols = img.shape
#noise = np.random.randint(-50, 50, (rows, cols)) #uniform

noise = np.random.normal(0, 30, (rows, cols)) #gaussian
img = img + noise
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
print(imean,ivar)


f = Figure(figsize=(5,4), dpi=100)
ax = f.add_subplot(111) #this is the plot element
ax.set_xlim([mean_value - 1.1*var_value,mean_value + 1.1*var_value])
ax.set_title ("Noise Estimation", fontsize=16)




x_axes = np.arange(imean - ivar, imean + ivar, (2*ivar)/len(h[0]))
y_axes = np.arange(0,np.amax(h[0]))
rects1 = ax.plot(x_axes, h[0], y_axes)


canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
f.savefig("hist.png")


tk.mainloop()








