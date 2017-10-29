import time

from avoiding_cards.game import GameLoop
from avoiding_cards.player_interfaces import ServerPlayerInterface
from avoiding_cards.server import Server

server = Server(4000)
server.start()

num_players = 3
while True:
    time.sleep(1)
    players = server.get_connected_clients()
    if len(players) >= num_players:
        break
players = players[:num_players]

the_players = [ServerPlayerInterface(server, 0),
               ServerPlayerInterface(server, 1),
               ServerPlayerInterface(server, 2),
               ]
GameLoop(the_players).start()
