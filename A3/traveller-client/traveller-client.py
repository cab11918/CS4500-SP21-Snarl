import sys
import json


def create_towns(town_1, town_2):
    print("The path was created.")


def place_char(char, town):
    print("The character was placed successfully.")


def is_unblocked(char, town):
    return True


def main():
    print("hi")
    input_str = sys.stdin.read().lstrip()
    parsed_input = ""
    try:
        parsed_input = json.loads(input_str)
        if not isinstance(parsed_input, dict):
            raise Exception("Invalid input.")
    except json.JSONDecodeError:
        raise Exception("Please enter a well-formed JSON.")

    try:
        if parsed_input["command"] == "roads":
            print("road")
        elif parsed_input["command"] == "place":
            print("place")
        elif parsed_input["command"] == "passage-safe?":
            print("ps")
        else:
            raise Exception("Invalid command.")
    except TypeError:
        raise Exception("Invalid input")

    sys.exit()


if __name__ == "__main__":
    # execute only if run as a script
    main()
