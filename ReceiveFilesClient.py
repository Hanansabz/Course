import socket
from shared.networking import create_client_socket, send_file, close_socket


def send_files_client(file_path, server_host, server_port):
    client_socket = create_client_socket(host=server_host, port=server_port)
    
    try:
        send_file(client_socket, file_path)
    
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        close_socket(client_socket)


file_path = r"C:\Users\Hanan\Documents\exmp\alice.txt"
server_host = 'localhost'
server_port = 8000

send_files_client(file_path, server_host, server_port)
