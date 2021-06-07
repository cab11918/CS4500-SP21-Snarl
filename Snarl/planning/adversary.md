  
    
**TO:** Manager      
**FROM:** Minghao Yu, Yuan Wang      
**DATE:** 03/27/2021      
**SUBJECT:** Adversary class representation  
      
## Adversary  
The Adversary class is a representation of the enemies in our game.  The adversary will eventually be controlled by AI algorithms. The moving ability and mechanism will be different from the player. It will interact with the game components by using the same logic of turn which was used for ``Player`` component.
  
The Adversary should consist of the following fields:    
* ``id (int)`` - The unique identifier for the Adversary, in future implementation, it could be used for distinguishing the different zombies by color or character image, etc. 
* ``name (str)``  - The string representation of the name which was created when the adversary was registered.
* ``type (str)`` - The string representation of the type of adversaries. It would be "zombie" and "ghost" for now.
* ``vision ([[Tile]])`` - The level information which adversaries have the access of viewing it. It might be a single room layout (if the type is zombie). It should be updated when the level was initialized. 
* `` players_pos ([tuple])`` - The array which represents all the current locations of the players. It would only be updated when the adversary start to move.
* ``position`` - A tuple which represents the current location of the ``Adversary	`` in the game state.
  
## Adversary Interface  
  * ``move()`` -  a function for adversary to return a next step based on the current game state.  
	  * params: None  
	  * return: tuple - a tuple representing the position of next step.  
	  * throw: Exception - if  no possible move can be provided.
  *  ``get_weight(pos)`` - get the weight of potential of the adversary itself moving to that tile. A weight is an int representing the importance to move toward that tile depending on various parameter of the state (i.e. exit status, the closest player around me, closest door, etc.)
	 * params: pos - get the weight of that position related to current position
	 * return: int - an int represent the priority of moving toward this tile.  
	 * throw: IndexError - if the pos is not on the board.
* ``update_status(state)`` - receive update from game_manager and update the vision, players_pos and position.
  * params: state - an updated game state
  * return: None
  * throw: Exception - if the state is malformed.