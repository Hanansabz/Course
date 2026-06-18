import socket
from shared.networking import create_server_socket, accept_client, receive_file, close_socket


def receive_files_server(save_path, server_host, server_port):
    server_socket = create_server_socket(host=server_host, port=server_port)

    while True:
        client_socket, client_address = accept_client(server_socket)

        destination = save_path + '/Received_file'
        received = receive_file(client_socket, destination)

        print(f"File received from {client_address}")
        print("File saved as 'Received_file'")
        close_socket(client_socket)

receive_files_server(r'C:\Users\Hanan\Course\Received_From_Client', 'localhost', 8000) 
