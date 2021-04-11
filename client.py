import socket


def client():
    print("Choose Option- \n 1. Enter '1' for localhost \n 2. Enter '2' for public host")
    ch = str(input("Enter Choice (default=1): ") or 1)
    if ch == "1":
        host = "localhost"
        port = 2020
    else:
        host = input("IP: ")
        port = int(input("Port: "))
    print("Connected to: ", host, ":", port)

    my_Socket = socket.socket()
    my_Socket.connect((host, port))

    print("Connected! {}:{}".format(host, port))

    message = input(" -> ")
    print("Waiting Server...")

    while message != 'q':
        my_Socket.send(message.encode())
        data = my_Socket.recv(1024).decode()

        print('Server: ' + data)

        message = input(" -> ")
        print("Waiting Server...")

    my_Socket.close()


if __name__ == '__main__':
    client()
