from functools import wraps
from datetime import datetime
import socket
import pickle
import time

from pynput import keyboard
from colorama import Fore


def main():
    try:
        ctrl_keyb()

    except (socket.error, OSError) as e:
        print(get_date(), Fore.RED + 'The following error encountered: ', e)
        print(get_date(), Fore.YELLOW + 'Retrying....')
        time.sleep(0.3)
        main()


def connect(*, host, port):
    def deco(func):
        @wraps(func)
        def connector(*args, **kwargs):
            sock = socket.socket()
            sock.bind((host, port))
            sock.listen()
            conn, addr = sock.accept()

            print(get_date(), Fore.GREEN + f'Connection Established!')
            print(' ' * 21, f'IP: {addr[0]}\n {" " * 21}PORT: {addr[1]}')

            func(conn, *args, **kwargs)
        return connector
    return deco


def get_date():
    return Fore.YELLOW + f"[{datetime.now().strftime('%x %X')}]: "


def on_action(key, conn, action):
    pressed = []
    actions = {
        'PRESS': (pressed.append, key not in pressed),
        'RELEASE': (pressed.remove, key in pressed)
    }

    lst_func, statement = actions[action]
    if statement:
        lst_func(key)
        print(pressed)

    key = getattr(key, 'name' if hasattr(key, 'name') else 'char')

    msg = pickle.dumps((key, action))
    conn.send(msg)


@connect(host='169.254.248.18', port=9827)
def ctrl_keyb(conn):
    with keyboard.Listener(on_press=lambda key: on_action(key, conn, 'PRESS'),
                           on_release=lambda key: on_action(key, conn, 'RELEASE')) as listener:
        print(get_date(), Fore.LIGHTBLUE_EX + 'Starting... ')
        listener.join()


if __name__ == '__main__':
    main()
