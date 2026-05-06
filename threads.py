from threading import Thread 
counter = 0 

def increment_counter():
    global counter 
    for _ in range(1000000):
        counter += 1

def increment_counter_thread():
    global counter
    for _ in range(1000000):
        counter -= 1

if __name__ == "__main__":
    thread1 = Thread(target=increment_counter)
    thread2 = Thread(target=increment_counter_thread)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f"Final counter value: {counter}")

