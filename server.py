import socket
from shared.networking import create_server_socket, accept_client, DEFAULT_BUFFER_SIZE


def receive_file(save_path, host, port):
    server_socket = create_server_socket(host=host, port=port)

    client_socket, client_address = accept_client(server_socket)

    data = client_socket.recv(DEFAULT_BUFFER_SIZE)
    print("received", data)

    # with open(save_path, "wb") as f:
    #     f.write(data)

receive_file("test.txt", "127.0.0.1", 8080)
