# import socket
# import csv
# import logging

# # Define the server IP address and port to listen on
# def get_ip_address():
#         try:
#             # Create a socket object
#             s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
#             # Connect to a remote server (doesn't have to be reachable)
#             s.connect(("8.8.8.8", 80))

#             # Get the IP address of the socket
#             ip_address = s.getsockname()[0]
            
#             # Close the socket
#             s.close()
            
#             return ip_address
#         except socket.error:
#             return "Unable to get IP Address"

# HOST = get_ip_address() # Listen on all available network interfaces
# PORT = 5094
# logging.basicConfig(filename='snmp_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# gramophile_dict = {}
# csv_file = "SNMP_gramophile.csv"
# with open(csv_file, mode="r") as file:
#     csv_reader = csv.reader(file)
#     header = next(csv_reader, None)
#     for row in csv_reader:
#         req = row[0]
#         res = row[1]
#         gramophile_dict[req] = res


# print(gramophile_dict)


# # Create a UDP socket
# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
#     # Bind the socket to the address and port
#     server_socket.bind((HOST, PORT))
    
#     logging.info(f"Server listening on {HOST}:{PORT}")

#     while True:
#         # Receive data from the client
#         try:
#             data, client_addr = server_socket.recvfrom(1024)
#             print(f"Recevied data from from {client_addr}:{data.decode('utf-8')}")

#             logging.info(f"Request received from {client_addr}: {data.decode('utf-8')}")

#         # Process the received data if necessary
       
#         # Send a response back to the client
#             data = data.decode('utf-8')
#             response = gramophile_dict.get(data)
#             if response is None:
#                 logging.warning(f"No response found for request: {data}")
#                 print(f"No response found for request: {data}")
#                 response = "No response found"
#             else:
#                 print(f"Response sent to {client_addr}: {response}")
#                 logging.info(f"Response sent to {client_addr}: {response}")

#             server_socket.sendto(response.encode('utf-8'), client_addr)
#         except Exception as e:
#             print(e)
import socket
import csv
import logging
import socket
import csv
import logging


class HART_IP_server:
    def __init__(self):
        self.HOST = self.get_ip_address()
        self.PORT = 5094
        self.gramophile_dict = {}

        self.csv_file = "/home/ubuntu/protocols/HART_IP_decoy/HART_IP_gramophile.csv"
        with open(self.csv_file, mode="r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader, None)
            for row in csv_reader:
                req = row[0]
                res = row[1]
                self.gramophile_dict[req] = res
        
        logging.basicConfig(filename='HART_IP_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_ip_address(self):
        try:
            # Create a socket object
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Connect to a remote server (doesn't have to be reachable)
            self.s.connect(("8.8.8.8", 80))

            # Get the IP address of the socket
            self.ip_address = self.s.getsockname()[0]
            
            # Close the socket
            self.s.close()
            
            return self.ip_address
        except socket.error:
            return "Unable to get IP Address"



    def udp_socket_connection(self):
        print(self.gramophile_dict)


        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            # Bind the socket to the address and port
            server_socket.bind((self.HOST, self.PORT))
            
            logging.info(f"Server listening on {self.HOST}:{self.PORT}")

            while True:
                # Receive data from the client
                try:
                    self.data, self.client_addr = server_socket.recvfrom(2048)
                    print(f"Recevied data from from {self.client_addr}:{self.data.decode('utf-8')}")

                    logging.info(f"Request received from {self.client_addr}: {self.data.decode('utf-8')}")

                # Process the received data if necessary
                    self.data = self.data.decode('utf-8')
            
                # Send a response back to the client
                    self.response = self.gramophile_dict.get(self.data)
                    if self.response is None:
                        logging.warning(f"No response found for request: {self.data}")
                        print(f"No response found for request: {self.data}")
                        self.response = "No response found"
                    else:
                        print(f"Response sent to {self.client_addr}: {self.response}")
                        logging.info(f"Response sent to {self.client_addr}: {self.response}")

                    server_socket.sendto(self.response.encode('utf-8'), self.client_addr)
                except Exception as e:
                    print(e)

if __name__ == "__main__":
    bacnet_server = HART_IP_server()
    bacnet_server.udp_socket_connection()