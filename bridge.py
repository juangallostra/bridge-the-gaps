# This is an answer to: https://codegolf.stackexchange.com/questions/189277/bridge-the-gaps

import sys
import os

from PIL import Image
import numpy as np
import scipy.ndimage


def obtain_groups(image, threshold, structuring_el):
    """
    Obtain isles of unconnected pixels via a threshold on the R channel
    """
    image_logical = (image[:, :, 1] < threshold).astype(np.int)
    return scipy.ndimage.measurements.label(image_logical, structure=structuring_el)


def swap_colors(image, original_color, new_color):
    """
    Swap all the pixels of a specific color by another color 
    """
    r1, g1, b1 = original_color  # RGB value to be replaced
    r2, g2, b2 = new_color  # New RGB value
    red, green, blue = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    image[:, :, :3][mask] = [r2, g2, b2]
    return image


def main(image_path=None):
    """
    For each processed image, we begin by changing the color 
    of all the white pixels in an image to red. By doing this,
    it is guaranteed that all the elements (any isle of black 
    pixels) are connected.

    Then, we iterate over all the pixels in the image starting 
    from the top left corner and moving right and down. For every
    red pixel we find we change its color to white. If after this
    change of color there is still only one element (an element 
    being now any isle of black and red pixels), we leave the pixel
    white and move on to the next pixel. However, if after the 
    color change from red to white the number of elements is bigger
    than one, we leave the pixel red and move on to the next pixel.

    The connections obtained by only using this method show a regular
    pattern and in some cases, there are unnecessary red pixels.

    This extra red pixels can be easily removed by iterating again over
    the image and performing the same operations as explained above but
    from the bottom right corner to the top left corner. This second 
    pass is much faster since the amount of red pixels that have to be
    checked.
    """
    images = os.listdir("images")
    f = open("results.txt", "w")

    if image_path is not None:
        images = [image_path]

    for image_name in images:
        im = Image.open("images/"+image_name).convert("RGBA")
        image = np.array(im)

        image = swap_colors(image, (255, 255, 255), (255, 0, 0))

        # create structuring element to determine unconnected groups of pixels in image
        s = scipy.ndimage.morphology.generate_binary_structure(2, 2)

        for i in np.ndindex(image.shape[:2]):
            # skip black pixels
            if sum(image[i[0], i[1]]) == 255:
                continue
            image[i[0], i[1]] = [255, 255, 255, 255]
            # label the different groups, considering diagonal connections as valid
            groups, num_groups = obtain_groups(image, 255, s)
            if num_groups != 1:
                image[i[0], i[1]] = [255, 0, 0, 255]
            # Show percentage
            print((i[1] + i[0]*im.size[0])/(im.size[0]*im.size[1]))

        # Number of red pixels
        red_p = 0
        for i in np.ndindex(image.shape[:2]):
            j = (im.size[1] - i[0] - 1, im.size[0] - i[1] - 1)
            # skip black and white pixels
            if sum(image[j[0], j[1]]) == 255 or sum(image[j[0], j[1]]) == 255*4:
                continue
            image[j[0], j[1]] = [255, 255, 255, 255]
            # label the different groups, considering diagonal connections as valid
            groups, num_groups = obtain_groups(image, 255, s)
            if num_groups != 1:
                image[j[0], j[1]] = [255, 0, 0, 255]
            # Show percentage
            print((j[1] + j[0]*im.size[0])/(im.size[0]*im.size[1]))
            red_p += (sum(image[j[0], j[1]]) == 255*2)

        print(red_p)
        f.write("r_"+image_name+": "+str(red_p)+"\n")

        im = Image.fromarray(image)
        # im.show()
        im.save("r_"+image_name)
    f.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
