import socket
from lib.id_gen import id_generator


def flood(ids, messages, host, port):
    for id in range(ids):
        for line in range(messages):
            s = socket.socket()
            s.connect((host, port))
            text = f'{id}%%{id_generator()}%%{id+line}'
            s.send(text.encode('ascii'))
            s.close()


if __name__ == "__main__":
    flood(35, 40, 'evgs89.hldns.ru', 30110)

