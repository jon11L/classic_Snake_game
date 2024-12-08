# classic Snake game

## Building the classic snake game with Tkinter module.

- The game is as usual the snake grows when eating an apple. and is done so  with checking and udating coordinates of the block representations for the objects Snake and Food.

- Two different game options (1: Wall limit is off. 2: Wall limit is on.) (New feature) 

- Timer and Score widgets. Reset to 0 on a new party.
- Restart button feature for continous running of the program without having to quit and re run.
- Pause/ Resume feature.
- Best score (new Feature added.) - display the top 3 score at the end of the game. 
    ScoresAre saved through any sessions not only for the current session

----------------------------------------------------------------
----------------------------------------------------------------

self.BASE_SPEED and self.MAX_SPEED can be edited at the top of the Game class 

- BASE_speed to change the speed of the game at the beginning.
- MAX_SPEED Set how fast the snake will move at it's maximum speed.
- self.current_speed (appointed near end of next_turn(), is the logic that control the gradual speed varation)

## Game logic:

'Start of program'

<img src="./screenshots/1.png" alt="some sample photos" width=350>

'choose the game's setting.'

<img src="./screenshots/2.png" alt="some sample photos" width=350>

'in gameplay Pause/Resume button active'

<img src="./screenshots/3.png" alt="some sample photos" width=350>

'Game over / user enter their names if in the top 3.'

<img src="./screenshots/4.png" alt="some sample photos" width=350>

'End of game screen, option to restart'

<img src="./screenshots/5.png" alt="some sample photos" width=350>


