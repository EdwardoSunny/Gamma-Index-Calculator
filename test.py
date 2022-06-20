from scipy.interpolate import interp1d
 
X = [1, 2, 3, 4, 5] # random x values
Y = [2.01, 1.99, 2, 10, 15] # random y values


 
# test value
interpolate_x = 3
 
# Finding the interpolation
y_interp = interp1d(X, Y)
print("Value of Y at x = {} is".format(interpolate_x),
      y_interp(interpolate_x))