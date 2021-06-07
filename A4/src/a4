#! /usr/bin/python3
import sys
import socket
import json

# Default value for hostname, port and username
PORT = 8000
HOSTNAME = '127.0.0.1'
USERNAME = "Glorifrir Flintshoulder"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
parsed_input = ""


def check_json_input():
    global parsed_input

    input_str = sys.stdin.readline().rstrip()

    try:
        parsed_input = json.loads(input_str)
    except json.JSONDecodeError:
        # if the input is not a json
        print("Invalid JSON")
        sys.exit()


def main():
    global sock, HOSTNAME, PORT, USERNAME

    # passing argument into hostname, port and username
    if len(sys.argv) > 1:
        HOSTNAME = sys.argv[1]
        if len(sys.argv) > 2:
            PORT = int(sys.argv[2])
            if len(sys.argv) > 3:
                USERNAME = sys.argv[3]

    # try to establish tcp connection
    try:
        sock.connect((HOSTNAME, PORT))
        print("Successfully connected!")
    except socket.error as err:
        print("Fail to connect to the server! %s" % err)
        sys.exit()

    # sign_up name for user
    sock.send(USERNAME.encode())
    res1 = ["the server will call me", USERNAME]
    print(json.dumps(res1))
    # receive session_id
    sock.recv(1024).decode()

    batch_request = {"characters": [], "query": {"character": "", "destination": ""}}
    create_towns_request = {"towns": [], "roads": []}

    check_json_input()
    # create_towns
    try:
        if parsed_input["command"] != "roads":

            raise KeyError()
        else:
            for cmd in parsed_input["params"]:
                create_towns_request["towns"].append(cmd["from"]),
                create_towns_request["towns"].append(cmd["to"]),
                create_towns_request["roads"].append({"from": cmd["from"], "to": cmd["to"]})
            # remove duplicated towns
            create_towns_request["towns"] = list(set(create_towns_request["towns"]))
            sock.send(json.dumps(create_towns_request).encode())
    except KeyError:
        print("invalid command")
        sys.exit()

    while True:
        check_json_input()

        try:
            if parsed_input["command"] == "place":
                # if given town is not valid
                if not parsed_input["params"]["town"] in create_towns_request["towns"]:
                    raise ValueError
                batch_request["characters"].append(
                    {"name": parsed_input["params"]["character"], "town": parsed_input["params"]["town"]})
            elif parsed_input["command"] == "passage-safe?":
                # if given character is not valid
                if not parsed_input["params"]["character"] in batch_request["characters"]:
                    raise ValueError
                batch_request["query"]["character"] = parsed_input["params"]["character"]
                batch_request["query"]["destination"] = parsed_input["params"]["town"]
                sock.send(json.dumps(batch_request).encode())
                server_response = sock.recv(1024).decode()
                for char in server_response["invalid"]:
                    res2 = ["invalid placement", {"name": char["name"], "town": char["town"]}]
                    print(json.dumps(res2))
                    res3 = ["the response for", {parsed_input["query"]}, "is", server_response["response"]]
                    print(json.dumps(res3))
                break
            else:
                print("Invalid command.")
                sys.exit()

        except (KeyError, TypeError):
            msg = {"error": "not a request", "object": parsed_input}
            print(json.dumps(msg))
            break
        # discard the invalid request
        except ValueError:
            pass

    # TCP disconnect
    sock.close()
    sys.exit()


if __name__ == "__main__":
    main()
