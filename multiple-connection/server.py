import socket
import threading
import time
from collections import defaultdict as df


all_connections = []
all_address = []
group_names = []
users = []
groups = df(list)
chats = df(list)

def create_socket():
    try:
        global server
        global host
        global port

        print(f"Creating socekt...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        print(host)
        port = 9999
    except socket.error as msg:
        print(f"Error in creating socekt: {msg}")

def bind_socket():
    try:
        global server
        global host
        global port

        print(f"Binding the port: {port}")
        server.bind((host, port))
        server.listen(5)
    except socket.error as msg:
        print(f"Error in binding socket: {msg} \n Retrying...")
        bind_socket()

# handling connections from multiple clients and saving to a list
# closing previous connections when server is restarted

def accept_connections():

    global groups
    global chats

    for connection in all_connections:
        connection.close()

    del all_connections[:]
    del all_address[:]
    del group_names[:]
    del users[:]
 
    while True:
        try:
            conn, adrs = server.accept()
            server.setblocking(1) # prevents timeout

            user_name = conn.recv(1024).decode('utf-8')
            print(f"User: {str(user_name)}")

            group_name = conn.recv(1024).decode('utf-8')
            print(f"Group: {str(group_name)}")


            all_connections.append(conn)
            all_address.append(adrs)
            users.append(user_name)

            if (group_name not in groups):
                print(f"Creating new group...")

            groups[group_name].append(conn)

            if (len(chats[group_name]) > 0):
                print(f"Sending earlier messages from {str(group_name)} to new user: {str(user_name)}")
                for msg in chats[group_name]:
                    conn.send(str.encode(msg))
            
            done = 'done'
            conn.send(str.encode(done))

            t = threading.Thread(target=recv_data, args=(group_name, conn, user_name))
            t.daemon = True
            t.start()
        except server.error as msg:
            print(f"Error in making connection: {msg}")

def recv_data(group_name, conn, user_name):

    global groups
    global chats

    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if (conn is None or data=='quit'):
                print(f"User: {str(user_name)} is disconeted")
                break

            print(f"{str(user_name)} > {str(data)}")
            message = str(user_name) + '>' + str(data)
            chats[group_name].append(message)

            for i, conn in enumerate(groups[group_name]):
                conn.send(message.encode('utf-8'))
        except:
            print(f"Client got disconeted....")
            break

def main():
    create_socket()
    bind_socket()
    accept_connections()

main()
