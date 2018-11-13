"""mean_filter_main.py: Star file to run mean_filter"""

# Example Usage: -i image -f filter -r filter_h -c filter_w -n noise

__author__ = "Yanyan Hu"
__email__ = "yhu24@uh.edu"
__version__ = "1.0.0"

import cv2
import sys
import numpy as np
from Mean_filtering import Mean_filtering
from datetime import datetime
import skimage
np.random.seed(1)


def main():
    """ The main function that parses input argument, calls the approciate
    filtering method and writes the output image"""

    # Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")
    parser.add_argument("-f", "--mean_filter", dest="mean_filter",
                        help="specify name of the mean filter(arithmetic, geometric, harmonic, contraharmonic)", metavar="MEAN FILTER")
    parser.add_argument("-r", "--filter_h", dest="filter_h",
                        help="specify the height of filter", metavar="FILTER HEIGHT")
    parser.add_argument("-c", "--filter_w", dest="filter_w",
                        help="specify the width of filter", metavar="FILTER WIDTH")
    parser.add_argument("-o", "--order", dest="order",
                        help="specify the order for contraharmonic mean filter", metavar="ORDER")
    parser.add_argument("-n", "--noise_type", dest="noise_type",
                        help="specify the type of noise", metavar="NOISE TYPE")

    args = parser.parse_args()

    # Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)

        output_dir = 'image_with_noise/'
        output_image_name = output_dir + image_name + "_grey" + ".jpg"
        cv2.imwrite(output_image_name, input_image)

    # Check filtering parameters
    if args.mean_filter is None:
        print("Mean filter not specified using default (arithmetic)")
        print("use the -h option to see usage information")
        mean_filter = 'arithmetic'
    elif args.mean_filter not in ['arithmetic', 'geometric', 'harmonic', 'contraharmonic']:
        print("Unknown mean filter, using default (arithmetic)")
        print("use the -h option to see usage information")
        mean_filter = 'arithmetic'
    else:
        mean_filter = args.mean_filter

    if args.filter_h is None:
        print("Filter height not specified using default (5)")
        print("use the -h option to see usage information")
        filter_h = 5
    else:
        filter_h = int(args.filter_h)

    if args.filter_w is None:
        print("Filter width not specified using default (5)")
        print("use the -h option to see usage information")
        filter_w = 5
    else:
        filter_w = int(args.filter_w)

    if args.noise_type is None:
        print("Noise type not specified using default (gaussian)")
        print("use the -h option to see usage information")
        noise_type = 'gaussian'
    elif args.noise_type not in ['gaussian', 'salt', 'pepper']:
        print("Unknown noise, using default (gaussian)")
        print("use the -h option to see usage information")
        noise_type = 'gaussian'
    else:
        noise_type = args.noise_type

    if mean_filter in ['contraharmonic']:
        if args.order is None:
            print("Order of the contraharmonic mean filter not specified, using default (2)")
            print("use the -h option to see usage information")
            order = 2
        else:
            order = float(args.order)

    # Add noise(mean, variance)
    rows, cols = input_image.shape
    # skimage.util.random_noise(input_image, mode='gaussian', mean=0, var=50, seed=None, clip=True)
    if noise_type == 'gaussian':
        noise_gaussian = np.random.normal(0, 20, (rows, cols))
        input_image = input_image + noise_gaussian
        input_image = np.where(input_image > 255, 255, input_image)
        input_image = np.where(input_image < 0, 0, input_image)

    elif noise_type == 'salt':
        noise_salt = np.random.randint(0, 256, (rows, cols))
        prob = 0.1
        noise_salt = np.where(noise_salt < prob * 256, 255, 0)
        input_image.astype("float")
        noise_salt.astype("float")
        input_image = input_image + noise_salt
        input_image = np.where(input_image > 255, 255, input_image)

    elif noise_type == 'pepper':
        noise_pepper = np.random.randint(0, 256, (rows, cols))
        prob = 0.1
        noise_pepper = np.where(noise_pepper < prob * 256, -255, 0)
        input_image.astype("float")
        noise_pepper.astype("float")
        input_image = input_image + noise_pepper
        input_image = np.where(input_image < 0, 0, input_image)

    output_dir = 'image_with_noise/'
    output_image_name = output_dir + image_name + '_' + noise_type + '_noise' + ".jpg"
    cv2.imwrite(output_image_name, input_image)

    output = None
    if mean_filter in ['arithmetic', 'geometric', 'harmonic']:
        Filter_obj = Mean_filtering(input_image, mean_filter, filter_h, filter_w)
        output = Filter_obj.filtering()
    else:
        Filter_obj = Mean_filtering(input_image, mean_filter, filter_h, filter_w, order)
        output = Filter_obj.filtering()

    # Write output file
    output_dir = 'output/'

    output_image_name = output_dir+image_name+"_"+mean_filter+datetime.now().strftime("%m%d-%H%M%S")+".jpg"
    cv2.imwrite(output_image_name, output)


if __name__ == "__main__":
    main()
