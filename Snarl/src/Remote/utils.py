import json
import socket
import time
import sys
import os


def send_msg(sock, msg):
    """
    The function takes a message and send it through TCP connection.
    :param sock: The socket it want to send to.
    :param msg: The message.
    :return: None
    """

    time.sleep(0.05)
    msg = msg + "\n"
    sock.send(msg.encode())


def receive_msg(sock):
    """
    The function receive a message through TCP connection.
    :param sock: The socket it want to listen to.
    :return: None
    """

    data = sock.recv(4096)
    if not data:
        return data
    response = data.decode()
    res_list = response.split("\n")
    return res_list[len(res_list) - 2]


def resource_path(relative_path):
    """
    The function which navigate the path when making the executable.
    :param relative_path: The path of the file.
    :return: The decorated path.
    :except: When the file was not found.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
