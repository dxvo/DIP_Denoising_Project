import numpy as np
def estimating(image):
    hist = np.histogram(image, bins=np.arange(256), density=True)
    mean_value = 0
    var_value = 0
    for pixel in range(255):
        mean_value += pixel * hist[0][pixel]
    for pixel in range(255):
        var_value += np.square(pixel - mean_value) * hist[0][pixel]

    var_value = np.sqrt(var_value)
    return hist, mean_value, var_value