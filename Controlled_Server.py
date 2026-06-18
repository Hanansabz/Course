import socket
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button



def start_connection(server_host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((server_host, server_port))
        server_socket.listen(1)
    except OSError as e:
        print(f"Failed to start server on {server_host}:{server_port}: {e}")
        server_socket.close()
        return

    print(f"Server listening on {server_host}: {server_port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
        except (ConnectionError, OSError) as e:
            print(f"Error accepting connection: {e}")
        


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