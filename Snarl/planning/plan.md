**TO:** Manager  
**FROM:** Minghao Yu, Yuan Wang  
**DATE:** 02/07/2021  
**SUBJECT:**  Project plan


**Pieces that make up a player**	
```
 • Name, ID
 • The position of the player (level, tile)
 • Vision distance
 • Action points (how many tiles player can move foward)
 • Inventory items
 • Health/attack point, if expelled
```

**Pieces that make up a automated adversaries**	
```
 • Adversary type (zombie, ghost, etc.), ID
 • The position of the adversary (level, tile)
 • Distance to object (keys, exits, players)
 • Action points
 • Health/attack point, if expelled

```

**Pieces that make up the game software**	
```
 • Map (levels, tiles, resources)
 • Tile (position, occupied, type, etc.)
 • Resource (key, exit, players, adversaries)
 • Game status (win/lose/ongoing, score, players/adversaries remain)
```

**Who knows what and who needs to know what**	
```
 • Adversaries know the position of the players/key/exit and how map is structured.
 Adversaries need to know who is the closest player to them and who is the closest 
 player to the key and exit.
 • Map knows how the game is proceeding, what make up a tile, the status of each ti
 le, whose turn is it currently and what to display for the players. Map should kno
 ws what would happen when there is an interaction between two different component.
 • Players know a limited part of the map around their avatar, whether they have ob
 tained the key or not. Player should know the position of adversaries/key/exit in 
 their vision.
 • Keys in different level know the position of themselves and who picked them up.
 • Exit of each level knows whether it has been unlocked
```
 
**Common Knowledge**	
```
 The common knowledge of this game should be around the data repesent the game in general.
 • who is playing at current turn should be shared
 • whether the exit has been unlocked
 • which level players're currently at
 
```


**Milestones**	
---
```
  2 • game model - basic constructors and data structure
  3 • game model/controller - data model and basic movements
  4 • game GUI - 2D array demo
  5 • game model - functions for advanced player operation & testing
  6 • game model - adversary AI implementation & testing
  7 • game controller & network - server for multiplayer client implementation & testing
  8 • game GUI - enhanced graphics for game pieces
  9 • testing - test the performance of all functionalities implemented working as a whole
 10 • testing & wrap up - fix potential issues and make the software an integreated piece
```
---
we start to implement our model by listing all the pieces in our software and make a UML diagram. Once we build the model, we could step forward to the basic user interaction part. For the controller part, we list out all the function we need for each piece of our software and apply that controller to the our model/view. The next step of our plan is enhancing our GUI. We will create pixel art visual components and consider what users need to know throughout GUI in different scenarios.    
