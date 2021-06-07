
  
**TO:** Manager    
**FROM:** Minghao Yu, Yuan Wang    
**DATE:** 03/01/2021    
**SUBJECT:** Player class representation
    
## Player
The Player class is a representation of the user who is interacting  with the game. It stores the information needed for the user and update them according to Game Manager.

The Player should consist of the following fields:  
* ``id (int)`` - The unique identifier for the Player, it will be used when the fields were updated by Game Manager.
* ``name (str)`` - A unique text representation of the Player's identity when playing the game.
* ``avatar (img)`` - A visual representation of the character controlled by player in the game (we specify the format of the image to be PNG for now).
* ``position [x,y]`` - A tuple which represents the location for the player in the ``curr_level``.  
* ``expelled (bool)`` - A  Boolean which represents whether the Player was expelled by the Adversary. 
* ``is_movable (bool)`` - A Boolean which represents whether the player can move(or to say, whether it's the player's turn). 
* ``vision [[Tile]]`` -  A 5x5 2D array of ``Tile``. This would be a part of the ``Level`` map which are visible to the player which contains all the information of the ``Level`` (e.g. type of the ``Tile``, ``Adversary``, ``Key`` and other ``Player``, etc.)
*  ``destination [x,y]`` -A Tuple which represents the location the player want to reach in their turn, the player can also choose to stay put and the ``destination`` remains unchanged.

## Player Interface
  
* ``set_pos(x,y)``:  a function which updates the  tuple value of the ``position`` according to changes in Game Manager.
   * params: pos - a tuple which represents the position.
   * return: None
   * throw: TypeError - if the ``position`` was not initialized.
* ``set_expelled(bool)``:  a function which updates the Boolean value of ``expelled`` according to changes in Game Manager.
   * params: expelled - a Boolean which represents the status of the Player is dead or alive.
   * return: None
   * throw: TypeError - if the ``expelled`` was not initialized.
* ``set_mobility(bool)``: a function which updates the Boolean value which represents if the player can take action right now.
   * params: can_move - a Boolean which represents ``is_movable``.
   * return: None  
   * throw: TypeError - if the ``is_movable`` was not initialized.
* ``update_vision([[]])``: a function which updates the 2D array that represents the player's vision according to the change of the ``position``.
   * params:  vision - a 5x5 2D array of ``Tile`` which represents the vision of the player.
   * return: none  
   * throw: TypeError - if the ``vision`` was not initialized
