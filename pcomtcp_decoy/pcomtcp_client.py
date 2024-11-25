import socket
import time
import re
import codecs


class PacketSender:
    def __init__(self, destination_ip, destination_port,function_code):
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.function_code = function_code

    def send_packet(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.destination_ip, self.destination_port)
            sock.connect(server_address)
            print(server_address,' --------- server address ')
        
            payload = "3233650008002f3030524346350d"
     
            message = bytes.fromhex(payload) 
    
            sock.sendall(message)
            data = sock.recv(1024)
            print(data,' ---------- response')
            sock.close()
            print("Packet sent successfully.")
        except Exception as e:
            print(f"Failed to send packet: {e}")

def main():
    destination_ip = "192.168.100.3"
    destination_port = 1240
    while True:
        for i in range(42,128):
            print("======================="*10)
            function_code = i
            code= hex(function_code)[2:]

            if (len(str(code)) == 1):
                code = '0' + str(code)
            print (code)

            packet_sender = PacketSender(destination_ip, destination_port,code)
            packet_sender.send_packet()
            time.sleep(0.5)

if __name__ == "__main__":
    main()