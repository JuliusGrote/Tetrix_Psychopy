This is an edited version of a "Pygame" Tetris game, available from:

https://github.com/educ8s/Python-Tetris-Game-Pygame

Important to check before playing:

- the game only works on windows!
- only works with Python installed (download from: https://www.python.org/downloads/)
- needs "Pygame" package installed (in windows command type: pip install pygame)

Score system: 

- down_key = 1 Score Point
- 1 line cleared = 100 Score Points * level
- 2 lines cleared = 300 Score Points * level
- 3 lines cleared = 500 Score Points * level
- 4 lines cleared = 800 Score Points * level

Level progression: defined by config.txt

In the folder containing the game there are 7 files besides the README:

1. the main game loop can be found in the Tetris_Psychopy.psyexp file as Tetris_Instance()!

2. config.txt: contains adjustable parameters of the game:
- Score keeping after "Game Over"
- Start speed, start level
- toggling Visual Control
--> for more info check descriptions in config.txt

3. game.py contains the game mechnanics such as moving the blocks, score, difficulty, game reset...; Code from config.txt is executed here 

4. grid.py contains information about how the grid, in which the blocks/Tetrominoes move, is built

5. block.py contains information about what the blocks/Tetrominoes can do e.g. move, rotate, etc.

6. blocks.py contains information about the shape and rotation state of the blocks as type of 2x2, 3x3, 4x4 Matrix depending on the block
	
7. scale.py extracts information from about screen size, so that the game window is depicted relative to screen size	
	
8. position.py acts as a storage for positioning information about the number of rows and columns in grid 



