import pickle
import time

from avoiding_cards import messages
from avoiding_cards.network import Client, ClientMessageHandler
from avoiding_cards.player import PlayerInterface
from avoiding_cards.player_interfaces import SimplePlayerInterface


class DefaultHandler(ClientMessageHandler):
    def __init__(self, player: PlayerInterface):
        self.player = player

    def handle(self, this_client: Client, data: bytes):
        msg = pickle.loads(data)
        if type(msg) == messages.PlayerNameMessage:
            name = self.player.name()
            response = pickle.dumps(messages.PlayerNameMessage(name))
            this_client.send_data(response)
        if type(msg) == messages.PlayerNumberMessage:
            number = msg.number
            self.player.receive_player_number(number)
        if type(msg) == messages.GameStateMessage:
            game_state = msg.game_state
            self.player.receive_game_state(game_state)
        if type(msg) == messages.LastActionMessage:
            action = msg.action
            self.player.receive_last_action(action)
        if type(msg) == messages.PointsMessage:
            points = msg.points
            self.player.receive_points(points)
        if type(msg) == messages.DoActionMessage:
            game_state = msg.game_state
            your_coins = msg.your_coins
            action = self.player.do_action(game_state, your_coins)
            response = pickle.dumps(messages.ActionResponseMessage(action))
            this_client.send_data(response)


pi = SimplePlayerInterface('MIKI-' + str(time.time()))
dh = DefaultHandler(pi)

client = Client('localhost', 4000, dh)
client.start()
while True:
    #time.sleep(2)
    #client.send_data(pickle.dumps(messages.PlayerNameMessage('ZZZ')))
    if not client.is_running():
        break