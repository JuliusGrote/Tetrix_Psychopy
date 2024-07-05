#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.1.1),
    on Juli 05, 2024, at 13:42
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware, iohub
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from create_processes
# import necessary packages and load them
import ctypes
import time
from pynput import keyboard as pynput_keyboard
from multiprocessing import Process, Value
from psychopy.visual.windowwarp import Warper

# Change the current working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# ensure that all classes can be imported from this folder
sys.path.append('PyGame_Tetris_Code')

# import tetris classes/methods
from game import Game
from tetris_instance import Tetris_Instance

# import paradigm modules in other files
from instructions import Instructions
from utils import *
from main_trials import *

# get config information
with open("config_paradigm_psychopy.txt", "r") as c_paradigm:
    config_paradigm = c_paradigm.read()
    exec(config_paradigm)

# initialize Pygame and Game
pygame.init()
game = Game()

# if N_repeats is None the function produces an error
if N_repeats != None:
    # create the main_trials-order for the main part
    create_trial_list(
                      N_repeats,
                      Main_trials_seed,
                      Motor_control_duration,
                      Watch_Tetris_duration,
                      Fixation_cross_duration
                      )

# set language according to setting in config file
Inst = Instructions()
Inst.set_instructions(
                      Language,
                      N_repeats,
                      Play_Tetris_duration,
                      Motor_control_duration,
                      Watch_Tetris_duration,
                      Fixation_cross_duration
                      )

# check in which order the keyboards were registered fordebugging purposes
list_keyboards()

# define a function to compare between high and low working memory load and speed / game difficulty
# define functions that creates a list with shuffled order of "high" and "low" wm_load and speed
# used to randomize the "high" and "low" "play_Tetris" amount of next block or game speed
# unfortunately it is less comlicated to define the function here compared to importing it from another module

def comp_wm_load_speed(total_trials, trial_nr):
    global wm_load_seq
    global speed_seq
    global high_level
    global low_level
    # create the arrays only on the first trial
    if trial_nr == 0: 
        # halfs the amount of conditions based on total trials
        n_per_load = int(total_trials/2)
        # creates a array of random order for each comparison that defines the order of "high" or "low" conditions in the "play_Tetris" parts.
        if Comp_wm_load == True and Comp_speed == False:
            wm_load_low = 'low_load'
            wm_load_high = 'high_load'
            wm_load_seq = [wm_load_low]*n_per_load + [wm_load_high]*n_per_load # add equal number of "high" and "low"
            np.random.seed(Load_seed) 
            wm_load_seq = shuffle_trials(wm_load_seq)
            print(f'wm_load_seq: {wm_load_seq}')
        elif Comp_speed == True and Comp_wm_load == False:
            speed_low = 'low_speed'
            speed_high = 'high_speed'
            speed_seq = [speed_low]*n_per_load + [speed_high]*n_per_load # add equal number of "high" and "low"
            np.random.seed(Speed_seed) 
            speed_seq = shuffle_trials(speed_seq)
            print(f'speed_seq: {speed_seq}')
         
        # if both comparison conditions are enabled, in order to get an equal distribution across all 4 different possible combination a tuple array is created.
        elif Comp_speed == True and Comp_wm_load == True:
            combinations = ([('low_load', 'low_speed')] + [('low_load', 'high_speed')] + [('high_load', 'low_speed')] + [('high_load', 'high_speed')]) * int(n_per_load/2) 
            
            # shuffle the tuple array into a random order
            np.random.seed(Comp_all_seed) 
            combinations = shuffle_trials(combinations)
            
            # unzip the tuple array in to the two part-arrays, which define the condition combinations in the "play_Tetris" parts
            wm_load_seq, speed_seq = zip(*combinations)
            print(f'wm_load_seq: {wm_load_seq} and speed_seq: {speed_seq}')
          # make sure that high_level and low_level are never equal or below 0 (game crash)  
        if Comp_speed == True:
            if abs(Low_level) >= game.level.value and Low_level < 0:
                low_level = 1
            else:
                low_level = game.level.value + Low_level
            if abs(High_level) >= game.level.value and High_level < 0:
                high_level = 1
            else:
                high_level = game.level.value + High_level
        # set this to false and ensure that the array creation is done only once!       
        first_trial = False
     
    # set "high" or "low" for "wm_load" or "speed" in the current trial
    if Comp_wm_load == True:
        print(f'Trial {trial_nr + 1} of {total_trials} - {wm_load_seq[trial_nr]}')
        if wm_load_seq[trial_nr] == 'low_load':
            game.three_next_blocks.value = False
        else:
            game.three_next_blocks.value = True
    if Comp_speed == True:
        print(f'Trial {trial_nr + 1} of {total_trials} - {speed_seq[trial_nr]}')
        if speed_seq[trial_nr] == 'low_speed':
            game.level.value = low_level
            game.level_for_main.value = low_level
        else:
            game.level.value = high_level
            game.level_for_main.value = high_level


# define a method to skip a trial that belongs to either to the "pretrial" or "main_trials" if those are disabled by config
def skip_if_enabled(part):
    if part == "pretrial" and game.pretrial_rounds == None or part == "main_trials" and N_repeats == None:
        # return False to set continueRoutine = False
        return False
    else:
        # return False to set continueRoutine = True
        return True
# Run 'Before Experiment' code from code_play


# Run 'Before Experiment' code from code_watch


# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.1.1'
expName = 'Tetrix_PsychoPy'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': 'sub00',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_loggingLevel = logging.getLevel('data')
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
    # override logging level
    _loggingLevel = logging.getLevel(
        prefs.piloting['pilotLoggingLevel']
    )

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s' % (expInfo['participant'], expName)
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='G:\\Meine Ablage\\Studium\\Github\\Tetrix_Psychopy\\Tetrix_PsychoPy.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='priority'
    )
    thisExp.setPriority('trigger.t', 31)
    thisExp.setPriority('thisRow.t', 30)
    thisExp.setPriority('Condition.started', 29)
    thisExp.setPriority('Condition.stopped', 28)
    thisExp.setPriority('Condition.duration', 27)
    thisExp.setPriority('game.score', 26)
    thisExp.setPriority('game.level', 24)
    thisExp.setPriority('game.speed', 23)
    thisExp.setPriority('game.wm_load_condition', 22)
    thisExp.setPriority('game.speed_condition', 21)
    thisExp.setPriority('Condition.info', 20)
    thisExp.setPriority('participant', 19)
    thisExp.setPriority('main_trials.thisTrialN', 18)
    thisExp.setPriority('main_trials.thisIndex', 17)
    thisExp.setPriority('main_trials.thisN', 16)
    thisExp.setPriority('main_trials.thisRepN', 15)
    thisExp.setPriority('targeted_duration', 14)
    thisExp.setPriority('control_condition', 13)
    thisExp.setPriority('Images_next_cond', 12)
    thisExp.setPriority('notes', 0)
    thisExp.setPriority('play_pretrial.started', -1)
    thisExp.setPriority('pretrial.round_t', -2)
    thisExp.setPriority('play_pretrial.stopped', -3)
    thisExp.setPriority('pretrial.score', -4)
    thisExp.setPriority('pretrial.start_level', -5)
    thisExp.setPriority('pretrial.fail_level', -6)
    thisExp.setPriority('pretrial.level_avg', -7)
    thisExp.setPriority('JND', -8)
    thisExp.setPriority('pretrial.game_speeds', -9)
    thisExp.setPriority('pretrial.completion_rate', -10)
    thisExp.setPriority('pretrial.weights', -11)
    thisExp.setPriority('pretrial.optimization_parameters', -12)
    thisExp.setPriority('expName', -13)
    thisExp.setPriority('date', -14)
    thisExp.setPriority('expStart', -15)
    thisExp.setPriority('frameRate', -16)
    thisExp.setPriority('psychopyVersion', -17)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # this outputs to the screen, not a file
    logging.console.setLevel(_loggingLevel)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=_loggingLevel)
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=[1707, 960], fullscr=_fullScr, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='Home_test', color=[-0.6549, -0.6549, -0.0039], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height', 
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [-0.6549, -0.6549, -0.0039]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.mouseVisible = False
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    ioSession = '1'
    if 'session' in expInfo:
        ioSession = str(expInfo['session'])
    ioServer = io.launchHubServer(window=win, experiment_code='Tetrix_PsychoPy', session_code=ioSession, datastore_name=thisExp.dataFileName, **ioConfig)
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_resp_return_response') is None:
        # initialise key_resp_return_response
        key_resp_return_response = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_return_response',
        )
    if deviceManager.getDevice('press_continue_1') is None:
        # initialise press_continue_1
        press_continue_1 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_1',
        )
    if deviceManager.getDevice('press_continue_2') is None:
        # initialise press_continue_2
        press_continue_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_2',
        )
    if deviceManager.getDevice('press_continue_2_1') is None:
        # initialise press_continue_2_1
        press_continue_2_1 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_2_1',
        )
    if deviceManager.getDevice('press_continue_3') is None:
        # initialise press_continue_3
        press_continue_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_3',
        )
    if deviceManager.getDevice('press_continue_3_1') is None:
        # initialise press_continue_3_1
        press_continue_3_1 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_3_1',
        )
    if deviceManager.getDevice('press_continue_3_3') is None:
        # initialise press_continue_3_3
        press_continue_3_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_3_3',
        )
    if deviceManager.getDevice('press_continue_3_4') is None:
        # initialise press_continue_3_4
        press_continue_3_4 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_3_4',
        )
    if deviceManager.getDevice('press_continue_4') is None:
        # initialise press_continue_4
        press_continue_4 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_4',
        )
    if deviceManager.getDevice('press_continue_4_1') is None:
        # initialise press_continue_4_1
        press_continue_4_1 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_4_1',
        )
    if deviceManager.getDevice('press_continue_5') is None:
        # initialise press_continue_5
        press_continue_5 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_5',
        )
    if deviceManager.getDevice('press_continue_5_1') is None:
        # initialise press_continue_5_1
        press_continue_5_1 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_5_1',
        )
    if deviceManager.getDevice('press_continue_6') is None:
        # initialise press_continue_6
        press_continue_6 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_6',
        )
    if deviceManager.getDevice('press_continue_7') is None:
        # initialise press_continue_7
        press_continue_7 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_7',
        )
    if deviceManager.getDevice('press_continue_7_1') is None:
        # initialise press_continue_7_1
        press_continue_7_1 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_7_1',
        )
    if deviceManager.getDevice('press_continue_6_2') is None:
        # initialise press_continue_6_2
        press_continue_6_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_6_2',
        )
    if deviceManager.getDevice('press_continue_8') is None:
        # initialise press_continue_8
        press_continue_8 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_8',
        )
    if deviceManager.getDevice('press_continue_9') is None:
        # initialise press_continue_9
        press_continue_9 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_9',
        )
    if deviceManager.getDevice('press_continue_10') is None:
        # initialise press_continue_10
        press_continue_10 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_10',
        )
    if deviceManager.getDevice('press_continue_10_1') is None:
        # initialise press_continue_10_1
        press_continue_10_1 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_10_1',
        )
    if deviceManager.getDevice('press_continue_11') is None:
        # initialise press_continue_11
        press_continue_11 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_11',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # prevent components from auto-drawing
    win.stashAutoDraw()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # flip the screen
        win.flip()
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # restore auto-drawn components
    win.retrieveAutoDraw()
    # reset any timers
    for timer in timers:
        timer.reset()


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # enter 'rush' mode (raise CPU priority)
    if not PILOTING:
        core.rush(enable=True)
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "load_processes" ---
    # Run 'Begin Experiment' code from create_processes
    #checks whether display orientation is altered (defined in "config_paradigm_psychopy.txt")
    if Flip_vertically == True or Flip_horizontally == True:
        
        #warping function provided by psychopy.visual.windowwarper
        #cannot be done "Before  experiment" due to win being defined at the end of "Before experiment"
        warper = Warper(win)
        
        #even if warping function is set warper needs to be updated before changes apply to the display
        #Psychopy uses switched arguments for a vertical and horizontal mirroring compared to "config_paradigm_psychopy.txt"
        warper.changeProjection(None, flipHorizontal = Flip_vertically, flipVertical = Flip_horizontally)
    
    #create a keyboard listener that collets Trigger by the MR
    #cannot be defined before the experiment due to globalCLock being defined in run(...)
    def check_for_trigger(key):
        try:
            if key.char =='q':
                return False
            if key.char == Trigger:
                thisExp.addData('trigger.t', globalClock.getTime(format='float'))
                thisExp.nextEntry()
        except AttributeError: 
            pass
    load_processes_text = visual.TextStim(win=win, name='load_processes_text',
        text='Start Processes...',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "check_for_processes" ---
    check_Text = visual.TextStim(win=win, name='check_Text',
        text='Checking for Processes...',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "show_pretrial" ---
    check_pretrial = visual.TextStim(win=win, name='check_pretrial',
        text='check pretrial\n',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "check_for_pretrial" ---
    duration_and_fix_play_pretrial = visual.TextStim(win=win, name='duration_and_fix_play_pretrial',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "show_play" ---
    check_play = visual.TextStim(win=win, name='check_play',
        text='check play',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "check_window_play" ---
    duration_and_fix_play = visual.TextStim(win=win, name='duration_and_fix_play',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "show_watch" ---
    check_watch = visual.TextStim(win=win, name='check_watch',
        text='check watch',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "check_window_watch" ---
    duration_and_fix_watch = visual.TextStim(win=win, name='duration_and_fix_watch',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "wait_1s" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "check_response_box" ---
    text_check_response = visual.TextStim(win=win, name='text_check_response',
        text=Inst.font_check_response,
        font='Open Sans',
        pos=(0, 0.2), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_check_response_2 = visual.TextStim(win=win, name='text_check_response_2',
        text=Inst.font_check_response_2,
        font='Open Sans',
        pos=(0, -0.2), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    text_1 = visual.TextStim(win=win, name='text_1',
        text='',
        font='Open Sans',
        pos=(-0.5, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    text_2 = visual.TextStim(win=win, name='text_2',
        text='',
        font='Open Sans',
        pos=(-0.25, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    text_3 = visual.TextStim(win=win, name='text_3',
        text='',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    text_4 = visual.TextStim(win=win, name='text_4',
        text='',
        font='Open Sans',
        pos=(0.25, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-6.0);
    text_5 = visual.TextStim(win=win, name='text_5',
        text='',
        font='Open Sans',
        pos=(0.5, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-7.0);
    key_resp_return_response = keyboard.Keyboard(deviceName='key_resp_return_response')
    
    # --- Initialize components for Routine "pretrial_intro" ---
    Intro_2 = visual.TextStim(win=win, name='Intro_2',
        text=Inst.font_Intro_2,
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Text_continue_1 = visual.TextStim(win=win, name='Text_continue_1',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_1 = keyboard.Keyboard(deviceName='press_continue_1')
    
    # --- Initialize components for Routine "explain_pretrial" ---
    explanation_pretrial = visual.TextStim(win=win, name='explanation_pretrial',
        text=Inst.font_explanation_pretrial,
        font='Open Sans',
        pos=(0, 0), height=0.06, wrapWidth=1.5, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_2 = visual.TextStim(win=win, name='Text_continue_2',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_2 = keyboard.Keyboard(deviceName='press_continue_2')
    
    # --- Initialize components for Routine "intro_how_to_play" ---
    text_how_to_play = visual.TextStim(win=win, name='text_how_to_play',
        text=Inst.font_how_to_play,
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Text_continue_2_1 = visual.TextStim(win=win, name='Text_continue_2_1',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_2_1 = keyboard.Keyboard(deviceName='press_continue_2_1')
    
    # --- Initialize components for Routine "explain_tetris_1" ---
    explain_game_mechanics_1 = visual.ImageStim(
        win=win,
        name='explain_game_mechanics_1', 
        image=Inst.img_explain_game_mechanics_1, mask=None, anchor='center',
        ori=0.0, pos=(0, 0.03), size=(0.84, 0.88),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Text_continue_3 = visual.TextStim(win=win, name='Text_continue_3',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_3 = keyboard.Keyboard(deviceName='press_continue_3')
    
    # --- Initialize components for Routine "explain_tetris_2" ---
    explain_game_mechanics_2 = visual.ImageStim(
        win=win,
        name='explain_game_mechanics_2', 
        image=Inst.img_explain_game_mechanics_2, mask=None, anchor='center',
        ori=0.0, pos=(0, 0.03), size=(0.9, 0.9),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Text_continue_3_1 = visual.TextStim(win=win, name='Text_continue_3_1',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_3_1 = keyboard.Keyboard(deviceName='press_continue_3_1')
    
    # --- Initialize components for Routine "explain_tetris_3" ---
    explain_game_mechanics_3 = visual.ImageStim(
        win=win,
        name='explain_game_mechanics_3', 
        image=Inst.img_explain_game_mechanics_3, mask=None, anchor='center',
        ori=0.0, pos=(0, 0.03), size=(1.25, 0.9),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Text_continue_3_3 = visual.TextStim(win=win, name='Text_continue_3_3',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_3_3 = keyboard.Keyboard(deviceName='press_continue_3_3')
    
    # --- Initialize components for Routine "explain_staircase" ---
    text_explain_staircase = visual.TextStim(win=win, name='text_explain_staircase',
        text=Inst.font_explain_staircase,
        font='Open Sans',
        pos=(0, 0), height=0.06, wrapWidth=1.5, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_3_4 = visual.TextStim(win=win, name='Text_continue_3_4',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_3_4 = keyboard.Keyboard(deviceName='press_continue_3_4')
    
    # --- Initialize components for Routine "explain_tetris_4" ---
    explain_controls = visual.ImageStim(
        win=win,
        name='explain_controls', 
        image=Inst.img_explain_controls, mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(1.25, 0.8),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Controls = visual.TextStim(win=win, name='Controls',
        text=Inst.font_Controls,
        font='Open Sans',
        pos=(0, 0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_4 = visual.TextStim(win=win, name='Text_continue_4',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0.0, -0.45), height=0.05, wrapWidth=2.0, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_4 = keyboard.Keyboard(deviceName='press_continue_4')
    
    # --- Initialize components for Routine "start_pretrial" ---
    text_start_pretrial = visual.TextStim(win=win, name='text_start_pretrial',
        text=Inst.font_start_pretrial
    ,
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_4_1 = keyboard.Keyboard(deviceName='press_continue_4_1')
    
    # --- Initialize components for Routine "wait_1s_pretrial" ---
    fix_wait_pretrial = visual.TextStim(win=win, name='fix_wait_pretrial',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "play_pretrial" ---
    fix_2 = visual.TextStim(win=win, name='fix_2',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Start_eytracking = hardware.eyetracker.EyetrackerControl(
        tracker=eyetracker,
        actionType='Start Only'
    )
    
    # --- Initialize components for Routine "wait_1s_pretrial" ---
    fix_wait_pretrial = visual.TextStim(win=win, name='fix_wait_pretrial',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "pause_n_sec" ---
    text_break = visual.TextStim(win=win, name='text_break',
        text=Inst.font_pause_n_sec,
        font='Open Sans',
        pos=(0, 0.15), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_pause_n_sec = visual.TextStim(win=win, name='text_pause_n_sec',
        text='',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "intro_main" ---
    intro_main_text = visual.TextStim(win=win, name='intro_main_text',
        text=Inst.font_intro_main,
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_continue_5 = visual.TextStim(win=win, name='text_continue_5',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_5 = keyboard.Keyboard(deviceName='press_continue_5')
    
    # --- Initialize components for Routine "intro_structure" ---
    text_intro_structure = visual.TextStim(win=win, name='text_intro_structure',
        text=Inst.font_intro_structure,
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_continue_5_1 = visual.TextStim(win=win, name='text_continue_5_1',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_5_1 = keyboard.Keyboard(deviceName='press_continue_5_1')
    
    # --- Initialize components for Routine "explain_basic_structure" ---
    controller_example_1 = visual.ImageStim(
        win=win,
        name='controller_example_1', 
        image='Images/controller.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.6, -0.2), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    watch_example_1 = visual.ImageStim(
        win=win,
        name='watch_example_1', 
        image='Images/eye.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.2, -0.2), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    motorcontrol_example_1 = visual.ImageStim(
        win=win,
        name='motorcontrol_example_1', 
        image='Images/button.png', mask=None, anchor='center',
        ori=0.0, pos=(0.2, -0.2), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    baseline_example_1 = visual.ImageStim(
        win=win,
        name='baseline_example_1', 
        image='Images/crosshair.png', mask=None, anchor='center',
        ori=0.0, pos=(0.6, -0.2), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-4.0)
    Announcement = visual.TextStim(win=win, name='Announcement',
        text=Inst.font_Announcement,
        font='Open Sans',
        pos=(0, 0.2), height=0.1, wrapWidth=1.8, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    Text_continue_6 = visual.TextStim(win=win, name='Text_continue_6',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-6.0);
    press_continue_6 = keyboard.Keyboard(deviceName='press_continue_6')
    
    # --- Initialize components for Routine "explain_play_Tetris" ---
    controller_example = visual.ImageStim(
        win=win,
        name='controller_example', 
        image='Images/controller.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0), size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    play_Tetris_text = visual.TextStim(win=win, name='play_Tetris_text',
        text=Inst.font_play_Tetris,
        font='Open Sans',
        pos=(0.2, 0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Text_continue_7 = visual.TextStim(win=win, name='Text_continue_7',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    press_continue_7 = keyboard.Keyboard(deviceName='press_continue_7')
    
    # --- Initialize components for Routine "explain_comp_load" ---
    # Run 'Begin Experiment' code from skip_explain_comp_load
    
        
    
    controller_example_2 = visual.ImageStim(
        win=win,
        name='controller_example_2', 
        image='Images/controller.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0), size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    text_comp_load = visual.TextStim(win=win, name='text_comp_load',
        text=Inst.font_explain_comp_load,
        font='Open Sans',
        pos=(0.2, 0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Text_continue_7_1 = visual.TextStim(win=win, name='Text_continue_7_1',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    press_continue_7_1 = keyboard.Keyboard(deviceName='press_continue_7_1')
    
    # --- Initialize components for Routine "explain_comp_speed" ---
    controller_example_3 = visual.ImageStim(
        win=win,
        name='controller_example_3', 
        image='Images/controller.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0), size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    text_comp_speed = visual.TextStim(win=win, name='text_comp_speed',
        text=Inst.font_explain_comp_speed,
        font='Open Sans',
        pos=(0.2, 0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Text_continue_7_2 = visual.TextStim(win=win, name='Text_continue_7_2',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    press_continue_6_2 = keyboard.Keyboard(deviceName='press_continue_6_2')
    
    # --- Initialize components for Routine "explain_motor_control" ---
    motorcontrol_example = visual.ImageStim(
        win=win,
        name='motorcontrol_example', 
        image='Images/button.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0.0), size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    text_motor = visual.TextStim(win=win, name='text_motor',
        text=Inst.font_motor,
        font='Open Sans',
        pos=(0.2, 0.0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Text_continue_8 = visual.TextStim(win=win, name='Text_continue_8',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    press_continue_8 = keyboard.Keyboard(deviceName='press_continue_8')
    
    # --- Initialize components for Routine "explain_watch_Tetris" ---
    watch_example = visual.ImageStim(
        win=win,
        name='watch_example', 
        image='Images/eye.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0.0), size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    text_watch = visual.TextStim(win=win, name='text_watch',
        text=Inst.font_watch,
        font='Open Sans',
        pos=(0.2, 0.0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Text_continue_9 = visual.TextStim(win=win, name='Text_continue_9',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    press_continue_9 = keyboard.Keyboard(deviceName='press_continue_9')
    
    # --- Initialize components for Routine "explain_fixation_cross" ---
    baseline_example = visual.ImageStim(
        win=win,
        name='baseline_example', 
        image='Images/crosshair.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0.0), size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    text_cross = visual.TextStim(win=win, name='text_cross',
        text=Inst.font_cross,
        font='Open Sans',
        pos=(0.2, 0.0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Text_continue_10 = visual.TextStim(win=win, name='Text_continue_10',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    press_continue_10 = keyboard.Keyboard(deviceName='press_continue_10')
    
    # --- Initialize components for Routine "explain_trials" ---
    img_explain_trials = visual.ImageStim(
        win=win,
        name='img_explain_trials', 
        image='Images/Explain_Trials.png', mask=None, anchor='center',
        ori=0.0, pos=(0, -0.1), size=(0.75, 0.53),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    text_explain_trials = visual.TextStim(win=win, name='text_explain_trials',
        text=Inst.font_explain_trials
    ,
        font='Open Sans',
        pos=(0, 0.32), height=0.05, wrapWidth=1.5, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    Text_continue_10_1 = visual.TextStim(win=win, name='Text_continue_10_1',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    press_continue_10_1 = keyboard.Keyboard(deviceName='press_continue_10_1')
    
    # --- Initialize components for Routine "start_experiment" ---
    Start = visual.TextStim(win=win, name='Start',
        text=Inst.font_start,
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_11 = visual.TextStim(win=win, name='Text_continue_11',
        text=Inst.font_continue,
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_11 = keyboard.Keyboard(deviceName='press_continue_11')
    
    # --- Initialize components for Routine "wait_1s" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "wait_1s" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "wait_for_trigger" ---
    wait_for_trigger_text = visual.TextStim(win=win, name='wait_for_trigger_text',
        text='Waiting for trigger to start...',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "wait_1s" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "three_seconds_timer" ---
    text_three_sec_timer = visual.TextStim(win=win, name='text_three_sec_timer',
        text='',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "show_play_tetris" ---
    Icon_for_play_Tetris = visual.ImageStim(
        win=win,
        name='Icon_for_play_Tetris', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=1.0,
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "wait_1s" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "tetris_condition" ---
    duration_and_fix_play_Tetris = visual.TextStim(win=win, name='duration_and_fix_play_Tetris',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "condition_ended" ---
    condition_ended_text = visual.TextStim(win=win, name='condition_ended_text',
        text=Inst.font_condition_ended,
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "wait_ISI_after_play_tetris" ---
    fix_after_play_Tetris = visual.TextStim(win=win, name='fix_after_play_Tetris',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "show_next_control" ---
    Icon_for_next_cond = visual.ImageStim(
        win=win,
        name='Icon_for_next_cond', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=1.0,
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "wait_1s" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "random_control_condition" ---
    press_shape = visual.ShapeStim(
        win=win, name='press_shape', vertices='cross',
        size=(0.075, 0.075),
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=1.0, depth=-1.0, interpolate=True)
    duration_and_fix = visual.TextStim(win=win, name='duration_and_fix',
        text='',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_button = visual.ImageStim(
        win=win,
        name='press_button', 
        image='Images/button.png', mask=None, anchor='center',
        ori=0.0, pos=(0, -0.02), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=1.0,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-3.0)
    
    # --- Initialize components for Routine "condition_ended" ---
    condition_ended_text = visual.TextStim(win=win, name='condition_ended_text',
        text=Inst.font_condition_ended,
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "wait_ISI_after_control" ---
    fix_after_control = visual.TextStim(win=win, name='fix_after_control',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "wait_10sec_for_Trigger" ---
    wait_10sec_for_trigger_text = visual.TextStim(win=win, name='wait_10sec_for_trigger_text',
        text='',
        font='Open Sans',
        pos=(0, 0.05), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "End" ---
    end_text = visual.TextStim(win=win, name='end_text',
        text=Inst.font_end,
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Stop_eyetracker = hardware.eyetracker.EyetrackerControl(
        tracker=eyetracker,
        actionType='Stop Only'
    )
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "load_processes" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from create_processes
    # creates a seperate process for the Pretrial rounds so that the experiment can continue but only if there are pretrial rounds set
    if skip_if_enabled("pretrial") == True:    
        pretrial_Tetris = Process(target=Tetris_Instance, args=(
                                  "pretrial_Tetris",
                                  False,
                                  True,
                                  game.toggle_pretrial,
                                  game.game_over_counter,
                                  game.score,
                                  game.level,
                                  game.speed,
                                  game.level_for_main,
                                  game.three_next_blocks,
                                  game.regression.x_array,
                                  game.regression.y_array,
                                  game.regression.weights,
                                  Flip_horizontally,
                                  Flip_vertically,
                                  Pygame_key_1,
                                  Pygame_key_2,
                                  Pygame_key_3,
                                  Pygame_key_4,
                                  ))
        pretrial_Tetris.start()
    
    #creates a seperate process for the Game so that the experiment can continue
    if skip_if_enabled("main_trials") == True:
        play_Tetris = Process(target=Tetris_Instance, args=(
                              "play_Tetris",
                              False,
                              False,
                              game.toggle_play,
                              game.game_over_counter,
                              game.score,
                              game.level,
                              game.speed,
                              game.level_for_main,
                              game.three_next_blocks,
                              game.regression.x_array,
                              game.regression.y_array,
                              game.regression.weights,
                              Flip_horizontally,
                              Flip_vertically,
                              Pygame_key_1,
                              Pygame_key_2,
                              Pygame_key_3,
                              Pygame_key_4,
                              ))
        play_Tetris.start()
    # create a window for the controll visual_control condition
        watch_Tetris = Process(target=Tetris_Instance, args=(
                               "watch_Tetris",
                               True,
                               False,
                               game.toggle_watch,
                               game.game_over_counter,
                               game.score,
                               game.level,
                               game.speed,
                               game.level_for_main,
                               game.three_next_blocks,
                               game.regression.x_array,
                               game.regression.y_array,
                               game.regression.weights,
                               Flip_horizontally,
                               Flip_vertically,
                               Pygame_key_1,
                               Pygame_key_2,
                               Pygame_key_3,
                               Pygame_key_4,
                               ))
        watch_Tetris.start()
    
    # start keyboard listener
    log_trigger = pynput_keyboard.Listener(on_press=check_for_trigger)
    log_trigger.start()
    
    
    # hides cursor that appears automatically after processes are created
    ctypes.windll.user32.ShowCursor(False)
    # keep track of which components have finished
    load_processesComponents = [load_processes_text]
    for thisComponent in load_processesComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "load_processes" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from create_processes
        # ensures that this condition starts properly
        if is_window_open("pretrial_Tetris") == True:
            continueRoutine = skip_if_enabled("main_trials")
        
        # *load_processes_text* updates
        
        # if load_processes_text is starting this frame...
        if load_processes_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            load_processes_text.frameNStart = frameN  # exact frame index
            load_processes_text.tStart = t  # local t and not account for scr refresh
            load_processes_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(load_processes_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            load_processes_text.status = STARTED
            load_processes_text.setAutoDraw(True)
        
        # if load_processes_text is active this frame...
        if load_processes_text.status == STARTED:
            # update params
            pass
        
        # if load_processes_text is stopping this frame...
        if load_processes_text.status == STARTED:
            if bool(is_window_open("watch_Tetris") == True):
                # keep track of stop time/frame for later
                load_processes_text.tStop = t  # not accounting for scr refresh
                load_processes_text.tStopRefresh = tThisFlipGlobal  # on global time
                load_processes_text.frameNStop = frameN  # exact frame index
                # update status
                load_processes_text.status = FINISHED
                load_processes_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in load_processesComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "load_processes" ---
    for thisComponent in load_processesComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from create_processes
    Get_on_top("PsychoPy")
    print('\n'.join([
        "--------------------",
        "Processes:",
        f"pretrial_Tetris loaded and paused (state: {game.toggle_pretrial.value})",
        f"play_Tetris loaded and paused (state: {game.toggle_play.value})",
        f"watch_Tetris loaded and paused (state: {game.toggle_watch.value})",
        "--------------------",
        ""
    ]))
    thisExp.nextEntry()
    # the Routine "load_processes" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "check_for_processes" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_get_on_top
    # gets PsychoPy on top initiall
    Get_on_top("PsychoPy")
    # keep track of which components have finished
    check_for_processesComponents = [check_Text]
    for thisComponent in check_for_processesComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "check_for_processes" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *check_Text* updates
        
        # if check_Text is starting this frame...
        if check_Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            check_Text.frameNStart = frameN  # exact frame index
            check_Text.tStart = t  # local t and not account for scr refresh
            check_Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(check_Text, 'tStartRefresh')  # time at next scr refresh
            # update status
            check_Text.status = STARTED
            check_Text.setAutoDraw(True)
        
        # if check_Text is active this frame...
        if check_Text.status == STARTED:
            # update params
            pass
        
        # if check_Text is stopping this frame...
        if check_Text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > check_Text.tStartRefresh + 3-frameTolerance:
                # keep track of stop time/frame for later
                check_Text.tStop = t  # not accounting for scr refresh
                check_Text.tStopRefresh = tThisFlipGlobal  # on global time
                check_Text.frameNStop = frameN  # exact frame index
                # update status
                check_Text.status = FINISHED
                check_Text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in check_for_processesComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "check_for_processes" ---
    for thisComponent in check_for_processesComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "show_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    show_pretrialComponents = [check_pretrial]
    for thisComponent in show_pretrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "show_pretrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_show_pretrial
        # skips this routine if there are no pretrial rounds set
        continueRoutine = skip_if_enabled("pretrial")
        
        # *check_pretrial* updates
        
        # if check_pretrial is starting this frame...
        if check_pretrial.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            check_pretrial.frameNStart = frameN  # exact frame index
            check_pretrial.tStart = t  # local t and not account for scr refresh
            check_pretrial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(check_pretrial, 'tStartRefresh')  # time at next scr refresh
            # update status
            check_pretrial.status = STARTED
            check_pretrial.setAutoDraw(True)
        
        # if check_pretrial is active this frame...
        if check_pretrial.status == STARTED:
            # update params
            pass
        
        # if check_pretrial is stopping this frame...
        if check_pretrial.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > check_pretrial.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                check_pretrial.tStop = t  # not accounting for scr refresh
                check_pretrial.tStopRefresh = tThisFlipGlobal  # on global time
                check_pretrial.frameNStop = frameN  # exact frame index
                # update status
                check_pretrial.status = FINISHED
                check_pretrial.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in show_pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "show_pretrial" ---
    for thisComponent in show_pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "check_for_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_show_and_hide_pretrial
    # skips this routine if there no pretrial rounds set
    if game.pretrial_rounds != None:
        Get_on_top("pretrial_Tetris")
    
    # keep track of which components have finished
    check_for_pretrialComponents = [duration_and_fix_play_pretrial]
    for thisComponent in check_for_pretrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "check_for_pretrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_show_and_hide_pretrial
        continueRoutine = skip_if_enabled("pretrial")
        
        # *duration_and_fix_play_pretrial* updates
        
        # if duration_and_fix_play_pretrial is starting this frame...
        if duration_and_fix_play_pretrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            duration_and_fix_play_pretrial.frameNStart = frameN  # exact frame index
            duration_and_fix_play_pretrial.tStart = t  # local t and not account for scr refresh
            duration_and_fix_play_pretrial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(duration_and_fix_play_pretrial, 'tStartRefresh')  # time at next scr refresh
            # update status
            duration_and_fix_play_pretrial.status = STARTED
            duration_and_fix_play_pretrial.setAutoDraw(True)
        
        # if duration_and_fix_play_pretrial is active this frame...
        if duration_and_fix_play_pretrial.status == STARTED:
            # update params
            pass
        
        # if duration_and_fix_play_pretrial is stopping this frame...
        if duration_and_fix_play_pretrial.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > duration_and_fix_play_pretrial.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                duration_and_fix_play_pretrial.tStop = t  # not accounting for scr refresh
                duration_and_fix_play_pretrial.tStopRefresh = tThisFlipGlobal  # on global time
                duration_and_fix_play_pretrial.frameNStop = frameN  # exact frame index
                # update status
                duration_and_fix_play_pretrial.status = FINISHED
                duration_and_fix_play_pretrial.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in check_for_pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "check_for_pretrial" ---
    for thisComponent in check_for_pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_show_and_hide_pretrial
    Get_on_top("PsychoPy")
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.500000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "show_play" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    show_playComponents = [check_play]
    for thisComponent in show_playComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "show_play" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_check_play
        # skipped if main part should be skipped according to setting in "config_paradigm_psychopy"
        continueRoutine = skip_if_enabled("main_trials")
        
        # *check_play* updates
        
        # if check_play is starting this frame...
        if check_play.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            check_play.frameNStart = frameN  # exact frame index
            check_play.tStart = t  # local t and not account for scr refresh
            check_play.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(check_play, 'tStartRefresh')  # time at next scr refresh
            # update status
            check_play.status = STARTED
            check_play.setAutoDraw(True)
        
        # if check_play is active this frame...
        if check_play.status == STARTED:
            # update params
            pass
        
        # if check_play is stopping this frame...
        if check_play.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > check_play.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                check_play.tStop = t  # not accounting for scr refresh
                check_play.tStopRefresh = tThisFlipGlobal  # on global time
                check_play.frameNStop = frameN  # exact frame index
                # update status
                check_play.status = FINISHED
                check_play.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in show_playComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "show_play" ---
    for thisComponent in show_playComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "check_window_play" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_play
    if skip_if_enabled("main_trials") == True:
        # set Tetris to foreground
        Get_on_top("play_Tetris")
    
    
    # keep track of which components have finished
    check_window_playComponents = [duration_and_fix_play]
    for thisComponent in check_window_playComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "check_window_play" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_play
        continueRoutine = skip_if_enabled("main_trials")
        
        # *duration_and_fix_play* updates
        
        # if duration_and_fix_play is starting this frame...
        if duration_and_fix_play.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            duration_and_fix_play.frameNStart = frameN  # exact frame index
            duration_and_fix_play.tStart = t  # local t and not account for scr refresh
            duration_and_fix_play.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(duration_and_fix_play, 'tStartRefresh')  # time at next scr refresh
            # update status
            duration_and_fix_play.status = STARTED
            duration_and_fix_play.setAutoDraw(True)
        
        # if duration_and_fix_play is active this frame...
        if duration_and_fix_play.status == STARTED:
            # update params
            pass
        
        # if duration_and_fix_play is stopping this frame...
        if duration_and_fix_play.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > duration_and_fix_play.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                duration_and_fix_play.tStop = t  # not accounting for scr refresh
                duration_and_fix_play.tStopRefresh = tThisFlipGlobal  # on global time
                duration_and_fix_play.frameNStop = frameN  # exact frame index
                # update status
                duration_and_fix_play.status = FINISHED
                duration_and_fix_play.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in check_window_playComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "check_window_play" ---
    for thisComponent in check_window_playComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_play
    Get_on_top("PsychoPy")
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.500000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "show_watch" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    show_watchComponents = [check_watch]
    for thisComponent in show_watchComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "show_watch" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_show_watch
        continueRoutine = skip_if_enabled("main_trials")
        
        # *check_watch* updates
        
        # if check_watch is starting this frame...
        if check_watch.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            check_watch.frameNStart = frameN  # exact frame index
            check_watch.tStart = t  # local t and not account for scr refresh
            check_watch.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(check_watch, 'tStartRefresh')  # time at next scr refresh
            # update status
            check_watch.status = STARTED
            check_watch.setAutoDraw(True)
        
        # if check_watch is active this frame...
        if check_watch.status == STARTED:
            # update params
            pass
        
        # if check_watch is stopping this frame...
        if check_watch.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > check_watch.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                check_watch.tStop = t  # not accounting for scr refresh
                check_watch.tStopRefresh = tThisFlipGlobal  # on global time
                check_watch.frameNStop = frameN  # exact frame index
                # update status
                check_watch.status = FINISHED
                check_watch.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in show_watchComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "show_watch" ---
    for thisComponent in show_watchComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "check_window_watch" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_watch
    #set Tetris to foreground
    Get_on_top("watch_Tetris")
    # keep track of which components have finished
    check_window_watchComponents = [duration_and_fix_watch]
    for thisComponent in check_window_watchComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "check_window_watch" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_watch
        continueRoutine = skip_if_enabled("main_trials")
        
        # *duration_and_fix_watch* updates
        
        # if duration_and_fix_watch is starting this frame...
        if duration_and_fix_watch.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            duration_and_fix_watch.frameNStart = frameN  # exact frame index
            duration_and_fix_watch.tStart = t  # local t and not account for scr refresh
            duration_and_fix_watch.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(duration_and_fix_watch, 'tStartRefresh')  # time at next scr refresh
            # update status
            duration_and_fix_watch.status = STARTED
            duration_and_fix_watch.setAutoDraw(True)
        
        # if duration_and_fix_watch is active this frame...
        if duration_and_fix_watch.status == STARTED:
            # update params
            pass
        
        # if duration_and_fix_watch is stopping this frame...
        if duration_and_fix_watch.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > duration_and_fix_watch.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                duration_and_fix_watch.tStop = t  # not accounting for scr refresh
                duration_and_fix_watch.tStopRefresh = tThisFlipGlobal  # on global time
                duration_and_fix_watch.frameNStop = frameN  # exact frame index
                # update status
                duration_and_fix_watch.status = FINISHED
                duration_and_fix_watch.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in check_window_watchComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "check_window_watch" ---
    for thisComponent in check_window_watchComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_watch
    Get_on_top("PsychoPy")
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.500000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "wait_1s" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_1sComponents = [fix]
    for thisComponent in wait_1sComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_1s" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix* updates
        
        # if fix is starting this frame...
        if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix.frameNStart = frameN  # exact frame index
            fix.tStart = t  # local t and not account for scr refresh
            fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
            # update status
            fix.status = STARTED
            fix.setAutoDraw(True)
        
        # if fix is active this frame...
        if fix.status == STARTED:
            # update params
            pass
        
        # if fix is stopping this frame...
        if fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                fix.tStop = t  # not accounting for scr refresh
                fix.tStopRefresh = tThisFlipGlobal  # on global time
                fix.frameNStop = frameN  # exact frame index
                # update status
                fix.status = FINISHED
                fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_1sComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_1s" ---
    for thisComponent in wait_1sComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "check_response_box" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_check_response
    create_dummi_screen_responsecheck()
    
    # variables for responsebox check that are displayed on screen
    x_1 = "-"
    x_2 = "-"
    x_3 = "-"
    x_4 = "-"
    x_5 = "-"
    x_1_1 =  "-"
    x_2_2 =  "-"
    x_3_3 =  "-"
    x_4_4 =  "-"
    x_5_5 =  "-"
    all_checked = False
    key_resp_return_response.keys = []
    key_resp_return_response.rt = []
    _key_resp_return_response_allKeys = []
    # keep track of which components have finished
    check_response_boxComponents = [text_check_response, text_check_response_2, text_1, text_2, text_3, text_4, text_5, key_resp_return_response]
    for thisComponent in check_response_boxComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "check_response_box" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_check_response
        continueRoutine = skip_if_enabled("main_trials")
        
        # checks keys and updated variables accordingly
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == Pygame_key_1:
                    if x_1 == '-':
                        x_1 = '1'
                    elif x_1 == '1':
                        x_1_1 = '1'
                if event.key == Pygame_key_2:
                    if x_2 == '-':
                        x_2 = '2'
                    elif x_2 == '2':
                        x_2_2 = '2'
                if event.key == Pygame_key_3:
                    if x_3 == '-':
                        x_3 = '3'
                    elif x_3 == '3':
                        x_3_3 = '3'
                if event.key == Pygame_key_4:
                    if x_4 == '-':
                        x_4 = '4'
                    elif x_4 == '4':
                        x_4_4 = '4'
                if event.key == Pygame_key_5:
                    if x_5 == '-':
                        x_5 = '5'
                    elif x_5 == '5':
                        x_5_5 = '5'
        if x_1_1 == "1" and x_2_2 == "2" and x_3_3 == "3" and x_4_4 == "4" and x_5_5 == "5":
            all_checked = True    
        
        # *text_check_response* updates
        
        # if text_check_response is starting this frame...
        if text_check_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_check_response.frameNStart = frameN  # exact frame index
            text_check_response.tStart = t  # local t and not account for scr refresh
            text_check_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_check_response, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_check_response.status = STARTED
            text_check_response.setAutoDraw(True)
        
        # if text_check_response is active this frame...
        if text_check_response.status == STARTED:
            # update params
            pass
        
        # *text_check_response_2* updates
        
        # if text_check_response_2 is starting this frame...
        if text_check_response_2.status == NOT_STARTED and all_checked == True:
            # keep track of start time/frame for later
            text_check_response_2.frameNStart = frameN  # exact frame index
            text_check_response_2.tStart = t  # local t and not account for scr refresh
            text_check_response_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_check_response_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_check_response_2.status = STARTED
            text_check_response_2.setAutoDraw(True)
        
        # if text_check_response_2 is active this frame...
        if text_check_response_2.status == STARTED:
            # update params
            pass
        
        # *text_1* updates
        
        # if text_1 is starting this frame...
        if text_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_1.frameNStart = frameN  # exact frame index
            text_1.tStart = t  # local t and not account for scr refresh
            text_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_1.status = STARTED
            text_1.setAutoDraw(True)
        
        # if text_1 is active this frame...
        if text_1.status == STARTED:
            # update params
            text_1.setText(f'{x_1}\n{x_1_1}', log=False)
        
        # *text_2* updates
        
        # if text_2 is starting this frame...
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_2.status = STARTED
            text_2.setAutoDraw(True)
        
        # if text_2 is active this frame...
        if text_2.status == STARTED:
            # update params
            text_2.setText(f'{x_2}\n{x_2_2}', log=False)
        
        # *text_3* updates
        
        # if text_3 is starting this frame...
        if text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_3.frameNStart = frameN  # exact frame index
            text_3.tStart = t  # local t and not account for scr refresh
            text_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_3.status = STARTED
            text_3.setAutoDraw(True)
        
        # if text_3 is active this frame...
        if text_3.status == STARTED:
            # update params
            text_3.setText(f'{x_3}\n{x_3_3}', log=False)
        
        # *text_4* updates
        
        # if text_4 is starting this frame...
        if text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_4.frameNStart = frameN  # exact frame index
            text_4.tStart = t  # local t and not account for scr refresh
            text_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_4, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_4.status = STARTED
            text_4.setAutoDraw(True)
        
        # if text_4 is active this frame...
        if text_4.status == STARTED:
            # update params
            text_4.setText(f'{x_4}\n{x_4_4}', log=False)
        
        # *text_5* updates
        
        # if text_5 is starting this frame...
        if text_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_5.frameNStart = frameN  # exact frame index
            text_5.tStart = t  # local t and not account for scr refresh
            text_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_5, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_5.status = STARTED
            text_5.setAutoDraw(True)
        
        # if text_5 is active this frame...
        if text_5.status == STARTED:
            # update params
            text_5.setText(f'{x_5}\n{x_5_5}', log=False)
        
        # *key_resp_return_response* updates
        waitOnFlip = False
        
        # if key_resp_return_response is starting this frame...
        if key_resp_return_response.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_return_response.frameNStart = frameN  # exact frame index
            key_resp_return_response.tStart = t  # local t and not account for scr refresh
            key_resp_return_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_return_response, 'tStartRefresh')  # time at next scr refresh
            # update status
            key_resp_return_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_return_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_return_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_return_response.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_return_response.getKeys(keyList=['return'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_return_response_allKeys.extend(theseKeys)
            if len(_key_resp_return_response_allKeys):
                key_resp_return_response.keys = _key_resp_return_response_allKeys[-1].name  # just the last key pressed
                key_resp_return_response.rt = _key_resp_return_response_allKeys[-1].rt
                key_resp_return_response.duration = _key_resp_return_response_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in check_response_boxComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "check_response_box" ---
    for thisComponent in check_response_boxComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_check_response
    # ends pygame instance
    pygame.quit()
    
    thisExp.nextEntry()
    # the Routine "check_response_box" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "pretrial_intro" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_1.keys = []
    press_continue_1.rt = []
    _press_continue_1_allKeys = []
    # keep track of which components have finished
    pretrial_introComponents = [Intro_2, Text_continue_1, press_continue_1]
    for thisComponent in pretrial_introComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "pretrial_intro" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Intro_2* updates
        
        # if Intro_2 is starting this frame...
        if Intro_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Intro_2.frameNStart = frameN  # exact frame index
            Intro_2.tStart = t  # local t and not account for scr refresh
            Intro_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Intro_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            Intro_2.status = STARTED
            Intro_2.setAutoDraw(True)
        
        # if Intro_2 is active this frame...
        if Intro_2.status == STARTED:
            # update params
            pass
        
        # *Text_continue_1* updates
        
        # if Text_continue_1 is starting this frame...
        if Text_continue_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_1.frameNStart = frameN  # exact frame index
            Text_continue_1.tStart = t  # local t and not account for scr refresh
            Text_continue_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_1.status = STARTED
            Text_continue_1.setAutoDraw(True)
        
        # if Text_continue_1 is active this frame...
        if Text_continue_1.status == STARTED:
            # update params
            pass
        
        # *press_continue_1* updates
        waitOnFlip = False
        
        # if press_continue_1 is starting this frame...
        if press_continue_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_1.frameNStart = frameN  # exact frame index
            press_continue_1.tStart = t  # local t and not account for scr refresh
            press_continue_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_1.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_1.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_1.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_1.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_1_allKeys.extend(theseKeys)
            if len(_press_continue_1_allKeys):
                press_continue_1.keys = _press_continue_1_allKeys[-1].name  # just the last key pressed
                press_continue_1.rt = _press_continue_1_allKeys[-1].rt
                press_continue_1.duration = _press_continue_1_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pretrial_introComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "pretrial_intro" ---
    for thisComponent in pretrial_introComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "pretrial_intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_2.keys = []
    press_continue_2.rt = []
    _press_continue_2_allKeys = []
    # keep track of which components have finished
    explain_pretrialComponents = [explanation_pretrial, Text_continue_2, press_continue_2]
    for thisComponent in explain_pretrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_pretrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_pretrial
        # skips this routine if there are no pretrial rounds set or there are no main trials
        continueRoutine = skip_if_enabled("pretrial") and skip_if_enabled("main_trials") or Include_explanations
        
        # *explanation_pretrial* updates
        
        # if explanation_pretrial is starting this frame...
        if explanation_pretrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            explanation_pretrial.frameNStart = frameN  # exact frame index
            explanation_pretrial.tStart = t  # local t and not account for scr refresh
            explanation_pretrial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(explanation_pretrial, 'tStartRefresh')  # time at next scr refresh
            # update status
            explanation_pretrial.status = STARTED
            explanation_pretrial.setAutoDraw(True)
        
        # if explanation_pretrial is active this frame...
        if explanation_pretrial.status == STARTED:
            # update params
            pass
        
        # *Text_continue_2* updates
        
        # if Text_continue_2 is starting this frame...
        if Text_continue_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_2.frameNStart = frameN  # exact frame index
            Text_continue_2.tStart = t  # local t and not account for scr refresh
            Text_continue_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_2.status = STARTED
            Text_continue_2.setAutoDraw(True)
        
        # if Text_continue_2 is active this frame...
        if Text_continue_2.status == STARTED:
            # update params
            pass
        
        # *press_continue_2* updates
        waitOnFlip = False
        
        # if press_continue_2 is starting this frame...
        if press_continue_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_2.frameNStart = frameN  # exact frame index
            press_continue_2.tStart = t  # local t and not account for scr refresh
            press_continue_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_2.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_2.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_2_allKeys.extend(theseKeys)
            if len(_press_continue_2_allKeys):
                press_continue_2.keys = _press_continue_2_allKeys[-1].name  # just the last key pressed
                press_continue_2.rt = _press_continue_2_allKeys[-1].rt
                press_continue_2.duration = _press_continue_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_pretrial" ---
    for thisComponent in explain_pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_pretrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "intro_how_to_play" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_2_1.keys = []
    press_continue_2_1.rt = []
    _press_continue_2_1_allKeys = []
    # keep track of which components have finished
    intro_how_to_playComponents = [text_how_to_play, Text_continue_2_1, press_continue_2_1]
    for thisComponent in intro_how_to_playComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "intro_how_to_play" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_how_to_play* updates
        
        # if text_how_to_play is starting this frame...
        if text_how_to_play.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            text_how_to_play.frameNStart = frameN  # exact frame index
            text_how_to_play.tStart = t  # local t and not account for scr refresh
            text_how_to_play.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_how_to_play, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_how_to_play.status = STARTED
            text_how_to_play.setAutoDraw(True)
        
        # if text_how_to_play is active this frame...
        if text_how_to_play.status == STARTED:
            # update params
            pass
        
        # *Text_continue_2_1* updates
        
        # if Text_continue_2_1 is starting this frame...
        if Text_continue_2_1.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            Text_continue_2_1.frameNStart = frameN  # exact frame index
            Text_continue_2_1.tStart = t  # local t and not account for scr refresh
            Text_continue_2_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_2_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_2_1.status = STARTED
            Text_continue_2_1.setAutoDraw(True)
        
        # if Text_continue_2_1 is active this frame...
        if Text_continue_2_1.status == STARTED:
            # update params
            pass
        
        # *press_continue_2_1* updates
        waitOnFlip = False
        
        # if press_continue_2_1 is starting this frame...
        if press_continue_2_1.status == NOT_STARTED and include_explanations:
            # keep track of start time/frame for later
            press_continue_2_1.frameNStart = frameN  # exact frame index
            press_continue_2_1.tStart = t  # local t and not account for scr refresh
            press_continue_2_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_2_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_2_1.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_2_1.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_2_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_2_1.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_2_1.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_2_1_allKeys.extend(theseKeys)
            if len(_press_continue_2_1_allKeys):
                press_continue_2_1.keys = _press_continue_2_1_allKeys[-1].name  # just the last key pressed
                press_continue_2_1.rt = _press_continue_2_1_allKeys[-1].rt
                press_continue_2_1.duration = _press_continue_2_1_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in intro_how_to_playComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "intro_how_to_play" ---
    for thisComponent in intro_how_to_playComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "intro_how_to_play" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_tetris_1" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_3.keys = []
    press_continue_3.rt = []
    _press_continue_3_allKeys = []
    # keep track of which components have finished
    explain_tetris_1Components = [explain_game_mechanics_1, Text_continue_3, press_continue_3]
    for thisComponent in explain_tetris_1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_tetris_1" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *explain_game_mechanics_1* updates
        
        # if explain_game_mechanics_1 is starting this frame...
        if explain_game_mechanics_1.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            explain_game_mechanics_1.frameNStart = frameN  # exact frame index
            explain_game_mechanics_1.tStart = t  # local t and not account for scr refresh
            explain_game_mechanics_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(explain_game_mechanics_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            explain_game_mechanics_1.status = STARTED
            explain_game_mechanics_1.setAutoDraw(True)
        
        # if explain_game_mechanics_1 is active this frame...
        if explain_game_mechanics_1.status == STARTED:
            # update params
            pass
        
        # *Text_continue_3* updates
        
        # if Text_continue_3 is starting this frame...
        if Text_continue_3.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            Text_continue_3.frameNStart = frameN  # exact frame index
            Text_continue_3.tStart = t  # local t and not account for scr refresh
            Text_continue_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_3.status = STARTED
            Text_continue_3.setAutoDraw(True)
        
        # if Text_continue_3 is active this frame...
        if Text_continue_3.status == STARTED:
            # update params
            pass
        
        # *press_continue_3* updates
        waitOnFlip = False
        
        # if press_continue_3 is starting this frame...
        if press_continue_3.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            press_continue_3.frameNStart = frameN  # exact frame index
            press_continue_3.tStart = t  # local t and not account for scr refresh
            press_continue_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_3.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_3.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_3_allKeys.extend(theseKeys)
            if len(_press_continue_3_allKeys):
                press_continue_3.keys = _press_continue_3_allKeys[-1].name  # just the last key pressed
                press_continue_3.rt = _press_continue_3_allKeys[-1].rt
                press_continue_3.duration = _press_continue_3_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_tetris_1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_tetris_1" ---
    for thisComponent in explain_tetris_1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_tetris_1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_tetris_2" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_3_1.keys = []
    press_continue_3_1.rt = []
    _press_continue_3_1_allKeys = []
    # keep track of which components have finished
    explain_tetris_2Components = [explain_game_mechanics_2, Text_continue_3_1, press_continue_3_1]
    for thisComponent in explain_tetris_2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_tetris_2" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *explain_game_mechanics_2* updates
        
        # if explain_game_mechanics_2 is starting this frame...
        if explain_game_mechanics_2.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            explain_game_mechanics_2.frameNStart = frameN  # exact frame index
            explain_game_mechanics_2.tStart = t  # local t and not account for scr refresh
            explain_game_mechanics_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(explain_game_mechanics_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            explain_game_mechanics_2.status = STARTED
            explain_game_mechanics_2.setAutoDraw(True)
        
        # if explain_game_mechanics_2 is active this frame...
        if explain_game_mechanics_2.status == STARTED:
            # update params
            pass
        
        # *Text_continue_3_1* updates
        
        # if Text_continue_3_1 is starting this frame...
        if Text_continue_3_1.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            Text_continue_3_1.frameNStart = frameN  # exact frame index
            Text_continue_3_1.tStart = t  # local t and not account for scr refresh
            Text_continue_3_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_3_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_3_1.status = STARTED
            Text_continue_3_1.setAutoDraw(True)
        
        # if Text_continue_3_1 is active this frame...
        if Text_continue_3_1.status == STARTED:
            # update params
            pass
        
        # *press_continue_3_1* updates
        waitOnFlip = False
        
        # if press_continue_3_1 is starting this frame...
        if press_continue_3_1.status == NOT_STARTED and Include_explanations:
            # keep track of start time/frame for later
            press_continue_3_1.frameNStart = frameN  # exact frame index
            press_continue_3_1.tStart = t  # local t and not account for scr refresh
            press_continue_3_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_3_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_3_1.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_3_1.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_3_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_3_1.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_3_1.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_3_1_allKeys.extend(theseKeys)
            if len(_press_continue_3_1_allKeys):
                press_continue_3_1.keys = _press_continue_3_1_allKeys[-1].name  # just the last key pressed
                press_continue_3_1.rt = _press_continue_3_1_allKeys[-1].rt
                press_continue_3_1.duration = _press_continue_3_1_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_tetris_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_tetris_2" ---
    for thisComponent in explain_tetris_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_tetris_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_tetris_3" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_3_3.keys = []
    press_continue_3_3.rt = []
    _press_continue_3_3_allKeys = []
    # keep track of which components have finished
    explain_tetris_3Components = [explain_game_mechanics_3, Text_continue_3_3, press_continue_3_3]
    for thisComponent in explain_tetris_3Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_tetris_3" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *explain_game_mechanics_3* updates
        
        # if explain_game_mechanics_3 is starting this frame...
        if explain_game_mechanics_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            explain_game_mechanics_3.frameNStart = frameN  # exact frame index
            explain_game_mechanics_3.tStart = t  # local t and not account for scr refresh
            explain_game_mechanics_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(explain_game_mechanics_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            explain_game_mechanics_3.status = STARTED
            explain_game_mechanics_3.setAutoDraw(True)
        
        # if explain_game_mechanics_3 is active this frame...
        if explain_game_mechanics_3.status == STARTED:
            # update params
            pass
        
        # *Text_continue_3_3* updates
        
        # if Text_continue_3_3 is starting this frame...
        if Text_continue_3_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_3_3.frameNStart = frameN  # exact frame index
            Text_continue_3_3.tStart = t  # local t and not account for scr refresh
            Text_continue_3_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_3_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_3_3.status = STARTED
            Text_continue_3_3.setAutoDraw(True)
        
        # if Text_continue_3_3 is active this frame...
        if Text_continue_3_3.status == STARTED:
            # update params
            pass
        
        # *press_continue_3_3* updates
        waitOnFlip = False
        
        # if press_continue_3_3 is starting this frame...
        if press_continue_3_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_3_3.frameNStart = frameN  # exact frame index
            press_continue_3_3.tStart = t  # local t and not account for scr refresh
            press_continue_3_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_3_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_3_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_3_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_3_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_3_3.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_3_3.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_3_3_allKeys.extend(theseKeys)
            if len(_press_continue_3_3_allKeys):
                press_continue_3_3.keys = _press_continue_3_3_allKeys[-1].name  # just the last key pressed
                press_continue_3_3.rt = _press_continue_3_3_allKeys[-1].rt
                press_continue_3_3.duration = _press_continue_3_3_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_tetris_3Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_tetris_3" ---
    for thisComponent in explain_tetris_3Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_tetris_3" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_staircase" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_3_4.keys = []
    press_continue_3_4.rt = []
    _press_continue_3_4_allKeys = []
    # keep track of which components have finished
    explain_staircaseComponents = [text_explain_staircase, Text_continue_3_4, press_continue_3_4]
    for thisComponent in explain_staircaseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_staircase" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_staircase
        # skips this routine if there are no pretrial rounds set or the staircase method is not enabled
        continueRoutine = skip_if_enabled("pretrial") and game.pretrial_staircase
        
        
        # *text_explain_staircase* updates
        
        # if text_explain_staircase is starting this frame...
        if text_explain_staircase.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_explain_staircase.frameNStart = frameN  # exact frame index
            text_explain_staircase.tStart = t  # local t and not account for scr refresh
            text_explain_staircase.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_explain_staircase, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_explain_staircase.status = STARTED
            text_explain_staircase.setAutoDraw(True)
        
        # if text_explain_staircase is active this frame...
        if text_explain_staircase.status == STARTED:
            # update params
            pass
        
        # *Text_continue_3_4* updates
        
        # if Text_continue_3_4 is starting this frame...
        if Text_continue_3_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_3_4.frameNStart = frameN  # exact frame index
            Text_continue_3_4.tStart = t  # local t and not account for scr refresh
            Text_continue_3_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_3_4, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_3_4.status = STARTED
            Text_continue_3_4.setAutoDraw(True)
        
        # if Text_continue_3_4 is active this frame...
        if Text_continue_3_4.status == STARTED:
            # update params
            pass
        
        # *press_continue_3_4* updates
        waitOnFlip = False
        
        # if press_continue_3_4 is starting this frame...
        if press_continue_3_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_3_4.frameNStart = frameN  # exact frame index
            press_continue_3_4.tStart = t  # local t and not account for scr refresh
            press_continue_3_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_3_4, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_3_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_3_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_3_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_3_4.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_3_4.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_3_4_allKeys.extend(theseKeys)
            if len(_press_continue_3_4_allKeys):
                press_continue_3_4.keys = _press_continue_3_4_allKeys[-1].name  # just the last key pressed
                press_continue_3_4.rt = _press_continue_3_4_allKeys[-1].rt
                press_continue_3_4.duration = _press_continue_3_4_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_staircaseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_staircase" ---
    for thisComponent in explain_staircaseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_staircase" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_tetris_4" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_4.keys = []
    press_continue_4.rt = []
    _press_continue_4_allKeys = []
    # keep track of which components have finished
    explain_tetris_4Components = [explain_controls, Controls, Text_continue_4, press_continue_4]
    for thisComponent in explain_tetris_4Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_tetris_4" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *explain_controls* updates
        
        # if explain_controls is starting this frame...
        if explain_controls.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            explain_controls.frameNStart = frameN  # exact frame index
            explain_controls.tStart = t  # local t and not account for scr refresh
            explain_controls.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(explain_controls, 'tStartRefresh')  # time at next scr refresh
            # update status
            explain_controls.status = STARTED
            explain_controls.setAutoDraw(True)
        
        # if explain_controls is active this frame...
        if explain_controls.status == STARTED:
            # update params
            pass
        
        # *Controls* updates
        
        # if Controls is starting this frame...
        if Controls.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Controls.frameNStart = frameN  # exact frame index
            Controls.tStart = t  # local t and not account for scr refresh
            Controls.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Controls, 'tStartRefresh')  # time at next scr refresh
            # update status
            Controls.status = STARTED
            Controls.setAutoDraw(True)
        
        # if Controls is active this frame...
        if Controls.status == STARTED:
            # update params
            pass
        
        # *Text_continue_4* updates
        
        # if Text_continue_4 is starting this frame...
        if Text_continue_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_4.frameNStart = frameN  # exact frame index
            Text_continue_4.tStart = t  # local t and not account for scr refresh
            Text_continue_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_4, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_4.status = STARTED
            Text_continue_4.setAutoDraw(True)
        
        # if Text_continue_4 is active this frame...
        if Text_continue_4.status == STARTED:
            # update params
            pass
        
        # *press_continue_4* updates
        waitOnFlip = False
        
        # if press_continue_4 is starting this frame...
        if press_continue_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_4.frameNStart = frameN  # exact frame index
            press_continue_4.tStart = t  # local t and not account for scr refresh
            press_continue_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_4, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_4.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_4.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_4_allKeys.extend(theseKeys)
            if len(_press_continue_4_allKeys):
                press_continue_4.keys = _press_continue_4_allKeys[-1].name  # just the last key pressed
                press_continue_4.rt = _press_continue_4_allKeys[-1].rt
                press_continue_4.duration = _press_continue_4_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_tetris_4Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_tetris_4" ---
    for thisComponent in explain_tetris_4Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_tetris_4" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "start_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_4_1.keys = []
    press_continue_4_1.rt = []
    _press_continue_4_1_allKeys = []
    # keep track of which components have finished
    start_pretrialComponents = [text_start_pretrial, press_continue_4_1]
    for thisComponent in start_pretrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "start_pretrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_start_pretrial
        # skips this routine if there are no pretrial rounds set
        continueRoutine = skip_if_enabled("pretrial")
        
        # *text_start_pretrial* updates
        
        # if text_start_pretrial is starting this frame...
        if text_start_pretrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_start_pretrial.frameNStart = frameN  # exact frame index
            text_start_pretrial.tStart = t  # local t and not account for scr refresh
            text_start_pretrial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_start_pretrial, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_start_pretrial.status = STARTED
            text_start_pretrial.setAutoDraw(True)
        
        # if text_start_pretrial is active this frame...
        if text_start_pretrial.status == STARTED:
            # update params
            pass
        
        # *press_continue_4_1* updates
        waitOnFlip = False
        
        # if press_continue_4_1 is starting this frame...
        if press_continue_4_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_4_1.frameNStart = frameN  # exact frame index
            press_continue_4_1.tStart = t  # local t and not account for scr refresh
            press_continue_4_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_4_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_4_1.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_4_1.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_4_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_4_1.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_4_1.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_4_1_allKeys.extend(theseKeys)
            if len(_press_continue_4_1_allKeys):
                press_continue_4_1.keys = _press_continue_4_1_allKeys[-1].name  # just the last key pressed
                press_continue_4_1.rt = _press_continue_4_1_allKeys[-1].rt
                press_continue_4_1.duration = _press_continue_4_1_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in start_pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "start_pretrial" ---
    for thisComponent in start_pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "start_pretrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "wait_1s_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_1s_pretrialComponents = [fix_wait_pretrial]
    for thisComponent in wait_1s_pretrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_1s_pretrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_wait_pretrial
        # skips this routine if there are no pretrial rounds set
        skip_if_enabled("pretrial")
        
        # *fix_wait_pretrial* updates
        
        # if fix_wait_pretrial is starting this frame...
        if fix_wait_pretrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_wait_pretrial.frameNStart = frameN  # exact frame index
            fix_wait_pretrial.tStart = t  # local t and not account for scr refresh
            fix_wait_pretrial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_wait_pretrial, 'tStartRefresh')  # time at next scr refresh
            # update status
            fix_wait_pretrial.status = STARTED
            fix_wait_pretrial.setAutoDraw(True)
        
        # if fix_wait_pretrial is active this frame...
        if fix_wait_pretrial.status == STARTED:
            # update params
            pass
        
        # if fix_wait_pretrial is stopping this frame...
        if fix_wait_pretrial.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_wait_pretrial.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                fix_wait_pretrial.tStop = t  # not accounting for scr refresh
                fix_wait_pretrial.tStopRefresh = tThisFlipGlobal  # on global time
                fix_wait_pretrial.frameNStop = frameN  # exact frame index
                # update status
                fix_wait_pretrial.status = FINISHED
                fix_wait_pretrial.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_1s_pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_1s_pretrial" ---
    for thisComponent in wait_1s_pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "play_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('play_pretrial.started', globalClock.getTime(format='float'))
    # Run 'Begin Routine' code from Tetris_pretrial
    # puts preTrial Tetris-Window on top
    Get_on_top("pretrial_Tetris")
    # waits one sec
    condition_or_wait_timer("wait")
    
    if skip_if_enabled("pretrial") == True:  
        # start Tetris pretrial
        game.toggle_pretrial.value = not game.toggle_pretrial.value
    
    if skip_if_enabled("pretrial") == True:
        # sets initial level tracking variable
        previous_level = game.level.value
        # log initial start_level
        thisExp.addData('Condition.info', 'info_preTrial_start')
        thisExp.nextEntry()
        thisExp.addData('pretrial.start_level', game.level.value)
    
    # keep track of which components have finished
    play_pretrialComponents = [fix_2, Start_eytracking]
    for thisComponent in play_pretrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "play_pretrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from Tetris_pretrial
        if skip_if_enabled("pretrial") == True:  
          # keep track of the level when it increases
            if previous_level < game.level.value:
                previous_level = game.level.value
                
            # adds useful parameters to the logfile when the level decreases (only happens when "game over")
            elif previous_level > game.level.value:    
                thisExp.addData('Condition.info', f'info_preTrial_round_{game.game_over_counter.value}')
                thisExp.addData('pretrial.fail_level', previous_level)
                thisExp.addData('pretrial.score', game.score.value)
                thisExp.addData('pretrial.round_t', globalClock.getTime(format='float'))
                thisExp.nextEntry()
                # adds new start level, except after last "game over "...
                if game.game_over_counter.value != game.pretrial_rounds:
                    thisExp.addData('pretrial.start_level', game.level.value)
                # reset previous_level according to new game.level.value
                previous_level = game.level.value
            
        # end pretrials if game over counter meets the amount of pretrial rounds set in the config files
        if game.game_over_counter.value == game.pretrial_rounds or game.pretrial_rounds == None:
           continueRoutine = False
        
        #keep track of weights and completion rate if you use jnd regression ans the Pretrial
        if game.jnd_regression == True and game.pretrial_rounds != None and frameN % 600 == 0:
            print(f' y_array: {game.regression.y_array[:]}')
            print(f' weights: {game.regression.weights[:]}')
        
        
        
        # *fix_2* updates
        
        # if fix_2 is starting this frame...
        if fix_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_2.frameNStart = frameN  # exact frame index
            fix_2.tStart = t  # local t and not account for scr refresh
            fix_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            fix_2.status = STARTED
            fix_2.setAutoDraw(True)
        
        # if fix_2 is active this frame...
        if fix_2.status == STARTED:
            # update params
            pass
        # *Start_eytracking* updates
        
        # if Start_eytracking is starting this frame...
        if Start_eytracking.status == NOT_STARTED and Eye_tracking == True:
            # keep track of start time/frame for later
            Start_eytracking.frameNStart = frameN  # exact frame index
            Start_eytracking.tStart = t  # local t and not account for scr refresh
            Start_eytracking.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Start_eytracking, 'tStartRefresh')  # time at next scr refresh
            # update status
            Start_eytracking.status = STARTED
        
        # if Start_eytracking is stopping this frame...
        if Start_eytracking.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Start_eytracking.tStartRefresh + 0-frameTolerance:
                # keep track of stop time/frame for later
                Start_eytracking.tStop = t  # not accounting for scr refresh
                Start_eytracking.tStopRefresh = tThisFlipGlobal  # on global time
                Start_eytracking.frameNStop = frameN  # exact frame index
                # update status
                Start_eytracking.status = FINISHED
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in play_pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "play_pretrial" ---
    for thisComponent in play_pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('play_pretrial.stopped', globalClock.getTime(format='float'))
    # Run 'End Routine' code from Tetris_pretrial
    # get back to Psychopy window
    Get_on_top("PsychoPy")
    # adds the achieved level and score to the data file
    thisExp.addData('pretrial.score', game.score.value)
    thisExp.addData('Condition.info', 'info_preTrial_sum')
    
    
    # execute game.level_for_main.value as defined by "config_tetris_game.txt"
    # skip automatically if pretrial_rounds are disabled
    if game.jnd_regression == True and game.pretrial_rounds != None:
        thisExp.addData('pretrial.level_avg', game.level_for_main.value)
        # overwrites game.level_for_main.value achieved by averaging with regression results
        game.level_for_main.value, popt, pcov = game.regression.determine_main_level()
        # log regression results
        thisExp.addData('pretrial.game_speeds', game.regression.x_array[:])
        thisExp.addData('JND', game.level_for_main.value)
        thisExp.addData('pretrial.completion_rate', game.regression.y_array[:])
        thisExp.addData('pretrial.weights', game.regression.weights[:])
        thisExp.addData('pretrial.optimization_parameters', popt)
        
    else:
        # do not log regression results if "Jnd_regression" is not enabled in config
        thisExp.addData('pretrial.game_speeds', None)
        thisExp.addData('pretrial.level_avg', game.level_for_main.value)
        thisExp.addData('JND', None)
        thisExp.addData('pretrial.completion_rate', None)
        thisExp.addData('pretrial.weights', None)
        thisExp.addData('pretrial.optimization_parameters', None)
        
    # skip this step if pretrials are disabled
    if game.pretrial_rounds != None:
        # sets new start level for main game (needs to be converted to an int, since this multiprocessing.values type cannot be changed
        game.level_for_main.value = round(game.level_for_main.value * game.level_for_main_factor)
        game.level.value = int(game.level_for_main.value)
    
    # resets absolut score
    game.score.value = 0
    
    # prints out the value for control purposes
    print('\n'.join([
    "--------------------",
    f"Main level: {game.level.value}",
    "--------------------",
    ""
    ]))
    
    # ends pretrial pygame process
    if game.pretrial_rounds != None:
        pretrial_Tetris.terminate()
        pretrial_Tetris.join()
    
    # make sure the eyetracker recording stops
    if Start_eytracking.status != FINISHED:
        Start_eytracking.status = FINISHED
    thisExp.nextEntry()
    # the Routine "play_pretrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "wait_1s_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_1s_pretrialComponents = [fix_wait_pretrial]
    for thisComponent in wait_1s_pretrialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_1s_pretrial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_wait_pretrial
        # skips this routine if there are no pretrial rounds set
        skip_if_enabled("pretrial")
        
        # *fix_wait_pretrial* updates
        
        # if fix_wait_pretrial is starting this frame...
        if fix_wait_pretrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix_wait_pretrial.frameNStart = frameN  # exact frame index
            fix_wait_pretrial.tStart = t  # local t and not account for scr refresh
            fix_wait_pretrial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix_wait_pretrial, 'tStartRefresh')  # time at next scr refresh
            # update status
            fix_wait_pretrial.status = STARTED
            fix_wait_pretrial.setAutoDraw(True)
        
        # if fix_wait_pretrial is active this frame...
        if fix_wait_pretrial.status == STARTED:
            # update params
            pass
        
        # if fix_wait_pretrial is stopping this frame...
        if fix_wait_pretrial.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix_wait_pretrial.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                fix_wait_pretrial.tStop = t  # not accounting for scr refresh
                fix_wait_pretrial.tStopRefresh = tThisFlipGlobal  # on global time
                fix_wait_pretrial.frameNStop = frameN  # exact frame index
                # update status
                fix_wait_pretrial.status = FINISHED
                fix_wait_pretrial.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_1s_pretrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_1s_pretrial" ---
    for thisComponent in wait_1s_pretrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "pause_n_sec" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_pause_n_sec
    # creates coutdown
    pause_timer = core.CountdownTimer(Pause_sec)
    # keep track of which components have finished
    pause_n_secComponents = [text_break, text_pause_n_sec]
    for thisComponent in pause_n_secComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "pause_n_sec" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_pause_n_sec
        # additionally checks whether main_trial or/and pretrial is enabled
        continueRoutine = skip_if_enabled("main_trials") and skip_if_enabled("pretrial")
        
        # lets timer run out
        if pause_timer.getTime() <= 0:
            # exits routine
            continueRoutine = False
        
        # *text_break* updates
        
        # if text_break is starting this frame...
        if text_break.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_break.frameNStart = frameN  # exact frame index
            text_break.tStart = t  # local t and not account for scr refresh
            text_break.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_break, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_break.status = STARTED
            text_break.setAutoDraw(True)
        
        # if text_break is active this frame...
        if text_break.status == STARTED:
            # update params
            pass
        
        # *text_pause_n_sec* updates
        
        # if text_pause_n_sec is starting this frame...
        if text_pause_n_sec.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_pause_n_sec.frameNStart = frameN  # exact frame index
            text_pause_n_sec.tStart = t  # local t and not account for scr refresh
            text_pause_n_sec.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_pause_n_sec, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_pause_n_sec.status = STARTED
            text_pause_n_sec.setAutoDraw(True)
        
        # if text_pause_n_sec is active this frame...
        if text_pause_n_sec.status == STARTED:
            # update params
            text_pause_n_sec.setText(int(pause_timer.getTime()) + 1
            , log=False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pause_n_secComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "pause_n_sec" ---
    for thisComponent in pause_n_secComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "pause_n_sec" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "intro_main" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_5.keys = []
    press_continue_5.rt = []
    _press_continue_5_allKeys = []
    # keep track of which components have finished
    intro_mainComponents = [intro_main_text, text_continue_5, press_continue_5]
    for thisComponent in intro_mainComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "intro_main" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_intro_main
        # skips this routine if there are no pretrial rounds or no main_trials set since it is uncessary to introduce the main part here...
        continueRoutine = skip_if_enabled("pretrial") and skip_if_enabled("main_trials")
        
        # *intro_main_text* updates
        
        # if intro_main_text is starting this frame...
        if intro_main_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            intro_main_text.frameNStart = frameN  # exact frame index
            intro_main_text.tStart = t  # local t and not account for scr refresh
            intro_main_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(intro_main_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            intro_main_text.status = STARTED
            intro_main_text.setAutoDraw(True)
        
        # if intro_main_text is active this frame...
        if intro_main_text.status == STARTED:
            # update params
            pass
        
        # *text_continue_5* updates
        
        # if text_continue_5 is starting this frame...
        if text_continue_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_continue_5.frameNStart = frameN  # exact frame index
            text_continue_5.tStart = t  # local t and not account for scr refresh
            text_continue_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_continue_5, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_continue_5.status = STARTED
            text_continue_5.setAutoDraw(True)
        
        # if text_continue_5 is active this frame...
        if text_continue_5.status == STARTED:
            # update params
            pass
        
        # *press_continue_5* updates
        waitOnFlip = False
        
        # if press_continue_5 is starting this frame...
        if press_continue_5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_5.frameNStart = frameN  # exact frame index
            press_continue_5.tStart = t  # local t and not account for scr refresh
            press_continue_5.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_5, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_5.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_5.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_5.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_5.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_5_allKeys.extend(theseKeys)
            if len(_press_continue_5_allKeys):
                press_continue_5.keys = _press_continue_5_allKeys[-1].name  # just the last key pressed
                press_continue_5.rt = _press_continue_5_allKeys[-1].rt
                press_continue_5.duration = _press_continue_5_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in intro_mainComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "intro_main" ---
    for thisComponent in intro_mainComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "intro_main" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "intro_structure" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_5_1.keys = []
    press_continue_5_1.rt = []
    _press_continue_5_1_allKeys = []
    # keep track of which components have finished
    intro_structureComponents = [text_intro_structure, text_continue_5_1, press_continue_5_1]
    for thisComponent in intro_structureComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "intro_structure" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_intro
        continueRoutine = skip_if_enabled("main_trials")
        
        # *text_intro_structure* updates
        
        # if text_intro_structure is starting this frame...
        if text_intro_structure.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_intro_structure.frameNStart = frameN  # exact frame index
            text_intro_structure.tStart = t  # local t and not account for scr refresh
            text_intro_structure.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_intro_structure, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_intro_structure.status = STARTED
            text_intro_structure.setAutoDraw(True)
        
        # if text_intro_structure is active this frame...
        if text_intro_structure.status == STARTED:
            # update params
            pass
        
        # *text_continue_5_1* updates
        
        # if text_continue_5_1 is starting this frame...
        if text_continue_5_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_continue_5_1.frameNStart = frameN  # exact frame index
            text_continue_5_1.tStart = t  # local t and not account for scr refresh
            text_continue_5_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_continue_5_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_continue_5_1.status = STARTED
            text_continue_5_1.setAutoDraw(True)
        
        # if text_continue_5_1 is active this frame...
        if text_continue_5_1.status == STARTED:
            # update params
            pass
        
        # *press_continue_5_1* updates
        waitOnFlip = False
        
        # if press_continue_5_1 is starting this frame...
        if press_continue_5_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_5_1.frameNStart = frameN  # exact frame index
            press_continue_5_1.tStart = t  # local t and not account for scr refresh
            press_continue_5_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_5_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_5_1.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_5_1.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_5_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_5_1.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_5_1.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_5_1_allKeys.extend(theseKeys)
            if len(_press_continue_5_1_allKeys):
                press_continue_5_1.keys = _press_continue_5_1_allKeys[-1].name  # just the last key pressed
                press_continue_5_1.rt = _press_continue_5_1_allKeys[-1].rt
                press_continue_5_1.duration = _press_continue_5_1_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in intro_structureComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "intro_structure" ---
    for thisComponent in intro_structureComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "intro_structure" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_basic_structure" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_6.keys = []
    press_continue_6.rt = []
    _press_continue_6_allKeys = []
    # keep track of which components have finished
    explain_basic_structureComponents = [controller_example_1, watch_example_1, motorcontrol_example_1, baseline_example_1, Announcement, Text_continue_6, press_continue_6]
    for thisComponent in explain_basic_structureComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_basic_structure" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_basic_structure
        continueRoutine = skip_if_enabled("main_trials")
        
        # *controller_example_1* updates
        
        # if controller_example_1 is starting this frame...
        if controller_example_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            controller_example_1.frameNStart = frameN  # exact frame index
            controller_example_1.tStart = t  # local t and not account for scr refresh
            controller_example_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(controller_example_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            controller_example_1.status = STARTED
            controller_example_1.setAutoDraw(True)
        
        # if controller_example_1 is active this frame...
        if controller_example_1.status == STARTED:
            # update params
            pass
        
        # *watch_example_1* updates
        
        # if watch_example_1 is starting this frame...
        if watch_example_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            watch_example_1.frameNStart = frameN  # exact frame index
            watch_example_1.tStart = t  # local t and not account for scr refresh
            watch_example_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(watch_example_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            watch_example_1.status = STARTED
            watch_example_1.setAutoDraw(True)
        
        # if watch_example_1 is active this frame...
        if watch_example_1.status == STARTED:
            # update params
            pass
        
        # *motorcontrol_example_1* updates
        
        # if motorcontrol_example_1 is starting this frame...
        if motorcontrol_example_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            motorcontrol_example_1.frameNStart = frameN  # exact frame index
            motorcontrol_example_1.tStart = t  # local t and not account for scr refresh
            motorcontrol_example_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(motorcontrol_example_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            motorcontrol_example_1.status = STARTED
            motorcontrol_example_1.setAutoDraw(True)
        
        # if motorcontrol_example_1 is active this frame...
        if motorcontrol_example_1.status == STARTED:
            # update params
            pass
        
        # *baseline_example_1* updates
        
        # if baseline_example_1 is starting this frame...
        if baseline_example_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            baseline_example_1.frameNStart = frameN  # exact frame index
            baseline_example_1.tStart = t  # local t and not account for scr refresh
            baseline_example_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(baseline_example_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            baseline_example_1.status = STARTED
            baseline_example_1.setAutoDraw(True)
        
        # if baseline_example_1 is active this frame...
        if baseline_example_1.status == STARTED:
            # update params
            pass
        
        # *Announcement* updates
        
        # if Announcement is starting this frame...
        if Announcement.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Announcement.frameNStart = frameN  # exact frame index
            Announcement.tStart = t  # local t and not account for scr refresh
            Announcement.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Announcement, 'tStartRefresh')  # time at next scr refresh
            # update status
            Announcement.status = STARTED
            Announcement.setAutoDraw(True)
        
        # if Announcement is active this frame...
        if Announcement.status == STARTED:
            # update params
            pass
        
        # *Text_continue_6* updates
        
        # if Text_continue_6 is starting this frame...
        if Text_continue_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_6.frameNStart = frameN  # exact frame index
            Text_continue_6.tStart = t  # local t and not account for scr refresh
            Text_continue_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_6, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_6.status = STARTED
            Text_continue_6.setAutoDraw(True)
        
        # if Text_continue_6 is active this frame...
        if Text_continue_6.status == STARTED:
            # update params
            pass
        
        # *press_continue_6* updates
        waitOnFlip = False
        
        # if press_continue_6 is starting this frame...
        if press_continue_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_6.frameNStart = frameN  # exact frame index
            press_continue_6.tStart = t  # local t and not account for scr refresh
            press_continue_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_6, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_6.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_6.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_6.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_6.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_6.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_6_allKeys.extend(theseKeys)
            if len(_press_continue_6_allKeys):
                press_continue_6.keys = _press_continue_6_allKeys[-1].name  # just the last key pressed
                press_continue_6.rt = _press_continue_6_allKeys[-1].rt
                press_continue_6.duration = _press_continue_6_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_basic_structureComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_basic_structure" ---
    for thisComponent in explain_basic_structureComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_basic_structure" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_play_Tetris" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_7.keys = []
    press_continue_7.rt = []
    _press_continue_7_allKeys = []
    # keep track of which components have finished
    explain_play_TetrisComponents = [controller_example, play_Tetris_text, Text_continue_7, press_continue_7]
    for thisComponent in explain_play_TetrisComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_play_Tetris" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_play
        continueRoutine = skip_if_enabled("main_trials")
        
        # *controller_example* updates
        
        # if controller_example is starting this frame...
        if controller_example.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            controller_example.frameNStart = frameN  # exact frame index
            controller_example.tStart = t  # local t and not account for scr refresh
            controller_example.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(controller_example, 'tStartRefresh')  # time at next scr refresh
            # update status
            controller_example.status = STARTED
            controller_example.setAutoDraw(True)
        
        # if controller_example is active this frame...
        if controller_example.status == STARTED:
            # update params
            pass
        
        # *play_Tetris_text* updates
        
        # if play_Tetris_text is starting this frame...
        if play_Tetris_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            play_Tetris_text.frameNStart = frameN  # exact frame index
            play_Tetris_text.tStart = t  # local t and not account for scr refresh
            play_Tetris_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(play_Tetris_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            play_Tetris_text.status = STARTED
            play_Tetris_text.setAutoDraw(True)
        
        # if play_Tetris_text is active this frame...
        if play_Tetris_text.status == STARTED:
            # update params
            pass
        
        # *Text_continue_7* updates
        
        # if Text_continue_7 is starting this frame...
        if Text_continue_7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_7.frameNStart = frameN  # exact frame index
            Text_continue_7.tStart = t  # local t and not account for scr refresh
            Text_continue_7.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_7, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_7.status = STARTED
            Text_continue_7.setAutoDraw(True)
        
        # if Text_continue_7 is active this frame...
        if Text_continue_7.status == STARTED:
            # update params
            pass
        
        # *press_continue_7* updates
        waitOnFlip = False
        
        # if press_continue_7 is starting this frame...
        if press_continue_7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_7.frameNStart = frameN  # exact frame index
            press_continue_7.tStart = t  # local t and not account for scr refresh
            press_continue_7.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_7, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_7.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_7.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_7.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_7.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_7.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_7_allKeys.extend(theseKeys)
            if len(_press_continue_7_allKeys):
                press_continue_7.keys = _press_continue_7_allKeys[-1].name  # just the last key pressed
                press_continue_7.rt = _press_continue_7_allKeys[-1].rt
                press_continue_7.duration = _press_continue_7_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_play_TetrisComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_play_Tetris" ---
    for thisComponent in explain_play_TetrisComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_play_Tetris" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_comp_load" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_7_1.keys = []
    press_continue_7_1.rt = []
    _press_continue_7_1_allKeys = []
    # keep track of which components have finished
    explain_comp_loadComponents = [controller_example_2, text_comp_load, Text_continue_7_1, press_continue_7_1]
    for thisComponent in explain_comp_loadComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_comp_load" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_comp_load
        # additionally checks whether main_trials are enabled at all and skips this routine if there no pretrial rounds set
        continueRoutine = skip_if_enabled("main_trials") and Comp_wm_load 
            
        
        
        # *controller_example_2* updates
        
        # if controller_example_2 is starting this frame...
        if controller_example_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            controller_example_2.frameNStart = frameN  # exact frame index
            controller_example_2.tStart = t  # local t and not account for scr refresh
            controller_example_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(controller_example_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            controller_example_2.status = STARTED
            controller_example_2.setAutoDraw(True)
        
        # if controller_example_2 is active this frame...
        if controller_example_2.status == STARTED:
            # update params
            pass
        
        # *text_comp_load* updates
        
        # if text_comp_load is starting this frame...
        if text_comp_load.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_comp_load.frameNStart = frameN  # exact frame index
            text_comp_load.tStart = t  # local t and not account for scr refresh
            text_comp_load.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_comp_load, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_comp_load.status = STARTED
            text_comp_load.setAutoDraw(True)
        
        # if text_comp_load is active this frame...
        if text_comp_load.status == STARTED:
            # update params
            pass
        
        # *Text_continue_7_1* updates
        
        # if Text_continue_7_1 is starting this frame...
        if Text_continue_7_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_7_1.frameNStart = frameN  # exact frame index
            Text_continue_7_1.tStart = t  # local t and not account for scr refresh
            Text_continue_7_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_7_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_7_1.status = STARTED
            Text_continue_7_1.setAutoDraw(True)
        
        # if Text_continue_7_1 is active this frame...
        if Text_continue_7_1.status == STARTED:
            # update params
            pass
        
        # *press_continue_7_1* updates
        waitOnFlip = False
        
        # if press_continue_7_1 is starting this frame...
        if press_continue_7_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_7_1.frameNStart = frameN  # exact frame index
            press_continue_7_1.tStart = t  # local t and not account for scr refresh
            press_continue_7_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_7_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_7_1.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_7_1.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_7_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_7_1.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_7_1.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_7_1_allKeys.extend(theseKeys)
            if len(_press_continue_7_1_allKeys):
                press_continue_7_1.keys = _press_continue_7_1_allKeys[-1].name  # just the last key pressed
                press_continue_7_1.rt = _press_continue_7_1_allKeys[-1].rt
                press_continue_7_1.duration = _press_continue_7_1_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_comp_loadComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_comp_load" ---
    for thisComponent in explain_comp_loadComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_comp_load" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_comp_speed" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_6_2.keys = []
    press_continue_6_2.rt = []
    _press_continue_6_2_allKeys = []
    # keep track of which components have finished
    explain_comp_speedComponents = [controller_example_3, text_comp_speed, Text_continue_7_2, press_continue_6_2]
    for thisComponent in explain_comp_speedComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_comp_speed" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_comp_speed
        #additionally checks whether main_trials are enabled at all or skips this routine if there no pretrial rounds set
        continueRoutine = skip_if_enabled("main_trials") and Comp_speed
        
        # *controller_example_3* updates
        
        # if controller_example_3 is starting this frame...
        if controller_example_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            controller_example_3.frameNStart = frameN  # exact frame index
            controller_example_3.tStart = t  # local t and not account for scr refresh
            controller_example_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(controller_example_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            controller_example_3.status = STARTED
            controller_example_3.setAutoDraw(True)
        
        # if controller_example_3 is active this frame...
        if controller_example_3.status == STARTED:
            # update params
            pass
        
        # *text_comp_speed* updates
        
        # if text_comp_speed is starting this frame...
        if text_comp_speed.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_comp_speed.frameNStart = frameN  # exact frame index
            text_comp_speed.tStart = t  # local t and not account for scr refresh
            text_comp_speed.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_comp_speed, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_comp_speed.status = STARTED
            text_comp_speed.setAutoDraw(True)
        
        # if text_comp_speed is active this frame...
        if text_comp_speed.status == STARTED:
            # update params
            pass
        
        # *Text_continue_7_2* updates
        
        # if Text_continue_7_2 is starting this frame...
        if Text_continue_7_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_7_2.frameNStart = frameN  # exact frame index
            Text_continue_7_2.tStart = t  # local t and not account for scr refresh
            Text_continue_7_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_7_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_7_2.status = STARTED
            Text_continue_7_2.setAutoDraw(True)
        
        # if Text_continue_7_2 is active this frame...
        if Text_continue_7_2.status == STARTED:
            # update params
            pass
        
        # *press_continue_6_2* updates
        waitOnFlip = False
        
        # if press_continue_6_2 is starting this frame...
        if press_continue_6_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_6_2.frameNStart = frameN  # exact frame index
            press_continue_6_2.tStart = t  # local t and not account for scr refresh
            press_continue_6_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_6_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_6_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_6_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_6_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_6_2.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_6_2.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_6_2_allKeys.extend(theseKeys)
            if len(_press_continue_6_2_allKeys):
                press_continue_6_2.keys = _press_continue_6_2_allKeys[-1].name  # just the last key pressed
                press_continue_6_2.rt = _press_continue_6_2_allKeys[-1].rt
                press_continue_6_2.duration = _press_continue_6_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_comp_speedComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_comp_speed" ---
    for thisComponent in explain_comp_speedComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_comp_speed" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_motor_control" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_8.keys = []
    press_continue_8.rt = []
    _press_continue_8_allKeys = []
    # keep track of which components have finished
    explain_motor_controlComponents = [motorcontrol_example, text_motor, Text_continue_8, press_continue_8]
    for thisComponent in explain_motor_controlComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_motor_control" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_motor
        continueRoutine = skip_if_enabled("main_trials")
        
        # *motorcontrol_example* updates
        
        # if motorcontrol_example is starting this frame...
        if motorcontrol_example.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            motorcontrol_example.frameNStart = frameN  # exact frame index
            motorcontrol_example.tStart = t  # local t and not account for scr refresh
            motorcontrol_example.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(motorcontrol_example, 'tStartRefresh')  # time at next scr refresh
            # update status
            motorcontrol_example.status = STARTED
            motorcontrol_example.setAutoDraw(True)
        
        # if motorcontrol_example is active this frame...
        if motorcontrol_example.status == STARTED:
            # update params
            pass
        
        # *text_motor* updates
        
        # if text_motor is starting this frame...
        if text_motor.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_motor.frameNStart = frameN  # exact frame index
            text_motor.tStart = t  # local t and not account for scr refresh
            text_motor.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_motor, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_motor.status = STARTED
            text_motor.setAutoDraw(True)
        
        # if text_motor is active this frame...
        if text_motor.status == STARTED:
            # update params
            pass
        
        # *Text_continue_8* updates
        
        # if Text_continue_8 is starting this frame...
        if Text_continue_8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_8.frameNStart = frameN  # exact frame index
            Text_continue_8.tStart = t  # local t and not account for scr refresh
            Text_continue_8.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_8, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_8.status = STARTED
            Text_continue_8.setAutoDraw(True)
        
        # if Text_continue_8 is active this frame...
        if Text_continue_8.status == STARTED:
            # update params
            pass
        
        # *press_continue_8* updates
        waitOnFlip = False
        
        # if press_continue_8 is starting this frame...
        if press_continue_8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_8.frameNStart = frameN  # exact frame index
            press_continue_8.tStart = t  # local t and not account for scr refresh
            press_continue_8.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_8, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_8.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_8.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_8.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_8.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_8.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_8_allKeys.extend(theseKeys)
            if len(_press_continue_8_allKeys):
                press_continue_8.keys = _press_continue_8_allKeys[-1].name  # just the last key pressed
                press_continue_8.rt = _press_continue_8_allKeys[-1].rt
                press_continue_8.duration = _press_continue_8_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_motor_controlComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_motor_control" ---
    for thisComponent in explain_motor_controlComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_motor_control" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_watch_Tetris" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_9.keys = []
    press_continue_9.rt = []
    _press_continue_9_allKeys = []
    # keep track of which components have finished
    explain_watch_TetrisComponents = [watch_example, text_watch, Text_continue_9, press_continue_9]
    for thisComponent in explain_watch_TetrisComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_watch_Tetris" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_watch
        continueRoutine = skip_if_enabled("main_trials")
        
        # *watch_example* updates
        
        # if watch_example is starting this frame...
        if watch_example.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            watch_example.frameNStart = frameN  # exact frame index
            watch_example.tStart = t  # local t and not account for scr refresh
            watch_example.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(watch_example, 'tStartRefresh')  # time at next scr refresh
            # update status
            watch_example.status = STARTED
            watch_example.setAutoDraw(True)
        
        # if watch_example is active this frame...
        if watch_example.status == STARTED:
            # update params
            pass
        
        # *text_watch* updates
        
        # if text_watch is starting this frame...
        if text_watch.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_watch.frameNStart = frameN  # exact frame index
            text_watch.tStart = t  # local t and not account for scr refresh
            text_watch.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_watch, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_watch.status = STARTED
            text_watch.setAutoDraw(True)
        
        # if text_watch is active this frame...
        if text_watch.status == STARTED:
            # update params
            pass
        
        # *Text_continue_9* updates
        
        # if Text_continue_9 is starting this frame...
        if Text_continue_9.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_9.frameNStart = frameN  # exact frame index
            Text_continue_9.tStart = t  # local t and not account for scr refresh
            Text_continue_9.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_9, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_9.status = STARTED
            Text_continue_9.setAutoDraw(True)
        
        # if Text_continue_9 is active this frame...
        if Text_continue_9.status == STARTED:
            # update params
            pass
        
        # *press_continue_9* updates
        waitOnFlip = False
        
        # if press_continue_9 is starting this frame...
        if press_continue_9.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_9.frameNStart = frameN  # exact frame index
            press_continue_9.tStart = t  # local t and not account for scr refresh
            press_continue_9.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_9, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_9.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_9.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_9.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_9.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_9.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_9_allKeys.extend(theseKeys)
            if len(_press_continue_9_allKeys):
                press_continue_9.keys = _press_continue_9_allKeys[-1].name  # just the last key pressed
                press_continue_9.rt = _press_continue_9_allKeys[-1].rt
                press_continue_9.duration = _press_continue_9_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_watch_TetrisComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_watch_Tetris" ---
    for thisComponent in explain_watch_TetrisComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_watch_Tetris" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_fixation_cross" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_10.keys = []
    press_continue_10.rt = []
    _press_continue_10_allKeys = []
    # keep track of which components have finished
    explain_fixation_crossComponents = [baseline_example, text_cross, Text_continue_10, press_continue_10]
    for thisComponent in explain_fixation_crossComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_fixation_cross" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_cross
        continueRoutine = skip_if_enabled("main_trials")
        
        # *baseline_example* updates
        
        # if baseline_example is starting this frame...
        if baseline_example.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            baseline_example.frameNStart = frameN  # exact frame index
            baseline_example.tStart = t  # local t and not account for scr refresh
            baseline_example.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(baseline_example, 'tStartRefresh')  # time at next scr refresh
            # update status
            baseline_example.status = STARTED
            baseline_example.setAutoDraw(True)
        
        # if baseline_example is active this frame...
        if baseline_example.status == STARTED:
            # update params
            pass
        
        # *text_cross* updates
        
        # if text_cross is starting this frame...
        if text_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_cross.frameNStart = frameN  # exact frame index
            text_cross.tStart = t  # local t and not account for scr refresh
            text_cross.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_cross, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_cross.status = STARTED
            text_cross.setAutoDraw(True)
        
        # if text_cross is active this frame...
        if text_cross.status == STARTED:
            # update params
            pass
        
        # *Text_continue_10* updates
        
        # if Text_continue_10 is starting this frame...
        if Text_continue_10.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_10.frameNStart = frameN  # exact frame index
            Text_continue_10.tStart = t  # local t and not account for scr refresh
            Text_continue_10.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_10, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_10.status = STARTED
            Text_continue_10.setAutoDraw(True)
        
        # if Text_continue_10 is active this frame...
        if Text_continue_10.status == STARTED:
            # update params
            pass
        
        # *press_continue_10* updates
        waitOnFlip = False
        
        # if press_continue_10 is starting this frame...
        if press_continue_10.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_10.frameNStart = frameN  # exact frame index
            press_continue_10.tStart = t  # local t and not account for scr refresh
            press_continue_10.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_10, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_10.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_10.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_10.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_10.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_10.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_10_allKeys.extend(theseKeys)
            if len(_press_continue_10_allKeys):
                press_continue_10.keys = _press_continue_10_allKeys[-1].name  # just the last key pressed
                press_continue_10.rt = _press_continue_10_allKeys[-1].rt
                press_continue_10.duration = _press_continue_10_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_fixation_crossComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_fixation_cross" ---
    for thisComponent in explain_fixation_crossComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_fixation_cross" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_trials" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_10_1.keys = []
    press_continue_10_1.rt = []
    _press_continue_10_1_allKeys = []
    # keep track of which components have finished
    explain_trialsComponents = [img_explain_trials, text_explain_trials, Text_continue_10_1, press_continue_10_1]
    for thisComponent in explain_trialsComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "explain_trials" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_explain_trials
        continueRoutine = skip_if_enabled("main_trials")
        
        # *img_explain_trials* updates
        
        # if img_explain_trials is starting this frame...
        if img_explain_trials.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            img_explain_trials.frameNStart = frameN  # exact frame index
            img_explain_trials.tStart = t  # local t and not account for scr refresh
            img_explain_trials.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(img_explain_trials, 'tStartRefresh')  # time at next scr refresh
            # update status
            img_explain_trials.status = STARTED
            img_explain_trials.setAutoDraw(True)
        
        # if img_explain_trials is active this frame...
        if img_explain_trials.status == STARTED:
            # update params
            pass
        
        # *text_explain_trials* updates
        
        # if text_explain_trials is starting this frame...
        if text_explain_trials.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            text_explain_trials.frameNStart = frameN  # exact frame index
            text_explain_trials.tStart = t  # local t and not account for scr refresh
            text_explain_trials.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_explain_trials, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_explain_trials.status = STARTED
            text_explain_trials.setAutoDraw(True)
        
        # if text_explain_trials is active this frame...
        if text_explain_trials.status == STARTED:
            # update params
            pass
        
        # *Text_continue_10_1* updates
        
        # if Text_continue_10_1 is starting this frame...
        if Text_continue_10_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_10_1.frameNStart = frameN  # exact frame index
            Text_continue_10_1.tStart = t  # local t and not account for scr refresh
            Text_continue_10_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_10_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_10_1.status = STARTED
            Text_continue_10_1.setAutoDraw(True)
        
        # if Text_continue_10_1 is active this frame...
        if Text_continue_10_1.status == STARTED:
            # update params
            pass
        
        # *press_continue_10_1* updates
        waitOnFlip = False
        
        # if press_continue_10_1 is starting this frame...
        if press_continue_10_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_10_1.frameNStart = frameN  # exact frame index
            press_continue_10_1.tStart = t  # local t and not account for scr refresh
            press_continue_10_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_10_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_10_1.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_10_1.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_10_1.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_10_1.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_10_1.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_10_1_allKeys.extend(theseKeys)
            if len(_press_continue_10_1_allKeys):
                press_continue_10_1.keys = _press_continue_10_1_allKeys[-1].name  # just the last key pressed
                press_continue_10_1.rt = _press_continue_10_1_allKeys[-1].rt
                press_continue_10_1.duration = _press_continue_10_1_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in explain_trialsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explain_trials" ---
    for thisComponent in explain_trialsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explain_trials" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "start_experiment" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_11.keys = []
    press_continue_11.rt = []
    _press_continue_11_allKeys = []
    # keep track of which components have finished
    start_experimentComponents = [Start, Text_continue_11, press_continue_11]
    for thisComponent in start_experimentComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "start_experiment" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from skip_start
        continueRoutine = skip_if_enabled("main_trials")
        
        # *Start* updates
        
        # if Start is starting this frame...
        if Start.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Start.frameNStart = frameN  # exact frame index
            Start.tStart = t  # local t and not account for scr refresh
            Start.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Start, 'tStartRefresh')  # time at next scr refresh
            # update status
            Start.status = STARTED
            Start.setAutoDraw(True)
        
        # if Start is active this frame...
        if Start.status == STARTED:
            # update params
            pass
        
        # *Text_continue_11* updates
        
        # if Text_continue_11 is starting this frame...
        if Text_continue_11.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Text_continue_11.frameNStart = frameN  # exact frame index
            Text_continue_11.tStart = t  # local t and not account for scr refresh
            Text_continue_11.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Text_continue_11, 'tStartRefresh')  # time at next scr refresh
            # update status
            Text_continue_11.status = STARTED
            Text_continue_11.setAutoDraw(True)
        
        # if Text_continue_11 is active this frame...
        if Text_continue_11.status == STARTED:
            # update params
            pass
        
        # *press_continue_11* updates
        waitOnFlip = False
        
        # if press_continue_11 is starting this frame...
        if press_continue_11.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_continue_11.frameNStart = frameN  # exact frame index
            press_continue_11.tStart = t  # local t and not account for scr refresh
            press_continue_11.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_continue_11, 'tStartRefresh')  # time at next scr refresh
            # update status
            press_continue_11.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_continue_11.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_continue_11.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_continue_11.status == STARTED and not waitOnFlip:
            theseKeys = press_continue_11.getKeys(keyList=['return', psychopy_key_1, psychopy_key_2, psychopy_key_3, psychopy_key_4, psychopy_key_5], ignoreKeys=["escape"], waitRelease=False)
            _press_continue_11_allKeys.extend(theseKeys)
            if len(_press_continue_11_allKeys):
                press_continue_11.keys = _press_continue_11_allKeys[-1].name  # just the last key pressed
                press_continue_11.rt = _press_continue_11_allKeys[-1].rt
                press_continue_11.duration = _press_continue_11_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in start_experimentComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "start_experiment" ---
    for thisComponent in start_experimentComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "start_experiment" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "wait_1s" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_1sComponents = [fix]
    for thisComponent in wait_1sComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_1s" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix* updates
        
        # if fix is starting this frame...
        if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix.frameNStart = frameN  # exact frame index
            fix.tStart = t  # local t and not account for scr refresh
            fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
            # update status
            fix.status = STARTED
            fix.setAutoDraw(True)
        
        # if fix is active this frame...
        if fix.status == STARTED:
            # update params
            pass
        
        # if fix is stopping this frame...
        if fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                fix.tStop = t  # not accounting for scr refresh
                fix.tStopRefresh = tThisFlipGlobal  # on global time
                fix.frameNStop = frameN  # exact frame index
                # update status
                fix.status = FINISHED
                fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_1sComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_1s" ---
    for thisComponent in wait_1sComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "wait_1s" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_1sComponents = [fix]
    for thisComponent in wait_1sComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_1s" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix* updates
        
        # if fix is starting this frame...
        if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix.frameNStart = frameN  # exact frame index
            fix.tStart = t  # local t and not account for scr refresh
            fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
            # update status
            fix.status = STARTED
            fix.setAutoDraw(True)
        
        # if fix is active this frame...
        if fix.status == STARTED:
            # update params
            pass
        
        # if fix is stopping this frame...
        if fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                fix.tStop = t  # not accounting for scr refresh
                fix.tStopRefresh = tThisFlipGlobal  # on global time
                fix.frameNStop = frameN  # exact frame index
                # update status
                fix.status = FINISHED
                fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_1sComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_1s" ---
    for thisComponent in wait_1sComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "wait_for_trigger" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from first_trigger
    # only adds first trigger data if main trials are enabled in "config_paradigm_psychopy"
    if skip_if_enabled("main_trials") == True:
        thisExp.addData('Condition.info', 'first_trigger')
    # keep track of which components have finished
    wait_for_triggerComponents = [wait_for_trigger_text]
    for thisComponent in wait_for_triggerComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_for_trigger" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from first_trigger
        # additionally checks whether main_trials are enabled at all
        continueRoutine = skip_if_enabled("main_trials")
        
        # waits for a keyboard input (that is the trigger signal from the MRI) as defined in the "config_paradigm_psychopy"
        if defaultKeyboard.getKeys(keyList=[Trigger]):
            continueRoutine = False
            
        
        
        # *wait_for_trigger_text* updates
        
        # if wait_for_trigger_text is starting this frame...
        if wait_for_trigger_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            wait_for_trigger_text.frameNStart = frameN  # exact frame index
            wait_for_trigger_text.tStart = t  # local t and not account for scr refresh
            wait_for_trigger_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(wait_for_trigger_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            wait_for_trigger_text.status = STARTED
            wait_for_trigger_text.setAutoDraw(True)
        
        # if wait_for_trigger_text is active this frame...
        if wait_for_trigger_text.status == STARTED:
            # update params
            pass
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_for_triggerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_for_trigger" ---
    for thisComponent in wait_for_triggerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "wait_for_trigger" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "wait_1s" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    wait_1sComponents = [fix]
    for thisComponent in wait_1sComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_1s" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix* updates
        
        # if fix is starting this frame...
        if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix.frameNStart = frameN  # exact frame index
            fix.tStart = t  # local t and not account for scr refresh
            fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
            # update status
            fix.status = STARTED
            fix.setAutoDraw(True)
        
        # if fix is active this frame...
        if fix.status == STARTED:
            # update params
            pass
        
        # if fix is stopping this frame...
        if fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix.tStartRefresh + 1-frameTolerance:
                # keep track of stop time/frame for later
                fix.tStop = t  # not accounting for scr refresh
                fix.tStopRefresh = tThisFlipGlobal  # on global time
                fix.frameNStop = frameN  # exact frame index
                # update status
                fix.status = FINISHED
                fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_1sComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_1s" ---
    for thisComponent in wait_1sComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "three_seconds_timer" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_three_sec_timer
    # creates coutdown
    three_sec_timer = core.CountdownTimer(3)
    # keep track of which components have finished
    three_seconds_timerComponents = [text_three_sec_timer]
    for thisComponent in three_seconds_timerComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "three_seconds_timer" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from code_three_sec_timer
        # additionally checks whether main_trials are enabled at all
        continueRoutine = skip_if_enabled("main_trials")
        
        
        
        
        # lets timer run out
        if three_sec_timer.getTime() <= 0:
            # exits routine
            continueRoutine = False
        
        
        
        # *text_three_sec_timer* updates
        
        # if text_three_sec_timer is starting this frame...
        if text_three_sec_timer.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_three_sec_timer.frameNStart = frameN  # exact frame index
            text_three_sec_timer.tStart = t  # local t and not account for scr refresh
            text_three_sec_timer.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_three_sec_timer, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_three_sec_timer.status = STARTED
            text_three_sec_timer.setAutoDraw(True)
        
        # if text_three_sec_timer is active this frame...
        if text_three_sec_timer.status == STARTED:
            # update params
            text_three_sec_timer.setText(int(three_sec_timer.getTime()) + 1
            , log=False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in three_seconds_timerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "three_seconds_timer" ---
    for thisComponent in three_seconds_timerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Run 'End Routine' code from code_three_sec_timer
    #if pretrials are disabled set the restart level/game.level_for_main.value to the Start_level from "config_tetris_game"
    if skip_if_enabled("pretrial") == False:
        game.level_for_main.value = game.level.value
        print(f'Restart Level set to {game.level_for_main.value}')
        
    # set main_trial repeats to 0 if its disabled in config
    if skip_if_enabled("main_trials") == False:
        n_repeats = 0
    
    # or set it to 1 if N_repeats is not None in config
    else:
        n_repeats = 1
    thisExp.nextEntry()
    # the Routine "three_seconds_timer" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    main_trials = data.TrialHandler(nReps=n_repeats, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('main_trials.csv'),
        seed=None, name='main_trials')
    thisExp.addLoop(main_trials)  # add the loop to the experiment
    thisMain_trial = main_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisMain_trial.rgb)
    if thisMain_trial != None:
        for paramName in thisMain_trial:
            globals()[paramName] = thisMain_trial[paramName]
    
    for thisMain_trial in main_trials:
        currentLoop = main_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisMain_trial.rgb)
        if thisMain_trial != None:
            for paramName in thisMain_trial:
                globals()[paramName] = thisMain_trial[paramName]
        
        # --- Prepare to start Routine "show_play_tetris" ---
        continueRoutine = True
        # update component parameters for each repeat
        Icon_for_play_Tetris.setSize((0.5, 0.5))
        Icon_for_play_Tetris.setImage('Images/controller.png')
        # keep track of which components have finished
        show_play_tetrisComponents = [Icon_for_play_Tetris]
        for thisComponent in show_play_tetrisComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "show_play_tetris" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 2.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Icon_for_play_Tetris* updates
            
            # if Icon_for_play_Tetris is starting this frame...
            if Icon_for_play_Tetris.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Icon_for_play_Tetris.frameNStart = frameN  # exact frame index
                Icon_for_play_Tetris.tStart = t  # local t and not account for scr refresh
                Icon_for_play_Tetris.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Icon_for_play_Tetris, 'tStartRefresh')  # time at next scr refresh
                # update status
                Icon_for_play_Tetris.status = STARTED
                Icon_for_play_Tetris.setAutoDraw(True)
            
            # if Icon_for_play_Tetris is active this frame...
            if Icon_for_play_Tetris.status == STARTED:
                # update params
                pass
            
            # if Icon_for_play_Tetris is stopping this frame...
            if Icon_for_play_Tetris.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Icon_for_play_Tetris.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    Icon_for_play_Tetris.tStop = t  # not accounting for scr refresh
                    Icon_for_play_Tetris.tStopRefresh = tThisFlipGlobal  # on global time
                    Icon_for_play_Tetris.frameNStop = frameN  # exact frame index
                    # update status
                    Icon_for_play_Tetris.status = FINISHED
                    Icon_for_play_Tetris.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in show_play_tetrisComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "show_play_tetris" ---
        for thisComponent in show_play_tetrisComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-2.000000)
        
        # --- Prepare to start Routine "wait_1s" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        wait_1sComponents = [fix]
        for thisComponent in wait_1sComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "wait_1s" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix* updates
            
            # if fix is starting this frame...
            if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix.frameNStart = frameN  # exact frame index
                fix.tStart = t  # local t and not account for scr refresh
                fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
                # update status
                fix.status = STARTED
                fix.setAutoDraw(True)
            
            # if fix is active this frame...
            if fix.status == STARTED:
                # update params
                pass
            
            # if fix is stopping this frame...
            if fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fix.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    fix.tStop = t  # not accounting for scr refresh
                    fix.tStopRefresh = tThisFlipGlobal  # on global time
                    fix.frameNStop = frameN  # exact frame index
                    # update status
                    fix.status = FINISHED
                    fix.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in wait_1sComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "wait_1s" ---
        for thisComponent in wait_1sComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "tetris_condition" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from execute_play_Tetris
        # sets "high" or "low" "speed" or "wm_load" if enabled in config
        comp_wm_load_speed(main_trials.nTotal, main_trials.thisN)
            
        # bring Tetris to foreground
        Get_on_top("play_Tetris")
        
        # wait one sec
        condition_or_wait_timer("wait")
        
        # Tetris resumes here
        game.toggle_play.value = not game.toggle_play.value
        
        # collect start time for logging
        condition_started = globalClock.getTime(format='float')
        
        # keep track of which components have finished
        tetris_conditionComponents = [duration_and_fix_play_Tetris]
        for thisComponent in tetris_conditionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "tetris_condition" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *duration_and_fix_play_Tetris* updates
            
            # if duration_and_fix_play_Tetris is starting this frame...
            if duration_and_fix_play_Tetris.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                duration_and_fix_play_Tetris.frameNStart = frameN  # exact frame index
                duration_and_fix_play_Tetris.tStart = t  # local t and not account for scr refresh
                duration_and_fix_play_Tetris.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(duration_and_fix_play_Tetris, 'tStartRefresh')  # time at next scr refresh
                # update status
                duration_and_fix_play_Tetris.status = STARTED
                duration_and_fix_play_Tetris.setAutoDraw(True)
            
            # if duration_and_fix_play_Tetris is active this frame...
            if duration_and_fix_play_Tetris.status == STARTED:
                # update params
                duration_and_fix_play_Tetris.setOpacity(None, log=False)
            
            # if duration_and_fix_play_Tetris is stopping this frame...
            if duration_and_fix_play_Tetris.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > duration_and_fix_play_Tetris.tStartRefresh + Play_Tetris_duration-frameTolerance:
                    # keep track of stop time/frame for later
                    duration_and_fix_play_Tetris.tStop = t  # not accounting for scr refresh
                    duration_and_fix_play_Tetris.tStopRefresh = tThisFlipGlobal  # on global time
                    duration_and_fix_play_Tetris.frameNStop = frameN  # exact frame index
                    # update status
                    duration_and_fix_play_Tetris.status = FINISHED
                    duration_and_fix_play_Tetris.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in tetris_conditionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "tetris_condition" ---
        for thisComponent in tetris_conditionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from execute_play_Tetris
        # get offset of the condition
        condition_stopped = globalClock.getTime(format='float')
        
        #pauses Tetris
        game.toggle_play.value = not game.toggle_play.value
        
        # waits one seconds
        condition_or_wait_timer("wait")
        # if the control condition is "watch_Tetris": sets Tetris window to background
        Get_on_top("PsychoPy")
        
        
        # the Routine "tetris_condition" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "condition_ended" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        condition_endedComponents = [condition_ended_text]
        for thisComponent in condition_endedComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "condition_ended" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *condition_ended_text* updates
            
            # if condition_ended_text is starting this frame...
            if condition_ended_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                condition_ended_text.frameNStart = frameN  # exact frame index
                condition_ended_text.tStart = t  # local t and not account for scr refresh
                condition_ended_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(condition_ended_text, 'tStartRefresh')  # time at next scr refresh
                # update status
                condition_ended_text.status = STARTED
                condition_ended_text.setAutoDraw(True)
            
            # if condition_ended_text is active this frame...
            if condition_ended_text.status == STARTED:
                # update params
                condition_ended_text.setOpacity(None, log=False)
            
            # if condition_ended_text is stopping this frame...
            if condition_ended_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > condition_ended_text.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    condition_ended_text.tStop = t  # not accounting for scr refresh
                    condition_ended_text.tStopRefresh = tThisFlipGlobal  # on global time
                    condition_ended_text.frameNStop = frameN  # exact frame index
                    # update status
                    condition_ended_text.status = FINISHED
                    condition_ended_text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in condition_endedComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "condition_ended" ---
        for thisComponent in condition_endedComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "wait_ISI_after_play_tetris" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from add_data_play_Tetris
        # check whether iti variation is enabled in config and set the iti accordingly
        if ISI_variation == True:
            # if a random seed is used for the iti variation make sure it is only used in the first trial
            # (or iti will be the same for each trial)
            if main_trials.thisN == 0:
                # create the intertrial interval variation array for "main_trials"
                # create an array of floats between ITI_lower and ITI_upper with 0.1 increments as extension variations of the intertrial interval
                isis = np.arange(ISI_lower, ISI_upper, 0.1)
                # apply seed if enabled in paradigm config
                np.random.seed(ISI_seed)
                
            # choose a random iti from the available "itis" range
            isi_add = np.random.choice(isis)
        else:
            isi_add = 0
        
        # keep track of which components have finished
        wait_ISI_after_play_tetrisComponents = [fix_after_play_Tetris]
        for thisComponent in wait_ISI_after_play_tetrisComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "wait_ISI_after_play_tetris" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix_after_play_Tetris* updates
            
            # if fix_after_play_Tetris is starting this frame...
            if fix_after_play_Tetris.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix_after_play_Tetris.frameNStart = frameN  # exact frame index
                fix_after_play_Tetris.tStart = t  # local t and not account for scr refresh
                fix_after_play_Tetris.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix_after_play_Tetris, 'tStartRefresh')  # time at next scr refresh
                # update status
                fix_after_play_Tetris.status = STARTED
                fix_after_play_Tetris.setAutoDraw(True)
            
            # if fix_after_play_Tetris is active this frame...
            if fix_after_play_Tetris.status == STARTED:
                # update params
                pass
            
            # if fix_after_play_Tetris is stopping this frame...
            if fix_after_play_Tetris.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fix_after_play_Tetris.tStartRefresh + 3 + isi_add-frameTolerance:
                    # keep track of stop time/frame for later
                    fix_after_play_Tetris.tStop = t  # not accounting for scr refresh
                    fix_after_play_Tetris.tStopRefresh = tThisFlipGlobal  # on global time
                    fix_after_play_Tetris.frameNStop = frameN  # exact frame index
                    # update status
                    fix_after_play_Tetris.status = FINISHED
                    fix_after_play_Tetris.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in wait_ISI_after_play_tetrisComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "wait_ISI_after_play_tetris" ---
        for thisComponent in wait_ISI_after_play_tetrisComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from add_data_play_Tetris
        # logs on-, offsets and condition duration, etc. in one row (in the data file .csv) for later processing
        thisExp.addData('Condition.started', condition_started)
        thisExp.addData('Condition.stopped', condition_stopped)
        thisExp.addData('targeted.duration', Play_Tetris_duration)
        thisExp.addData('Condition.duration', condition_stopped - condition_started)
        thisExp.addData('Condition.info', 'info_play_Tetris')
        thisExp.addData('game.score', game.score.value)
        thisExp.addData('game.score', game.score.value)
        thisExp.addData('game.level', game.level.value)
        thisExp.addData('game.speed', game.speed.value)
        if Comp_wm_load == True:
            thisExp.addData('game.wm_load_condition', wm_load_seq[main_trials.thisN])
        else: 
            thisExp.addData('game.wm_load_condition', None)
        if Comp_speed == True:
            thisExp.addData('game.speed_condition', speed_seq[main_trials.thisN])
        else:
            thisExp.addData('game.speed_condition', None)
        
        thisExp.nextEntry()
        # the Routine "wait_ISI_after_play_tetris" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "show_next_control" ---
        continueRoutine = True
        # update component parameters for each repeat
        Icon_for_next_cond.setSize((0.5, 0.5))
        Icon_for_next_cond.setImage(images_next_cond)
        # keep track of which components have finished
        show_next_controlComponents = [Icon_for_next_cond]
        for thisComponent in show_next_controlComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "show_next_control" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 2.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Icon_for_next_cond* updates
            
            # if Icon_for_next_cond is starting this frame...
            if Icon_for_next_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Icon_for_next_cond.frameNStart = frameN  # exact frame index
                Icon_for_next_cond.tStart = t  # local t and not account for scr refresh
                Icon_for_next_cond.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Icon_for_next_cond, 'tStartRefresh')  # time at next scr refresh
                # update status
                Icon_for_next_cond.status = STARTED
                Icon_for_next_cond.setAutoDraw(True)
            
            # if Icon_for_next_cond is active this frame...
            if Icon_for_next_cond.status == STARTED:
                # update params
                pass
            
            # if Icon_for_next_cond is stopping this frame...
            if Icon_for_next_cond.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Icon_for_next_cond.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    Icon_for_next_cond.tStop = t  # not accounting for scr refresh
                    Icon_for_next_cond.tStopRefresh = tThisFlipGlobal  # on global time
                    Icon_for_next_cond.frameNStop = frameN  # exact frame index
                    # update status
                    Icon_for_next_cond.status = FINISHED
                    Icon_for_next_cond.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in show_next_controlComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "show_next_control" ---
        for thisComponent in show_next_controlComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-2.000000)
        
        # --- Prepare to start Routine "wait_1s" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        wait_1sComponents = [fix]
        for thisComponent in wait_1sComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "wait_1s" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix* updates
            
            # if fix is starting this frame...
            if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix.frameNStart = frameN  # exact frame index
                fix.tStart = t  # local t and not account for scr refresh
                fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
                # update status
                fix.status = STARTED
                fix.setAutoDraw(True)
            
            # if fix is active this frame...
            if fix.status == STARTED:
                # update params
                pass
            
            # if fix is stopping this frame...
            if fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fix.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    fix.tStop = t  # not accounting for scr refresh
                    fix.tStopRefresh = tThisFlipGlobal  # on global time
                    fix.frameNStop = frameN  # exact frame index
                    # update status
                    fix.status = FINISHED
                    fix.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in wait_1sComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "wait_1s" ---
        for thisComponent in wait_1sComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "random_control_condition" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from execute_codition
        # if the control condition is "watch_Tetris": set Tetris to foreground
        Get_on_top(control_condition)
        # wait one sec
        condition_or_wait_timer("wait")
        # if the control condition is "watch_Tetris": Tetris begins here
        if control_condition == "watch_Tetris":
            # watch Tetris resumes here
            game.toggle_watch.value = not game.toggle_watch.value
        
        # collect start time for logging
        condition_started = globalClock.getTime(format='float')
        
        press_shape.setOpacity(0.0)
        duration_and_fix.setText('+')
        press_button.setOpacity(0.0)
        # keep track of which components have finished
        random_control_conditionComponents = [press_shape, duration_and_fix, press_button]
        for thisComponent in random_control_conditionComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "random_control_condition" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from execute_codition
            # create a press rhythm if enabled by "config_paradigm_psychopy" by changing the opacity of the shape/image periodically
            if control_condition == "motor_control" and Show_motor_rhythm == True:
                press_rhythm = core.getTime()
                if Motor_symbol == "shape":
                    if press_rhythm % (game.speed.value/1000 * 2.5) < (game.speed.value/1000):  
                        press_shape.setOpacity(1)
                    else:
                        press_shape.setOpacity(0)
                elif Motor_symbol == "button":
                    
                    if press_rhythm % (game.speed.value/1000 * 2.5) < (game.speed.value/1000):
                        press_button.setOpacity(1)
                    else:
                        press_button.setOpacity(0)
            
            # *press_shape* updates
            
            # if press_shape is starting this frame...
            if press_shape.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                press_shape.frameNStart = frameN  # exact frame index
                press_shape.tStart = t  # local t and not account for scr refresh
                press_shape.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(press_shape, 'tStartRefresh')  # time at next scr refresh
                # update status
                press_shape.status = STARTED
                press_shape.setAutoDraw(True)
            
            # if press_shape is active this frame...
            if press_shape.status == STARTED:
                # update params
                pass
            
            # if press_shape is stopping this frame...
            if press_shape.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > press_shape.tStartRefresh + control_condition-frameTolerance:
                    # keep track of stop time/frame for later
                    press_shape.tStop = t  # not accounting for scr refresh
                    press_shape.tStopRefresh = tThisFlipGlobal  # on global time
                    press_shape.frameNStop = frameN  # exact frame index
                    # update status
                    press_shape.status = FINISHED
                    press_shape.setAutoDraw(False)
            
            # *duration_and_fix* updates
            
            # if duration_and_fix is starting this frame...
            if duration_and_fix.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                duration_and_fix.frameNStart = frameN  # exact frame index
                duration_and_fix.tStart = t  # local t and not account for scr refresh
                duration_and_fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(duration_and_fix, 'tStartRefresh')  # time at next scr refresh
                # update status
                duration_and_fix.status = STARTED
                duration_and_fix.setAutoDraw(True)
            
            # if duration_and_fix is active this frame...
            if duration_and_fix.status == STARTED:
                # update params
                duration_and_fix.setOpacity(None, log=False)
            
            # if duration_and_fix is stopping this frame...
            if duration_and_fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > duration_and_fix.tStartRefresh + control_duration-frameTolerance:
                    # keep track of stop time/frame for later
                    duration_and_fix.tStop = t  # not accounting for scr refresh
                    duration_and_fix.tStopRefresh = tThisFlipGlobal  # on global time
                    duration_and_fix.frameNStop = frameN  # exact frame index
                    # update status
                    duration_and_fix.status = FINISHED
                    duration_and_fix.setAutoDraw(False)
            
            # *press_button* updates
            
            # if press_button is starting this frame...
            if press_button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                press_button.frameNStart = frameN  # exact frame index
                press_button.tStart = t  # local t and not account for scr refresh
                press_button.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(press_button, 'tStartRefresh')  # time at next scr refresh
                # update status
                press_button.status = STARTED
                press_button.setAutoDraw(True)
            
            # if press_button is active this frame...
            if press_button.status == STARTED:
                # update params
                pass
            
            # if press_button is stopping this frame...
            if press_button.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > press_button.tStartRefresh + Targeted_duration-frameTolerance:
                    # keep track of stop time/frame for later
                    press_button.tStop = t  # not accounting for scr refresh
                    press_button.tStopRefresh = tThisFlipGlobal  # on global time
                    press_button.frameNStop = frameN  # exact frame index
                    # update status
                    press_button.status = FINISHED
                    press_button.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in random_control_conditionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "random_control_condition" ---
        for thisComponent in random_control_conditionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from execute_codition
        # resets opacity
        press_shape.setOpacity(0)
        press_button.setOpacity(0)
        # get offset of the condition
        condition_stopped = globalClock.getTime(format='float')
        
        # if the control condition is "watch_Tetris": pauses Tetris
        if control_condition == "watch_Tetris":
            # watch_Tetris pauses here
            game.toggle_watch.value = not game.toggle_watch.value
            
        # waits one seconds
        condition_or_wait_timer("wait")
        # if the control condition is "watch_Tetris": sets Tetris window to background
        Get_on_top("PsychoPy")
        
        
        # the Routine "random_control_condition" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "condition_ended" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        condition_endedComponents = [condition_ended_text]
        for thisComponent in condition_endedComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "condition_ended" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *condition_ended_text* updates
            
            # if condition_ended_text is starting this frame...
            if condition_ended_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                condition_ended_text.frameNStart = frameN  # exact frame index
                condition_ended_text.tStart = t  # local t and not account for scr refresh
                condition_ended_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(condition_ended_text, 'tStartRefresh')  # time at next scr refresh
                # update status
                condition_ended_text.status = STARTED
                condition_ended_text.setAutoDraw(True)
            
            # if condition_ended_text is active this frame...
            if condition_ended_text.status == STARTED:
                # update params
                condition_ended_text.setOpacity(None, log=False)
            
            # if condition_ended_text is stopping this frame...
            if condition_ended_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > condition_ended_text.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    condition_ended_text.tStop = t  # not accounting for scr refresh
                    condition_ended_text.tStopRefresh = tThisFlipGlobal  # on global time
                    condition_ended_text.frameNStop = frameN  # exact frame index
                    # update status
                    condition_ended_text.status = FINISHED
                    condition_ended_text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in condition_endedComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "condition_ended" ---
        for thisComponent in condition_endedComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "wait_ISI_after_control" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from add_data_control
        # check whether iti variation is enabled in config
        if ISI_variation == True:    
            isi_add = np.random.choice(isis)
        else:
            isi_add = 0
        
        
        # keep track of which components have finished
        wait_ISI_after_controlComponents = [fix_after_control]
        for thisComponent in wait_ISI_after_controlComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "wait_ISI_after_control" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix_after_control* updates
            
            # if fix_after_control is starting this frame...
            if fix_after_control.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix_after_control.frameNStart = frameN  # exact frame index
                fix_after_control.tStart = t  # local t and not account for scr refresh
                fix_after_control.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix_after_control, 'tStartRefresh')  # time at next scr refresh
                # update status
                fix_after_control.status = STARTED
                fix_after_control.setAutoDraw(True)
            
            # if fix_after_control is active this frame...
            if fix_after_control.status == STARTED:
                # update params
                pass
            
            # if fix_after_control is stopping this frame...
            if fix_after_control.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fix_after_control.tStartRefresh + 3 + isi_add-frameTolerance:
                    # keep track of stop time/frame for later
                    fix_after_control.tStop = t  # not accounting for scr refresh
                    fix_after_control.tStopRefresh = tThisFlipGlobal  # on global time
                    fix_after_control.frameNStop = frameN  # exact frame index
                    # update status
                    fix_after_control.status = FINISHED
                    fix_after_control.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in wait_ISI_after_controlComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "wait_ISI_after_control" ---
        for thisComponent in wait_ISI_after_controlComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from add_data_control
        # logs on and offsets and condition duration into one line for later processing
        thisExp.addData('Condition.started', condition_started)
        thisExp.addData('Condition.stopped', condition_stopped)
        thisExp.addData('targeted.duration', control_duration)
        thisExp.addData('Condition.duration', condition_stopped - condition_started)
        thisExp.addData('Condition.info', f'info_{control_condition}')
        
        # the Routine "wait_ISI_after_control" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed n_repeats repeats of 'main_trials'
    
    
    # --- Prepare to start Routine "wait_10sec_for_Trigger" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from wait_10sec_for_trigger_code
    # creates coutdown
    timer_wait_for_trigger = core.CountdownTimer(10)
    # keep track of which components have finished
    wait_10sec_for_TriggerComponents = [wait_10sec_for_trigger_text]
    for thisComponent in wait_10sec_for_TriggerComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "wait_10sec_for_Trigger" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from wait_10sec_for_trigger_code
        # additionally checks whether main_trials are enabled at all
        continueRoutine = skip_if_enabled("main_trials")
        
        # use a while loop to do nothing until the time runs out but can be interuptes by trigger (trigger signal determined by "config_paradigm_psychopy.txt")
        if timer_wait_for_trigger.getTime() <= 0:
            continueRoutine = False # exit the loop  
        # reset timer
        elif defaultKeyboard.getKeys(keyList=[Trigger]):
           timer_wait_for_trigger.reset()
        
        
        
        # *wait_10sec_for_trigger_text* updates
        
        # if wait_10sec_for_trigger_text is starting this frame...
        if wait_10sec_for_trigger_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            wait_10sec_for_trigger_text.frameNStart = frameN  # exact frame index
            wait_10sec_for_trigger_text.tStart = t  # local t and not account for scr refresh
            wait_10sec_for_trigger_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(wait_10sec_for_trigger_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            wait_10sec_for_trigger_text.status = STARTED
            wait_10sec_for_trigger_text.setAutoDraw(True)
        
        # if wait_10sec_for_trigger_text is active this frame...
        if wait_10sec_for_trigger_text.status == STARTED:
            # update params
            wait_10sec_for_trigger_text.setText(f'Wait for remaining triggers...\n\n{round(timer_wait_for_trigger.getTime())}', log=False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in wait_10sec_for_TriggerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "wait_10sec_for_Trigger" ---
    for thisComponent in wait_10sec_for_TriggerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "wait_10sec_for_Trigger" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "End" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from wait_3sec_to_end
    # creates coutdown
    timer_wait_3_sec = core.CountdownTimer(3)
    # keep track of which components have finished
    EndComponents = [end_text, Stop_eyetracker]
    for thisComponent in EndComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "End" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from wait_3sec_to_end
        # due to the eyetracking component not ending the routine an additional routine breaker is needed
        # use a while loop to do nothing until the time runs out 
        if timer_wait_3_sec.getTime() <= 0:
            continueRoutine = False # exit the loop and the routine --> paradigm ends
            
        
        # *end_text* updates
        
        # if end_text is starting this frame...
        if end_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            end_text.frameNStart = frameN  # exact frame index
            end_text.tStart = t  # local t and not account for scr refresh
            end_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end_text, 'tStartRefresh')  # time at next scr refresh
            # update status
            end_text.status = STARTED
            end_text.setAutoDraw(True)
        
        # if end_text is active this frame...
        if end_text.status == STARTED:
            # update params
            pass
        # *Stop_eyetracker* updates
        
        # if Stop_eyetracker is stopping this frame...
        if Stop_eyetracker.status == STARTED:
            if bool(Eye_tracking == True):
                # keep track of stop time/frame for later
                Stop_eyetracker.tStop = t  # not accounting for scr refresh
                Stop_eyetracker.tStopRefresh = tThisFlipGlobal  # on global time
                Stop_eyetracker.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.addData('Stop_eyetracker.stopped', t)
                # update status
                Stop_eyetracker.status = FINISHED
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in EndComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "End" ---
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # make sure the eyetracker recording stops
    if Stop_eyetracker.status != FINISHED:
        Stop_eyetracker.status = FINISHED
    thisExp.nextEntry()
    # the Routine "End" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    # Run 'End Experiment' code from create_processes
    # Terminate game and watch process
    if skip_if_enabled("main_trials") == True:
        play_Tetris.terminate()
        watch_Tetris.terminate()
    log_trigger.stop()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)
    # end 'rush' mode
    core.rush(enable=False)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='comma')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # shut down eyetracker, if there is one
    if deviceManager.getDevice('eyetracker') is not None:
        deviceManager.removeDevice('eyetracker')
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    # shut down eyetracker, if there is one
    if deviceManager.getDevice('eyetracker') is not None:
        deviceManager.removeDevice('eyetracker')
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
