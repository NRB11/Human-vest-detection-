import socket
import threading

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            # Receive data from the server
            data = client_socket.recv(1024)
            print(data.decode())
        except:
            break

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server address
server_address = "192.168.56.139"
name = input("what is your name: ")
server_port = 55700

# Connect to the server
client_socket.connect((server_address, server_port))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    # Send messages to the server
    message = input()
    client_socket.send((name + ": " + message).encode())
    

# Close the socket
client_socket.close()