import socket


def create_socket():
    print("CREATE SOCKET")
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('', 9090))
        print("BIND OK")
    except OSError as msg:
        sock.close()
        print("OS ERROR: ", msg)
        return False
    sock.listen(1)
    conn, addr = sock.accept()
    print("CLIENT CONNECTED")
    return sock, conn, addr


def main_loop():
    while True:
        try:
            sock, conn, addr = create_socket()
            data = conn.recv(1024)
            if data == b'\x06':
                conn.send(b'\x06')
                print("EOT")
                sock.close()
            elif data:
                data = data.decode(encoding = 'ascii').split('%%')
                conn.send(b'\x06')
                sock.close()
                print("RECEIVED: ", str(data))
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    main_loop()