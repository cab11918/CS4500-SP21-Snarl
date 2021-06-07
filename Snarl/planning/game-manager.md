**TO:** Manager    
**FROM:** Yuan Wang, Minghao Yu	   
**DATE:** 3/2/2021    
**SUBJECT:** Game Manager Interface representation     	

## Game Manager

For the game manager, it is responsible for accepting registration from the users and add then as a Player to the game model. Game Manager should also keep track with all update, making sure the data from game state and data passed in Players component are consistent. In the aspect of event handling, Game Manager 
should have basic functionalities to accept queries of movement from users.

fields for Game Manager:
- `player_list` - an array of Player components representing the collection of all player and data that usesrs need. The `players` feild in Game State is now modified as a list of position.
- `adversary_list` - an array of Adversary components representing all the data that adversaires need for future AI design
- `curr_state` - a `GameState` representing the ongoing game, storing all data that a Snarl game need. 
- `rule_checker` - a `RuleChecker` representing the rule checking component of the game.  The Validity of all movement requests from users should be checked by this rule checker.
- `selected_tile` - a `Tile` representing which tile is being chosen by the user. This can be referred by the move request(i.e. destination)

## The Game Manager Interface

- `register_player(name)`: a function that accpets the registration from a user. It takes the name provided by user and instantiate a Player Object
	- param: name(str)
	- return: none
	- throw: IndexError when player_list is full
- `set_level(level)`: set the `Level` in the `GameState` to be the given level representation and initiate the game state
	- param: level(`Level`)
	- return: none
	- throw: TypeError when curr_state is malformed or uninitialized
- `handle_move(from, to)`: handle the move request from user. Apply the move to the game state and then update all data in curr_state and players if the movement is valid. Abort it if it is invalid.
	- param: from((int, int)), to((int, int))
	- return: none
	- throw: exception when rule checker reject the given move requet
- `get_player(id)`: get the player from player_list with given id
	- param: id(int)
	- return: Player
	- throw:  TypeError when player is not found
- `update_pos(player)`: update the position of the given player in curr_state and player_list
	- param: player(Player)
	- return: none
	- throw: TypeError if player is not found
- `get_vision(id)`: generate the 2d array representing the vision of the player with given id from the curr_state
	- param: id(int)
	- return: [[`Tile`]]
	- throw:  TypeError when player is not found
- `set_vision(player)`: update the vision of the given player in player_list
	- param: player(Player)
	- return: none
	- throw: TypeError if player is not found
