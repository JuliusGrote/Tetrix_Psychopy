from grid import Grid
from blocks import *
import random
import pygame
from multiprocessing import Value
import ctypes

pygame.init()

#config file is read and executed
with open("PyGame_Tetris_Code/config_tetris_game.txt", "r") as c_tetris:
	config_tetris = c_tetris.read()
	exec(config_tetris)

class Game:
	
	def __init__(self):
		
				#define core relevant objects
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		
				#define game machnism variables
		self.game_over = False
		self.pretrial = True
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
		self.level = Value('i', Start_level)
		self.score = Value('i', 0)
		self.speed = Start_speed
		self.total_lines_cleared = 0

	def calculate_speed(self):
		self.speed = round((Start_speed/1250 - ((self.level.value - 1) * Speed_slope)) ** (self.level.value - 1) * 1000)
		pygame.time.set_timer(pygame.USEREVENT, self.speed)
		pygame.time.set_timer(pygame.USEREVENT + 1, round(260 * 6 / self.level.value))
		
	def check_for_Keep_score(self):
		if Keep_score == False:
			self.score.value = 0

	def exe_visual_control(self):
		self.grid.reset()
		possible_moves = [1, 2, 3, 4, 5, 6, 7]
		move = random.choices(possible_moves, weights = ([15, 4, 4, 13 - self.level.value, 5, 3, 3])) [0]
		if move == 1:
			pass
		elif move == 2:
			self.move_left()
		elif move == 3:
			self.move_right()
		elif move == 4:
			self.move_down()
		elif move == 5:
			self.rotate()
		elif move == 6:
			self.move_right()
			self.move_right()
		elif move == 7:
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
		lines_for_levelup = Lines_for_levelup 
		if self.total_lines_cleared >= lines_for_levelup:
			self.level.value += 1
			self.total_lines_cleared = 0

			
	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
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
			
	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
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
		self.check_for_Keep_score()
		if self.pretrial == True:
			self.level_for_main.value += 1/3 * self.level.value
			self.game_over_counter.value += 1
			self.level.value = Start_level
		elif self.pretrial == False: 
			self.level.value = round(self.level_for_main.value * 0.75)
			
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
		self.grid.draw(screen)
		self.current_block.draw(screen, 22 * self.grid.scale.scale_factor + self.grid.scale.x_displacement,  20 * self.grid.scale.scale_factor )
		if self.next_block.id == 3:
			self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 305 * self.grid.scale.scale_factor)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 283 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 288 * self.grid.scale.scale_factor)
		else:
			self.next_block.draw(screen, 296 * self.grid.scale.scale_factor + self.grid.scale.x_displacement, 288 * self.grid.scale.scale_factor)



		
