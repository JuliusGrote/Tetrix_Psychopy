import random
import pygame
from multiprocessing import Value
import os
import json
from datetime import datetime
import time

from PyGame_Tetris_Code.blocks import *
from PyGame_Tetris_Code.grid import Grid
from PyGame_Tetris_Code.regression import Regression

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


class Game:
	'''
	define game class with all relevant game mechanics

	Attributes:

		grid: object, the grid class
		regression: object, the regression class
		blocks: list, all the blocks in the game
		current_block: object, the current block
		next_block: object, the next block
		next_next_block: object, the next next block
		next_next_next_block: object, the next next next block
		game_over: bool, game over state
		pretrial: bool, pretrial state
		pretrial_staircase: bool, pretrial staircase state
		pretrial_rounds: int, pretrial rounds
		game_over_counter: int, game over counter
		three_next_blocks: bool, three next blocks state
		toggle_pretrial: bool, toggle pretrial state
		toggle_play: bool, toggle play state
		toggle_watch: bool, toggle watch state
		pause: bool, pause state
		visual_control: bool, visual control state
		level_for_main: float, level for main trials
		level_for_main_factor: float, level for main trials factor
		level: int, level
		score: int, score
		automatic_restart: bool, automatic restart state
		accelerate_down: bool, accelerate down state
		accelerate_type: bool, accelerate type state
		start_down: float, start down acceleration
		start_interval: int, start interval
		down_interval: int, down interval
		speed: int, speed
		total_lines_cleared: int, total lines cleared
		replay_enabled: bool, whether replay of movements is enabled
		recorded_blocks: list, list of blocks used in the recording
		recorded_moves: list, list of moves and their timestamps/types
		replay_block_index: int, index of the current block in the replay
		replay_move_index: int, index of the current move in the replay
		is_recording: bool, whether the game is currently recording moves
		is_replaying: bool, whether the game is currently replaying moves
		stack_in_visual_control: bool, whether blocks stack in visual control mode (even if invisible)

		
	Methods:

		calculate_speed() -> None
			calculate the speed of the game (time interval for block movement)
		exe_visual_control() -> None
			perform a random move in the visual control instead of the player
		update_score(lines_cleared: int, move_down_points: int) -> None
			update the score of the game
		update_level() -> None
			update the level of the game
		get_random_block() -> object
			get a random block from the block list
		rotate() -> None
			rotate the current block by 90 degrees in clockwise direction
		move_left() -> None
			move the current block one cell to the left
		move_right() -> None
			move the current block one cell to the right
		move_down() -> None
			move the current block one cell down
		accelerate_downwards() -> None
			accelerate the down movement of the current block if the accelerate down setting is enabled
		lock_block() -> None
			lock the current block in place on the grid
		reset() -> None
			reset the game grid and various game variables depending on config
		block_fits() -> bool
			check whether the current block fits in the current position
		block_inside() -> bool
			check whether the current block is inside the grid
		draw(screen: object) -> None
			draw the grid and all the blocks in it and the next blocks on the screen
		init_recording() -> None
			initialize the recording of moves
		save_recording() -> None
			save the recorded moves to a json file
		init_replay() -> bool
			initialize the replay of recorded moves
		restore_state(state: dict) -> None
			restore the game state from a dictionary
		unserialize_block(name: str) -> object
			create a block object from its class name
		record_move(elapsed_time: float, action: str) -> None
			record a move with its timestamp and other details
	'''

	def __init__(self):

		# Replay attributes
		
		self.replay_enabled = False # Default, overridden by tetris_instance
		self.recorded_blocks = []
		self.recorded_moves = []
		self.replay_block_index = 0
		self.replay_move_index = 0
		self.is_recording = False
		self.is_replaying = False
		self.last_replay_saved_at = 0.0
		self.last_replay_mtime = 0.0
		self.stack_in_visual_control = True # Default, overridden by tetris_instance
		self.recording_condition = 'pretrial' # Default condition for recording, set by tetris_instance
		
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
				# because they are imported and used in "Tetris_psychopy"

		## regression variables 
		self.regression.weights[Start_level - 1] += 1
		self.jnd_regression = Jnd_regression
		## game over state at game start
		self.game_over = False
		## pretrial design variables
		self.pretrial = None
		self.pretrial_staircase = Pretrial_staircase
		self.pretrial_rounds = Pretrial_rounds
		self.game_over_counter = Value('i', 0)
		## GUI and pause variables
		self.three_next_blocks = Value('b', Toggle_three_next_blocks)
		self.toggle_pretrial = Value('b', Start_Pause)
		self.toggle_play = Value('b', Start_Pause)
		self.toggle_watch = Value('b', Start_Pause)
		self.pause = Start_Pause
		self.visual_control = None
		## game level and score variables
		self.level_for_main = Value('f', 0)
		self.level_for_main_factor = Level_for_main_factor
		self.level = Value('i', Start_level)
		self.score = Value('i', 0)
		## control variables
		self.automatic_restart = Restart_automatically
		self.accelerate_down = Accelerate_down
		self.accelerate_type = Accelerate_type
		self.start_down = None
		self.start_interval = Down_interval
		self.down_interval = Down_interval
		self.speed = Value('i', Start_speed)
		self.total_lines_cleared = 0

	def calculate_speed(self):
		self.speed.value = round(self.regression.speed_formula(self.level.value))
		# sets USEREVENT according to game.speed for "play_Tetris" and "Visual_control" until game.level 7
		pygame.time.set_timer(pygame.USEREVENT, self.speed.value)
		# if game.speed exeeds level 7 use a linear incease for movements of "Visual_Control"
		pygame.time.set_timer(pygame.USEREVENT + 1, round(260 * 8/ self.level.value))


	def exe_visual_control(self):
		possible_moves = [1, 2, 3, 4, 5, 6, 7, 8]
		# choose a random move (each move has differents weights/likelihoods)
		move = visual_rand.choices(possible_moves, weights = ([5 + self.level.value * 6, 5, 5, (20 - self.level.value * 2) / 4 , (19 - self.level.value * 2) / 5, 6, 3, 3])) [0]
		
		# Don't record moves during random visual control (only during replay)
		if self.is_recording and not self.replay_enabled:
			return
		
		actions = {
			# move 1 is just passing time/do nothing
			2: (self.move_left, 'left', 1),
			3: (self.move_right, 'right', 1),
			4: (self.move_down, 'down', 1),
			6: (self.rotate, 'rotate', 1),
			7: (self.move_right, 'right', 2),
			8: (self.move_left, 'left', 2)
		}

		if move in actions:
			method, name, repeats = actions[move]
			for _ in range(repeats):
				method()
				
		
		# this is only performed when down acceleration is enabled
		elif move == 5 and self.accelerate_down:
			self.start_down = time.time()
	
	def update_score(self, lines_cleared, move_down_points):
		# logic to prevent score updating in random visual control (to not affect main trial score)
		if self.visual_control and not self.replay_enabled:
			return

		cleared_points_map = {
			1: One_line_cleared,
			2: Two_lines_cleared,
			3: Three_lines_cleared,
			4: Four_lines_cleared
		}

		if lines_cleared in cleared_points_map:
			if not self.visual_control: # Only update total lines cleared for actual player
				self.total_lines_cleared += lines_cleared
			self.score.value += (cleared_points_map[lines_cleared] * self.level.value)

		if not self.pause:
			# add move down points
			self.score.value += move_down_points
		self.update_level()

	def update_level(self):
		# works only if the level progression in the main trials or pretrials is enabled depending on the current tetris process
		if (Level_progression_main and not self.pretrial) or (self.pretrial and Level_progression_pre):

			if self.total_lines_cleared < Lines_for_levelup:
				return
			
			if self.jnd_regression and self.pretrial:
				self.regression.y_array[self.level.value - 1] += 1

			self.level.value += 1
			self.total_lines_cleared = 0

			if self.jnd_regression and self.pretrial:
				self.regression.weights[self.level.value - 1] += 1

	def get_random_block(self):
		# logic to handle replay of blocks
		if self.is_replaying:
			if len(self.recorded_blocks) > self.replay_block_index:
				block_name = self.recorded_blocks[self.replay_block_index]
				self.replay_block_index += 1
				try:
					block_class = globals()[block_name]
					return block_class()
				except KeyError:
					pass 

		# this makes sure that a single block cannot be chosen two times in row but all the other blocks need to be chosen first
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = block_rand.choice(self.blocks)
		self.blocks.remove(block)
		if self.is_recording:
			self.recorded_blocks.append(type(block).__name__)
		return block
		
	def rotate(self):
		self.current_block.rotate()
		# if the block has no space to move that way undo the move
		if not self.block_inside() or not self.block_fits():
			self.current_block.undo_rotation()

	def move_left(self):
		self.current_block.move(0, -1)
		# if the block has no space to move that way undo the move
		if not self.block_inside() or not self.block_fits():
			self.current_block.move(0, 1)
	
	def move_right(self):
		self.current_block.move(0, 1)
		# if the has no space to move that way undo the move
		if not self.block_inside() or not self.block_fits():
			self.current_block.move(0, -1)
	
	def move_down(self, score_action=False):
		self.current_block.move(1, 0)
		# if the block has no space to move that way undo the move
		if not self.block_inside() or not self.block_fits():
			self.current_block.move(-1, 0)
			# if the block has reached the bottom of the grid (or lands on top of another block) then lock the block in place
			self.lock_block(score_action)
			
	def accelerate_downwards(self):
		if self.start_down and time.time() - self.start_down > self.down_interval:
			# reset time stamp
			self.start_down = time.time()
			# only if time interval is above the cutoff is the time interval further decreased (adjustable in config)
			if self.down_interval > Cutoff_down:
				self.down_interval *= Down_factor	
			self.move_down()
			if self.is_recording:
				# Record with acceleration type if accelerate_down is enabled
				action = f'down_{self.accelerate_type}' if self.accelerate_down else 'down'
				self.record_move(time.time() - self.recording_start_time, action)

	# lock block in place
	def lock_block(self, score_action=False):
		# resets down acceleration if enabled 
		# In replay,there is no have start_down set, ergo trust the score_action flag from the recorder
		if self.accelerate_down and (self.start_down or (self.is_replaying and score_action)):
			# adds score points if down accelaration was used to lock block
			self.update_score(0, Lock_score * self.level.value)
			# reset interval and start_down
			self.start_down = None
			self.down_interval = self.start_interval
			
		# check where the block was positioned in the grid and add those tiles as "barriers"/immovable parts of the grid
		tiles = self.current_block.get_cell_positions()
		# fill the grid at all cell positions the block occupies with its block id
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
			
		# in the visual control ("watch_Tetris" in Tetris_Psychopy) the grid is reset so that blocks do not stack
		# Condition based on config setting Stack_in_visual_control
		# If replay is enabled, do not reset logic/physics even if stack should be hidden visually
		if self.visual_control and not self.stack_in_visual_control and not self.replay_enabled:
			self.grid.reset()

		# get new a block and update next blocks
		if not self.three_next_blocks.value:
			self.current_block = self.next_block
			self.next_block = self.get_random_block()
		else:
			self.current_block = self.next_block
			self.next_block = self.next_next_block
			self.next_next_block = self.next_next_next_block
			self.next_next_next_block = self.get_random_block()

		if self.is_recording:
			self.record_move(time.time() - self.recording_start_time, 'spawn')

		# check for full rows and update score 
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.update_score(rows_cleared, 0)

		# if the locked block does not fit in the current position
		# that means it overlaps with another already locked block and the game is lost
		if not self.block_fits():
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
		# Skip reset if in Visual Control (random mode) unless pretrial config prevents it? 
		# Note: visual_control property might be None during __init__, but reset() is called again later?
		if (not Keep_score_pre and self.pretrial) or (not Keep_score_main and not self.pretrial and not self.visual_control):
			self.score.value = 0

		# during pretrials additional mechanics are called
		if self.pretrial:
			# add level to the mean level reached in the pretrials
			# if "Jnd_regression" is enabled in "config_tetris_game" "game.level_for_main.value" will be overwritten at the end of the routine "play_pretrial" in "Tetris_Psychopy"
			self.level_for_main.value += 1/self.pretrial_rounds * self.level.value
			# increase the game over counter by one
			self.game_over_counter.value += 1
			# if the staircase design is enabled the new level is set here
			if self.pretrial_staircase:
				# if you set a "Restart_round" in the config then the level is reset to "Start_level" every "Restart_round" rounds here
				if Restart_round and self.game_over_counter.value % Restart_round == 0:
					self.level.value = Start_level
				else:					
					# do not reset the level to "Start_level" but multiply by "Stair_factor" defined in config
					self.level.value = round(Stair_factor * self.level.value)

			# if stair case design is not enabled reset level to "Start_level"
			else: 
				self.level.value = Start_level
				
			# add a weight to the new level if "Jnd_regression" is enabled
			if self.jnd_regression and self.game_over_counter.value != self.pretrial_rounds:
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
			if not self.grid.is_empty(tile.row, tile.column):
				return False
		return True
	
	# check whether the block is actually inside the grid					
	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			# all tiles of the block must be inside the grid in order to "return True" (the block is inside the grid)
			if not self.grid.is_inside(tile.row, tile.column):
				return False
		return True

	# draw grid and all the blocks in it and the next blocks
	def draw(self, screen):
		# define a y-shift for the position of the other next blocks compared to the first "next" block
		three_next_blocks_y_shift = 90
		# draw the grid 
		# If stack disabled in visual control, hide blocks visually but keep logic if needed
		draw_blocks = True
		if self.visual_control and not self.stack_in_visual_control:
			draw_blocks = False
			
		self.grid.draw(screen, draw_blocks=draw_blocks)
		# draw the current block at a specific position based on screen size
		self.current_block.draw(screen, 22 * self.grid.scale.scale_factor + self.grid.scale.x_displacement,  20 * self.grid.scale.scale_factor )
		# for the visual control window, check whether the "Hide_next_visual" is enabled in config and do not draw the next blocks if so
		if not Hide_next_visual and self.visual_control or not self.visual_control:
			# if "three_next_blocks" setting is disabled draw only one next block
			if not self.three_next_blocks.value:
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

	def init_recording(self):
		self.is_recording = True
		self.is_replaying = False
		self.recorded_blocks = []
		self.recorded_moves = []
		self.recording_start_time = time.time()
		
		# Capture Initial State
		self.initial_state = {
			'grid': [row[:] for row in self.grid.grid], # Deep copy of grid
			'current_block': {
				'type': type(self.current_block).__name__,
				'rotation_state': self.current_block.rotation_state,
				'row_offset': self.current_block.row_offset,
				'column_offset': self.current_block.column_offset
			},
			'next_blocks': [type(b).__name__ for b in [self.next_block, self.next_next_block, self.next_next_next_block]],
			'score': self.score.value,
			'level': self.level.value,
			'speed': self.speed.value
		}

		# Record initial blocks types anyway for robustness
		for b in [self.current_block, self.next_block, self.next_next_block, self.next_next_next_block]:
			self.recorded_blocks.append(type(b).__name__)
			
		# Log the spawn of the initial block so it appears in the CSV at t=0
		self.record_move(0.0, 'spawn')

	def save_recording(self):
		if not self.is_recording: return
		try:
			data = {
				'saved_at': time.time(),
				'initial_state': getattr(self, 'initial_state', None),
				'blocks': self.recorded_blocks,
				'moves': self.recorded_moves
			}
			with open("replay_data.json", "w") as f:
				json.dump(data, f)
		except Exception as e:
			print(f"Error saving recording: {e}")

	def init_replay(self):
		if not self.replay_enabled: return False
		
		# Check for file existence
		if not os.path.exists("replay_data.json"): 
			if self.last_replay_mtime != 0.0:
				# File disappeared, reset (though we don't clear state)
				self.last_replay_mtime = 0.0
			return False 
		
		# Check modification time to avoid reading/parsing identical file
		try:
			mtime = os.path.getmtime("replay_data.json")
		except OSError:
			return False

		# If file is same or older than last loaded, skip
		if mtime <= self.last_replay_mtime:
			return False

		try:
			with open("replay_data.json", "r") as f:
				data = json.load(f)
			
			# Update mtime tracker immediately
			self.last_replay_mtime = mtime
			
			saved_at = data.get('saved_at', 0.0)
			if saved_at and saved_at <= self.last_replay_saved_at:
				return False
			self.last_replay_saved_at = saved_at
			self.recorded_blocks = data.get('blocks', [])
			self.recorded_moves = data.get('moves', [])
			initial_state = data.get('initial_state', None)
			
			if not self.recorded_blocks and not initial_state: return False
			
			self.is_replaying = True
			self.replay_block_index = 0
			self.replay_move_index = 0
			
			# If full initial state, restore it
			if initial_state:
				self.restore_state(initial_state)
			
			# Fallback for old data: manually reconstruct from block list
			elif len(self.recorded_blocks) >= 4:
				self.reset()
				self.current_block = self.unserialize_block(self.recorded_blocks[0])
				self.next_block = self.unserialize_block(self.recorded_blocks[1])
				self.next_next_block = self.unserialize_block(self.recorded_blocks[2])
				self.next_next_next_block = self.unserialize_block(self.recorded_blocks[3])
				self.replay_block_index = 4
				
			return True
		except Exception as e:
			print(f"Error initializing replay: {e}")
			return False
			
	def restore_state(self, state):
		# Restore Grid
		self.grid.grid = state['grid']
		
		# Restore Level/Score
		self.score.value = state['score']
		self.level.value = state['level']
		self.speed.value = state['speed']
		
		# Restore Blocks
		# Current Block
		block_info = state['current_block']
		self.current_block = self.unserialize_block(block_info['type'])
		self.current_block.rotation_state = block_info['rotation_state']
		self.current_block.row_offset = block_info['row_offset']
		self.current_block.column_offset = block_info['column_offset']

		# Next Blocks
		next_block_names = state['next_blocks']
		self.next_block = self.unserialize_block(next_block_names[0])
		self.next_next_block = self.unserialize_block(next_block_names[1])
		self.next_next_next_block = self.unserialize_block(next_block_names[2])
		
		# Align recorded_blocks index
		# Restore 1 current + 3 next blocks = 4 blocks used
		self.replay_block_index = 4

	def unserialize_block(self, name):
		try:
			return globals()[name]()
		except:
			return IBlock() 


	def record_move(self, elapsed_time, action):
		if self.is_recording:
			try:
				block_type = type(self.current_block).__name__
			except:
				block_type = "Unknown"
			
			self.recorded_moves.append({
				'time': elapsed_time, 
				'abs_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
				'action': action,
				'block': block_type,
				'position_x': self.current_block.column_offset,
				'position_y': self.current_block.row_offset,
				'score': self.score.value,
				'level': self.level.value,
				'game_over_count': self.game_over_counter.value,
				'condition': self.recording_condition
			})