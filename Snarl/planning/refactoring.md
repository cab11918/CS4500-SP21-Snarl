# Milestone 6 - Refactoring Report

**Team members:** Minghao Yu, Yuan Wang

**Github team/repo:** [p6-refactoring](https://github.ccs.neu.edu/CS4500-S21/Londolond/tree/p6-refactoring)

## Plan

- ``sys.path()`` insert causing ``isInstance()`` wrong behavior(referencing issue).
- ``update_pos()`` only support updating a given player's position which is unnecessary.
- ``Player``  need to be inside of ``Client``  for GUI rendering instead of putting GUI functions in ``Player`` .
- Following the best practice of Python, the getters/setters should be removed.

## Changes

- we switch to absolute import instead of inserting path when importing
    - removed all sys.path.insert() when importing module
    - switch to absolute import with specific path to the modules.
- change data structure of key and exit in our GameState
    - remove key_pos and exit_pos in game_state due to the misinterpretation in previous assignment
    - add key and exit as an object in the field of game_state, more data are accessible through key and exit field.
- add more tests for game manager and rulechecker
    - add more necessary tests for game_manager and rulechecker to ensure the correctness of our implementation
- experimenting Pygame
    - attempt to implement GUI using Pygame library
- change update_pos
    - change update_pos to be the function update all players and adversaries in the game manager
- remove adv and player id in constructor
    - id should be automatically generated instead of manually initiated
- remove getter and setters
    - we realized getter and setter are not pythonic way of getting and setting class field, so we removed getters and
      setters in previous implementation

## Future Work

- Get familiar with Pygame library and start to build a 'Human Interface' for any information the player needs.
- Build a mock-up server to start testing the communication between ``Server`` and ``Game Manager``.
- Find a complete gaming asset for characters, objects and the tile map.

## Conclusion

For this milestone, the main task is to ensure the code correctness by adding more test cases. We also learned about the
PyGame library to make sure we are ready for future implementation. We are also making changes to improve our design and
be ready for any possible changes in future.
  
