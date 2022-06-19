from scipy.interpolate import interp1d
 
X = [1,2,3,4,5] # random x values
Y = [1,2,3,4,9] # random y values
 
# test value
interpolate_x = 5
 
# Finding the interpolation
y_interp = interp1d(X, Y)
print("Value of Y at x = {} is".format(interpolate_x),
      y_interp(interpolate_x))