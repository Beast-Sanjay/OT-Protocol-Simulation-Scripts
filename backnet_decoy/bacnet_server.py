import socket
import csv
import logging
import socket
import csv
import logging


class Bacnet_server:
    def __init__(self):
        self.HOST = self.get_ip_address()
        self.PORT = 47808
        self.gramophile_dict = {}

        self.csv_file = "/home/ubuntu/protocols/backnet_decoy/Backnet_gramophile.csv"
        with open(self.csv_file, mode="r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader, None)
            for row in csv_reader:
                req = row[0]
                res = row[1]
                self.gramophile_dict[req] = res
        
        logging.basicConfig(filename='bacnet_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    bacnet_server = Bacnet_server()
    bacnet_server.udp_socket_connection()