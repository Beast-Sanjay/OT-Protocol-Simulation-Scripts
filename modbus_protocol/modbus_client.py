import socket
import time


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
            #message = bytes.fromhex('000000000006ff' + self.function_code +'08d20002')
            payload = "000200000006000300630001"
            #sock.send(b'0001000000060a0100000001')
            
            message = bytes.fromhex(payload) #000000000005002b0e0100
            print(message,' ========= message payload ====================== ',payload)
            sock.sendall(message)
            data = sock.recv(1024)
            print(data,' ---------- response')
            sock.close()
            print("Packet sent successfully.")
        except Exception as e:
            print(f"Failed to send packet: {e}")

def main():
    # destination_ip = "202.122.17.19"
    destination_ip = "192.168.100.3"
    destination_port = 502
    while True:
        for i in range(42,128):
            print("=======================")
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