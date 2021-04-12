import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.0.102'
port = 9999

client.connect((host, port))


def send(msg):
    message = msg.encode('utf-8')
    client.send(message)

send('hello world')
send('quit')