import csv
import random

def create_trials(n_trials, trials_seed): #function to create the main trials

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

		# create a list of row types repeated n//len(row_types) times
		rows = row_types * (n_trials)

		# randomly shuffle the rows
		random.shuffle(rows)

		# initialize variables to ensure no row type occurs more than twice in a row
		last_row_type = None
		second_last_row_type = None

		# the total number of trials should be n_trials * len(row_types)
		n = n_trials * len(row_types)
			
		# create a loop that ensures each trials does not occur more than two times in a row
		for i in range(n):
			row_type = rows[i]

			# check if the row type is the same as the last two row types
			while row_type == last_row_type and row_type == second_last_row_type:
				# if it is, shuffle the remaining unprocessed elements in the list
				remaining_rows = rows[i:]
				random.shuffle(remaining_rows)
				rows[i:] = remaining_rows
			row_type = rows[i]

		# write the row to the CSV file
		writer.writerow(row_type)

		# update the last two row types
		second_last_row_type = last_row_type
		last_row_type = row_type