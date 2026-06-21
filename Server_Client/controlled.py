import socket
import json
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button

# don't instantiate controllers at import time (pynput may require main thread / GUI context)
keyboard = None
mouse = None

def control_keyboard(key_name, action):
    if action == "key_press":
        keyboard.press(key_name)
    elif action == "key_release":
        keyboard.release(key_name)



def control_mouse(x, y, button_name, action):
    mouse.position = (x, y)

    if button_name in ("Button.left", "left"):
        btn = Button.left
    elif button_name in ("Button.right", "right"):
        btn = Button.right
    else:
        btn = None

    if btn is None:
        return

    # accept boolean or descriptive action strings
    if action in (True, "pressed", "press", "down"):
        mouse.press(btn)
    elif action in (False, "released", "release", "up"):
        mouse.release(btn)
def main(server_host, server_port):
    # instantiate controllers in main (runs in the main thread)
    global keyboard, mouse
    keyboard = KeyboardController()
    mouse = MouseController()

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
            except json.JSONDecodeError:
                print("Bad JSON:", message)
                continue

            event_type = event.get("type")
            event_data = event.get("data", {})

            if event_type == "key_press":
                key_name = event_data.get("key")
                control_keyboard(key_name, "key_press")
            elif event_type == "key_release":
                key_name = event_data.get("key")
                control_keyboard(key_name, "key_release")
            elif event_type == "mouse_move":
                x = event_data.get("x")
                y = event_data.get("y")
                if x is not None and y is not None:
                    mouse.position = (x, y)
            elif event_type == "mouse_click":
                x = event_data.get("x")
                y = event_data.get("y")
                button_name = event_data.get("button")
                action = event_data.get("action")
                control_mouse(x, y, button_name, action)
            elif event_type == "mouse_scroll":
                dx = event_data.get("dx", 0)
                dy = event_data.get("dy", 0)
                mouse.scroll(dx, dy)
            else:
                print("Unknown event:", event)

            print(event)



server_host = '0.0.0.0'
server_port = 8000
main(server_host, server_port)