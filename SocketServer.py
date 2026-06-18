import socket

def start_echo_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = 'localhost'
    server_port = 8080

    try:
        server_socket.bind((server_host, server_port))
        server_socket.listen(1)
    except OSError as e:
        print(f"Failed to start server on {server_host}:{server_port}: {e}")
        server_socket.close()
        return

    print(f"Server listening on {server_host}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                print(f"Received from client: {message}")

                client_socket.sendall(data)
        except (ConnectionError, OSError) as e:
            print(f"Error communicating with {client_address}: {e}")
        finally:
            print(f"Connection with {client_address} closed")
            client_socket.close()