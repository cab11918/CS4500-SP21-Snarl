
**TO:** Manager  
**FROM:** Minghao Yu, Yuan Wang  
**DATE:** 02/15/2021  
**SUBJECT:**  Snarl game states representation


## Snarl game states
For our game state, we would ensure the players and adversaries to have valid moves on the map and we would track the progress of game. 

The game states should consist of the following global variables:
* ``level`` - Indicating the nth level players are in, determing whether the game is over
* ``board`` - A 2D array model representing the current level
* ``turn`` - A flag representing whose turn currently is, switched based on the interaction between players and the game manager
* ``locked`` - A boolean representing whether the key is picked up and the exit is open
* ``players_pos`` - A dictionary representing the data where the key is player's id and the value is the position(``point``)
* ``advers_pos`` - A dictionary representing the data where the key is adversary's id and the value is the position(``point``)
---

To track the player's move, we need to know the player's position (Which tile the player's currently in). A position is a ``x(int)`` and a ``y(int)`` coordinate. The ``Tile`` Object  refers to any tile of a level. We would also track the position of those tiles and the ``type`` of them. For the ``type``, it's also an attribute of ``Tile``. There are 5 types, ``wall``, ``floor``, ``door`` , ``hallway``and ``exit``, for those  types of tile, ``wall`` differed from other four types, is non-walkable and players cannot move to this ``Tile`` with this attribute. ``floor``, ``door`` , ``hallway``and ``exit`` are walkable tiles allowing players to be in. 

## Game State Interface

* ``is_game_over()``:  checks whether the game is over by ``level``, returns True if the ``level`` reaches the predetermined number of levels in Snarl
	* params: none
	* return: boolean
	* throw: none
* ``get_board()``:  returns the ``board`` model
	* params: none
	* return: [[``Tile``]]
	* throw: if no board is initialized
* ``is_valid_move(from, to)``: check whether the given move is valid
	* params: 
		*  from(``Point``): starting point(representing by (x, y))
		* to(``Point``): destination
	* return: boolean
	* throw: if the move is out of bound
* ``move(from, to)``: attempt to move a character(player, adversary) to the designated point
	* params: 
		*  from(``Point``): starting point(representing by (x, y))
		* to(``Point``): destination
	* return: none
	* throw: none (``handled by is_valid_move``）
* ``switch_turn()``: switch the ``turn`` to the subsequent flag and notify the client
	* params: none
	* return: int (the flag representing the player for the next movement)
	* throw: none
* ``advance_level()``: advanced to next level and reinitialize the board
	* params: none
	* return: none
	* throw: none
* ``can_exit()``: check whether players can move to the next level
	* params: none
	* return: boolean
	* throw: none