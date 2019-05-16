import socket
import random, string
from time import sleep


def id_generator(size = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

id = '001'
counter = 15
while counter:
    counter -= 1
    sock = socket.socket()
    sock.connect(('localhost', 30110))
    text = id + '%%' + id_generator()
    print(text)
    sock.send(text.encode('ascii'))
    reply = sock.recv(1024)
    if reply != b'06': print('Error!!! reply = ', str(reply))
    sock.close()
    sleep(2)
print('finished')


