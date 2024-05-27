from colors import Colors
import pygame
from position import Position
from scale import Scale

# create a parent class for common features of all the blocks
# most variables and functions are further specified and used by the child (specific) block classes - see "blocks.py"
class Block:
	def __init__(self, id):
		# the id is later defined in the specific block child class in "blocks.py"
		self.id = id
		# the cells are also block specific and defined in the block child class 
		self.cells = {}
		# import the scale class 
		self.scale = Scale()
		# variables important for block positioning
		self.cell_size = 30 * self.scale.scale_factor
		self.row_offset = 0
		self.column_offset = 0
		self.rotation_state = 0
		# get all the colors from the "Colors" class
		self.colors = Colors.get_cell_colors()

	# define a function that moves the block's position
	def move(self, rows, columns):
		self.row_offset += rows
		self.column_offset += columns

	# define a function that gets the current position of the block depending on its rotation state
	def get_cell_positions(self):
		# get current rotation state
		tiles = self.cells[self.rotation_state]
		# create an empty array
		moved_tiles = []
		# append the the new positon of the block to "moved_tiles" based on the how much columns and rows the block has been moved
		# (row_offset and columns_offset)
		for position in tiles:
			position = Position(position.row + self.row_offset, position.column + self.column_offset)
			moved_tiles.append(position)
		return moved_tiles

	# increase the "rotation_state" of a block by increasing it by one and if it reached the last rotation state call the first one again (0)
	def rotate(self):
		self.rotation_state += 1
		if self.rotation_state == len(self.cells):
			self.rotation_state = 0

	# undoes the rotation by decreasing the "rotation_state"
	def undo_rotation(self):
		self.rotation_state -= 1
		if self.rotation_state == -1:
			self.rotation_state = len(self.cells) - 1

	# draw the block based on its current position and with predefined offset on the screen using "pygame.rect"s
	def draw(self, screen, offset_x, offset_y):
		tiles = self.get_cell_positions()
		for tile in tiles:
			tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, 
				offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
			# use colors according to block id as defined in the "Colors" class
			pygame.draw.rect(screen, self.colors[self.id], tile_rect)
