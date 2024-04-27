# This is an edited version of a "Pygame" Tetris game, available from [here](https://github.com/educ8s/Python-Tetris-Game-Pygame)

## Important to check before playing:
- The game only works on windows!
- When not using PsychoPy, only works with Python installed: [download](https://www.python.org/downloads/)
- Needs "Pygame" package installed:
  
  ```shell
  pip install pygame
  ```

## Score system: 
- Down_key = 1 Score Point
- 1 line cleared = 100 Score Points * level
- 2 lines cleared = 300 Score Points * level
- 3 lines cleared = 500 Score Points * level
- 4 lines cleared = 800 Score Points * level

## Level progression:
Defined by [config_tetris_game](config_tetris_game.txt)

## In the folder containing the game there are 7 files besides the README:

1. the main game loop can be found in the Tetris_Psychopy.psyexp file as Tetris_Instance()!

2. [config_tetris_game](config_tetris_game.txt): contains adjustable parameters of the game:
	- Score keeping after "Game Over"
	- Start speed, start level
	- Number of Pretrial rounds
	- etc.

	&rarr; for more infos check descriptions in [config_tetris_game](config_tetris_game.txt)

3. [game.py](game.py) contains the game mechnanics such as moving the blocks, score, difficulty, game reset...; Code from config.txt is executed here 

4. [grid.py](grid.py) contains information about how the grid, in which the blocks/Tetrominoes move, is built

5. [block.py](block.py) contains information about what the blocks/Tetrominoes can do e.g. move, rotate, etc.

6. [blocks.py](blocks.py) contains information about the shape and rotation state of the blocks as type of 2x2, 3x3, 4x4 Matrix depending on the block
	
7. [scale.py](scale.py) extracts information from about screen size, so that the game window is depicted relative to screen size	
	
8. [position.py](position.py) acts as a storage for positioning information about the number of rows and columns in grid 



