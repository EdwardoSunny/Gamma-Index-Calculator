import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2, math
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

# read as gray scale
reference = cv2.imread('2DGammaImageCalc/referenceImage.jpg', 0) # reference image
test = cv2.imread('2DGammaImageCalc/testImage.jpg', 0) # test image
#
spacing = 0.1 # pixel spacing, scaling between pixel and real life, real units/pixel (e.g. mm/pixel)
search_radius = 1 # real units (e.g. mm)
search_percent = 0.1 # decimal standing for percent
radial_step_size = 1 # real units (e.g. mm)
angular_step_size = 1 # degrees

# find edge bdoing try catch

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

    refVal = reference[refPos[0], refPos[1]]
    xRefRealPos = refPos[0]*spacing
    yRefRealPos = refPos[1]*spacing

    # in real units (mm)

    rCount = radial_step_size
    while (rCount < search_radius+radial_step_size):
        thetaCount = angular_step_size
        while (thetaCount < 360+angular_step_size):
            # starting with the positive x axis, ccw
            yTestBasedOnStartPos = rCount * math.sin(math.radians(thetaCount))
            xTestBasedOnStartPos = rCount * math.cos(math.radians(thetaCount))

            # refPos is where the current reference pixel is, since
            # the calculations above is relative to where the reference pixel is,
            # must add to find where it actually is (localize the vector)

            # real x, y test positions
            # otherwise everything is positive
            
            if (thetaCount >= 0 and thetaCount <= 90):
                yTestBasedOnStartPos *= -1
            elif (thetaCount > 90 and thetaCount <= 180):
                xTestBasedOnStartPos *= -1
                yTestBasedOnStartPos *= -1
            elif (thetaCount > 180 and thetaCount <= 270):
                xTestBasedOnStartPos *= -1

            xTestRealPos = xTestBasedOnStartPos + refPos[0]
            yTestRealPos = yTestBasedOnStartPos + refPos[1]
            
            if not(xTestRealPos < 0 or xTestRealPos > testXData[len(testXData)-1] or yTestRealPos < 0 or yTestRealPos > testXData[len(testXData)-1]):
                currVal = interpFunction(xTestRealPos, yTestRealPos)
                currentToTestDistance = abs(math.sqrt(((xRefRealPos - xTestRealPos) ** 2) + ((yRefRealPos - yTestRealPos) ** 2)))
                currGamma = math.sqrt((((currentToTestDistance) ** 2) / search_radius) + ((refVal - currVal) ** 2) / search_percent)
                gammaList.append(currGamma) 
            thetaCount += angular_step_size
        rCount += radial_step_size
        
    return gammaList

def main():
    gammaData = get_2D_gamma_full_for_one_pixel([1,1])
    print(min(gammaData))

if (__name__ == '__main__'):
    main()