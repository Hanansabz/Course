import socket 

def receive_files_server(save_path, server_host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((server_host, server_port))
    server_socket.listen(1)
    print(f"Server listening on {server_host}: {server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        file_size = int.from_bytes(client_socket.recv(4), 'big')
        print(f"Expecting to receive a file of size: {file_size} bytes")

        received = 0

        with open(save_path + '/Received_file', 'wb') as f:
            while received < file_size:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)
                received += len(data)

        print(f"File received from {client_address}")
        print(f"Total bytes received: {received}")
        print("File saved as 'Received_file'")
        client_socket.close()
        print("Closing the connection...")

receive_files_server(r'C:\Users\Hanan\Course\Received_From_Client', 'localhost', 8000) 