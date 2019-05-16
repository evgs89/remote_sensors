import socket
import random, string
from time import sleep


def id_generator(size = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

id = '002'
counter = 15
while counter:
    counter -= 1
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    text = id + '%%' + id_generator(24)
    print(text)
    sock.send(text.encode('ascii'))
    reply = sock.recv(1024)
    if reply != b'06': print('Error!!! reply = ', str(reply))
    sock.close()
    sleep(3)
print('finished')


