import socket

def start_echo_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IPv4 socket
    server_host = 'localhost'
    server_port = 8080

    client_socket.connect((server_host, server_port))
    print(f"Connected to {server_host} on port {server_port}")

    while True:
        message = input("Enter a message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        client_socket.sendall(message.encode('utf-8'))
        data = client_socket.recv(1024)
        echo_message = data.decode('utf-8')

        print(f"Server's responce: {echo_message}")

    print("Closing the connection...")
    client_socket.close()
