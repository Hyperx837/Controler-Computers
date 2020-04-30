import socket


# todo: make two function that will control a computer (for mouse, for keyboard)

sock = socket.socket()
host = '192.168.56.1'
sock.connect((host, ))
