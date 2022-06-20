from scipy.interpolate import interp1d

X = [1, 2, 3, 4, 5, 6, 7, 8]

Y = [10, 15, 10, 2, 3, 4, 6, 2.2] # random y values



# test value
interpolate_x = 1

# Finding the interpolation
y_interp = interp1d(X, Y)
print("Value of Y at x = {} is".format(interpolate_x),
      y_interp(interpolate_x)) 