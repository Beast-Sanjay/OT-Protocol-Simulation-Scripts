import socket

# Define the server IP address and port to send data to
server_ip = "192.168.100.3"  # Replace with the server's IP address
server_port = 161

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Message to send to the server
message = "302602010004067075626c6963a019020126020100020100300e300c06082b060102010102000500"

# Send the message to the server
client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

# Receive the response from the server
response, addr = client_socket.recvfrom(1024)
print(f"Received response from {addr}: {response.decode('utf-8')} and type : {type(response)}")

# Close the client socket
client_socket.close()
