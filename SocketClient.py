import socket

def start_echo_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IPv4 socket
    server_host = 'localhost'
    server_port = 8080

    try:
        client_socket.connect((server_host, server_port))
    except (ConnectionRefusedError, OSError) as e:
        print(f"Failed to connect to {server_host}:{server_port}: {e}")
        client_socket.close()
        return

    print(f"Connected to {server_host} on port {server_port}")

    try:
        while True:
            message = input("Enter a message to send (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024)
            if not data:
                print("Server closed the connection.")
                break
            echo_message = data.decode('utf-8')

            print(f"Server's responce: {echo_message}")
    except (ConnectionError, OSError) as e:
        print(f"Connection error: {e}")
    finally:
        print("Closing the connection...")
        client_socket.close()
