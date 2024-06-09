import csv
import numpy.random as random

# two handy methods to create the main_trials and shuffle a speciefied array of conditions

# create a method that creates the main_trials
def create_trial_list(n_trials, trials_seed):

	# set a random seed if enabled in the config
	random.seed(trials_seed)
	# define the row types
	row_types = [
		("motor_control", "Images/button.png"),
		("watch_Tetris", "Images/eye.png"),
		("fixation_cross", "Images/crosshair.png")
	]


	# initialize the CSV file
	with open('main_trials.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["control_condition", "images_next_cond"])

		# create a list of row types repeated row_types * n_trials times
		rows = row_types * n_trials
		rows = shuffle_trials(rows)

		for i in range(len(rows)):
			# get the current row type
			row_type = rows[i]
			# write the row to the CSV file
			writer.writerow(row_type)

# create a method that shuffles the trials but so that each condition occurs no more than twice in a row
def shuffle_trials(rows):
		# randomly shuffle the rows
		random.shuffle(rows)

		# initialize variables to ensure no row type occurs more than twice in a row
		last_row_type = None
		second_last_row_type = None
			
		# create a loop that ensures each trials does not occur more than two times in a row
		for i in range(len(rows)):
			row_type = rows[i]
			
			# check if the row type is the same as the last two row types
			while row_type == last_row_type and row_type == second_last_row_type:
				# if it is, shuffle the remaining unprocessed elements in the list
				remaining_rows = rows[i:]
				random.shuffle(remaining_rows)
				rows[i:] = remaining_rows
				# set the new row type
				row_type = rows[i]

			# update the last two row types
			second_last_row_type = last_row_type
			last_row_type = row_type

		return rows