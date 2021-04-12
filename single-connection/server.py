import socket

# create a socket (connect two devices)
def create_socket():
    try:
        global host
        global port
        global server

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        port = 9999

    except socket.error as msg:
        print("Error in creating socket: " + str(msg))

# binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global server

        print("Binding the port: " + str(port))
        server.bind((host, port))
        server.listen(5)

    except socket.error as msg:
        print("Error in binding socket: " + str(msg) + "\n" + "Retrying....")
        bind_socket()

# establish connection with a client (socket must be listening)
def accept_socket():
    conn, adrs = server.accept()
    print("Connection has been established at IP: " + str(adrs[0]) + "and PORT: " + str(adrs[1]))
    handle_client(conn, adrs)
    conn.close()

# Handle client
def handle_client(conn, adrs):

    print(f"New connection {adrs} connected")
    connected = True
    while connected:
        client_resp = str(conn.recv(1024), 'utf-8')
        if client_resp:
            if client_resp == 'quit':
                connected = False
            print(client_resp, end="")

    conn.close()

def main():
    create_socket()
    bind_socket()
    accept_socket()

main()