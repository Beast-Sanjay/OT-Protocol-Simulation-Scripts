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
            #message = bytes.fromhex('000000000006ff' + self.function_code +'08d20002')
            payload = "010100090000000101470012617474726962757465732d6368617273657400057574662d3848001b617474726962757465732d6e61747572616c2d6c616e67756167650005656e2d757345000b7072696e7465722d757269001b6970703a2f2f31302e31302e31302e3235313a3633312f6970702f2100066a6f622d696400040000001042001472657175657374696e672d757365722d6e616d65000567756573744400147265717565737465642d61747472696275746573001a6a6f622d6d656469612d7368656574732d636f6d706c6574656444000000096a6f622d737461746503"
            #cleaned_string = re.sub(r'\\([0-7]{1,3})', lambda x: codecs.decode(x.group(), 'unicode_escape'), payload)
            #sock.send(b'0001000000060a0100000001')
            #print(cleaned_string,' ------ cleaned')
            message = bytes.fromhex(payload) #000000000005002b0e0100
            #print(message,' ========= message payload ====================== ',cleaned_string)
            sock.sendall(message)
            data = sock.recv(1024)
            print(data,' ---------- response')
            sock.close()
            print("Packet sent successfully.")
        except Exception as e:
            print(f"Failed to send packet: {e}")

def main():
#    destination_ip = "202.122.17.19"
    destination_ip = "192.168.100.3"
    destination_port = 631
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