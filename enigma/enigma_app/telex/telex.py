import ipaddress
import socket
import re


class Telex:

    def transmit(inpt, ip_address, port_number):
        """

        """
        # prompt for ip address and port number to send to.
        # prompt for message to send.
        # encode message and send.
        HEADERSIZE = 10

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip_address, port_number))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                inpt = f"{len(inpt):<{HEADERSIZE}}" + inpt
                while True:
                    conn.sendall(inpt.encode("utf-8"))
                    break

    def recieve(ip_address, port_number):
        """

        """
        # prompt for ip address and port number to listen on.
        # decode recieved message.
        # print message.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port_number))
            data = s.recv(1024)
        data = data.decode()
        return data
        """
        HEADERSIZE = 10

        full_msg = ''
        new_msg = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port_number))
            while True:
                msg = s.recv(16)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False
                full_msg += msg.decode("utf-8")

                if len(full_msg)-HEADERSIZE == msglen:
                    msg = full_msg[HEADERSIZE:]
                    return msg

    def get_ip_address():
        """

        """
        while True:
            ip_address = input("Enter an IPV4 address: ")
            pattern = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
            match = re.search(pattern, ip_address)
            if match:
                try:
                    ip_address = ipaddress.ip_address(match.group())
                except ValueError:
                    print(f"{ip_address} is not a valid ip address. Try again.")
                else:
                    break
            else:
                print(f"{ip_address} is not a valid ip address. Try again.")
        return str(ip_address)

    def get_port_number():
        """

        """
        while True:
            try:
                port_number = input("Enter a port number: ")
                port_number = int(port_number)
            except ValueError:
                print(f"{port_number} is not a valid port number. Try again.")
            else:
                if port_number < 0 or port_number > 65535:
                    print(f"{port_number} must be in range 0-65535. try again.")
                else:
                    break
        return port_number

