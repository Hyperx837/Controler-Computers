from functools import wraps
import pickle
import socket
import time

from pynput.keyboard import Controller, Key
import colorama

keyboard = Controller()


def connect(*, port: int, host: str):
    """
    make  A Threaded socket connected function when this decorator is applied
    """
    def deco(func):
        @wraps(func)
        def connector(*args, **kwargs):
            sock = socket.socket()
            try:
                sock.connect((host, port))
                print(f'Connected!!! IP: {host} \n\t     PORT: {port}')

            except socket.error:
                time.sleep(0.5)
                connector(*args, **kwargs)
            
            func(sock, *args, **kwargs)

        return connector
    return deco


@connect(host='169.254.248.18', port=9827)
def ctrl_keyb(sock):
    while True:
        try:
            key, action = pickle.loads(sock.recv(1000))
            if hasattr(Key, key):
                key = getattr(Key, key)

            {
                'PRESS': keyboard.press,
                'RELEASE': keyboard.release,
            }[action](key)

        except (AttributeError, KeyError, Controller.InvalidKeyException):
            print('The command entered is not supported')


if __name__ == '__main__':
    ctrl_key()
