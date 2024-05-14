import random
import pygame
from multiprocessing import Value
import ctypes
from blocks import *
from grid import Grid
from regression import Regression
import time

#config file is read and executed
with open("PyGame_Tetris_Code/config_tetris_game.txt", "r") as c_tetris:
	config_tetris = c_tetris.read()
	exec(config_tetris)

pygame.init()



#apply seeds for random.choice() function defined in config_tetris_game.txt
random.seed(Visual_seed)
visual_rand = random.Random()
random.seed(Block_seed)
block_rand = random.Random()

class Game:
	
	def __init__(self):
		
				#define core relevant objects
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.next_next_block = self.get_random_block()
		self.next_next_next_block = self.get_random_block()
		
				#define game mechanism variables
		self.regression = Regression()
		self.regression.weights[Start_level - 1] += 1
		self.jnd_regression = Jnd_regression
		self.game_over = False
		self.pretrial = Pretrial
		self.pretrial_staircase = Pretrial_staircase
		self.pretrial_rounds = Pretrial_rounds
		self.three_next_blocks = Value('b', Toggle_three_next_blocks)
		self.game_over_counter = Value('i', 0)
		self.toggle_pretrial = Value('b', Start_Pause)
		self.toggle_play = Value('b', Start_Pause)
		self.toggle_watch = Value('b', Start_Pause)
		self.pause = Start_Pause
		self.toggle_fullpretrial = Value('b', Start_Fullscreen)
		self.toggle_fullplay = Value('b', Start_Fullscreen)
		self.toggle_fullwatch = Value('b', Start_Fullscreen)
		self.visual_control = Visual_control
		self.level_for_main = Value('f', 0)
		self.level_for_main_factor = Level_for_main_factor
		self.level = Value('i', Start_level)
		self.score = Value('i', 0)
		self.automatic_restart = Restart_automatically
		self.accelerate_down = Accelerate_down
		self.start_down = None
		self.start_interval = Down_interval
		self.down_interval = Down_interval
		self.speed = Value('i', Start_speed)
		self.total_lines_cleared = 0

	# sets the "pygame.USEREVENTs" for the game loop of "Tetris_Instance()" in "Tetris_Psychopy.psyexp"
	def calculate_speed(self):
		self.speed.value = round(self.regression.speed_formula(self.level.value))
		#sets USEREVENT according to game.speed for "play_Tetris" and "Visual_control" until game.level 7
		pygame.time.set_timer(pygame.USEREVENT, self.speed.value)
		#if game.speed exceeds human capanilites use a linear incease for movements of "Visual_Control"
		pygame.time.set_timer(pygame.USEREVENT + 1, round(260 * 6 / self.level.value))

	
	def check_for_Keep_score(self):
		if Keep_score == False:
			self.score.value = 0

	def exe_visual_control(self):
		possible_moves = [1, 2, 3, 4, 5, 6, 7, 8]
		move = visual_rand.choices(possible_moves, weights = ([6 + self.level.value * 1.5, 5, 5, (20 - self.level.value * 2) / 4 , (20 - self.level.value * 2.5) / 3, 6, 3, 3])) [0]
		if move == 1:
			pass
		elif move == 2:
			self.move_left()
		elif move == 3:
			self.move_right()
		elif move == 4:
			self.move_down()
		#this is only performed when 
		elif move == 5 and self.accelerate_down == True:
			#start_down acceleration
			self.start_down = time.time()
		elif move == 6:
			self.rotate()
		elif move == 7:
			self.move_right()
			self.move_right()
		elif move == 8:
			self.move_left()
			self.move_left()
		
			
	def update_score(self, lines_cleared, move_down_points):
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
			self.score.value += move_down_points
		self.update_level()
	
	def update_level(self):
		if Level_progression_main == True or self.pretrial == True:		
			if self.total_lines_cleared >= Lines_for_levelup:
				#add 1 to y_array[old_level]
				if self.jnd_regression == True and self.pretrial == True:
					self.regression.y_array[self.level.value - 1] += 1
				#update level
				self.level.value += 1
				self.total_lines_cleared = 0
				#add to weights[new_level]
				if self.jnd_regression == True and self.pretrial == True:
					self.regression.weights[self.level.value - 1] += 1
			
	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = block_rand.choice(self.blocks)
		self.blocks.remove(block)
		return block
	
	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

			
	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)
	
		
	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()
	#mediates speed up of down acceleration
	def accelerate_downwards(self):
		if self.start_down != None and time.time() - self.start_down > self.down_interval:
			self.start_down = time.time()
			if self.down_interval > Cutoff_down:
				self.down_interval *= Down_factor  # adjust this to control the speed-up rate	
			self.move_down()
			
	def lock_block(self):
		#resets down acceleration if enabled 
		if self.accelerate_down == True and self.start_down != None:
			self.start_down = None
			if self.down_interval <= 0.05:
				self.update_score(0, self.level.value)
			self.down_interval = self.start_interval	
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		if self.visual_control == True:
				self.grid.reset()
		if self.three_next_blocks.value == False:
			self.current_block = self.next_block
			self.next_block = self.get_random_block()
		else:
			self.current_block = self.next_block
			self.next_block = self.next_next_block
			self.next_next_block = self.next_next_next_block
			self.next_next_next_block = self.get_random_block()
			
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.update_score(rows_cleared, 0)
		if self.block_fits() == False:
			self.game_over = True

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.next_next_block = self.get_random_block()
		self.next_next_next_block = self.get_random_block()		
		self.check_for_Keep_score()
		if self.pretrial == True:
			#if "Jnd_regression" is enabled in "config_tetris_game" "game.level_for_main.value" will be overwritten at the end of the routine "play_pretrial"
			self.level_for_main.value += 1/self.pretrial_rounds * self.level.value
			self.game_over_counter.value += 1
			
			if self.pretrial_staircase == True:
				if Restart_round != None and self.game_over_counter.value % Restart_round == 0:
					self.level.value = Start_level
				else:					
					self.level.value = round(Stair_factor * self.level.value)
			else: 
				self.level.value = Start_level
				
			#add a weight to the new level if "Jnd_regression" is enabled
			if self.jnd_regression == True and self.game_over_counter.value != self.pretrial_rounds:
					self.regression.weights[self.level.value - 1] += 1
				
		#restart level for main_trials				
		else: 
			self.level.value = int(self.level_for_main.value)
			
	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True
		
	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
						
	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

	def draw(self, screen):
		three_next_blocks_y_shift = 90
		self.grid.draw(screen)
		self.current_block.draw(screen, 22 * self.grid.scale.scale_factor + self.grid.scale.x_displacement,  20 * self.grid.scale.scale_factor )
		if Hide_next_visual == False and self.visual_control == True or self.visual_control == False:
			if self.three_next_blocks.value == False:
				if self.next_block.id == 3:
					self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 305 * self.grid.scale.scale_factor)
				elif self.next_block.id == 4:
					self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 288 * self.grid.scale.scale_factor)
				else:
					self.next_block.draw(screen, 296 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 288 * self.grid.scale.scale_factor)
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