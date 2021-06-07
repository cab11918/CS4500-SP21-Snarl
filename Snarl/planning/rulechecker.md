**TO:**  Manager  
**FROM:**  Minghao Yu, Yuan Wang  
**DATE:**  02/15/2021  
**SUBJECT:**  Snarl RuleChecker Interface

## Snarl Rule Checker

For the Rule Checker, it validates the movement and the interaction of players and adversaries. It also check if the level or the game is ended. It will also check for invalid GameState and reject it if needed. 

The Rule Checker class should consist of the following fields:

-   `state`  - The state Rule Checker is checking which contains all information needed for validation. A state has all players and adversaries location, exit/turn/level status, and the game board, etc.


## Rule Checker Interface

-   `is_valid_move(from,to)`: a top-level validity checker which will return true for the move if all the helper-function passed. The helpers ensure the distance of the movement, the target tile and the interactions happened after the move are all valid.
    -   params: 
	    - `from` - the start point of the movement represented by `(x,y)`.
	    - `to` - the end point of the movement represented by `(x,y)`.
    -   return: a `Boolean` which represent if the move is valid.
    -   throw: any invalid condition of the movement.

-   `is_valid_dist(from,to)`: a helper function for `is_valid_move(from,to)` which ensure the move is under 2 cardinal moves away. 
    -   params: 
	    - `from` - the start point of the movement represented by `(x,y)`.
	    - `to` - the end point of the movement represented by `(x,y)`.
    -   return: a `Boolean` which represent if the move is in a valid distance.
    -   throw: the error message which indicates the failure of movement due to the wrong distance.

-   `is_valid_tile(from,to)`: a helper function for `is_valid_move(from,to)` which ensure the target `Tile` is a **traversable** `Tile` (e.g. floor, hallway, door). 
    -   params: 
	    - `from` - the start point of the movement represented by `(x,y)`.
	    - `to` - the end point of the movement represented by `(x,y)`.
    -   return: a `Boolean` which represent if the target tile is either a `floor`, `hallway` or `door` .
    -   throw: the error message which indicates the failure of movement due to a non-traversable `Tile` (e.g. a `wall`).

-   `can_interact(from,to)`: a helper function for `is_valid_move(from,to)` which ensure the interaction that will happen after the movement would be valid. The `Player` can interact with `Key`, `Adversary` but not other `Player`.
    -   params: 
	    - `from` - the start point of the movement represented by `(x,y)`.
	    - `to` - the end point of the movement represented by `(x,y)`.
    -   return: a `Boolean` which represent if the interaction is either `Player` -> Object or `Player` -> `Adversary`.
    -   throw: the error message which indicates the failure of movement due to a invalid interaction which will happen after the move.

-   `is_level_end()`:  a function to check if the players can move to the next level. 
    -   return: a `Boolean` which represent if the level end either because all the players were expelled or because the key was found by players and they enter the exit.
    -   throw: the error message which indicates if the level is ended and potential reasons for not ending it.

-   `is_game_over()`:  a function to check if the game is over. 
    -   return: a `Boolean` which represent if the game is over. The game is over if all the `Player`s were expelled in the current level, or one of the player reach `Exit` of the final `Level`.
    -   throw: the error message which indicates if the game is over and potential reasons for not ending it.


