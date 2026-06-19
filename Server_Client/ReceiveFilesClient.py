import socket 
import os

def send_files_client(file_path, server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IPv4 socket
    client_socket.connect((server_host, server_port))
    print(f"Connected to {server_host}: {server_port}")
    
    try:
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")

        client_socket.sendall(file_size.to_bytes(4, 'big'))  # Send file size as 4 bytes
        
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
        print("File sent successfully.")
    
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Closing the connection...")
        client_socket.close()


file_path = r"C:\Users\Hanan\Documents\exmp\alice.txt"
server_host =  'localhost'
server_port = 8000

send_files_client(file_path, server_host, server_port)


