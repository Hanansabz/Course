import socket
import json
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

keyboard = None
mouse = None

def control_keyboard(key_name, action):
    try:
        # Try to find a special key 
        key_to_use = getattr(Key, key_name.lower())
    except AttributeError:
        # If that fails, it is just a normal letter or number
        key_to_use = key_name

    # Run the action
    if action == "key_press":
        keyboard.press(key_to_use)
    elif action == "key_release":
        keyboard.release(key_to_use)

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

    if action in (True, "pressed", "press", "down"):
        mouse.press(btn)
    elif action in (False, "released", "release", "up"):
        mouse.release(btn)


def handle_client(conn, addr):
    print("Connected:", addr)

    global keyboard, mouse
    keyboard = KeyboardController()
    mouse = MouseController()

    buffer = ""
    try:
        while True:
            data = conn.recv(1024)

            if not data:
                print("Client disconnected")
                break

            buffer += data.decode(errors="ignore")

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message.strip():
                    continue

                try:
                    event = json.loads(message)
                    print("EVENT:", event)
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
                    action = event_data.get("pressed")
                    control_mouse(x, y, button_name, action)
                elif event_type == "mouse_scroll":
                    dx = event_data.get("dx", 0)
                    dy = event_data.get("dy", 0)
                    mouse.scroll(dx, dy)
                else:
                    print("Unknown event:", event)

                print(event)

    except Exception as e:
        print("Connection error:", e)

    finally:
        conn.close()
        print("Connection closed")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(1)

    print("Server running on", PORT)

    while True:
        try:
            conn, addr = server.accept()
            handle_client(conn, addr)

        except Exception as e:
            print("Server error:", e)

HOST = "192.168.1.181"
PORT = 8000
start_server()