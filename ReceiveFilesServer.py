import socket 

def receive_files_server(save_path, server_host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((server_host, server_port))
        server_socket.listen(1)
        print(f"Server listening on {server_host}: {server_port}")
    except OSError as e:
        print(f"Failed to start server on {server_host}:{server_port}: {e}")
        server_socket.close()
        return

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            raw_size = client_socket.recv(4)
            if len(raw_size) < 4:
                print(f"Client {client_address} disconnected before sending file size.")
                client_socket.close()
                continue

            file_size = int.from_bytes(raw_size, 'big')
            print(f"Expecting to receive a file of size: {file_size} bytes")

            received = 0

            with open(save_path + '/Received_file', 'wb') as f:
                while received < file_size:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)

            if received < file_size:
                print(f"Warning: expected {file_size} bytes but only received {received} bytes from {client_address}.")
            else:
                print(f"File received from {client_address}")
                print(f"Total bytes received: {received}")
                print("File saved as 'Received_file'")

        except (ConnectionError, OSError) as e:
            print(f"Connection error with client: {e}")
        finally:
            client_socket.close()
            print("Closing the connection...")

receive_files_server(r'C:\Users\Hanan\Course\Received_From_Client', 'localhost', 8000) 