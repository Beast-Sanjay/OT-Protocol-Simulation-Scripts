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
        
            payload = "0300002102f080320700000001000800080001120411440100ff09000401310003"

            # payload = payload.encode('utf-8')
            message = bytes.fromhex(payload)
        
            sock.sendall(message)
            print(message,' ---------- message')
            data = sock.recv(4096)
            print(data,' ---------- response')
            sock.close()
            print("Packet sent successfully.")
        except Exception as e:
            print(f"Failed to send packet: {e}")

def main():
    destination_ip = "192.168.100.6"
    destination_port = 102
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
