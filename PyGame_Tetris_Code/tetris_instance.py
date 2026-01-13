# This file contains the main function of the game. It is the entry point of the game and starts the game loop.
# In Tetrix_PsychoPy.psyexp the game is started as a subprocess with the mulitprocessing library.  

import pygame
import ctypes
import time
import sys
import os

from PyGame_Tetris_Code.game import Game
from PyGame_Tetris_Code.colors import Colors

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
                    pygame_key_4,
                    replay_movements=False,
                    stack_in_visual_control=True
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
        replay_movements: bool, whether to replay recorded movements in visual control mode (from config_paradigm_psychopy)
        stack_in_visual_control: bool, whether block stacking is enabled in visual control mode (from config_paradigm_psychopy)
    '''

    # Set replay enabled from argument
    # If the argument is passed, it overrides the config_tetris_game setting (which is defaulted to False/undefined)
    game.replay_enabled = replay_movements
    game.stack_in_visual_control = stack_in_visual_control

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
    
    clock = pygame.time.Clock()
    game.calculate_speed()

    start_time = None
    replay_time = 0
    last_time = time.time()
    
    GAME_UPDATE = pygame.USEREVENT
    VISUAL_CONTROL_CAP = pygame.USEREVENT + 1
    
    previous_level = None
    previous_three_next_blocks = None

    screen = pygame.display.set_mode((game.grid.scale.screen_w, game.grid.scale.screen_h), pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption(window_name)
    ctypes.windll.user32.ShowCursor(False)
    
    title_font = pygame.font.Font(None, game.grid.scale.scale_font)
    score_surface = title_font.render("Score", True, Colors.white)
    next_surface = title_font.render("Next", True, Colors.white)
    game_over_surface = title_font.render("GAME OVER", True, Colors.white)
    level_surface = title_font.render("Level", True, Colors.white )    
    score_rect = pygame.Rect(346  * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 70  * game.grid.scale.scale_factor, 170  * game.grid.scale.scale_factor, 60  * game.grid.scale.scale_factor)
   
    # Replay actions
    replay_actions = {
        'left': game.move_left,
        'right': game.move_right,
        'rotate': game.rotate,
        'down': lambda: game.move_down(score_action=True),
        'gravity': game.move_down,
        'reset': lambda: (setattr(game, 'game_over', False), game.reset())
    }

    # Input actions (key -> (method, name))
    # Note: 'down' (pygame_key_1) has special logic so it is handled separately
    key_actions = {
        pygame_key_2: (game.move_left, 'left'),
        pygame_key_3: (game.rotate, 'rotate'),
        pygame_key_4: (game.move_right, 'right')
    }

    # game loop 
    # be catious when changing code in here!
    while True:
        
        now = time.time()
        dt = now - last_time
        last_time = now

        # Preload replay data if valid and paused to avoid graphic glitches at start of replay
        if game.pause == True and game.visual_control == True and game.replay_enabled and not game.is_replaying:
            if game.init_replay(): 
                game.is_replaying = True

        for event in pygame.event.get():
            new_pause_state = pause_state.value
            
            # Detect Pause State Change
            if game.pause != new_pause_state:
                if new_pause_state == False: # Unpausing (Start of Block)
                    if game.visual_control == False:
                        game.init_recording()
                        start_time = time.time()
                    elif game.visual_control == True and game.replay_enabled:
                        # if not already preloaded try to load
                        if not game.is_replaying:
                            if game.init_replay():
                                game.is_replaying = True
                        
                        if game.is_replaying:
                             replay_time = 0 
                        else:
                             game.is_replaying = False
                elif new_pause_state == True: # Pausing (End of Block)
                     
                     if (game.visual_control == False or (game.visual_control == True and not game.replay_enabled)) and game.is_recording:
                         game.save_recording()
                     
                     elif game.visual_control == True and game.replay_enabled:
                         game.is_replaying = False
                         try:
                            if os.path.exists("replay_data.json"): os.remove("replay_data.json")
                         except:
                             pass
            
            game.pause = new_pause_state
      
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    if game.visual_control == True and game.replay_enabled:
                        try:
                            if os.path.exists("replay_data.json"): os.remove("replay_data.json")
                        except:
                            pass
                    elif (game.visual_control == False or (game.visual_control == True and not game.replay_enabled)) and game.is_recording:
                         game.save_recording()
                    pygame.quit()
                    sys.exit()
            
            if event.type == pygame.QUIT:
                 if game.visual_control == True and game.replay_enabled:
                    try:
                        if os.path.exists("replay_data.json"): os.remove("replay_data.json")
                    except:
                        pass
                 elif (game.visual_control == False or (game.visual_control == True and not game.replay_enabled)) and game.is_recording:
                     game.save_recording()
                 pygame.quit()
                 sys.exit()

            if game.pause == False:  
                # Failsafe: Ensure recording starts if game started immediately without unpausing
                if game.visual_control == False and not game.is_recording:
                     start_time = time.time()
                     game.init_recording()

                if game.visual_control == True and not game.is_replaying:
                    if event.type == GAME_UPDATE and game.level.value <= 6: 
                        game.exe_visual_control()
                    if  event.type == VISUAL_CONTROL_CAP and game.level.value >= 6:
                        game.exe_visual_control()
                   
                # checks for keyboard input to play the game and for game over
                if event.type == pygame.KEYDOWN and game.visual_control == False:
                    current_time = time.time() - start_time if start_time else 0
                    
                    if game.game_over == True:
                        game.game_over = False
                        game.reset()
                    
                    elif game.game_over == False:
                        if event.key in key_actions:
                            method, name = key_actions[event.key]
                            method()
                            if game.is_recording: game.record_move(current_time, name)
                        
                        # Handle down movement specially (for acceleration logic)
                        elif event.key == pygame_key_1:
                            game.move_down()
                            if game.is_recording: game.record_move(current_time, 'down')
                            if game.accelerate_down == True and game.start_down is None:
                                game.start_down = time.time()
                        
                if event.type == GAME_UPDATE and game.game_over == False and not game.is_replaying:
                    game.move_down()
                    if game.is_recording:
                         current_time = time.time() - start_time if start_time else 0
                         game.record_move(current_time, 'gravity')

            if game.accelerate_down == True and game.accelerate_type == "hold" and event.type == pygame.KEYUP and event.key == pygame_key_1:                    
                 # resets parameter so the acceleration starts from the same speed each time
                 game.start_down = None                       

        # Replay logic moved here to access updated pause state
        if game.is_replaying and not game.pause:
            replay_time += dt
            while game.replay_move_index < len(game.recorded_moves):
                next_move = game.recorded_moves[game.replay_move_index]
                if replay_time >= next_move['time']:
                    action = next_move['action']
                    if action in replay_actions:
                         replay_actions[action]()
                    game.replay_move_index += 1
                else:
                    break

                                    
                # restart automatically or with a keypress depending on config
                if event.type == GAME_UPDATE and game.game_over == True:

                    if event.type == pygame.KEYDOWN or game.automatic_restart == True:
                        game.game_over = False
                        game.reset()
                        if game.is_recording:
                            current_time = time.time() - start_time if start_time else 0
                            game.record_move(current_time, 'reset')
                        
        if game.accelerate_down == True and game.pause == False and game.game_over == False:
            game.accelerate_downwards()

        score_value_surface = title_font.render(str(game.score.value), True, Colors.white)
        level_value_surface = title_font.render(str(game.level.value), True, Colors.white)
                
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
        
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (386 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 40 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        screen.blit(next_surface, (398 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 200 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        screen.blit(level_surface, (426 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 590 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor))
        screen.blit(level_value_surface, (518 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 590 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor, 20 * game.grid.scale.scale_factor))
        
        if game.game_over == True:
            screen.blit(game_over_surface, (340 * game.grid.scale.scale_factor + game.grid.scale.x_displacement, 540 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor, 50 * game.grid.scale.scale_factor))
        
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0 , 10)
        game.draw(screen)
        
        # if the disply needs to be flipped vertically this function does it
        if flip_vertically == True or flip_horizontally == True:
            original_surf = pygame.display.get_surface() # collect all different surfaces on the screen to a new one
            flipped_surface = pygame.transform.flip(original_surf, flip_vertically, flip_horizontally)
            screen.blit(flipped_surface, dest=(0, 0))
            
        pygame.display.update()
        clock.tick(60)