import socket

from tests.id_gen import id_generator


class Sender(object):
    def __init__(self, id_, host, port):
        self.id = id_
        self.host = host
        self.port = port

    def send(self):
        text = f'{str(self.id)}%%{id_generator()}'
        try:
            sock = socket.socket()
            sock.connect((self.host, self.port))
            sock.send(text.encode('ascii'))
            reply = sock.recv(1024)
            assert (reply == b'06')
            sock.close()
            return text, reply
        except ConnectionRefusedError:
            print(f'Socket {self.host}:{self.port} is inactive or busy')
            return text, None
