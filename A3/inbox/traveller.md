Implementation language: Python, 3.6.8 

The Traveller supports the services of a route planner through a simple-graph network of towns for a role-playing game. It must support the functionalities of creating a town network with named nodes, be able to place a named character in a town, and be able to query whether a specified character can reach a designated town without running into any other characters. Only one character is allowed in each town, so when moving between towns, the specified character cannot pass through an already occupied town.

What we need:
- Data
    - Character (id, name, current town id)
    - Town (id, name, current character id of character in town)
    - Network (dictionary that stores town ids mapped to their connected towns’ ids)
    - List of Characters in game
- Operations
    - Town.is_empty()
    - add_character(id, name, curr_town), remove_character(id), add_town(id, name, curr_character), remove_town(id)
    - add_char_to_town(char_id, town_id), remove_char_from_town(char_id, town_id)
        - Adding: Pre: Town is_empty() == true; Post: Town is_empty() == false
        - Removing: Pre: Town is_empty() == false; Post: Town is_empty() == true
    - can_be_reached(curr_town_id, end_town_id) (towns along path must be empty)
    - is_valid_path(town_id_1, town_id_2) (simple network can’t have duplicate paths or loops)
    - add_path(town_id_1, town_id_2), remove_path(town_id_1, town_id_2) (add town ids to dictionary key values)
        - Pre: Path being added is_valid_path(town_id_1, town_id_2) == true

Use cases:
- Creating a town network: add towns → path → check if path is valid → add path
- Placing a character in a town: add character → check town empty → add to town
- Query if character can reach a town: check destination is empty → destination can be reached → remove character from current town → add character to destination
