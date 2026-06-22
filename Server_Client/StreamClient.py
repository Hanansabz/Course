from pynput import keyboard, mouse
import socket
import json
import threading
import time
import cv2
import numpy as np

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
def recv_all(sock, count):
    buf = b""
    while len(buf) < count:
        chunk = sock.recv(count - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def screen_stream_client(host, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print('Connected to screen stream', host, port)

            while True:
                header = recv_all(s, 4)
                if not header:
                    break
                length = int.from_bytes(header, 'big')
                payload = recv_all(s, length)
                if payload is None:
                    break

                frame = np.frombuffer(payload, dtype=np.uint8)
                img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                if img is None:
                    continue

                cv2.imshow('Remote Screen', img)
                if cv2.waitKey(1) == ord('|'):
                    break

            s.close()
        except Exception as e:
            print('Screen stream error:', e)
            time.sleep(1)


def main(HOST, PORT):
    
    STREAM_PORT = 9000

    connect_to_server(HOST, PORT)

    # start screen stream thread
    t_stream = threading.Thread(target=screen_stream_client, args=(HOST, STREAM_PORT), daemon=True)
    t_stream.start()

    # start input listeners
    with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
         mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as m_listener:
        k_listener.join()

HOST = "localhost"
PORT = 8000
main(HOST, PORT)