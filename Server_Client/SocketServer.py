import socket

def start_echo_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '0.0.0.0'
    server_port = 8080
    server_socket.bind((server_host, server_port))
    server_socket.listen(1)

    print(f"Server listening on {server_host} : {server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"Received from client: {message}")

            # Echo the message back to the client
            client_socket.sendall(data)

        
        print(f"Connection with {client_address} closed")
        client_socket.close()

start_echo_server()