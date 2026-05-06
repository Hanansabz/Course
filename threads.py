from threading import Thread, Lock
counter = 0 
counter_lock = Lock()

def increment_counter():
    global counter 
    for _ in range(1000000):
        with counter_lock:
            counter += 1

def decrement_counter():
    global counter
    for _ in range(1000000):
        with counter_lock:
            counter -= 1

if __name__ == "__main__":
    thread1 = Thread(target=increment_counter)
    thread2 = Thread(target=decrement_counter)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f"Final counter value: {counter}")

