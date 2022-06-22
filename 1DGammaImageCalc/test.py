from scipy.interpolate import interp1d

X = [0, 2, 3, 4, 5, 6, 7, 8]

Y = [1,2,3,6,5,6,7,8] # random y values



# test value
interpolate_x = 4

# Finding the interpolation
y_interp = interp1d(X, Y)
print("Value of Y at x = {} is".format(interpolate_x),
      y_interp(interpolate_x)) 