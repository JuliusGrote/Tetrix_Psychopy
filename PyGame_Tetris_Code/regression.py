import numpy as np
from multiprocessing import Array
from scipy.optimize import curve_fit

# config file is read and executed, needed for regression parameters
with open("PyGame_Tetris_Code/config_tetris_game.txt", "r") as c_tetris:
	config_tetris = c_tetris.read()
	exec(config_tetris)

class Regression:
	# define the important arrays for the regression 
	# similar to the Game() class most arrays here are multiprocessing arrays 
	# because they are accessed and transformed by multiple processes
	def __init__(self):
		self.x_range = np.arange(1, Regression_range + 1)
		self.x_array = Array('d', np.round(self.speed_formula(self.x_range)))
		self.y_array = Array('d', np.zeros(Regression_range))
		self.weights = Array('d', np.zeros(Regression_range))

	def speed_formula(self, x):
		return ((Start_speed/1250 - ((x - 1) * Speed_slope)) ** (x - 1) * 1000)	
	
	def logistic(self, x, a, b):
    # in theoy at infinte game.speeds the logistic should apporach 1
	# so the numerator is set to 1 limiting the upper y limit to 1
	    return 1 / (1 + np.exp(-b*(x-a)))

	# function that performs the actual regression using scipy
	def logistic_regression(self, x_data, y_data, weights):
		popt, pcov = curve_fit(self.logistic, x_data, y_data, sigma = 1 / weights)
		# return the optimization parameters and covariance
		return popt, pcov

	# finds the nearest value of a value "n" in an array "values" (here used to determine the level closest to the Jnd)
	def find_nearest(self, values, n):
		return min(values, key=lambda x: abs(x - n))

	# main function to determine the JND and the level closest to it
	def determine_main_level(self):
		print(f'raw y_array: {self.y_array[:]}')
		# divide self.y_array by self.weights but without getting a zero error 
		# this results in an array holding the completion rate of each tetris level.
		for i in range(len(self.y_array)):
			# operation is not performed when dividing by 0
			if self.weights[i] != 0:
				self.y_array[i] = self.y_array[i] / self.weights[i]
				
			# assign each weight at least one for regression sigma
			self.weights[i] = self.weights[i] + 1

		# transform the multiprocessing array into a numpy array that can be used for the regression
		sigma_weights = np.array(self.weights[:])
		print(f'normalized y_array: {self.y_array[:]}')
		print(f'weights: {self.weights[:]}')
		
		# perform regression
		popt, pcov = self.logistic_regression(self.x_array[:], self.y_array[:], sigma_weights)
		# print results
		print(f'parameters: {popt}, covariance: {pcov}')

		# JND (half maximal value of the function and turning point of the curve) correlates to the "a" parameter of regression function (popt[0]) 
		jnd = popt[0]

		# find the game.speed (of a level) that the calculated jnd is nearest to
		nearest_speed = self.find_nearest(self.x_array[:], jnd)
		# find the level of that game.speed (position in the x array + 1)
		jnd_level = self.x_array[:].index(nearest_speed) + 1
		print(f'JND level : {jnd_level}')
		return jnd_level, popt, pcov