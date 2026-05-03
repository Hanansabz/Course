import socket

def receive_file(save_path, host, port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    data = client_socket.recv(1024)
    print("received", data)

    # with open(save_path, "wb") as f:
    #     f.write(data)

receive_file("test.txt", "127.0.0.1", 8080)

