#! /usr/bin/python3
import sys
import json


def total_sum(nj):
    # total_sum takes a NumJSON, and it returns the sum of all numeric value in this NumJSON
    count = 0
    if isinstance(nj, list):
        # When the NumJSON is an array of NumJSON
        for num in nj:
            count += total_sum(num)
        return count
    elif isinstance(nj, int):
        # When the NumJSON is a number
        return nj
    elif isinstance(nj, dict):
        # When the NumJSON is an object
        try:
            return total_sum(nj['payload'])
        except KeyError:
            return 0
    else:
        # If it is a String
        return 0


def total_prod(nj):
    # total_prod takes a NumJSON, and it returns the product of all numeric value in this NumJSON
    product = 1
    if isinstance(nj, list):
        for num in nj:
            product *= total_prod(num)
        return product
    elif isinstance(nj, int):

        return nj
    elif isinstance(nj, dict):
        try:
            return total_prod(nj['payload'])
        except KeyError:
            return 1
    else:
        return 1


def main():
    result = []  # The output of the main function
    input_str = sys.stdin.read().lstrip()
    temp = input_str
    if sys.argv[1] != "--sum" and sys.argv[1] != "--product":
        print("Usage: please type\"--sum\" or \"--product\".\n")  # When the user type wrong command
        sys.exit()
    while input_str:
        while temp:
            try:
                nj = json.loads(temp)
                t = {"object": nj, "total": total_sum(nj) if sys.argv[1] == "--sum" else total_prod(nj)}
                result.append(t)
                break
            except json.JSONDecodeError:
                temp = temp[:-1]
                pass
        if len(temp) == 0:
            break
        input_str = input_str[len(temp):]
        temp = input_str

    print(json.dumps(result))

    print("Exit")


if __name__ == "__main__":
    main()
