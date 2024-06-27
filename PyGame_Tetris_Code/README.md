# The game code in this folder is a modified version of a "pygame" Tetris game, available from [here](https://github.com/educ8s/Python-Tetris-Game-Pygame).

## Important to check before playing

- The game only works on windows!
- When not using the PsychoPy standalone version, only works with Python installed: [Download here](https://www.python.org/downloads/)
- Needs "Pygame" package installed:
  
  ```shell
  pip install pygame
  ```

## Score system

- Down_key = 1 score point
	- If you enabled "Accelerate down" in [config_tetris_game](config_tetris_game.txt), each time a block is locked using that method an extra $game.level * 1$ points is given)
- 1 line cleared = 100 score points * level
- 2 lines cleared = 300 score points * level
- 3 lines cleared = 500 score points * level
- 4 lines cleared = 800 score points * level

## Level progression

Defined by [config_tetris_game](config_tetris_game.txt)

## In this folder there are 9 files besides this README.md

1. [config_tetris_game](config_tetris_game.txt): contains adjustable parameters of the game:
	- Score keeping after "Game Over"
	- Start speed, start level
	- Number of Pretrial rounds
	- etc.
	&rarr; for more infos check descriptions in [config_tetris_game.txt](config_tetris_game.txt)

2. [tetris_instance.py](tetris_instance.py) is the main file to run the game. It contains the main loop of the game, the game window and player input handling.

3. [game.py](game.py) contains the game mechanics such as moving the blocks, score, difficulty, game reset...; Code of [config_tetris_game.txt](config_tetris_game.txt) is executed here.

4. [grid.py](grid.py) contains information about how the grid, in which the blocks/Tetrominoes move, is built.

5. [block.py](block.py) contains information about what the blocks/Tetrominoes can do e.g. move, rotate, etc.

6. [blocks.py](blocks.py) contains information about the shape and rotation state of the blocks as type of 2x2, 3x3, 4x4 matrices depending on the block.
	
7. [scale.py](scale.py) extracts information from about screen size, so that the game window is depicted relative to screen size.
	
8. [position.py](position.py) acts as a storage for positioning information about the number of rows and columns in grid.

9. [colors.py](colors.py) contains a class with defining the colors used in the game.

10. [regression.py](regression.py) stores the regression mechanic if the "Jnd_regression" in [config_tetris_game.txt](config_tetris_game.txt) is enabled.