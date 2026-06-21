from pynput import keyboard, mouse


def on_press(key):
    try:
        print('key: {0} pressed'.format(key))
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    print('key: {0} released'.format(key))

def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released', (x, y)))

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up', (x, y)))

with keyboard.Listener(on_press=on_press,on_release=on_release) as keyboard_listener, mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll) as mouse_listener:
    keyboard_listener.join()
    mouse_listener.join()
