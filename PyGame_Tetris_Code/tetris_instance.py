# This file contains the main function of the game. It is the entry point of the game and starts the game loop.
# In Tetrix_PsychoPy.psyexp the game is started as a subprocess with the mulitprocessing library.  

# import libraries
import pygame
import ctypes
import time
import sys
# import game classes
from PyGame_Tetris_Code.game import Game
from PyGame_Tetris_Code.colors import Colors

# initialize pygame and game
game = Game()

def Tetris_Instance(
                    window_name,
                    is_control,
                    pretrial,
                    pause_state,
                    game_over_counter,
                    score,
                    level,
                    speed,
                    level_for_main,
                    three_next_blocks,
                    x_array,
                    y_array,
                    weights,
                    flip_vertically,
                    flip_horizontally,
                    pygame_key_1,
                    pygame_key_2,
                    pygame_key_3,
                    pygame_key_4        
):
    
    '''
    This function hosts the game loop and all the game logic. It is the entry point of the game and starts the game loop.
    Updates the game state and the GUI. It also checks for keyboard input and game over conditions.

    Parameters:
        window_name: str, name of the window
        is_control: bool, whether the game is controlled by the AI or not
        pretrial: bool, whether the game is in pretrial mode or not
        pause_state: multiprocessing.Value, shared memory variable to control the pause state
        game_over_counter: multiprocessing.Value, shared memory variable to count the game over events
        score: multiprocessing.Value, shared memory variable to store the score
        level: multiprocessing.Value, shared memory variable to store the level
        speed: multiprocessing.Value, shared memory variable to store the speed
        level_for_main: multiprocessing.Value, shared memory variable to store the level for the main game
        three_next_blocks: multiprocessing.Value, shared memory variable to store whether three next blocks are shown or not
        x_array: multiprocessing.Array, shared memory array to store the x values for the regression - if enabled in config 
        y_array: multiprocessing.Array, shared memory array to store the y values for the regression
        weights: multiprocessing.Array, shared memory array to store the weights for the regression 
        flip_vertically: bool, whether the screen should be flipped vertically or not
        flip_horizontally: bool, whether the screen should be flipped horizontally or not
        pygame_key_1: str, pygame key for moving the block down
        pygame_key_2: str, pygame key for moving the block left
        pygame_key_3: str, pygame key for rotating the block
        pygame_key_4: str, pygame key for moving the block right
    '''

    # transfer Tetris_Instance() parameters from parent to child process
    game.visual_control = is_control
    game.pretrial = pretrial
    game.game_over_counter = game_over_counter
    game.score = score
    game.level = level
    game.speed = speed
    game.level_for_main = level_for_main
    game.three_next_blocks = three_next_blocks
    game.regression.x_array = x_array
    game.regression.y_array = y_array
    game.regression.weights = weights
    
    # set gamespeed
    clock = pygame.time.Clock()
    game.calculate_speed()

    # define the USEREVENTS
    GAME_UPDATE = pygame.USEREVENT
    VISUAL_CONTROL_CAP = pygame.USEREVENT + 1
    
    #set "previous" variables to None
    previous_level = None
    previous_three_next_blocks = None

    # name and initialize GUI
    screen = pygame.display.set_mode((game.grid.scale.screen_w, game.grid.scale.screen_h), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption(window_name)
    ctypes.windll.user32.ShowCursor(False)
    
    # create static graphic objects for the game
    title_font = pygame.font.Font(None, game.grid.scale.scale_font)
    score_surface = title_font.render("Score", True, Colors.white)
    next_surface = title_font.render("Next", True, Colors.white)
    game_over_surface = title_font.render("GAME OVER", True, Colors.white)
    level_surface = title_font.render("Level", True, Colors.white )    
    score_rect = pygame.Rect(346  * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 70  * game.grid.scale.scale_factor, 170  * game.grid.scale.scale_factor, 60  * game.grid.scale.scale_factor)
   
    # game loop 
    # be catious when changing code in here!
    while True:
        for event in pygame.event.get():
            # changes pausing state according to is_paused()
            game.pause = pause_state.value
      
            # defines how to quit the game using ESCAPE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    pygame.quit()
                    sys.exit()
            
            if game.pause == False:  
                # execute visual control mode
                if game.visual_control == True:
                    if event.type == GAME_UPDATE and game.level.value <= 6: 
                        game.exe_visual_control()
                    if  event.type == VISUAL_CONTROL_CAP and game.level.value >= 6:
                        game.exe_visual_control()
                   
                # checks for keyboard input to play the game and for game over
                if event.type == pygame.KEYDOWN and game.visual_control == False:
                    if game.game_over == True:
                        game.game_over = False
                        game.reset()
                    if event.key == pygame_key_2 and game.game_over == False:
                        game.move_left()
                    if event.key == pygame_key_4 and game.game_over == False:
                        game.move_right()
                    if event.key == pygame_key_1 and game.game_over == False:
                        # even if accelerate is enabled this the playing experience is better if you can move the block down one cell manually as well. 
                        game.move_down()
                        if game.accelerate_down == True:
                            # starts down movement by setting the start time "start_down" here
                            game.start_down = time.time()
                        
                    if event.key == pygame_key_3 and game.game_over == False:
                        game.rotate()
                        
                # checks whether its game over or not                               
                if event.type == GAME_UPDATE and game.game_over == False:
                    game.move_down()

                                    
                # restart automatically or with a keypress depending on config
                if event.type == GAME_UPDATE and game.game_over == True:

                    if event.type == pygame.KEYDOWN or game.automatic_restart == True:
                        game.game_over = False
                        game.reset()
                        
            # checks whether down key is lifted to stop acceleration
            if game.accelerate_down == True and game.accelerate_type == "hold" and event.type == pygame.KEYUP and event.key == pygame_key_1:                    
                        # resets parameter so the acceleration starts from the same speed each time
                        game.start_down = None                       
                   

        # logic for the accelerate down movement outside of pygame event
        if game.accelerate_down == True and game.pause == False and game.game_over == False:
            game.accelerate_downwards()

        # create the GUI for score and level     
        score_value_surface = title_font.render(str(game.score.value), True, Colors.white)
        level_value_surface = title_font.render(str(game.level.value), True, Colors.white)
                
        # checks whether level changed and adjusts speed accordingly
        if previous_level != game.level.value:
            game.calculate_speed()
            previous_level = game.level.value
            
        # checks whether game.three_next_blocks.value changed and sets new "height" of rect for NEXT-blocks accordingly
        if previous_three_next_blocks != game.three_next_blocks.value:
            if game.three_next_blocks.value == False:
               next_rect_height = 180 
            else:
               next_rect_height = 285
            # draw next rect
            next_rect = pygame.Rect(346 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 230  * game.grid.scale.scale_factor, 170  * game.grid.scale.scale_factor, next_rect_height * game.grid.scale.scale_factor)
            previous_three_next_blocks = game.three_next_blocks.value 
        
        # creates  GUI for changeable objects
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (386 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 40 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        screen.blit(next_surface, (398 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 200 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        screen.blit(level_surface, (426 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 590 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor))
        screen.blit(level_value_surface, (518 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 590 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor))
        
        # displays game over message
        if game.game_over == True:
            screen.blit(game_over_surface, (340 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 540 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        
        # blit screen elements
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0 , 10)
        game.draw(screen)
        
        # if the disply needs to be flipped vertically this function does it
        if flip_vertically == True or flip_horizontally == True:
            original_surf = pygame.display.get_surface() # collect all different surfaces on the screen to a new one
            flipped_surface = pygame.transform.flip(original_surf, flip_vertically, flip_horizontally)
            screen.blit(flipped_surface, dest=(0, 0))
            
        # updates screen in clock.tick(x) per second
        pygame.display.update()
        clock.tick(60)