import socket

from tests.id_gen import id_generator


def sender(id_, host, port):
    sock = socket.socket()
    sock.connect((host, port))
    text = f'{str(id_)}%%{id_generator()}'
    sock.send(text.encode('ascii'))
    reply = sock.recv(1024)
    sock.close()
    return text, reply
