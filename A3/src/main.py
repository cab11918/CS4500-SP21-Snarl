#! /usr/bin/python3
import socket
import json

# Variables that aws used to create a connection on localhost and listen to the sockets.
PORT = 8000
HOSTNAME = 'localhost'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOSTNAME, PORT))
sock.listen(1)
connection, address = sock.accept()


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


def render_num_json(input_str):
    result = []  # The output of the main function
    temp = input_str
    while input_str:
        while temp:
            try:
                nj = json.loads(temp)
                t = {"object": nj, "total": total_sum(nj)}
                result.append(t)
                break
            except json.JSONDecodeError:
                temp = temp[:-1]
                pass
        if len(temp) == 0:
            break
        input_str = input_str[len(temp):]
        temp = input_str
    # Send the output and avoid outputting the results in one line
    connection.send(json.dumps(result).encode(encoding='utf-8') + "\n".encode(encoding='utf-8'))


def main():
    global sock, HOSTNAME, PORT
    # connect to the server

    while True:

        input_str = connection.recv(1024).decode('utf-8')
        end_index = input_str.find("END")
        if end_index != -1:
            if end_index == 0:
                break
            input_str = input_str[:end_index]
            render_num_json(input_str)
            break
        else:
            render_num_json(input_str)

    sock.close()


if __name__ == "__main__":
    main()
