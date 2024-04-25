**Tetris Experiment for Psychopy 2024.1.1**:

- - -  

**Getting Started**:

- Make sure you downloaded at least Version: "Psychopy 2024.1.1" or higher
 (download from https://www.psychopy.org/download.html)

- Open the Tetris_Psychopy.psyexp file

- Check whether pynput is installed (tools --> plugin/package manager --> plugins --> search "pynput" and install if necessary)

- To start, press "run"/green startbutton and enter the current subject id

**General Structure**:


--> The Paradigm consists of a "pre-trial" part, in which the individual skill of a participant is determined by playing three rounds and calculating the mean level reached. The "main part" holds the actual fMRI related experiment. There are 4 condition blocks in one trial lasting 20sec each with 20 trials in total 


*Pretrial*:



1. All windows are checked to be created correctly and then the subject is asked to press the required buttons on the responsebox twice (adjust your settings in "config_paradigm_psychopy.txt")



2. Instuctions for playing Tetris follow on how to play the game (with one responsebox using the right hand)



3. To determine how skilled a subject is in playing Tetris, the participant plays 3 rounds of Tetris starting from the lowest and slowest level 1. Afterwards, the level for the actual MRI measurement is calculated based on: pretrial-levels/3 * 0.75


4. The 4 conditions in the main part are explained



*Main Structure*:

5. Each condition per default lasts 20sec to create maximal playtime while still beeing below the low-pass-filter (can be altered, though not recommended, in "loop_template.xslx" in the "duration" column)


6. The paradigm waits for remaining triggers and then ends


*Conditions*:

1. play_Tetris: Subjects play the game normally while beeing instructed to focus on mental rotation/imagery (adopted from [Agren et al. 2021](https://link.springer.com/article/10.1007/s12144-021-02081-z))

2. watch_Tetris: Control condition to account for basic visual processing not important for VSWM functions, mental imagery or planning. Subjects are instructed to just watch so automatic gameplay. Blocks do not stack in this condition to avoid that subject participate in the game subconsciously.

3. motor_control: Control condition to account for basic motor activity. Subjects are instructed to press the available buttons as if they continued playing the game (if enabled in "config_paradigm_psychopy.txt" a set visual press rhythm based on current game.speed can be seen on the display)

4. fixation_cross: Baseline condition. Subjects are instructed to just look at the fixation cross and do nothing else 

- - - 
**Config**:


1. Config of the general experiment: "config_paradigm_psychopy.txt"

2. Config of game specifics: "PyGame_Tetris_Code/config_Tetris_game.txt"

- - - 
**Game Code**:

For further information on game code read the README.md file in the "PyGame_Tetris_Code" folder

- - -
**Log Files** are collected in the "data" folder as a csv file containing the trigger signal time stemps, on- and offsets of each condition, game scores and levels, etc...

- - -
**Version Compatibility**:

The Experiment is constructed for PsychoPy 2024.1.1. You can set which Psychopy Version to use in the "Basic" tab of the experiment settings (gear-symbol). By default, this is not enabled due to a bug in the PsychoPy 2024.1.1 builder marking any experiment using this set version as incompatible with Python 3.8 (this issue seems to be fixed in Psychopy 2024.1.2).
**.py File**:


The experiment is available as python script as well. Make sure to install the correct "psychopy --version" in cmd and add the additional packages "pygame" and "pynput". 


- - - 
*potential errors*:

if this message occurs: 

'File "C:\Users\Julius\AppData\Local\Programs\Python\Python310\lib\subprocess.py", line 1456, in _execute_child:
hp, ht, pid, tid = _winapi.CreateProcess(executable, args,

FileNotFoundError: [WinError 2] Das System kann die angegebene Datei nicht finden



remove this line from the code:



psychopy.useVersion('your version') 

- - -
**Eye Tracking**:

*currently under development*

Eyetracking can be activated in "config_paradigm_psychopy.txt"

In order to set which eye tracker to use go to: Setting (gear symbol) --> go to the "Eyetracking" tab --> select your "Eyetracking Device" 


















 



