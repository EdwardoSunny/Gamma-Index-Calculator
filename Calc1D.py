__author__ = "Edward Sun, Torrey Pines High School, 2022"
__email__ = "edward.sun2015@gmail.com"

import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.interpolate import interp1d

# configurable constants
image = [2.01, 1.99, 2, 10, 15, 10, 2, 3, 4, 6, 2.2, 1, 10, 4, 5, 6, 6, 7] # image
spacing = 1 # pixel spacing, scaling between pixel and real life, real units/pixel (e.g. mm/pixel)
search_size = 4 # real units (e.g. mm)
search_percent = 0.03 # decimal standing for percent
step_size = 1 # real units (e.g. mm)
left_image_bound = 0 # set by person, draw, etc. in pixels, 0 indexing
right_image_bound = 7 # set by person, draw, etc. in pixels, 0 indexing

# static constants 
image = image[left_image_bound:right_image_bound+1]
print("bounded image: " + str(image))

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
    left_edge = 1 if refPos - search_size <= 0 else (refPos - search_size) * spacing
    right_edge = (len(image)) * spacing if refPos + search_size > len(image) * spacing else refPos + search_size

    imageList = pixel_list_to_real(image)
    imageList = image_to_interp_data(image)
    lin_val_interp = interp1d(imageList[0], imageList[1])
    refVal = lin_val_interp(refPos)

    # forwards search, no '+ step_size if want refPos itself gamma calculated with itself(=0.0)'
    i = refPos + step_size
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
    while (i >= left_edge):
        currVal = lin_val_interp(i)
        # if currGamma <= 1, pass
        currGamma = math.sqrt((((refPos - i) ** 2) / search_size) + ((refVal - currVal) ** 2) / search_percent)
        gamma = [currGamma, *gamma]
        pos = [i, *pos]
        i -= step_size

    return gamma

def get_passing_rate():
    totalPass = 0
    for i in range(0, len(image)):
        currGammaList = get_1D_gamma_full_for_one_pixel(i+1)
        currGamma = min(currGammaList)
        if (currGamma <= 1):
            totalPass += 1
    passDecimal = totalPass/len(image)

    return str(passDecimal * 100) + '%'

def get_gamma_image():
    gammaImage = []
    for i in range(0, len(image)):
        currGammaList = get_1D_gamma_full_for_one_pixel(i+1)
        print("Gamma for pixel " + str(i+1))
        print(currGammaList)
        currGamma = min(currGammaList)
        print(currGamma)
        gammaImage.append(currGamma)
    imageArr = arrays_to_img(gammaImage, get_pixel_pos(len(gammaImage)))
    npImageArr = np.array(imageArr)
    return npImageArr

def main():
    plt.figure("Orginial Image")
    imageArr = arrays_to_img(image, get_pixel_pos(len(image)))
    npImageArr = np.array(imageArr)
    imgOriginal = plt.imshow(npImageArr, cmap='gray')
    # print(npImageArr)
   
    plt.figure("Gamma Image")
    npGammaArr = get_gamma_image()
    gammaImg = plt.imshow(npGammaArr, cmap='gray')
    # print(npGammaArr)
    plt.text(-5, 0, 'Passing Rate: ' + str(get_passing_rate()), bbox=dict(fill=False, edgecolor='red', linewidth=3))

    plt.show()
    

if (__name__ == '__main__'):
    main()
    
