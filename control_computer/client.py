from functools import wraps
from threading import Thread
# import asyncio
import pickle
import socket
import time

from pynput.keyboard import Controller, Key
from pynput import mouse
import colorama

keyboard = Controller()
# globals()['Button'] = mouse.Button
mouse = mouse.Controller()


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

            Thread(target=func(sock, *args, **kwargs)).start()

        return connector
    return deco


@connect(host='169.254.248.18', port=3321)
def ctrl_mouse(sock):
    while True:
        args = pickle.loads(sock.recv(1000))
        if len(args) > 4:
            mouse.position = args

        elif args[3].__class__ == bool:
            *_, button, pressed = args
            if pressed:
                mouse.press(button)

            else:
                mouse.release(button)

        else:
            *_, dx, dy = args
            mouse.scroll(dx, dy)


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


def main():
    try:
        for func in ctrl_keyb, ctrl_mouse:
            Thread(target=func).start()

    except:
        main()


if __name__ == '__main__':
    main()
