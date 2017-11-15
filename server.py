#!/usr/bin/env python3

''' Original code from: https://github.com/xysun/pychat
    Updated for use in OU ACM Chapter's networking talk
    This file contains the server code for running the
    chatroom '''

import select
import sys
from utils import Hall, Player
import utils

READ_BUFFER = 4096

def main():
    ''' Main function for  '''
    host = sys.argv[1] if len(sys.argv) >= 2 else ''
    listen_sock = utils.create_socket((host, utils.PORT))

    hall = Hall()
    connection_list = []
    connection_list.append(listen_sock)

    while True:
        # Player.fileno()
        read_players, _, error_sockets = select.select(connection_list, [], [])
        # the _ means drop the value in python
        for player in read_players:
            if player is listen_sock: # new connection, player is a socket
                new_socket, _ = player.accept() # the _ means drop the value in python
                new_player = Player(new_socket)
                connection_list.append(new_player)
                hall.welcome_new(new_player)

            else: # new message
                msg = player.sock.recv(READ_BUFFER)
                if msg:
                    msg = msg.decode().lower()
                    hall.handle_msg(player, msg)
                else:
                    player.sock.close()
                    connection_list.remove(player)

        for sock in error_sockets: # close error sockets
            sock.close()
            connection_list.remove(sock)

if __name__ == '__main__':
    main()
