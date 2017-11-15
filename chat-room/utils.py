''' Original code from: https://github.com/xysun/pychat
    Updated for use in OU ACM Chapter's networking talk
    This file contains classes to create a 3 tier chatroom
    arch.'''

import socket

MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'


def create_socket(address):
    ''' Utility for creating sockets '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(address)
    sock.listen(MAX_CLIENTS)
    print("Now listening at ", address)
    return sock

class Hall:
    ''' Hall class for pychat '''
    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.room_player_map = {} # {playerName: roomName}

    def welcome_new(self, new_player):
        ''' Welcome prompt for all new users '''
        new_player.sock.sendall(b'Welcome to pychat.\nPlease tell us your name:\n')

    def list_rooms(self, player):
        ''' List the rooms currently in the chatroom '''
        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently. Create your own!\n' \
                + 'Use [<join> room_name] to create a room.\n'
            player.sock.sendall(msg.encode())
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.sock.sendall(msg.encode())

    def handle_msg(self, player, msg):
        ''' Message handler '''
        instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'[<join> room_name] to join/create/switch to a room\n' \
            + b'[<manual>] to show instructions\n' \
            + b'[<quit>] to quit\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'

        print(player.name + " says: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            player.name = name
            print("New connection from:", player.name)
            player.sock.sendall(instructions)

        elif "<join>" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                if player.name in self.room_player_map: # switching?
                    if self.room_player_map[player.name] == room_name:
                        player.sock.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else: # switch
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.sock.sendall(instructions)

        elif "<list>" in msg:
            self.list_rooms(player)

        elif "<manual>" in msg:
            player.sock.sendall(instructions)

        elif "<quit>" in msg:
            player.sock.sendall(QUIT_STRING.encode())
            self.remove_player(player)

        else:
            # check if in a room or not first
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg.encode())
            else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'
                player.sock.sendall(msg.encode())

    def remove_player(self, player):
        ''' Remove a player from the chatroom '''
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        print("Player: " + player.name + " has left\n")

class Room:
    ''' Room class for the chatroom '''
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name

    def welcome_new(self, from_player):
        ''' Welcome prompt for all new users to a room '''
        msg = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.sock.sendall(msg.encode())

    def broadcast(self, from_player, msg):
        ''' Broadcast messages to all other users '''
        msg = from_player.name.encode() + b":" + msg
        for player in self.players:
            player.sock.sendall(msg)

    def remove_player(self, player):
        ''' Remove player from room '''
        self.players.remove(player)
        leave_msg = player.name.encode() + b"has left the room\n"
        self.broadcast(player, leave_msg)

class Player:
    ''' Player, a.k.a users class for the chatroom '''
    def __init__(self, sock, name="new"):
        sock.setblocking(0)
        self.sock = sock
        self.name = name

    def fileno(self):
        ''' Return fileno method '''
        return self.sock.fileno()
