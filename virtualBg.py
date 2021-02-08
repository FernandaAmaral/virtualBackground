"""Virtual Background Interface

This script uses the tkinter module to create a GUI for
1: Selecting a desired virtual background image
2: Taking a picture of the real background using webcam
3. Controlling the background replacement algorithm paramenters
(binary image threshold and opening/closing kernel size)

This script requires that `opencv and matplotlib` be installed within
the Python environment you are running this script in.

This file can also be imported as a module and contains the following
functions:
    * replace_bg - returns the picture with replaced background
"""


import cv2
import numpy as np
import matplotlib.pyplot as plt

# Macros
THRESHOLD = 90
N_OPENING = 8
N_CLOSING = 80


class virtualBackground(object):
    def __init__(self, bg, virtualbg):
        self.bg = bg
        self.virtualbg = virtualbg
        self._resize_image()

    def replace_bg(self, pic, threshold=THRESHOLD, n_opening=N_OPENING, n_closing=N_CLOSING):
        """Replaces the real background of the image "pic" by a virtual background

        Parameters
        ----------
        pic : image
            The frame you want the background to be replaced
        threshold : int
            Threshold in pixels for image binarization after bg subtraction
        n_opening: int
            Size of opening kernel matrix for opening operation
        n_closing: int
            Size of opening kernel matrix for closing operation

        Returns
        -------
        image
            Picture with replaced background
        """
        # Saves the arguments parameters
        self.threshold = threshold
        self.n_opening = int(n_opening)
        self.n_closing = int(n_closing)

        # Get the binary picture
        binary_pic = self._get_binary_pic(pic)

        # Removes the real background (background area is 0 in binary pic)
        new_pic = pic * binary_pic

        # Removes the foreground pixels from the virtual background
        new_bg = self.virtualbg * (1 - binary_pic)

        # Create the new image by summing the foreground with the virtual bg
        new_pic = new_bg + new_pic
        new_pic = new_pic.astype('uint8')
        return cv2.cvtColor(new_pic, cv2.COLOR_BGR2RGBA)

    def _resize_image(self):
        """Resize the virtual bakground image if it doesn't fit the real
        background shape"""
        dim = tuple(reversed(self.bg.shape[:-1]))
        if(self.virtualbg.shape != self.bg.shape):
            self.virtualbg = cv2.resize(self.virtualbg, dim)

    def _get_binary_pic(self, pic):
        """Subtracts the background from pic and uses the threshold parameter to
        create a binary matrix containing the labels (0 for background and 1
        for foreground)

        Parameters
        ----------
        pic : image
            The frame you want the background to be replaced

        Returns
        -------
        np.matrix
            Binary matrix
        """
        # Subtract the background from the original image
        binary_pic = pic - self.bg

        # Apply morphological operations (opening/closing)
        binary_pic = self._morph_operations(binary_pic)

        # Take the mean value from the 3 channels (RGB)
        binary_pic = binary_pic.mean(axis=(2))

        # Calculate binary matrix using user defined threshold
        binary_pic = binary_pic > self.threshold

        # Convert the matrix to 3d space (repeating the same)
        return np.repeat(binary_pic[:, :, np.newaxis], 3, axis=2)

    def _morph_operations(self, image):
        """Perform opening and closing operations on image for noise removal

        Parameters
        ----------
        image : image
            The noisy binary image

        Returns
        -------
        image
            Noise clean binary image
        """
        kernel = np.ones((self.n_opening, self.n_opening))
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((self.n_closing, self.n_closing))
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        return closing

    def plot(self, image):
        """Plot the image

        Parameters
        ----------
        image : image
        """
        plt.imshow(image)
        plt.show()


if __name__ == '__main__':
    pic = cv2.imread('images/image.jpg')
    bg = cv2.imread('images/bg.jpg')
    virtualbg = cv2.imread('images/virtualbg.jpg')

    vbg = virtualBackground(bg, virtualbg)
    new_pic = vbg.replace_bg(pic)
    vbg.plot(new_pic)
