import pygame
from PyGame_Tetris_Code.colors import Colors
from PyGame_Tetris_Code.scale import Scale

class Grid:
	'''
	The grid class is responsible for the game grid. It contains all the functions that are used to manipulate the grid.

	Attributes:

		num_rows: int, number of rows in the grid
		num_cols: int, number of columns in the grid
		cell_size: int, the size of the cell in the grid
		grid: list, the grid matrix
		colors: dict, the colors of the cells in the grid
		scale: object, the scale class

	Methods:

		print_grid() -> None
			prints the grid
		is_inside(row: int, column: int) -> bool
			checks if a specific cell is inside the grid
		is_empty(row: int, column: int) -> bool
			checks if a specific cell is empty
		is_row_full(row: int) -> bool
			checks if a specific row is full
		clear_row(row: int) -> None
			clears a specific row 
		move_row_down(row: int, num_rows: int) -> None
			moves a specific row down 
		clear_full_rows() -> int
			clears all full rows (if any) and moves the rows above down
		reset() -> None
			resets the grid
		draw(screen: object) -> None
			draws the grid on the screen (pygame.rects)
	'''

	def __init__(self):
		# pass the the scale class for drawing
		self.scale = Scale ()
		# define how many rows and columns the grid has
		self.num_rows = 20
		self.num_cols = 10
		# define how many pixels each cell has
		self.cell_size = 30 * self.scale.scale_factor
		# create a grid matrix with all zeros (no cells occupied by blocks at start)
		self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
		# get colors from the "Colors" class
		self.colors = Colors.get_cell_colors()

	# for testing purposes create a print function that prints the grid
	def print_grid(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				print(self.grid[row][column], end = " ")
			print()
			
	# check whether a specific cell/tile position is inside the grid
	def is_inside(self, row, column):
		if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
			return True
		return False

	# check whether a specific cell of the grid is empry or not
	def is_empty(self, row, column):
		if self.grid[row][column] == 0:
			return True
		return False

	# check whether a specfic row is filled or not
	def is_row_full(self, row):
		for column in range(self.num_cols):
			if self.grid[row][column] == 0:
				return False
		return True

	# clear a specific row 
	def clear_row(self, row):
		for column in range(self.num_cols):
			self.grid[row][column] = 0
	
	# move a specific row one row down (i.e. if the row below was cleared)
	def move_row_down(self, row, num_rows):
		for column in range(self.num_cols):
			self.grid[row+num_rows][column] = self.grid[row][column]
			self.grid[row][column] = 0

	# clears a row if it is completely filled and moves the rows above down with the functions defined above
	def clear_full_rows(self):
		completed = 0
		for row in range(self.num_rows-1, 0, -1):
			if self.is_row_full(row):
				self.clear_row(row)
				completed += 1
			elif completed > 0:
				self.move_row_down(row, completed)
		return completed

	# resets the grid to 0 (i.e. after game over or during visual control mode)
	def reset(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				self.grid[row][column] = 0

	# draws the grid on the screen with "pygame.rect"s
	def draw(self, screen):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				cell_value = self.grid[row][column]
				cell_rect = pygame.Rect(column * self.cell_size + 22 * self.scale.scale_factor + self.scale.x_displacement, row * self.cell_size + 20 * self.scale.scale_factor,
				self.cell_size - 1, self.cell_size - 1)
				# colors are according to block id (i.e. tiles occupied of the o block are "yellow") or "dark_grey" if no block-tile occupies that cell
				pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
