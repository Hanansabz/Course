"""Shared networking utilities for socket-based client/server communication."""

import socket


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8080
DEFAULT_BUFFER_SIZE = 1024


def create_server_socket(host=DEFAULT_HOST, port=DEFAULT_PORT, backlog=1):
    """Create, bind, and start listening on a TCP server socket."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(backlog)
    print(f"Server listening on {host}:{port}")
    return server_socket


def accept_client(server_socket):
    """Accept a client connection and print the connection info."""
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    return client_socket, client_address


def create_client_socket(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Create a TCP client socket and connect to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    return client_socket


def receive_all(sock, expected_size, buffer_size=DEFAULT_BUFFER_SIZE):
    """Receive exactly `expected_size` bytes from a socket."""
    received = 0
    chunks = []
    while received < expected_size:
        data = sock.recv(buffer_size)
        if not data:
            break
        chunks.append(data)
        received += len(data)
    return b''.join(chunks), received


def send_file(sock, file_path):
    """Send a file over a socket, prefixed with its 4-byte size."""
    import os
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size} bytes")
    sock.sendall(file_size.to_bytes(4, 'big'))

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(DEFAULT_BUFFER_SIZE)
            if not data:
                break
            sock.sendall(data)
    print("File sent successfully.")


def receive_file(sock, save_path, buffer_size=DEFAULT_BUFFER_SIZE):
    """Receive a file from a socket (expects 4-byte size prefix)."""
    file_size = int.from_bytes(sock.recv(4), 'big')
    print(f"Expecting to receive a file of size: {file_size} bytes")

    received = 0
    with open(save_path, 'wb') as f:
        while received < file_size:
            data = sock.recv(buffer_size)
            if not data:
                break
            f.write(data)
            received += len(data)

    print(f"Total bytes received: {received}")
    return received


def close_socket(sock, label="connection"):
    """Close a socket with a log message."""
    print(f"Closing the {label}...")
    sock.close()
