import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.interpolate import interp1d


image = [2.01, 1.99, 2, 10, 15] # image
spacing = 1 # pixel spacing, scaling between pixel and real life, real units/pixel (e.g. mm/pixel)

refPos = 2

search_size = 4 # real units (e.g. mm)
search_percent = 0.03 # decimal standing for percent

step_size = 1 # real units (e.g. mm)
left_edge = 1 if refPos - search_size <= 0 else (refPos - search_size) * spacing
right_edge = (len(image)) * spacing if refPos + search_size > len(image) * spacing else refPos + search_size

def pixel_list_to_real(img):
    for i in img:
        i *= spacing
    return img

def image_to_interp_data(img):
    # [xs, ys]
    coordinateList = [[], image]
    for i in range(1, len(img)+1):
        coordinateList[0].append(i)
    return coordinateList

def arrays_to_img(pixelVal, pixelPos):
    pixelArr = []
    for pixel in pixelPos:
        pixelArr.append([pixelVal[pixel], pixelVal[pixel], pixelVal[pixel]])
    return pixelArr

def get_pixel_pos(n):
    arr = []
    for i in range(0, n):
        arr.append(i)
    return arr

# gets the Gamma for one pixel
def get_1D_gamma_full_for_one_pixel(refPos):
    imageList = pixel_list_to_real(image)
    imageList = image_to_interp_data(image)
    print(imageList[0])
    print(imageList[1])
    lin_val_interp = interp1d(imageList[0], imageList[1])
    print('intr 3:' + str(lin_val_interp(1)))
    refVal = lin_val_interp(refPos)

    # forwards search
    i = refPos
    gamma = []
    pos = []

    while (i <= right_edge):
        currVal = lin_val_interp(i)
        # if currGamma <= 1, pass
        currGamma = math.sqrt((((refPos - i) ** 2) / search_size) + ((refVal - currVal) ** 2) / search_percent)
        gamma.append(currGamma)
        pos.append(i)
        i += step_size
        

    # backwards search
    i = refPos - step_size
    print(i)
    while (i >= left_edge):
        currVal = lin_val_interp(i)
        # if currGamma <= 1, pass
        currGamma = math.sqrt((((refPos - i) ** 2) / search_size) + ((refVal - currVal) ** 2) / search_percent)
        gamma = [currGamma, *gamma]
        pos = [i, *pos]
        i -= step_size

    return gamma

# def get_gamma_image():



def main():
    # imageArr = arrays_to_img(image, get_pixel_pos(len(image)))
    # npImageArr = np.array(imageArr)
    # print(npImageArr)
    # imgOriginal = plt.imshow(npImageArr)
    # plt.show()
    
    # gammaImgSize = left_edge - right_edge + 1
    # gamma = arrays_to_img(get_1D_gamma_full_for_one_pixel(refPos), get_pixel_pos(gammaImgSize))
    # npGammaArr = np.array(gamma)
    # imgGamma = plt
    print(get_1D_gamma_full_for_one_pixel(refPos))



    

if (__name__ == '__main__'):
    main()
    
