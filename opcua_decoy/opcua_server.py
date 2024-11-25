import socket
import csv
import logging


def get_ip_address():
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Connect to a remote server (doesn't have to be reachable)
            s.connect(("8.8.8.8", 80))

            # Get the IP address of the socket
            ip_address = s.getsockname()[0]
            
            # Close the socket
            s.close()
            
            return ip_address
        except socket.error:
            return "Unable to get IP Address"
        
HOST = get_ip_address()  # Standard loopback interface address (localhost)
#HOST = socket.gethostbyname(socket.gethostname())
PORT = 4840  # Port to listen on (non-privileged ports are > 1023)
logging.basicConfig(filename='opcua_server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_response(req_hex):
    try:
        print(req_hex,' ------------- req hex')
        req = req_hex.replace(" ", "")
        #print(req,' --------------- req -----')
        response = gramophile_dict[str(req)]
        #print(response,' -------------------------------- response ::::::',type(response))
        message = bytes.fromhex(str(response))
        #print(message,' ---------- message')
        return message
    except Exception as e:
        return ""


gramophile_dict = {}
csv_file = "opcua_gramophile.csv"
with open(csv_file, mode="r") as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader, None)
    for row in csv_reader:
        req = row[0]
        res = row[1]
        gramophile_dict[req] = res


print(gramophile_dict)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        client_socket, client_address = s.accept()
        print(f"Accepted connection from {client_address}")
        logging.info(f"Accepted connection from {client_address}")

        try:
            # Receive data from the client (TCP payload)
            data = client_socket.recv(1024)  # Receive up to 1024 bytes
            data.decode('utf-8')
            print(" ==========================================================================================================================================================================")
            print(data)
            logging.info(f"Request recieved from {client_address} : {data}")
            if not data:
                # No more data, close the client socket
                client_socket.close()
                logging.info(f"Closing connection to {client_address}")
                continue

            rcv_payload = str(data).split('\'')[1]
            print(rcv_payload,' ----------- rcv')
            unescaped_bytes = rcv_payload.encode().decode('unicode_escape')
            result_hex = " ".join(format(ord(byte), '02x') for byte in unescaped_bytes)
            print('Recieved message: ' + result_hex)
            # Send a response back to the client (optional)
            response = send_response(result_hex)
            print(response,' ------------ response')
            logging.info(f"Response send to {client_address} : {response}")
            
            client_socket.sendall(response)
        except Exception as e:
            # Handle exceptions gracefully, if necessary
            print(f"An error occurred: {str(e)}")
        finally:
            # Close the client socket
            client_socket.close()