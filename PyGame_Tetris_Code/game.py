# import relevant python packages
import random
import pygame
from multiprocessing import Value
import ctypes
# import classes from the other game files
from blocks import *
from grid import Grid
from regression import Regression
import time

# config file is read and executed
with open("PyGame_Tetris_Code/config_tetris_game.txt", "r") as c_tetris:
	config_tetris = c_tetris.read()
	exec(config_tetris)

pygame.init()



# apply seeds for random.choice() function defined in "config_tetris_game.txt"
random.seed(Visual_seed)
visual_rand = random.Random()
random.seed(Block_seed)
block_rand = random.Random()

# define game class with all relevant game mechanics
class Game:
	
	def __init__(self):
		
				# pass imported classes and define block related objects
		self.grid = Grid()
		self.regression = Regression()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.next_next_block = self.get_random_block()
		self.next_next_next_block = self.get_random_block()
		
				# define game mechanism variables
				# some variables here are defined as "multiprocessing values" 
				# since they need to be synchronized between the main process of "Tetris_Psychopy" and all the different Tetris processes!
				# some variables are defined as class variables ("self.") 
				# because they are imported and used in "Tetris_psychopy"
		## regression variables 
		self.regression.weights[Start_level - 1] += 1
		self.jnd_regression = Jnd_regression
		## game over state at game start
		self.game_over = False
		## pretrial design variables
		self.pretrial = Pretrial
		self.pretrial_staircase = Pretrial_staircase
		self.pretrial_rounds = Pretrial_rounds
		self.game_over_counter = Value('i', 0)
		## GUI and pause variables
		self.three_next_blocks = Value('b', Toggle_three_next_blocks)
		self.toggle_pretrial = Value('b', Start_Pause)
		self.toggle_play = Value('b', Start_Pause)
		self.toggle_watch = Value('b', Start_Pause)
		self.pause = Start_Pause
		self.toggle_fullpretrial = Value('b', Start_Fullscreen)
		self.toggle_fullplay = Value('b', Start_Fullscreen)
		self.toggle_fullwatch = Value('b', Start_Fullscreen)
		self.visual_control = Visual_control
		## game level and score variables
		self.level_for_main = Value('f', 0)
		self.level_for_main_factor = Level_for_main_factor
		self.level = Value('i', Start_level)
		self.score = Value('i', 0)
		## control variables
		self.automatic_restart = Restart_automatically
		self.accelerate_down = Accelerate_down
		self.start_down = None
		self.start_interval = Down_interval
		self.down_interval = Down_interval
		self.speed = Value('i', Start_speed)
		self.total_lines_cleared = 0

	# set the "pygame.USEREVENTs" for the game loop of "Tetris_Instance()" in "Tetris_Psychopy"
	def calculate_speed(self):
		self.speed.value = round(self.regression.speed_formula(self.level.value))
		# sets USEREVENT according to game.speed for "play_Tetris" and "Visual_control" until game.level 7
		pygame.time.set_timer(pygame.USEREVENT, self.speed.value)
		# if game.speed exeeds level 7 use a linear incease for movements of "Visual_Control"
		pygame.time.set_timer(pygame.USEREVENT + 1, round(260 * 8/ self.level.value))

	# check whether score keeping is enabled
	def check_for_Keep_score(self):
		if Keep_score == False:
			self.score.value = 0

	# here the visual control randomizer is defined 
	def exe_visual_control(self):
		# define possible moves
		possible_moves = [1, 2, 3, 4, 5, 6, 7, 8]
		# choose a random move (each move has differents weights/likelihoods)
		move = visual_rand.choices(possible_moves, weights = ([5 + self.level.value * 6, 5, 5, (20 - self.level.value * 2) / 4 , (19 - self.level.value * 2) / 5, 6, 3, 3])) [0]
		# execute chosen move
		if move == 1:
			pass
		elif move == 2:
			self.move_left()
		elif move == 3:
			self.move_right()
		elif move == 4:
			self.move_down()
		# this is only performed when down acceleration is enabled
		elif move == 5 and self.accelerate_down == True:
			# start_down acceleration
			self.start_down = time.time()
		elif move == 6:
			self.rotate()
		elif move == 7:
			self.move_right()
			self.move_right()
		elif move == 8:
			self.move_left()
			self.move_left()
		
	# here, score updates are managed		
	def update_score(self, lines_cleared, move_down_points):
		# depending on how much lines were cleared increase score
		if lines_cleared == 1:
			self.score.value += (100 * self.level.value)
			self.total_lines_cleared += 1
		elif lines_cleared == 2:
			self.score.value += (300 * self.level.value)
			self.total_lines_cleared += 2
		elif lines_cleared == 3:
			self.score.value += (500 * self.level.value)
			self.total_lines_cleared += 3
		elif lines_cleared == 4:
			self.score.value += (800 * self.level.value)
			self.total_lines_cleared += 4
		if self.pause == False:
			# add move down points
			self.score.value += move_down_points
		# depending on how much lines were cleared the level is updated
		self.update_level()

	# here, the level updates are managed
	def update_level(self):
		# works only if the level progression in the main trials or pretrials is enabled depending on the current tetris process
		if Level_progression_main == True and self.pretrial == False or self.pretrial == True and Level_progression_pre == True:		
			if self.total_lines_cleared >= Lines_for_levelup:
				# add 1 to y_array[old_level] if Jnd_regression is enabled in config
				if self.jnd_regression == True and self.pretrial == True:
					self.regression.y_array[self.level.value - 1] += 1
				# update level
				self.level.value += 1
				self.total_lines_cleared = 0
				# add to weights[new_level] if Jnd_regression is enabled in config
				if self.jnd_regression == True and self.pretrial == True:
					self.regression.weights[self.level.value - 1] += 1

	# here, a new random block is chosen each time it is needed
	def get_random_block(self):
		# this makes sure that a single block cannot be chosen two times in row but all the other blocks need to be chosen first
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		# choose random block
		block = block_rand.choice(self.blocks)
		# remove this block from the block array
		self.blocks.remove(block)
		return block

	# rotate the current block clockwise		
	def rotate(self):
		self.current_block.rotate()
		# if the block has no space to move that way undo the move
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
	
	# move the block one to the left on the grid
	def move_left(self):
		self.current_block.move(0, -1)
		# if the block has no space to move that way undo the move
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	# move the block one to the right on the grid		
	def move_right(self):
		self.current_block.move(0, 1)
		# if the has no space to move that way undo the move
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)
	
	# move the block one down on the grid	
	def move_down(self):
		self.current_block.move(1, 0)
		# if the block has no space to move that way undo the move
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			# if the block has reached the bottom of the grid (or lands on top of another block) then lock the block in place
			self.lock_block()
			
	# mediates speed increase of down acceleration
	def accelerate_downwards(self):
	
		if self.start_down != None and time.time() - self.start_down > self.down_interval:
			# reset time stamp
			self.start_down = time.time()
			# only if time interval is above the cutoff is the time interval further decreased (adjustable in config)
			if self.down_interval > Cutoff_down:
				self.down_interval *= Down_factor	
			self.move_down()

	# lock block in place
	def lock_block(self):
		# resets down acceleration if enabled 
		if self.accelerate_down == True and self.start_down != None:
			self.start_down = None
			# adds points depending on the level to the score if down accelaration was used to lock block
			if self.down_interval <= 0.05:
				self.update_score(0, self.level.value)
			# reset interval
			self.down_interval = self.start_interval

		# check where the block was positioned in the grid and add those tiles as "barriers"/immovable parts of the grid
		tiles = self.current_block.get_cell_positions()
		# fill the grid at all cell positions the block occupies with its block id
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		# in the visual control ("watch_Tetris" in Tetris_Psychopy) the grid is reset so that blocks do not stack
		if self.visual_control == True:
				self.grid.reset()

		# get new a block and update next blocks
		if self.three_next_blocks.value == False:
			self.current_block = self.next_block
			self.next_block = self.get_random_block()
		else:
			self.current_block = self.next_block
			self.next_block = self.next_next_block
			self.next_next_block = self.next_next_next_block
			self.next_next_next_block = self.get_random_block()

		# check for full rows and update score 
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.update_score(rows_cleared, 0)

		# if the locked block does not fit in the current position
		# that means it overlaps with another already locked block and the game is lost
		if self.block_fits() == False:
			self.game_over = True

	# manages reset mechanics after "game_over"
	def reset(self):
		# reset the grid
		self.grid.reset()
		# get new blocks
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.next_next_block = self.get_random_block()
		self.next_next_next_block = self.get_random_block()	
		# check for score keeping
		self.check_for_Keep_score()

		# during pretrials additional mechanics are called
		if self.pretrial == True:
			# add level to the mean level reached in the pretrials
			# if "Jnd_regression" is enabled in "config_tetris_game" "game.level_for_main.value" will be overwritten at the end of the routine "play_pretrial" in "Tetris_Psychopy"
			self.level_for_main.value += 1/self.pretrial_rounds * self.level.value
			# increase the game over counter by one
			self.game_over_counter.value += 1
			# if the staircase design is enabled the new level is set here
			if self.pretrial_staircase == True:
				# if you set a "Restart_round" in the config then the level is reset to "Start_level" every "Restart_round" rounds here
				if Restart_round != None and self.game_over_counter.value % Restart_round == 0:
					self.level.value = Start_level
				else:					
					# do not reset the level to "Start_level" but multiply by "Stair_factor" defined in config
					self.level.value = round(Stair_factor * self.level.value)

			# if stair case design is not enabled reset level to "Start_level"
			else: 
				self.level.value = Start_level
				
			# add a weight to the new level if "Jnd_regression" is enabled
			if self.jnd_regression == True and self.game_over_counter.value != self.pretrial_rounds:
					self.regression.weights[self.level.value - 1] += 1
				
		# restart level for "main_trials" ("level_for_main" is set in "Tetris_psychopy")		
		else: 
			self.level.value = int(self.level_for_main.value)

	# check whether a block that needs to be locked fits into the position without colliding with other already locked blocks 
	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			# the necessary tiles must be empty (0) to "return True" 
			# meaning that the current block does not occupy the tile of another already locked block
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True
	
	# check whether the block is actually inside the grid					
	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			# all tiles of the block must be inside the grid in order to "return True" (the block is inside the grid)
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

	# draw grid and all the blocks in it and the next blocks
	def draw(self, screen):
		# define a y-shift for the position of the other next blocks compared to the first "next" block
		three_next_blocks_y_shift = 90
		# draw the grid 
		self.grid.draw(screen)
		# draw the current block at a specific position based on screen size
		self.current_block.draw(screen, 22 * self.grid.scale.scale_factor + self.grid.scale.x_displacement,  20 * self.grid.scale.scale_factor )
		# for the visual control window, check whether the "Hide_next_visual" is enabled in config and do not draw the next blocks if so
		if Hide_next_visual == False and self.visual_control == True or self.visual_control == False:
			# if "three_next_blocks" setting is disabled draw only one next block
			if self.three_next_blocks.value == False:
				# for the I block define a different position since it is a 4x4 matrix compared to the other 3x3 matrix blocks
				if self.next_block.id == 3:
					self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 305 * self.grid.scale.scale_factor)
				# for the o block define a different position since it is a 2x2 matrix compared to the other 3x3 matrix blocks
				elif self.next_block.id == 4:
					self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 288 * self.grid.scale.scale_factor)
				# all other blocks are defined as 3x3 matrices so they can be drawn at the same position on the screen
				else:
					self.next_block.draw(screen, 296 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 288 * self.grid.scale.scale_factor)

			# if the "three_next_blocks" is enabled draw the three next blocks 
			# shift the position of the second and third next block by multiplications of "three_next_blocks_y_shift" - all other aspects stay the same
			else:
				if self.next_block.id == 3:
					self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 270 * self.grid.scale.scale_factor)
				elif self.next_block.id == 4:
					self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 253 * self.grid.scale.scale_factor)
				else:
					self.next_block.draw(screen, 296 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 253 * self.grid.scale.scale_factor)
				if self.next_next_block.id == 3:
				    self.next_next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, (270 + three_next_blocks_y_shift) * self.grid.scale.scale_factor)
				elif self.next_next_block.id == 4:
					self.next_next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, (253 + three_next_blocks_y_shift) * self.grid.scale.scale_factor)
				else:
					self.next_next_block.draw(screen, 296 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, (253 + three_next_blocks_y_shift) * self.grid.scale.scale_factor)
				if self.next_next_next_block.id == 3:
				    self.next_next_next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, (270 + three_next_blocks_y_shift* 2) * self.grid.scale.scale_factor)
				elif self.next_next_next_block.id == 4:
					self.next_next_next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, (253 + three_next_blocks_y_shift * 2) * self.grid.scale.scale_factor)
				else:
					self.next_next_next_block.draw(screen, 296 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, (253 + three_next_blocks_y_shift * 2) * self.grid.scale.scale_factor)