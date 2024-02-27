import socket

# Define host and port
HOST = '172.20.10.4'  # Loopback address for localhost
PORT = 25000        # Port to listen on

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    # Accept incoming connections
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    with client_socket:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Process received data
            print(f"Received: {data.decode()}")

            # Send a response back to the client
            client_socket.sendall(b"Message received!")
