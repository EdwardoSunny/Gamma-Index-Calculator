import math
from scipy.interpolate import interp1d


image = [2.01, 1.99, 2, 10, 15] # image
spacing = 1 # pixel spacing, scaling between pixel and real life, real units/pixel (e.g. mm/pixel)

search_size = 2 # real units (e.g. mm)
search_percent = 0.03 # decimal standing for percent

step_size = 1 # real units (e.g. mm)
left_edge = 1
right_edge = (len(image)) * spacing

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


# gets the Gamma for one pixel
def get_1D_gamma_full(refPos):
    imageList = pixel_list_to_real(image)
    imageList = image_to_interp_data(image)
    lin_val_interp = interp1d(imageList[0], imageList[1])
        
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
    print(gamma)
        

    # backwards search
    i = refPos - step_size
    while (i >= left_edge):
        currVal = lin_val_interp(i)
        # if currGamma <= 1, pass
        currGamma = math.sqrt((((refPos - i) ** 2) / search_size) + ((refVal - currVal) ** 2) / search_percent)
        gamma = [currGamma, *gamma]
        pos = [i, *pos]
        i -= step_size

    # find min of gammas
    print(pos)
    return gamma

def main():
    print(get_1D_gamma_full(2))
    

if (__name__ == '__main__'):
    main()
    
