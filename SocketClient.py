import socket
from shared.networking import create_client_socket, close_socket, DEFAULT_BUFFER_SIZE


def start_echo_client():
    client_socket = create_client_socket(host='localhost', port=8080)

    while True:
        message = input("Enter a message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(DEFAULT_BUFFER_SIZE)
        echo_message = data.decode('utf-8')

        print(f"Server's responce: {echo_message}")

    close_socket(client_socket)
