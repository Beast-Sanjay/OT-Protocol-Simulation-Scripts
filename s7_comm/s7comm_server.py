import socket
import csv
import logging

class s7commServer:
    def __init__(self):
        self.HOST = self.get_ip_address()
        self.PORT = 102
        self.gramophile_dict = {}

        self.csv_file = "/home/ubuntu/protocols/s7_comm/s7comm_gramophile.csv"
        with open(self.csv_file, mode="r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader, None)
            for row in csv_reader:
                req = row[0]
                res = row[1]
                self.gramophile_dict[req] = res
        
        logging.basicConfig(filename='s7comm_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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


    def send_response(self, reqs_hex):
        self.reqs_hex = reqs_hex
        try:
            print(self.reqs_hex,' ------------- req hex')
            self.req = self.reqs_hex.replace(" ", "")
            #print(req,' --------------- req -----')
            self.response = self.gramophile_dict[str(self.req)]
            #print(response,' -------------------------------- response ::::::',type(response))
            self.message = bytes.fromhex(str(self.response))
            #print(message,' ---------- message')
            return self.message
        except Exception as e:
            return ""

    def tcp_socket_connection(self):
        print(self.gramophile_dict)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            while True:
                self.client_socket, self.client_address = s.accept()
                print(f"Accepted connection from {self.client_address}")
                logging.info(f"Accepted connection from {self.client_address}")

                try:
                    # Receive data from the client (TCP payload)
                    self.data = self.client_socket.recv(4096)  # Receive up to 4096 bytes
                    print(self.data)  
                    # self.data = self.data.decode('utf-8')
                    print(" ==========================================================================================================================================================================")
            
                    logging.info(f"Request received from {self.client_address} : {self.data}")
                    if not self.data:
                        # No more data, close the client socket
                        self.client_socket.close()
                        logging.info(f"Closing connection to {self.client_address}")
                        continue

                    self.rcv_payload = str(self.data).split('\'')[1]
                    print(self.rcv_payload,' ----------- rcv')
                    unescaped_bytes = self.rcv_payload.encode().decode('unicode_escape')
                    result_hex = " ".join(format(ord(byte), '02x') for byte in unescaped_bytes)
                    print('Received message: ' + result_hex)
                    # Send a response back to the client (optional)
                    response = self.send_response(result_hex)
                    print(response,' ------------ response')
                    logging.info(f"Response sent to {self.client_address} : {response}")
                    
                    self.client_socket.sendall(response)
                    # return True
                
                except Exception as e:
                    # Handle exceptions gracefully, if necessary
                    print(f"An error occurred: {str(e)}")
    
                finally:
                    # Close the client socket
                    self.client_socket.close()

if __name__ == "__main__":
    modbus_server = s7commServer()
    modbus_server.tcp_socket_connection()   