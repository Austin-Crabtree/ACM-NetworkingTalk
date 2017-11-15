#!/usr/bin/env python3

''' Original code from: https://github.com/xysun/pychat
    Updated for use in OU ACM Chapter's networking talk
    This file contains code for running the client'''

import select
import socket
import sys
import utils

READ_BUFFER = 4096

def prompt():
    ''' Prompt for client input '''
    print('#> ', end=' ', flush=True)

def main():
    ''' Main function for the client script '''
    if len(sys.argv) < 2:
        print("Usage: Python3 client.py [hostname]", file=sys.stderr)
        sys.exit(1)
    else:
        server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_connection.connect((sys.argv[1], utils.PORT))

    print("Connected to server\n")
    msg_prefix = ''

    socket_list = [sys.stdin, server_connection]

    while True:
        read_sockets, _, _ = select.select(socket_list, [], [])
        # the _ means drop the value in python
        for sock in read_sockets:
            if sock is server_connection: # incoming message
                msg = sock.recv(READ_BUFFER)
                if not msg:
                    print("Server down!")
                    sys.exit(2)
                else:
                    if msg == utils.QUIT_STRING.encode():
                        sys.stdout.write('Bye\n')
                        sys.exit(2)
                    else:
                        sys.stdout.write(msg.decode())
                        if 'Please tell us your name' in msg.decode():
                            msg_prefix = 'name: ' # identifier for name
                        else:
                            msg_prefix = ''
                        prompt()

            else:
                msg = msg_prefix + sys.stdin.readline()
                server_connection.sendall(msg.encode())

if __name__ == '__main__':
    main()
