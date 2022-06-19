import math


image = [2.1, 2, 3, 4, 5] # image
spacing = 1 # pixel spacing, scaling between pixel and real life, real units/pixel (e.g. mm/pixel)

search_size = 2 # real units (e.g. mm)
search_percent = 0.3 # deciaml standing for percent

def image_to_function_list(img):
    coordinateList = []
    for i in range(0, len(img)):
        # x is independent var, index
        # y is dependent var, value of pixel in image
        coordinateList.append([i, img[i]])
    return coordinateList

def linear_interpolate(d, x):
    output = d[0][1] + (x - d[0][0]) * ((d[1][1] - d[0][1])/(d[1][0] - d[0][0]))
 
    return output

# gets the Gamma for one pixel
def get_1D_GI(refPos):
    imageList = image_to_function_list(image)
    gamma = []

    refVal = linear_interpolate(imageList, refPos)

    # forwards search
    for i in range(refPos, len(imageList) * spacing, 1): # step? increment by what?
        currVal = linear_interpolate(imageList, i)
        # if currGamma <= 1, pass
        currGamma = math.sqrt((((refPos - i) ** 2) / search_size) + ((refVal - currVal) ** 2) / search_percent)
        gamma.append(currGamma)

    # backwards search
    for i in range(refPos, 0, -1):
        currVal = linear_interpolate(imageList, i)
        # if currGamma <= 1, pass
        currGamma = math.sqrt((((refPos - i) ** 2) / search_size) + ((refVal - currVal) ** 2) / search_percent)
        gamma.append(currGamma)

    # find min of gammas
    print(gamma)
    return min(gamma)

def main():
    print(get_1D_GI(1))
    

if (__name__ == '__main__'):
    main()
    
