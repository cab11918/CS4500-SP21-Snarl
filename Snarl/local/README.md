  
## Local Snarl  
The local_Snarl is an executable which open the Pygame Window for our game. The player can control themselves by using keyboard(For this version, it only supports 1 Player).

### How to run it
To start, simply follow the commands below:

- ``--levels FILENAME`` - The ``FILENAME`` is the name of the level information file. The program only support ``.levels`` file and the path should be correct.
-  ``--players N`` - The ``N`` is the number of players. Right now the program only support 1 Player, thus the input might not change the behavior of the program.
- ``--start N`` - The ``N`` is the number of level the player choose to start from. If the number provided is greater than the level number in ``levels file``, it might cause the program to crash.
- ``--observe`` - This allow the user to enter the observer mode. A Pygame window will popup and display the whole level information.
- After all the configuration were entered, the game will ask for the player name, the player can enter the name and press ``Enter``. After that, a pygame window will popup and the game will start.

### Control

- Use the arrow keys to move the target indicator (↑, ↓, →, ←)
- Press the enter key to confirm the move(⏎, Notice that an invalid move won't change the player's position on board).

### Additional Information

The game will be displayed in a separate Pygame window, but the configuration input and event logs will be printed in Terminal.
 
  
