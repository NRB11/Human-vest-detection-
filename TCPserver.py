import socket
import threading

# Define host and port
HOST = '172.20.10.4'  # Loopback address for localhost
PORT = 55711       # Port to listen on

# List to store client sockets
client_sockets = []

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")
    
    # Add client socket to the list
    client_sockets.append((client_socket, client_address))

    with client_socket:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Process received data
            print(f"Received from {client_address}: {data.decode()}")

            # Broadcast the message to all connected clients
            broadcast_message(data, client_address)

# Function to broadcast a message to all connected clients
def broadcast_message(message, sender_address):
    for client_socket, client_address in client_sockets:
        try:
            # Include sender's address in the message
            client_socket.sendall(f"{sender_address}: {message}".encode())
        except Exception as e:
            # Handle exceptions such as disconnected clients
            print(f"Error broadcasting message: {e}")

# Function to continuously receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

        # Start a new thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
