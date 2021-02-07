############################# Virtual Background ####################################
# Author: Fernanda Amaral Melo
# Contact: fernanda.amaral.melo@gmail.com
#####################################################################################

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Macros
THRESH = 90


class virtualBackground(object):
    def __init__(self, bg, virtualbg):
        self.bg = bg
        self.virtualbg = virtualbg
        self._resizeImage()

    def replaceBg(self, pic):
        binary_pic = self._getBinaryPic(pic)
        new_pic = pic * binary_pic
        new_bg = self.virtualbg * (1 - binary_pic)
        new_pic = new_bg + new_pic
        return new_pic.astype('uint8')

    def _resizeImage(self):
        dim = tuple(reversed(self.bg.shape[:-1]))
        if(self.virtualbg.shape != self.bg.shape):
            self.virtualbg = cv2.resize(self.virtualbg, dim)

    def _getBinaryPic(self, pic):
        binary_pic = pic - self.bg
        th, binary_pic = cv2.threshold(binary_pic, THRESH, 255, cv2.THRESH_BINARY)
        binary_pic = self.morphOperations(binary_pic)
        binary_pic = binary_pic > THRESH
        return binary_pic.astype(int)

    def morphOperations(self, image):
        size = image.shape
        kernel = np.ones((int(size[0]/100), int(size[1]/100)))
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((int(size[0]/5), int(size[1]/5)))
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        return closing

    def plot(self, image):
        plt.imshow(image)
        plt.show()


if __name__ == '__main__':
    pic = cv2.imread('images/image.jpg')
    bg = cv2.imread('images/bg.jpg')
    virtualbg = cv2.imread('images/virtualbg.jpg')

    vbg = virtualBackground(bg, virtualbg)
    new_pic = vbg.replaceBg(pic)
    vbg.plot(new_pic)
