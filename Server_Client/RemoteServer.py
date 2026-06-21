import socket
import json
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

keyboard = KeyboardController()
mouse = MouseController()

def controll_keyboard(key_name, action):
    if action == "key_press":
        keyboard.press(key_name)
    elif action == "key_release":
        keyboard.release(key_name)


def controll_mouse(x, y, button_name, action):
    mouse.position = (x, y)

    if button_name == "Button.left":
        btn = Button.left
    elif button_name == "Button.right":
        btn = Button.right
    else:
        return

    if action == "True":
        mouse.press(btn)
    elif action == "False":
        mouse.release(btn)

def main(server_host, server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_host, server_port))
    server.listen(1)

    print("Waiting for connection...")

    conn, addr = server.accept()

    print("Connected:", addr)

    buffer = ""

    while True:
        data = conn.recv(1024).decode()

        if not data:
            break

        buffer += data

        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)

            try:
                event = json.loads(message)
                event_type = event["type"]
                event_data = event["data"]

                if event_type == "key_press":
                    key_name = event_data["key"]
                    action = "key_press"
                    controll_keyboard(key_name, action)
                elif event_type == "key_release":
                    key_name = event_data["key"]
                    action = "key_release"
                    controll_keyboard(key_name, action)
                elif event_type == "mouse_move" + "mouse_scroll" + "mouse_click" :
                    x = event_data["x"]
                    y = event_data["y"]
                    button_name = "button"
                    action = "pressed"

            except json.JSONDecodeError:
                print("Bad JSON:", message)



server_host = '0.0.0.0'
server_port = 8000
main(server_host, server_port)