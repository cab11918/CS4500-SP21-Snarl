  
## Adversary Strategies 
In Snarl, the adversaries will be actors that were controlled by AI. Here, we will introduce our strategies for making the zombies and ghosts move. The main goal is to make the game become more interesting and more challenging (for the playability, we will make the adversaries move randomly when they have no target, and to make the game more challenging, we would utilize the moves of the adversaries to prevent the player exiting the level or collecting the key). 

### Zombie

For the zombies, the strategy is very straightforward, since they can't leave the room they were originally spawned in, the zombie will keep randomly moving inside the room when there's no player. Once a player entered the room, the zombie will keep moving toward the player until they kill the player or miss the target (The best way to catch the player would be standing near the door tile of the room, but we want the game to be more interesting, so we choose to make them move randomly).


### Ghost

For the ghosts, there will be a natural ``N`` which determines whether the ghost should keep chasing the player. If the actual distance to the player is less than ``N``, the algorithm will find the shortest path to that player and moving toward it. If the actual distance to player is bigger than ``N``, the ghost will then randomly choose an adjacent tile and interact with it (might teleport the ghost to another random room). Eventually the ghost will find the player and continue chasing him.

  
