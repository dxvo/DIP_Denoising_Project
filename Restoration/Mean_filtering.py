import numpy as np

class Mean_filtering:
    image = None
    filter = None
    filter_h = None
    filter_w = None
    order = None

    def __init__(self, image, mean_filter_name, filter_h, filter_w, order=0):
        """initializes the variables frequency filtering on an input image
        takes as input:
        image: the input image
        filter_name: the name of the mask to use
        cutoff: the cutoff frequency of the filter
        order: the order of the filter (only for butterworth
        returns"""
        self.image = image
        if mean_filter_name == 'arithmetic':
            self.filter = self.get_arithmetic_mean_filter
        elif mean_filter_name == 'geometric':
            self.filter = self.get_geometric_mean_filter
        elif mean_filter_name == 'harmonic':
            self.filter = self.get_harmonic_mean_filter
        elif mean_filter_name == 'contraharmonic':
            self.filter = self.get_contraharmonic_mean_filter

        self.filter_h = filter_h
        self.filter_w = filter_w
        self.order = order

    def zero_pad(self, image, pad_h, pad_w):
        image_pad = np.pad(image, ((pad_h,pad_h), (pad_w,pad_w)), 'constant', constant_values=0)
        return image_pad

    def get_arithmetic_mean_filter(self, image_slice, filter_h, filter_w):
        element_filtered = 1/(filter_h*filter_w) * np.sum(image_slice)
        return element_filtered

    def get_geometric_mean_filter(self, image_slice, filter_h, filter_w):
        continuous_product = 1
        for h in range(filter_h):
            for w in range(filter_w):
                if image_slice[h, w] != 0:
                    continuous_product *= image_slice[h, w]

        element_filtered = pow(continuous_product, 1/(filter_h * filter_w))
        return element_filtered

    def get_harmonic_mean_filter(self, image_slice, filter_h, filter_w):
        continuous_inverse_summary = 0
        for h in range(filter_h):
            for w in range(filter_w):
                if image_slice[h, w] != 0:
                    continuous_inverse_summary += 1 / image_slice[h, w]

        element_filtered = filter_h * filter_w / continuous_inverse_summary
        return element_filtered

    def get_contraharmonic_mean_filter(self, image_slice, filter_h, filter_w, order):
        continuous_power_summary1 = 0
        continuous_power_summary2 = 0
        if order > 0:
            for h in range(filter_h):
                for w in range(filter_w):
                    continuous_power_summary1 += pow(image_slice[h, w], order+1)
                    continuous_power_summary2 += pow(image_slice[h, w], order)
        else:
            for h in range(filter_h):
                for w in range(filter_w):
                    if image_slice[h, w] != 0:
                        continuous_power_summary1 += 1 / pow(image_slice[h, w], -(order + 1))
                        continuous_power_summary2 += 1 / pow(image_slice[h, w], -order)

        element_filtered = continuous_power_summary1 / continuous_power_summary2
        return element_filtered

    def full_contrast_stretch(self, image):
        """Create a full contrast stretch of the image
        input: image
        return an image with full contrast stretch
        """
        min_pixel = np.min(image)
        max_pixel = np.max(image)
        image = np.uint8(255 / (max_pixel - min_pixel) * (image - min_pixel) + 0.5)

        return image

    def filtering(self):
        pad_h = int(1/2 * (self.filter_h - 1))
        pad_w = int(1/2 * (self.filter_w - 1))
        image_pad = self.zero_pad(self.image, pad_h, pad_w)

        height, width = self.image.shape
        image_filtered = np.zeros(shape=(height, width))

        for h in range(height):
            for w in range(width):
                vert_start = h
                vert_end = h + self.filter_h
                horiz_start = w
                horiz_end = w + self.filter_w
                image_slice = image_pad[vert_start:vert_end, horiz_start:horiz_end]
                if self.filter == self.get_arithmetic_mean_filter:
                    image_filtered[h, w] = self.get_arithmetic_mean_filter(image_slice, self.filter_h, self.filter_w)
                elif self.filter == self.get_geometric_mean_filter:
                    image_filtered[h, w] = self.get_geometric_mean_filter(image_slice, self.filter_h, self.filter_w)
                elif self.filter == self.get_harmonic_mean_filter:
                    image_filtered[h, w] = self.get_harmonic_mean_filter(image_slice, self.filter_h, self.filter_w)
                else:
                    image_filtered[h, w] = self.get_contraharmonic_mean_filter(image_slice, self.filter_h, self.filter_w, self.order)

        image_filtered = self.full_contrast_stretch(image_filtered)
        return image_filtered



