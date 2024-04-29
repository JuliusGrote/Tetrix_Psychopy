# Tetris Experiment for Psychopy 2024.1.1:

- - -  
## Getting Started:

- Make sure you downloaded at least Version: "Psychopy 2024.1.1" or higher
 ([download here](https://www.psychopy.org/download.html))

- Open the [Tetris_Psychopy.psyexp](Tetris_Psychopy.psyexp) file

- Check whether pynput is installed ("Tools" &rarr; "Plugin/package manager" &rarr; "Plugins" &rarr; search "pynput" and install if necessary)

- To start, press "run"/green startbutton and enter the current subject id

- - -
## General Structure:

&rarr; The Paradigm consists of a "Pre-Trial" part, in which the individual skill of a participant is determined by playing three rounds and calculating the mean level reached. The "Main Part" holds the actual fMRI related experiment. There are 2 condition blocks in one trial lasting 20sec each with 
30 trials in total (can be altered, though not recommended, in [config_paradigm_psychopy](config_paradigm_psychopy.txt))

### Conditions:

1. play_Tetris: Subjects play the game normally while beeing instructed to focus on mental rotation/imagery (adopted from [Agren et al. 2021](https://link.springer.com/article/10.1007/s12144-021-02081-z)). Additionally, the "wm_load" can be analyzied using randomized "high" and "low" "play_Tetris" trials. See [config_paradigm_psychopy](config_paradigm_psychopy.txt) for more information!

2. watch_Tetris: Control condition to account for basic visual processing not important for VSWM functions, mental imagery or planning. Subjects are instructed to just watch so automatic gameplay. Blocks do not stack in this condition to avoid that subject participate in the game subconsciously.

3. motor_control: Control condition to account for basic motor activity. Subjects are instructed to press the available buttons as if they continued playing the game (if enabled in "config_paradigm_psychopy.txt" a set visual press rhythm based on current game.speed can be seen on the display).

4. fixation_cross: Baseline condition. Subjects are instructed to just look at the fixation cross and do nothing else. 

### Pretrial:

1. All windows are checked to be created correctly and then the subject is asked to press the required buttons on the responsebox twice (adjust your settings in [config_paradigm_psychopy](config_paradigm_psychopy.txt))

2. Instuctions for playing Tetris follow on how to play the game (with one responsebox using the right hand)

3. To determine how skilled a subject is in playing Tetris, the participant plays 3 rounds of Tetris starting from the lowest and slowest level 1. Afterwards, the level for the actual MRI measurement is calculated based on: $levelformain / 3 * 0.75$.

4. The 4 conditions in the main part are explained.

### Main Structure:


5. Each trials begins with one block of "play_Tetris" and is followed by one control condition that is selected randomly &rarr; repreat &rarr; loops until each control condition ("watch_Tetris", "motor_control", "fixation_cross") has been played for 10 times (default, "n_repeats" can be altered in [config_paradigm_psychopy](config_paradigm_psychopy.txt))

6. The paradigm waits for remaining triggers and then ends.


- - - 
## Config:

1. Config of the general experiment: [config_paradigm_psychopy](config_paradigm_psychopy.txt)

2. Config of game specifics: [config_tetris_game](./PyGame_Tetris_Code/config_tetris_game.txt)

- - - 

## Languages:

&rarr; This Experiment is available in **English** and **German**, see [config_paradigm_psychopy](config_paradigm_psychopy.txt)



&rarr; Note that this refers to the instructions for participants only, to edit information go to [instructions.py](instructions.py)



- - -
## Game Code:

For further information on game code read the [README.md](PyGame_Tetris_Code/README.md) file in the "PyGame_Tetris_Code" folder.

- - -
## Log Files:
Are collected in the [data](./data/) folder as a **csv** (not the .log) file named "subeject{subjectnumber}_Tetris_Psychopy.csv".

### Structure:
- By default, Psychopy adds the predefined "Exp.info" as columns to the Data Logfile containing information such as subject_id, date and time stamps as well as trial information, etc. 
- For analysis purposes, the file contains following data:
	- "trigger.t": Time stamps for each arriving MRI trigger.
	- "thisRow.t": Onset for each trial.
	- "Condition.started": Onset of each condition block.
	- "Condition.stopped": Offset of each condition block.
	- "Condition.duration": Duration of each condition block.
	- "Condition.info": Serves as pointer to indicate the specific and important information of each condition.
	- "game.score" : Score obtained after each "play_Tetris" condition.
    - "game.level" : Level of the finished "play_Tetris" condition.
    - "game.speed" : Speed of the falling Blocks, similar to "game.level" but correlated linearly to game difficulty (for more info see [config_tetris_game](./PyGame_Tetris_Code/config_tetris_game.txt))
	- "play_pretrial.started" : Onset of "pre_Trials".
	- "play_pretrial.stopped" : Offset of "pre_Trials".
	- "pretrial_score": Score obtained in the "pre_Trials".
	- "pretrial_level_avg": Mean level reached in the "pre_Trials".
 
- - -
## Version Compatibility:

The Experiment is constructed for PsychoPy 2024.1.1. You can set which Psychopy Version to use in the "Basic" tab of the experiment settings (gear-symbol). By default, this is not enabled due to a bug in the PsychoPy 2024.1.1 builder marking any experiment using this set version as incompatible with Python 3.8 (this issue seems to be fixed in Psychopy 2024.1.2).

- - -
## .py File:

The experiment is available as python script as well. Make sure to install the correct "psychopy --version {your version}" in cmd and add the additional packages "pygame" and "pynput" 

```shell
#Install a package
pip install {your package}
```

### Potential Errors:

*if this message occurs:* 

``` 
'File "C:\Users\Julius\AppData\Local\Programs\Python\Python310\lib\subprocess.py", line 1456, in _execute_child:
hp, ht, pid, tid = _winapi.CreateProcess(executable, args,

FileNotFoundError: [WinError 2] Das System kann die angegebene Datei nicht finden
```

*remove this line from the code:*

```python
psychopy.useVersion('your version') 
```
- - -
## Eye Tracking:

*currently under development*, *no ROIs defined yet!*

Eyetracking can be activated in "config_paradigm_psychopy.txt".

In order to set which eye tracker to use go to: Setting (gear symbol) &rarr; go to the "Eyetracking" tab &rarr; select your "Eyetracking Device".


















 



