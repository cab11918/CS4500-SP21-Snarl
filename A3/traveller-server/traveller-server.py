import sys
import socket

characters = []  # a list represents all characters
towns = []  # a list represents all towns
network = {}  # a list represents the network of the towns
visited = []  # a global variable for can_be_reached()


def add_character(id, name, curr_town):
    characters.append(Character(id, name, curr_town))


def remove_character(id):
    if len(characters) == 0:
        raise Exception("No character to be removed!")
    else:
        for c in characters:
            if c.id == id:
                characters.remove(c)


def add_town(id, name, curr_character):
    towns.append(Town(id, name, curr_character))
    network[id] = []


def remove_town(id):
    if len(towns) == 0:
        raise Exception("No town to be removed!")
    else:
        for t in towns:
            if t.id == id:
                towns.remove(t)
        network[id] = None
        for conn in network.keys():
            if id in network[conn]:
                del network[conn]


def add_char_to_town(char_id, town_id):
    for t in towns:
        if t.id == town_id:
            if t.is_empty():
                t.curr_char_id = char_id
                for c in characters:
                    if c.id == char_id:
                        c.current_town_id = town_id
                        break
            else:
                raise Exception("The given town is not empty!")


def remove_char_from_town(char_id, town_id):
    for t in towns:
        if t.id == town_id:
            if not t.is_empty():
                t.curr_char_id = None
                for c in characters:
                    if c.id == char_id:
                        c.current_town_id = None
                        break
            else:
                raise Exception("Cannot remove character from an empty town!")


def can_be_reached(curr_town_id, end_town_id):
    global visited
    visited.append(curr_town_id)
    for tid in network[curr_town_id]:
        if tid == end_town_id:
            for t in towns:
                if t.id == tid:
                    visited = []
                    return t.is_empty
    # if it doesn't find destination from current town:
    for tid in network[curr_town_id]:
        visited.append(tid)
        can_be_reached(tid, end_town_id)
    # finally return false
    visited = []
    return False


def is_valid_path(town_id_1, town_id_2):
    return not (town_id_2 in network[town_id_1]) or \
           (town_id_1 in network[town_id_2]) or \
           town_id_1 == town_id_2


def add_path(town_id_1, town_id_2):
    network[town_id_1].append(town_id_2)
    network[town_id_2].append(town_id_1)


def remove_path(town_id_1, town_id_2):
    network[town_id_1].remove(town_id_2)
    network[town_id_2].remove(town_id_1)


class Character:
    # Character constructor
    def __init__(self, char_id, char_name, curr_town_id):
        self.char_id = char_id
        self.char_name = char_name
        self.curr_town_id = curr_town_id


class Town:
    # Town constructor
    def __init__(self, town_id, town_name, curr_char_id):
        self.town_id = town_id
        self.town_name = town_name
        self.curr_char_id = curr_char_id

    def is_empty(self):
        if self.curr_char_id:
            return True
        else:
            return False


class Network:
    # Network constructor
    def __init__(self, net_dict):
        self.net_dict = net_dict


class ListOfChars:
    # Network constructor
    def __init__(self, list_of_chars):
        self.list_of_chars = list_of_chars
