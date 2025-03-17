# this file creates the main_trials.csv file that contains the conditions for the main trials
import csv
import numpy.random as random

def create_trial_list(
                      n_trials: int,
                      trials_seed: int,
                      motor_control_duration: int,
                      watch_Tetris_duration: int,
                      fixation_cross_duration: int
                      ) -> None:
    '''
    a method that creates the main_trials.csv file that contains the conditions for the main trials
    
    Parameters:
        n_trials: int
            the number of trials in the experiment
        trials_seed: int
            the seed for the random number generator
        motor_control_duration: int
            the duration of the motor control condition
        watch_Tetris_duration: int
            the duration of the watch Tetris condition
        fixation_cross_duration: int
            the duration of the fixation cross condition
    '''

    row_headers = ["control_condition", "images_next_cond", "targeted_duration"]
    
    # Create potential row types
    potential_row_types = [
        ("motor_control", "Images/button.png", motor_control_duration),
        ("watch_Tetris", "Images/eye.png", watch_Tetris_duration),
        ("fixation_cross", "Images/crosshair.png", fixation_cross_duration)
    ]
    
    # Filter out row types with None or 0 duration
    row_types = [row for row in potential_row_types if row[2] is not None and row[2] != 0]
    
    # Check if there are any valid row types
    if not row_types:
        raise ValueError("Warning: No valid conditions found. All durations are None or 0.")
        
    
    # set a random seed if enabled in the config
    random.seed(trials_seed)

    # initialize the CSV file
    with open('main_trials.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row_headers)

        # create a list of row types repeated row_types * n_trials times
        rows = row_types * n_trials
        rows = shuffle_trials(rows)

        for i in range(len(rows)):
            # get the current row type
            row_type = rows[i]
            # write the row to the CSV file
            writer.writerow(row_type)

# create a method that shuffles the trials but so that each condition occurs no more than twice in a row
def shuffle_trials(rows: list) -> list:
    '''
    a method that shuffles the trials but so that each condition occurs no more than twice in a row

    Parameters:
        rows: list
            a list of the row types

    Returns:
        list
            a list of the row types that has been shuffled
    '''

    # randomly shuffle the rows
    random.shuffle(rows)

    # initialize variables to ensure no row type occurs more than twice in a row
    last_row_type = None
    second_last_row_type = None
        
    # create a loop that ensures each trials does not occur more than two times in a row
    for i in range(len(rows)):
        row_type = rows[i]

        # Check if the row type is the same as the last two row types
        if row_type == last_row_type and row_type == second_last_row_type:
            swapped = False

            # Look for a different element to swap with
            for j in range(i+1, len(rows)):
                # Look for a different element to swap with
                if rows[j] != row_type:
                    # Swap the elements
                    rows[i], rows[j] = rows[j], rows[i]
                    swapped = True
                    break
                
            # Execute if no different element is found
            if not swapped:
                # If no different element is found, shuffle the remaining elements
                # This is a fallback and should rarely happen with a diverse enough input list
                remaining_rows = rows[i:]
                random.shuffle(remaining_rows)
                rows[i:] = remaining_rows

            # After swapping or shuffling, set the new row type
            row_type = rows[i]

        # Update the last two row types
        second_last_row_type = last_row_type
        last_row_type = row_type
    
    return rows