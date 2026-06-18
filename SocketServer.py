import socket
from shared.networking import create_server_socket, accept_client, DEFAULT_BUFFER_SIZE


def start_echo_server():
    server_socket = create_server_socket(host='localhost', port=8080)

    while True:
        client_socket, client_address = accept_client(server_socket)

        while True:
            data = client_socket.recv(DEFAULT_BUFFER_SIZE)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"Received from client: {message}")

            # Echo the message back to the client
            client_socket.sendall(data)

        
        print(f"Connection with {client_address} closed")
        client_socket.close()
