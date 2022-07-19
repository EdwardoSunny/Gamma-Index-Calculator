import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2, math
import numpy as np
from scipy import interpolate
# assumes images are same resoltion/size

# this only works for square, full images (pixels values are not transparent, etc.)
# image geometry
# pixel wise:
# 0 1 2 3 4 5 x
# 0 1 2 3 4 5
# 0 1 2 3 4 5
# ...
# y
# [y][x]

# real units (mm) wise
# 0 1 2 3 4 5 x
# 1 2 3 4 5 6
# 2 3 4 5 6 7
# 3 4 5 6 7 8
# y
# [y][x]

# definition of 0mm is at the left edge of the first pixel

# read as gray scale
reference = cv2.imread('ref2.jpg', 0) # reference image
test = cv2.imread('ref2.jpg', 0) # test image
#
spacing = 0.1 # pixel spacing, scaling between pixel and real life, real units/pixel (e.g. mm/pixel)
search_radius = 1 # real units (e.g. mm)
search_percent = 0.1 # decimal standing for percent
radial_step_size = 1 # real units (e.g. mm)
angular_step_size = 1 # degrees

gammaImage = []

def test_image_pos_to_real_units(imgDimData):
    for i in imgDimData:
        i *= spacing
    return imgDimData

def get_interp_image_x_y(xRange, yRange):
    xData = []
    yData = []
    for i in range (1, xRange+1):
        xData.append(i)
    for i in range(1, yRange+1):
        yData.append(i)
    return [xData, yData]

# ref pos is a list [x, y] from original image
# computes gamma by interating test image
def get_2D_gamma_full_for_one_pixel(refPos):
    gammaList = []
    # range of x values
    testXYData = get_interp_image_x_y(len(test[0]), len(test))
    # interp data
    testXData = test_image_pos_to_real_units(testXYData[0])
    testYData = test_image_pos_to_real_units(testXYData[1])
    testZData = test

    interpFunction = interpolate.interp2d(testXData, testYData, testZData, kind='linear')

    refVal = reference[refPos[1]][refPos[0]]
    xRefRealPos = refPos[0]*spacing
    yRefRealPos = refPos[1]*spacing

    print("ref" + str(xRefRealPos))
    print(yRefRealPos)


    # in real units (mm)

    rCount = 0
    thetaCount = 0
    while (rCount < search_radius+radial_step_size):
        rCount += radial_step_size
        print(rCount)
        while (thetaCount < 360+angular_step_size):
            # starting with the positive x axis, ccw
            xTestBasedOnStartPos = rCount * math.cos(math.radians(thetaCount))
            # multiply -1 to redfine stupid coord sys
            yTestBasedOnStartPos = rCount * math.sin(math.radians(thetaCount)) * -1


            # refPos is where the current reference pixel is, since
            # the calculations above is relative to where the reference pixel is,
            # must add to find where it actually is (localize the vector)

            xTestRealPos = xTestBasedOnStartPos + refPos[0]
            yTestRealPos = yTestBasedOnStartPos + refPos[1]
    
            if not(xTestRealPos < 0 or xTestRealPos > testXData[len(testXData)-1] or yTestRealPos < 0 or yTestRealPos > testXData[len(testXData)-1]):
                # if (rCount == radial_step_size):
                #     print(thetaCount)
                currVal = interpFunction(xTestRealPos, yTestRealPos)
                # maybe this is wrong
                currentToTestDistance = abs(math.sqrt(((xRefRealPos - xTestRealPos) ** 2) + ((yRefRealPos - yTestRealPos) ** 2)))
                currGamma = math.sqrt((((currentToTestDistance) ** 2) / search_radius) + ((refVal - currVal) ** 2) / search_percent)
                gammaList.append(currGamma)
            print(thetaCount)
            thetaCount += angular_step_size        
    
    return gammaList

def get_zero_matrix(n, m):
    zeros = []

    for i in range(0, m):
        tempVector = []
        for m in range(0, n):
            tempVector.append(0)
        zeros.append(tempVector)
    

def get_gamma_image():
    for y in range(0, len(reference)):
        currentRow = []
        for x in range(0, len(reference[0])):
            print("x: " + str(x) + " y: " + str(y))
            currFullGamma = get_2D_gamma_full_for_one_pixel([x, y])
            currGamma = min(currFullGamma)
            currentRow.append(currGamma)
        gammaImage.append(currentRow)
    print(gammaImage)
    return gammaImage

def get_passing_rate():
    totalPass = 0
    for gammaRow in gammaImage:
        for gammaVal in gammaRow:
            if (gammaVal <= 1):
                totalPass += 1
    passDecimal = totalPass/len(gammaImage)
    print(totalPass)
    return str(passDecimal * 100) + '%'

def main():
    gammaImage = get_gamma_image()

    plt.figure("Original Reference Image")
    npReferenceImageArr = np.array(reference)
    imgOriginalReference = plt.imshow(npReferenceImageArr, cmap='gray')

    plt.figure("Original Test Image")
    npTestImageArr = np.array(test)
    imgTest = plt.imshow(npTestImageArr, cmap='gray')

    plt.figure("Gamma Image")
    npGammaImageArr = np.array(gammaImage)
    imgGamma = plt.imshow(npGammaImageArr, cmap='gray')
    passingRate = get_passing_rate()
    plt.text(-2, -1, 'Passing Rate: ' + str(passingRate), bbox=dict(fill=False, edgecolor='red', linewidth=3))


    plt.show()



if (__name__ == '__main__'):
    main()
