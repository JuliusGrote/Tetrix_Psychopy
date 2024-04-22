#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.1.0),
    on April 19, 2024, at 16:55
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

import psychopy
psychopy.useVersion('2024.1.0')


# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
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
#import necessary packages for Tetris and load them
import ctypes
import pygame
from pynput import keyboard as pynput_keyboard
from multiprocessing import Process, Value
from psychopy.visual.windowwarp import Warper
#ensure that all classes can be imported from this folder
sys.path.append('PyGame_Tetris_Code')
from game import Game
from colors import Colors

#Initialize Pygame and Game
pygame.init()
game = Game()

#get config information
with open("config_paradigm_psychopy.txt", "r") as c_paradigm:
    config_paradigm = c_paradigm.read()
    exec(config_paradigm)

#define Tetris game as a global function 
def Tetris_Instance(
            window_name,
            is_control,
            pretrial,
            pause_state,
            game_over_counter,
            score,
            level,
            level_for_main
    ):
        
    #transfer game parameters from parent to child process
    game.visual_control = is_control
    game.pretrial = pretrial
    game.game_over_counter = game_over_counter
    game.score = score
    game.level = level
    game.level_for_main = level_for_main
    
    #set gamespeed
    clock = pygame.time.Clock()
    game.calculate_speed()
    GAME_UPDATE = pygame.USEREVENT
    VISUAL_CONTROL_CAP = pygame.USEREVENT + 1
    previous_level = game.level.value
    
    #name and initialize GUI
    screen = pygame.display.set_mode((game.grid.scale.screen_w, game.grid.scale.screen_h), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption(window_name)
    ctypes.windll.user32.ShowCursor(False)
    
    #create graphic object for the game
    title_font = pygame.font.Font(None, game.grid.scale.scale_font)
    score_surface = title_font.render("Score", True, Colors.white)
    next_surface = title_font.render("Next", True, Colors.white)
    game_over_surface = title_font.render("GAME OVER", True, Colors.white)
    level_surface = title_font.render("Level", True, Colors.white )
    
    score_rect = pygame.Rect(346  * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 70  * game.grid.scale.scale_factor, 170  * game.grid.scale.scale_factor, 60  * game.grid.scale.scale_factor)
    next_rect = pygame.Rect(346 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 230  * game.grid.scale.scale_factor, 170  * game.grid.scale.scale_factor, 180  * game.grid.scale.scale_factor)
       
    while True:
        for event in pygame.event.get():
        #changes pausing state according to is_paused()
            game.pause = pause_state.value
      
        #defines how to quit the game using ESCAPE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()
            
            if game.pause == False:  
                #execute visual control mode
                if game.visual_control == True:
                    if event.type == GAME_UPDATE and game.level.value <= 6: 
                        game.exe_visual_control()
                    if  event.type == VISUAL_CONTROL_CAP and game.level.value > 6:
                        game.exe_visual_control()
                   
                  #checks forKeyboard input to play the game
                if event.type == pygame.KEYDOWN and game.visual_control == False:
                    if game.game_over == True:
                        game.game_over = False
                        game.reset()
                    if event.key == pygame_key_2 and game.game_over == False:
                        game.move_left()
                    if event.key == pygame_key_4 and game.game_over == False:
                        game.move_right()
                    if event.key == pygame_key_1 and game.game_over == False:
                        game.move_down()
                        game.update_score(0, 1)
                    if event.key == pygame_key_3 and game.game_over == False:
                        game.rotate()
                    
                 #checks whether its game over or not
                if event.type == GAME_UPDATE and game.game_over == False:
                    game.move_down()
                  
                if event.type == GAME_UPDATE and game.game_over == True:
                    game.game_over = False
                    game.reset()
               
             
        score_value_surface = title_font.render(str(game.score.value), True, Colors.white)
        level_value_surface = title_font.render(str(game.level.value), True, Colors.white)
                
        #checks whether level changed and adjusts speed accordingly
        if previous_level != game.level.value:
            game.calculate_speed()
            previous_level = game.level.value
             
        #creates  GUI for changeable objects
            
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (386 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 40 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        screen.blit(next_surface, (398 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 200 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        screen.blit(level_surface, (426 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 590 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor))
        screen.blit(level_value_surface, (518 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 590 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor))
        #displays game over message
        if game.game_over == True:
            screen.blit(game_over_surface, (340 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 450 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
               
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0 , 10)
        #pygamefunction do execute screen instructions
             
        game.draw(screen)
        #if the disply needs to be flipped vertically thus function does it
        if flip_vertically == True or flip_horizontally == True:
            original_surf = pygame.display.get_surface()
            flipped_surface = pygame.transform.flip(original_surf, flip_vertically, flip_horizontally)
            screen.blit(flipped_surface, dest=(0, 0))
            
         #updates screen in clock.tick(x) per second
        pygame.display.update()
        clock.tick(60)
#checks whether a specific window is created
def is_window_open(window_title):        
    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    if hwnd == 0: # Window not found
        return False  
    else:
        return True 

# define function to bring the window with a specific title to the foreground
def Get_on_top(window_title):
    active_window = None
    HWND_TOPMOST = -1
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
    if hwnd != 0:
        active_window = ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        # Simulate left mouse button press and release to make window active(only once)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
        ctypes.windll.user32.ShowCursor(False)
        
# Create a countdown timer with a "x"-second duration or speficific for a condition
def condition_or_wait_timer(name_or_duration): 
    if name_or_duration == "wait":
        t = 1
    elif name_or_duration == "Tetris":
        t = 30
    else:
        t = float(name_or_duration)
    timer = core.CountdownTimer(t)
    # Use a while loop to do nothing until the time runs out
    while timer.getTime() > 0:
        pass
        
#define Pause method for each specific process
def is_paused(process):
    if str(process) == "play_Tetris":
        game.toggle_play.value = not game.toggle_play.value     
    elif str(process) == "watch_Tetris":
        game.toggle_watch.value = not game.toggle_watch.value
    elif str(process) == "pretrial_Tetris":
        game.toggle_pretrial.value = not game.toggle_pretrial.value
# Run 'Before Experiment' code from code_play


# Run 'Before Experiment' code from code_watch


# Run 'Before Experiment' code from code_check_response
#creates an pygame dummy screen to test the pygame.keys that are used
def create_dummi_screen_responsecheck():
    dummi_screen = pygame.display.set_mode((100, 100), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("check_responsebox")
    handle = ctypes.windll.user32.FindWindowW(None, "check_responsebox")

    # Set the desired window position to be outside of the visible window (e.g., 10000 pixels from the left, 1000 pixels from the top)
    window_x, window_y = 10000, 10000
    ctypes.windll.user32.SetWindowPos(handle, -1, window_x, window_y, 0, 0, 0x0001)
# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.1.0'
expName = 'Tetris_fMRI'  # from the Builder filename that created this script
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
        originPath='G:\\Meine Ablage\\Studium\\Bachelorarbeit\\Code\\Tetris_Psychopy\\Tetris_fMRI.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='priority'
    )
    thisExp.setPriority('trigger.t', 30)
    thisExp.setPriority('thisRow.t', 29)
    thisExp.setPriority('Condition.started', 28)
    thisExp.setPriority('Condition.stopped', 27)
    thisExp.setPriority('Condition.duration', 26)
    thisExp.setPriority('condition', 25)
    thisExp.setPriority('participant', 24)
    thisExp.setPriority('game.score', 23)
    thisExp.setPriority('trials.thisTrialN', 22)
    thisExp.setPriority('trials.thisIndex', 21)
    thisExp.setPriority('trials.thisN', 20)
    thisExp.setPriority('trials.thisRepN', 19)
    thisExp.setPriority('targeted_duration', 18)
    thisExp.setPriority('Images_next_cond', 17)
    thisExp.setPriority('notes', 0)
    thisExp.setPriority('play_pretrial.started', -1)
    thisExp.setPriority('play_pretrial.stopped', -2)
    thisExp.setPriority('pretrial_score', -3)
    thisExp.setPriority('pretrial_level_avg', -4)
    thisExp.setPriority('expName', -5)
    thisExp.setPriority('date', -6)
    thisExp.setPriority('expStart', -7)
    thisExp.setPriority('frameRate', -8)
    thisExp.setPriority('psychopyVersion', -9)
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
    ioServer = io.launchHubServer(window=win, **ioConfig)
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
    if deviceManager.getDevice('press_continue_3') is None:
        # initialise press_continue_3
        press_continue_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_3',
        )
    if deviceManager.getDevice('press_continue_4') is None:
        # initialise press_continue_4
        press_continue_4 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_4',
        )
    if deviceManager.getDevice('press_continue_5') is None:
        # initialise press_continue_5
        press_continue_5 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_5',
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
    if deviceManager.getDevice('press_continue_11') is None:
        # initialise press_continue_11
        press_continue_11 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='press_continue_11',
        )
    if deviceManager.getDevice('wait_for_trigger_response') is None:
        # initialise wait_for_trigger_response
        wait_for_trigger_response = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='wait_for_trigger_response',
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
    if flip_vertically == True or flip_horizontally == True:
        
        #warping function provided by psychopy.visual.windowwarper
        warper = Warper(win)
        
        #even if warping function is set warper needs to be updated before changes apply to the display
        #Psychopy uses switched arguments for a vertical and horizontal mirroring compared to "config_paradigm_psychopy.txt"
        warper.changeProjection(None, flipHorizontal = flip_vertically, flipVertical = flip_horizontally)
    
    #create a keyboard listener that collets Trigger by the MR
    #cannot be defined before the experiment due to globalCLock being defined in run(...)
    def check_for_trigger(key):
        try:
            if key.char =='q':
                return False
            if key.char == trigger:
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
        depth=0.0);
    
    # --- Initialize components for Routine "show_pretrial" ---
    check_pretrial = visual.TextStim(win=win, name='check_pretrial',
        text=' check pretrial\n',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
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
        depth=0.0);
    
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
        depth=0.0);
    
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
    # Run 'Begin Experiment' code from code_check_response
    #variables for responsebox check that are displayed on screen
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
    text_check_response = visual.TextStim(win=win, name='text_check_response',
        text='Please press each button on the responsebox twice!',
        font='Open Sans',
        pos=(0, 0.2), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    text_check_response_2 = visual.TextStim(win=win, name='text_check_response_2',
        text='Responses checked successfully!',
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
        text='Welcome to the Tetris experiment',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Text_continue_1 = visual.TextStim(win=win, name='Text_continue_1',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_1 = keyboard.Keyboard(deviceName='press_continue_1')
    
    # --- Initialize components for Routine "explain_pretrial" ---
    explanation_pretrial = visual.TextStim(win=win, name='explanation_pretrial',
        text='During this first part of the experiment, you will play Tetris and get used to the setup!\n\nHow to play:',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=1.5, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Text_continue_2 = visual.TextStim(win=win, name='Text_continue_2',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_2 = keyboard.Keyboard(deviceName='press_continue_2')
    
    # --- Initialize components for Routine "explain_tetris_1" ---
    explain_game_mechanics = visual.ImageStim(
        win=win,
        name='explain_game_mechanics', 
        image='Images/explain_game_mechanics.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0.05), size=(1.75, 0.9),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Text_continue_3 = visual.TextStim(win=win, name='Text_continue_3',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_3 = keyboard.Keyboard(deviceName='press_continue_3')
    
    # --- Initialize components for Routine "explain_tetris_2" ---
    explain_controls = visual.ImageStim(
        win=win,
        name='explain_controls', 
        image='Images/Tetris_explains.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=(1.04, 0.8),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    Controls = visual.TextStim(win=win, name='Controls',
        text='This is how you move the Tetris-Blocks:',
        font='Open Sans',
        pos=(0, 0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_4 = visual.TextStim(win=win, name='Text_continue_4',
        text='Press any button to start the first TETRIS-GAME!',
        font='Open Sans',
        pos=(0.0, -0.45), height=0.05, wrapWidth=2.0, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_4 = keyboard.Keyboard(deviceName='press_continue_4')
    
    # --- Initialize components for Routine "wait_1s" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "play_pretrial" ---
    fix_2 = visual.TextStim(win=win, name='fix_2',
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
    
    # --- Initialize components for Routine "intro_main" ---
    intro_main_text = visual.TextStim(win=win, name='intro_main_text',
        text='Now the main part of the experiment begins!',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    text_continue_5 = visual.TextStim(win=win, name='text_continue_5',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    press_continue_5 = keyboard.Keyboard(deviceName='press_continue_5')
    
    # --- Initialize components for Routine "explanation_basic_structure" ---
    Announcement = visual.TextStim(win=win, name='Announcement',
        text='During the Experiment you will encounter 4 different symbols:',
        font='Open Sans',
        pos=(0, 0.2), height=0.1, wrapWidth=1.8, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
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
        image='Images/hand.png', mask=None, anchor='center',
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
    press_continue_6 = keyboard.Keyboard(deviceName='press_continue_6')
    Text_continue_6 = visual.TextStim(win=win, name='Text_continue_6',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-6.0);
    
    # --- Initialize components for Routine "explain_play_Tetris" ---
    controller_example = visual.ImageStim(
        win=win,
        name='controller_example', 
        image='Images/controller.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0), size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    play_Tetris_text = visual.TextStim(win=win, name='play_Tetris_text',
        text='Controller: Play the game! Try to focus on MENTALLY ROTATING the blocks when playing! The starting level is adjusted based on the level you reached in the earlier rounds!',
        font='Open Sans',
        pos=(0.2, 0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_7 = visual.TextStim(win=win, name='Text_continue_7',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_7 = keyboard.Keyboard(deviceName='press_continue_7')
    
    # --- Initialize components for Routine "explain_motor_control" ---
    motorcontrol_example = visual.ImageStim(
        win=win,
        name='motorcontrol_example', 
        image='Images/hand.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0.0), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    text_motor = visual.TextStim(win=win, name='text_motor',
        text='Hand: Press the Buttons ALTERNATELY (one after another) to the rhythm displayed on the screen!',
        font='Open Sans',
        pos=(0.2, 0.0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_8 = visual.TextStim(win=win, name='Text_continue_8',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_8 = keyboard.Keyboard(deviceName='press_continue_8')
    
    # --- Initialize components for Routine "explain_watch_Tetris" ---
    watch_example = visual.ImageStim(
        win=win,
        name='watch_example', 
        image='Images/eye.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0.0), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    text_watch = visual.TextStim(win=win, name='text_watch',
        text='Eye: Watch Tetris! Just look at the screen while a game recording is played for you. Do not press any buttons!',
        font='Open Sans',
        pos=(0.2, 0.0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_9 = visual.TextStim(win=win, name='Text_continue_9',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_9 = keyboard.Keyboard(deviceName='press_continue_9')
    
    # --- Initialize components for Routine "explain_fixation_cross" ---
    baseline_example = visual.ImageStim(
        win=win,
        name='baseline_example', 
        image='Images/crosshair.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.65, 0.0), size=(0.2, 0.2),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    text_cross = visual.TextStim(win=win, name='text_cross',
        text='Fixation Cross: just look at the cross in the middle of the screen and do nothing else!',
        font='Open Sans',
        pos=(0.2, 0.0), height=0.06, wrapWidth=1.25, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    Text_continue_10 = visual.TextStim(win=win, name='Text_continue_10',
        text='Press any button to continue!',
        font='Open Sans',
        pos=(0, -0.45), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    press_continue_10 = keyboard.Keyboard(deviceName='press_continue_10')
    
    # --- Initialize components for Routine "start_experiment" ---
    Start = visual.TextStim(win=win, name='Start',
        text='Now, the experiment starts!',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    Text_continue_11 = visual.TextStim(win=win, name='Text_continue_11',
        text='Press any button to start!',
        font='Open Sans',
        pos=(0, -0.4), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
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
    wait_for_trigger_response = keyboard.Keyboard(deviceName='wait_for_trigger_response')
    
    # --- Initialize components for Routine "Show_next_Cond" ---
    Icon_for_next_cond = visual.ImageStim(
        win=win,
        name='Icon_for_next_cond', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), size=1.0,
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "Condition" ---
    press_cross = visual.ShapeStim(
        win=win, name='press_cross', vertices='cross',
        size=(0.075, 0.075),
        ori=0.0, pos=(0, 0), anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=1.0, depth=-1.0, interpolate=True)
    duration_and_fix = visual.TextStim(win=win, name='duration_and_fix',
        text='+',
        font='Open Sans',
        pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "wait_1s_after_cond" ---
    fix_after_cond = visual.TextStim(win=win, name='fix_after_cond',
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
    End_Font = visual.TextStim(win=win, name='End_Font',
        text='Thank you for your Participation!',
        font='Open Sans',
        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
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
    #creates a seperate process for the Pretrial rounds so that the experiment can continue
    pretrial_Tetris = Process(target=Tetris_Instance, args=(
                              "pretrial_Tetris",
                              False,
                              True,
                              game.toggle_pretrial,
                              game.game_over_counter,
                              game.score,
                              game.level,
                              game.level_for_main
                              ))
    pretrial_Tetris.start()
    
    #creates a seperate process for the Game so that the experiment can continue
    play_Tetris = Process(target=Tetris_Instance, args=(
                          "play_Tetris",
                          False,
                          False,
                          game.toggle_play,
                          game.game_over_counter,
                          game.score,
                          game.level,
                          game.level_for_main,
                          ))
    play_Tetris.start()
    #create a window for the controll visual_control condition
    watch_Tetris = Process(target=Tetris_Instance, args=(
                           "watch_Tetris",
                           True,
                           False,
                           game.toggle_watch,
                           game.game_over_counter,
                           game.score,
                           game.level,
                           game.level_for_main,
                           ))
    watch_Tetris.start()
    
    #start keyboard listener
    log_trigger = pynput_keyboard.Listener(on_press=check_for_trigger)
    log_trigger.start()
    
    #hides cursor that appears automatically after processes are created
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
    print(game.toggle_pretrial.value)
    print(game.toggle_play.value)
    print(game.toggle_watch.value)
    thisExp.nextEntry()
    # the Routine "load_processes" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "check_for_processes" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code_2
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
        
        # *check_pretrial* updates
        
        # if check_pretrial is starting this frame...
        if check_pretrial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    is_paused("pretrial_Tetris")
    is_paused("pretrial_Tetris")
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
    #set Tetris to foreground
    Get_on_top("play_Tetris")
    is_paused("play_Tetris")
    is_paused("play_Tetris")
    
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
    is_paused("watch_Tetris")
    is_paused("watch_Tetris")
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
        #checks keys and updated variables accordingly
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame_key_1:
                    if x_1 == '-':
                        x_1 = '1'
                    elif x_1 == '1':
                        x_1_1 = '1'
                if event.key == pygame_key_2:
                    if x_2 == '-':
                        x_2 = '2'
                    elif x_2 == '2':
                        x_2_2 = '2'
                if event.key == pygame_key_3:
                    if x_3 == '-':
                        x_3 = '3'
                    elif x_3 == '3':
                        x_3_3 = '3'
                if event.key == pygame_key_4:
                    if x_4 == '-':
                        x_4 = '4'
                    elif x_4 == '4':
                        x_4_4 = '4'
                if event.key == pygame_key_5:
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
    #ends pygame instance
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
    
    # --- Prepare to start Routine "explain_tetris_1" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_3.keys = []
    press_continue_3.rt = []
    _press_continue_3_allKeys = []
    # keep track of which components have finished
    explain_tetris_1Components = [explain_game_mechanics, Text_continue_3, press_continue_3]
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
        
        # *explain_game_mechanics* updates
        
        # if explain_game_mechanics is starting this frame...
        if explain_game_mechanics.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            explain_game_mechanics.frameNStart = frameN  # exact frame index
            explain_game_mechanics.tStart = t  # local t and not account for scr refresh
            explain_game_mechanics.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(explain_game_mechanics, 'tStartRefresh')  # time at next scr refresh
            # update status
            explain_game_mechanics.status = STARTED
            explain_game_mechanics.setAutoDraw(True)
        
        # if explain_game_mechanics is active this frame...
        if explain_game_mechanics.status == STARTED:
            # update params
            pass
        
        # *Text_continue_3* updates
        
        # if Text_continue_3 is starting this frame...
        if Text_continue_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
        if press_continue_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
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
    press_continue_4.keys = []
    press_continue_4.rt = []
    _press_continue_4_allKeys = []
    # keep track of which components have finished
    explain_tetris_2Components = [explain_controls, Controls, Text_continue_4, press_continue_4]
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
    
    # --- Prepare to start Routine "play_pretrial" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('play_pretrial.started', globalClock.getTime(format='float'))
    # Run 'Begin Routine' code from Tetris_pretrial
    #puts preTrial Tetris-Window on top
    Get_on_top("pretrial_Tetris")
    #waits one sec
    condition_or_wait_timer("wait")
    #start Tetris
    is_paused("pretrial_Tetris")
    # keep track of which components have finished
    play_pretrialComponents = [fix_2]
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
        
        # if fix_2 is stopping this frame...
        if fix_2.status == STARTED:
            if bool(game.game_over_counter.value == 3):
                # keep track of stop time/frame for later
                fix_2.tStop = t  # not accounting for scr refresh
                fix_2.tStopRefresh = tThisFlipGlobal  # on global time
                fix_2.frameNStop = frameN  # exact frame index
                # update status
                fix_2.status = FINISHED
                fix_2.setAutoDraw(False)
        
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
    #adds the achieved level and score to the data file
    thisExp.addData('pretrial_score', game.score.value)
    #resets absolut score
    game.score.value = 0
    thisExp.addData('pretrial_level_avg', game.level_for_main.value)
    #sets new start level for main game
    game.level.value = round(game.level_for_main.value * 0.75)
    
    #ends pretrial pygame
    pretrial_Tetris.terminate()
    pretrial_Tetris.join()
    
    Get_on_top("PsychoPy")
    thisExp.nextEntry()
    # the Routine "play_pretrial" was not non-slip safe, so reset the non-slip timer
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
    
    # --- Prepare to start Routine "explanation_basic_structure" ---
    continueRoutine = True
    # update component parameters for each repeat
    press_continue_6.keys = []
    press_continue_6.rt = []
    _press_continue_6_allKeys = []
    # keep track of which components have finished
    explanation_basic_structureComponents = [Announcement, controller_example_1, watch_example_1, motorcontrol_example_1, baseline_example_1, press_continue_6, Text_continue_6]
    for thisComponent in explanation_basic_structureComponents:
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
    
    # --- Run Routine "explanation_basic_structure" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
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
        for thisComponent in explanation_basic_structureComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "explanation_basic_structure" ---
    for thisComponent in explanation_basic_structureComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    # the Routine "explanation_basic_structure" was not non-slip safe, so reset the non-slip timer
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
    thisExp.addData('explain_watch_Tetris.started', globalClock.getTime(format='float'))
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
    thisExp.addData('explain_watch_Tetris.stopped', globalClock.getTime(format='float'))
    thisExp.nextEntry()
    # the Routine "explain_watch_Tetris" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "explain_fixation_cross" ---
    continueRoutine = True
    # update component parameters for each repeat
    thisExp.addData('explain_fixation_cross.started', globalClock.getTime(format='float'))
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
    thisExp.addData('explain_fixation_cross.stopped', globalClock.getTime(format='float'))
    thisExp.nextEntry()
    # the Routine "explain_fixation_cross" was not non-slip safe, so reset the non-slip timer
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
    # Run 'Begin Routine' code from log_first_trigger
    thisExp.addData('condition', 'first_trigger')
    wait_for_trigger_response.keys = []
    wait_for_trigger_response.rt = []
    _wait_for_trigger_response_allKeys = []
    # keep track of which components have finished
    wait_for_triggerComponents = [wait_for_trigger_text, wait_for_trigger_response]
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
        
        # *wait_for_trigger_response* updates
        waitOnFlip = False
        
        # if wait_for_trigger_response is starting this frame...
        if wait_for_trigger_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            wait_for_trigger_response.frameNStart = frameN  # exact frame index
            wait_for_trigger_response.tStart = t  # local t and not account for scr refresh
            wait_for_trigger_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(wait_for_trigger_response, 'tStartRefresh')  # time at next scr refresh
            # update status
            wait_for_trigger_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(wait_for_trigger_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(wait_for_trigger_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if wait_for_trigger_response.status == STARTED and not waitOnFlip:
            theseKeys = wait_for_trigger_response.getKeys(keyList=['t'], ignoreKeys=["escape"], waitRelease=False)
            _wait_for_trigger_response_allKeys.extend(theseKeys)
            if len(_wait_for_trigger_response_allKeys):
                wait_for_trigger_response.keys = _wait_for_trigger_response_allKeys[-1].name  # just the last key pressed
                wait_for_trigger_response.rt = _wait_for_trigger_response_allKeys[-1].rt
                wait_for_trigger_response.duration = _wait_for_trigger_response_allKeys[-1].duration
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
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('loop_template.xlsx'),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    
    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
        )
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "Show_next_Cond" ---
        continueRoutine = True
        # update component parameters for each repeat
        Icon_for_next_cond.setSize((0.5, 0.5))
        Icon_for_next_cond.setImage(Images_next_cond)
        # keep track of which components have finished
        Show_next_CondComponents = [Icon_for_next_cond]
        for thisComponent in Show_next_CondComponents:
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
        
        # --- Run Routine "Show_next_Cond" ---
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
            for thisComponent in Show_next_CondComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Show_next_Cond" ---
        for thisComponent in Show_next_CondComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-2.000000)
        
        # --- Prepare to start Routine "Condition" ---
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from execute_codition
        #set Tetris to foreground
        Get_on_top(condition)
        
        #initialize press rhythm
        if condition == "motor_control" and show_motor_rhythm == True:
            pygame.init()
            game.calculate_speed()
        
        #wait one sec
        condition_or_wait_timer("wait")
        #Tetris begins here
        is_paused(condition)
        
        #collect start time for logging
        condition_started = globalClock.getTime(format='float')
        
        press_cross.setOpacity(0.0)
        # keep track of which components have finished
        ConditionComponents = [press_cross, duration_and_fix]
        for thisComponent in ConditionComponents:
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
        
        # --- Run Routine "Condition" ---
        routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # Run 'Each Frame' code from execute_codition
            #created a press rhythm if enabled by "config_paradigm_psychopy.txt" by changing the opacity of the cross shape periodically
            if condition == "motor_control" and show_motor_rhythm == True:
                press_rhythm = core.getTime()
                if press_rhythm % (game.speed/1000 * 2) < (game.speed/2000):   
                    press_cross.setOpacity(1)
                else:
                    press_cross.setOpacity(0)
            
            # *press_cross* updates
            
            # if press_cross is starting this frame...
            if press_cross.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                press_cross.frameNStart = frameN  # exact frame index
                press_cross.tStart = t  # local t and not account for scr refresh
                press_cross.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(press_cross, 'tStartRefresh')  # time at next scr refresh
                # update status
                press_cross.status = STARTED
                press_cross.setAutoDraw(True)
            
            # if press_cross is active this frame...
            if press_cross.status == STARTED:
                # update params
                pass
            
            # if press_cross is stopping this frame...
            if press_cross.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > press_cross.tStartRefresh + targeted_duration-frameTolerance:
                    # keep track of stop time/frame for later
                    press_cross.tStop = t  # not accounting for scr refresh
                    press_cross.tStopRefresh = tThisFlipGlobal  # on global time
                    press_cross.frameNStop = frameN  # exact frame index
                    # update status
                    press_cross.status = FINISHED
                    press_cross.setAutoDraw(False)
            
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
                if tThisFlipGlobal > duration_and_fix.tStartRefresh + targeted_duration-frameTolerance:
                    # keep track of stop time/frame for later
                    duration_and_fix.tStop = t  # not accounting for scr refresh
                    duration_and_fix.tStopRefresh = tThisFlipGlobal  # on global time
                    duration_and_fix.frameNStop = frameN  # exact frame index
                    # update status
                    duration_and_fix.status = FINISHED
                    duration_and_fix.setAutoDraw(False)
            
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
            for thisComponent in ConditionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Condition" ---
        for thisComponent in ConditionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from execute_codition
        #resets opacity
        press_cross.setOpacity(0)
        #get offset of the condition
        condition_stopped = globalClock.getTime(format='float')
        #pauses Tetris
        is_paused(condition)
        #waits one seconds
        condition_or_wait_timer("wait")
        #sets Tetris window to background
        Get_on_top("PsychoPy")
        
        
        # the Routine "Condition" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "wait_1s_after_cond" ---
        continueRoutine = True
        # update component parameters for each repeat
        # keep track of which components have finished
        wait_1s_after_condComponents = [fix_after_cond]
        for thisComponent in wait_1s_after_condComponents:
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
        
        # --- Run Routine "wait_1s_after_cond" ---
        routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix_after_cond* updates
            
            # if fix_after_cond is starting this frame...
            if fix_after_cond.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix_after_cond.frameNStart = frameN  # exact frame index
                fix_after_cond.tStart = t  # local t and not account for scr refresh
                fix_after_cond.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix_after_cond, 'tStartRefresh')  # time at next scr refresh
                # update status
                fix_after_cond.status = STARTED
                fix_after_cond.setAutoDraw(True)
            
            # if fix_after_cond is active this frame...
            if fix_after_cond.status == STARTED:
                # update params
                pass
            
            # if fix_after_cond is stopping this frame...
            if fix_after_cond.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fix_after_cond.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    fix_after_cond.tStop = t  # not accounting for scr refresh
                    fix_after_cond.tStopRefresh = tThisFlipGlobal  # on global time
                    fix_after_cond.frameNStop = frameN  # exact frame index
                    # update status
                    fix_after_cond.status = FINISHED
                    fix_after_cond.setAutoDraw(False)
            
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
            for thisComponent in wait_1s_after_condComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "wait_1s_after_cond" ---
        for thisComponent in wait_1s_after_condComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # Run 'End Routine' code from add_data_condition
        #logs on and offsets and condition duration into one line for later processing
        thisExp.addData('Condition.started', condition_started)
        thisExp.addData('Condition.stopped', condition_stopped)
        thisExp.addData('Condition.duration', condition_stopped - condition_started)
        if condition == "play_Tetris":
            thisExp.addData('game.score', game.score.value)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if routineForceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        thisExp.nextEntry()
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
    # completed 1.0 repeats of 'trials'
    
    
    # --- Prepare to start Routine "wait_10sec_for_Trigger" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from wait_10sec_for_trigger_code
    #creates coutdown
    timer = core.CountdownTimer(10)
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
        # Use a while loop to do nothing until the time runs out but can be interuptes by trigger (trigger signal determined by "config_paradigm_psychopy.txt")
        if timer.getTime() <= 0:
            continueRoutine = False # Exit the loop  
        #reset timer
        elif defaultKeyboard.getKeys(keyList=["t"]):
           timer.reset()
        
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
            wait_10sec_for_trigger_text.setText(f'Wait for remaining triggers...\n\n{round(timer.getTime())}', log=False)
        
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
    # keep track of which components have finished
    EndComponents = [End_Font]
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
    while continueRoutine and routineTimer.getTime() < 3.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *End_Font* updates
        
        # if End_Font is starting this frame...
        if End_Font.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            End_Font.frameNStart = frameN  # exact frame index
            End_Font.tStart = t  # local t and not account for scr refresh
            End_Font.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(End_Font, 'tStartRefresh')  # time at next scr refresh
            # update status
            End_Font.status = STARTED
            End_Font.setAutoDraw(True)
        
        # if End_Font is active this frame...
        if End_Font.status == STARTED:
            # update params
            pass
        
        # if End_Font is stopping this frame...
        if End_Font.status == STARTED:
            # is it time to stop? (based on local clock)
            if tThisFlip > 3-frameTolerance:
                # keep track of stop time/frame for later
                End_Font.tStop = t  # not accounting for scr refresh
                End_Font.tStopRefresh = tThisFlipGlobal  # on global time
                End_Font.frameNStop = frameN  # exact frame index
                # update status
                End_Font.status = FINISHED
                End_Font.setAutoDraw(False)
        
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
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-3.000000)
    thisExp.nextEntry()
    # Run 'End Experiment' code from create_processes
    #Terminate game and watch process
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
