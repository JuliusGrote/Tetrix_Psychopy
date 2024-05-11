import numpy as np
from multiprocessing import Array
from scipy.optimize import curve_fit

#config file is read and executed, needed for regression parameters
with open("PyGame_Tetris_Code/config_tetris_game.txt", "r") as c_tetris:
	config_tetris = c_tetris.read()
	exec(config_tetris)

class Regression:

	def __init__(self):
		self.x_range = np.arange(1, Regression_range + 1)
		self.x_array = Array('d', np.round(self.speed_formula(self.x_range)))
		self.y_array = Array('d', np.zeros(Regression_range))
		self.weights = Array('d', np.zeros(Regression_range))

	def speed_formula(self, x):
		return ((Start_speed/1250 - ((x - 1) * Speed_slope)) ** (x - 1) * 1000)	
	
	def logistic(self, x, a, b):
    #in theoy at infinte game.speeds the logistic should apporach 1 and at 0 game.speed the completion rate of at that specific game.speed should also be 0.
	#so the neumerator is set to 1 limiting the upper y limit to 1
	    return 1 / (1 + np.exp(-b*(x-a)))

	#function that performs the actual regression using scipy
	def logistic_regression(self, x_data, y_data, weights):
		popt, pcov = curve_fit(self.logistic, x_data, y_data, sigma = 1 / weights)
		return popt, pcov

	def find_nearest(self, values, n):
		return min(values, key=lambda x: abs(x - n))
	
	def determine_main_level(self):
		print(f'raw y_array: {self.y_array[:]}')
		#divide self.y_array by self.weights but without getting a zero error 
		for i in range(len(self.y_array)):
			#operation is not performed when deviding by 0
			if self.weights[i] != 0:
				self.y_array[i] = self.y_array[i] / self.weights[i]
				
			#assigning each weight at least one for regression sigma
			self.weights[i] = self.weights[i] + 1

		sigma_weights = np.array(self.weights[:])
		print(f'normalized y_array: {self.y_array[:]}')
		print(f'weights: {self.weights[:]}')
		
		#perform regression
		popt, pcov = self.logistic_regression(self.x_array[:], self.y_array[:], sigma_weights)
		#print results
		print(f'parameters: {popt}, covariance: {pcov}')

		#JND correlates to the b parameter of regression function (popt[0])
		jnd = popt[0]
		nearest_speed = self.find_nearest(self.x_array[:], jnd)
		#find the level that is neares to the speed of JND
		jnd_level = self.x_array[:].index(nearest_speed) + 1
		print(f'JND level : {jnd_level}')
		return jnd_level, popt, pcov