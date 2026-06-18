import socket

def receive_file(save_path, host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
    except OSError as e:
        print(f"Failed to start server on {host}:{port}: {e}")
        server_socket.close()
        return

    try:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        data = client_socket.recv(1024)
        if not data:
            print(f"Client {client_address} disconnected without sending data.")
        else:
            print("received", data)

        # with open(save_path, "wb") as f:
        #     f.write(data)
    except (ConnectionError, OSError) as e:
        print(f"Connection error: {e}")
    finally:
        server_socket.close()

receive_file("test.txt", "127.0.0.1", 8080)

