
import sys
from PIL import Image
import numpy as np
import scipy.ndimage


def obtain_groups(image, threshold, structuring_element):
    """
    Obtain groups of unconnected pixels
    """
    image_logical = (image[:, :, 0] < threshold).astype(np.int)
    return scipy.ndimage.measurements.label(image_logical, structure=structuring_element)

def find_shortest_distance(groups):
    """
    Find shortest distance between all groups
    """

def connect_groups(shortest_distance):
    """
    Connect two groups
    """

def main(image):
    """
    """
    # Open image and set black pixels to 1 and white pixels to 0
    image = np.asarray(Image.open(image))
    # create structuring element to determine unconnected groups of pixels in image
    s = scipy.ndimage.morphology.generate_binary_structure(2,2)
    # label the different groups, considering diagonal connections as valid
    groups, num_groups = obtain_groups(image, 255, s)
    while (num_groups):
    #     shortest_distance = find_shortest_distance(groups)
    #     image = connect_groups(shortest_distance)
        groups, num_groups = obtain_groups(image, s)
    # return image

if __name__ == "__main__":
    main(sys.argv[1])