import socket
import threading
import time


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.0.105'
port = 9999

client.connect((host, port))
print(f"Connected to server")

user_name = input('Enter your user name')
group_name = input('Enter the group you want to join')

client.send(str.encode(user_name))
time.sleep(0.1)
client.send(str.encode(group_name))

receving = True

while True:

    if receving:
        print(f"Receiving earlier chats from {str(group_name)}...")
    while receving:
        data = client.recv(1024).decode('utf-8')
        print(str(data))
        if data=='done':
            receving = False
        
    data = input('Say something: ')
    client.send(str.encode(data))
    if data=='quit':
        print(f"leaving chat...")
        break
