from pynput import keyboard, mouse
import socket
import json

client = None


def connect_to_server(HOST, PORT):
    global client

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            print(f"Connected to: {HOST} on {PORT}")
            break

        except Exception as e:
            print("Retrying connection...", e)


def send_event(event_type, data):
    global client

    if client is None:
        return  # ignore events until connected

    try:
        message = {
            "type": event_type,
            "data": data
        }

        client.sendall((json.dumps(message) + "\n").encode())

    except (BrokenPipeError, OSError):
        print("Connection lost")
        client = None


def serialize_key(key):
    key_char = getattr(key, "char", None)
    if key_char is not None:
        return key_char

    key_name = getattr(key, "name", None)
    if key_name is not None:
        return key_name

    return str(key)


def on_press(key):
    send_event("key_press", {"key": serialize_key(key)})


def on_release(key):
    send_event("key_release", {"key": serialize_key(key)})


def on_move(x, y):
    send_event("mouse_move", {"x": x, "y": y})


def on_click(x, y, button, pressed):
    send_event("mouse_click", {
        "x": x,
        "y": y,
        "button": str(button),
        "pressed": pressed})


def on_scroll(x, y, dx, dy):
    send_event("mouse_scroll", {
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy})

HOST = "192.168.1.181" 
PORT = 8000
connect_to_server(HOST, PORT)

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
) as keyboard_listener, mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
) as mouse_listener:

    keyboard_listener.join()