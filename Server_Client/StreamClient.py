from pynput import keyboard
import socket
import json
import threading
import time
import cv2
import numpy as np

client = None
window_name = "Remote Screen"
frame_size = None
window_size = None
frame_lock = threading.Lock()

MAX_WINDOW_WIDTH = 1280
MAX_WINDOW_HEIGHT = 720


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


def send_mouse_move(x, y):
    send_event("mouse_move", {"x": x, "y": y})


def send_mouse_click(x, y, button, pressed):
    send_event("mouse_click", {
        "x": x,
        "y": y,
        "button": button,
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


def compute_window_size(image_width, image_height):
    ratio = min(
        MAX_WINDOW_WIDTH / image_width,
        MAX_WINDOW_HEIGHT / image_height,
        1.0
    )
    return (int(image_width * ratio), int(image_height * ratio))


def map_window_to_remote(x, y):
    with frame_lock:
        if frame_size is None or window_size is None:
            return None, None
        remote_w, remote_h = frame_size
        win_w, win_h = window_size

    x = min(max(x, 0), win_w - 1)
    y = min(max(y, 0), win_h - 1)
    remote_x = int(round(x * remote_w / win_w))
    remote_y = int(round(y * remote_h / win_h))
    remote_x = min(max(remote_x, 0), remote_w - 1)
    remote_y = min(max(remote_y, 0), remote_h - 1)
    return remote_x, remote_y


def on_mouse_event(event, x, y, flags, param):
    remote_x, remote_y = map_window_to_remote(x, y)
    if remote_x is None or remote_y is None:
        return

    if event == cv2.EVENT_MOUSEMOVE:
        send_mouse_move(remote_x, remote_y)
    elif event == cv2.EVENT_LBUTTONDOWN:
        send_mouse_click(remote_x, remote_y, "left", True)
    elif event == cv2.EVENT_LBUTTONUP:
        send_mouse_click(remote_x, remote_y, "left", False)
    elif event == cv2.EVENT_RBUTTONDOWN:
        send_mouse_click(remote_x, remote_y, "right", True)
    elif event == cv2.EVENT_RBUTTONUP:
        send_mouse_click(remote_x, remote_y, "right", False)


def screen_stream_client(host, port):
    global frame_size, window_size

    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(window_name, on_mouse_event)

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

                with frame_lock:
                    frame_size = (img.shape[1], img.shape[0])
                    window_size = compute_window_size(*frame_size)

                if window_size != (img.shape[1], img.shape[0]):
                    img = cv2.resize(img, window_size, interpolation=cv2.INTER_AREA)

                cv2.imshow(window_name, img)
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
    with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener:
        k_listener.join()

HOST = "192.168.1.181"
PORT = 8000
main(HOST, PORT)