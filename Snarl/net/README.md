## Snarl Server

The Snarl Server is a program which collect the usernames and host the game for the players connected
using ``Snarl Client``.

### How to run it

To start, simply follow the commands below:

- ``--levels FILENAME`` - The ``FILENAME`` is the name of the level information file. The program only
  support ``.levels`` file, and the path should be correct. Default is ``snarl.levels``.
- ``--clients N`` - The ``N`` is the number of clients that allow to be connected. The Snarl game supports maximum of 4
  players and minimum of 1 player, thus the input might not change the behavior of the program. Default is 4.
- ``--wait N`` - The ``N`` is the time ``Snarl Server`` should wait for each    ``Snarl Client``. Once it receives a
  connection and accept the name, it will wait for the next ``Snarl Client`` for N seconds. When the number meets the
  number specified in ``--clients``, the Game will start directly. The ``N`` will be        ``60`` if not specified.
- ``--observe`` - This allows the ``Snarl Server`` to enter the observer mode. A Pygame window will popup and display the
  current game information. It gives the server host an ability to monitor the progress of the game in real-time.
  Default is ``False``(if the map is too big, you need to manually resize the window).
- ``--address IP`` - When ``IP`` was specified, the ``Snarl Server`` will host the game on this IP address. Default is
  127.0.0.1 (local host).
- ``--port NUM`` - A ``NUM`` is a port number the socket will listen to. Default is 45678.

### Additional Information

The information ``Snarl Server`` generated will be displayed in Terminal.

## Snarl Client

The Snarl Client is a program which prompt user for a name to be used in the game and provide a vision and control
system for player to interact with the game.

### How to run it

To start, simply follow the commands below:

- ``--address IP`` - When ``IP`` was specified, the ``Snarl Server`` will host the game on this IP address. Default is
  127.0.0.1 (local host).
- ``--port NUM`` - A ``NUM`` is a port number the socket will listen to. Default is 45678.

### Control

- Use the arrow keys to move the target indicator (↑, ↓, →, ←)
- Press the enter key to confirm the move(⏎, Notice that an invalid move won't change the player's position on board).

### Additional Information

The information ``Snarl Client`` generated will be displayed in Terminal.