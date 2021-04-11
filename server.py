import socket
import time
from pyngrok import ngrok


def server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "localhost"
    s.bind((server_ip, port))
    s.listen(1)
    conn, addr = s.accept()
    print("Connection from: " + str(addr))
    while True:
        while True:  # this line, if the client closed the connection, it waits for new connections.
            try:
                data = str(conn.recv(1024).decode())
                print("Client: " + data)
                break
            except ConnectionResetError:
                time.sleep(1)
                conn, addr = s.accept()
                print("Connection from: " + str(addr))
        if data == "q":
            break
        else:
            message = input(" -> ")
            print("Waiting Client...")
            conn.send(message.encode())
    conn.close()


def ngrok_setup(port):
    try:
        with open("ngrok_token.txt", "r") as f:
            token = f.read()
    except Exception as e:
        print("Error occured, mabye because of following reason-")
        print("'ngrok_token.txt' file misssing")
        print("Invalid or no Token in 'ngrok_token.txt' file")
        print("Error- \n ", e)

    try:
        ngrok.set_auth_token(token)
    except Exception as e:
        print("Invalid Token, get your token from: https://dashboard.ngrok.com/get-started/your-authtoken")
        print("Error- \n ", e)
        
    url = ngrok.connect(port, "tcp")
    only_url = url.public_url.split("//")[-1]
    url, port = only_url.split(":")[0], only_url.split(":")[1]
    print("Tunnel Created at: ", f"{url}:{port}")
    ip = socket.gethostbyname(url)
    print("Send this IP to client: ", ip)
    print("Send this PORT to client: ", port)
    print("Server is started on: ", f"{ip}:{port}")


if __name__ == '__main__':
    print("Choose Option- \n 1. Enter '1' for localhost \n 2. Enter '2' for public host")
    ch = str(input("Enter Choice (default=1): ") or 1)
    port = 2020
    if ch != "1":
        ngrok_setup(port)
    else:
        print("Server is started on localhost")
    server(port)
