import socket
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button
from shared.networking import create_server_socket, accept_client


def start_connection(server_host, server_port):
    server_socket = create_server_socket(host=server_host, port=server_port)

    while True:
        client_socket, client_address = accept_client(server_socket)
        


def controll_keyboard(key_name, action):
    if action == "down":
        keyboard.press(key_name)
    elif action == "up":
        keyboard.release(key_name)


def controll_mouse(x, y, button_name, action):
    mouse.position = (x, y)

    if button_name == "left":
        btn = Button.left
    elif button_name == "right":
        btn = Button.right
    else:
        return

    if action == "down":
        mouse.press(btn)
    elif action == "up":
        mouse.release(btn)

server_host = "localhost" 
server_port = 8000  
start_connection(server_host, server_port)

keyboard = KeyboardController()
mouse = MouseController()
