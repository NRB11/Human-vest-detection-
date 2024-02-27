import socket
import threading

# Define host and port
HOST = '172.20.10.4'  # Loopback address for localhost
PORT =  55711       # Port to listen on

# List to store client sockets
client_sockets = []

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")
    
    # Add client socket to the list
    client_sockets.append(client_socket)

    with client_socket:
        while socket.connected:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Process received data
            print(f"Received from {client_address}: {data.decode()}")

            # Broadcast the message to all connected clients
            broadcast_message(data)

# Function to broadcast a message to all connected clients
def broadcast_message(message):
    for client_socket in client_sockets:
        try:
            client_socket.sendall(message)
        except Exception as e:
            # Handle exceptions such as disconnected clients
            print(f"Error broadcasting message: {e}")

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
