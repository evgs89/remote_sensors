import socket
from socketserver import BaseRequestHandler, TCPServer
import threading, queue
from time import sleep

Q = queue.Queue()


class MyTCPHandler(BaseRequestHandler):
    def handle(self):
        self.request.settimeout(5)
        data = bytearray()
        while True:
            try:
                chunk = self.request.recv(1024)
                data += chunk
                print(data)
            except socket.timeout:
                break
            if not chunk: break
        self.server.queue.put_nowait(data)


def start_server(host, port, q):
    TCPServer.allow_reuse_address = True
    server = TCPServer((host, port), MyTCPHandler)
    server.queue = q
    server.serve_forever()


if __name__ == '__main__':
    try:
        TCPServer.allow_reuse_address = True
        server = TCPServer(('', 9090), MyTCPHandler)
        server.queue = Q
        t = threading.Thread(target = server.serve_forever)
        t.daemon = True
        t.start()
        while True:
            try:
                data = Q.get_nowait()
                if data:
                    print("RECEIVED: ", data.decode('ascii'))
            except queue.Empty:
                sleep(.1)
    except KeyboardInterrupt:
        print('exititng')
        server.shutdown()
        print('ok')

#
# def create_socket():
#     print("CREATE SOCKET")
#     sock = socket.socket()
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     try:
#         sock.bind(('', 9090))
#         print("BIND OK")
#     except OSError as msg:
#         sock.close()
#         print("OS ERROR: ", msg)
#         return False
#     sock.listen(5)
#     conn, addr = sock.accept()
#     print("CLIENT CONNECTED")
#     return sock, conn, addr
#
#
# def main_loop():
#     t = threading.Thread(target = start_server, args = ('', 9090))
#     t.daemon = True
#     t.start()
#     while True:
#         try:
#             sock, conn, addr = create_socket()
#             data = conn.recv(1024)
#             if data == b'\x06':
#                 conn.send(b'\x06')
#                 print("EOT")
#                 sock.close()
#             elif data:
#                 data = data.decode(encoding = 'ascii').split('%%')
#                 conn.send(b'\x06')
#                 sock.close()
#                 print("RECEIVED: ", str(data))
#         except Exception as e:
#             print(str(e))
#

