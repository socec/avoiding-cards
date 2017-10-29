import pickle
import random
import time
from typing import List

from avoiding_cards import messages
from avoiding_cards.player import GameState, PlayerAction, PlayerInterface
from avoiding_cards.network import Server


class ServerPlayerInterface(PlayerInterface):
    def __init__(self, server: Server, player_number: int):
        self.server = server
        self.player_number = player_number
        self.timeout = 1  # seconds

    def name(self) -> str:
        msg = pickle.dumps(messages.PlayerNameMessage(''))
        self.server.send_to_client(msg, self.player_number)
        time.sleep(self.timeout)
        response = pickle.loads(self.server.read_client_data(self.player_number))
        return response.name

    def receive_player_number(self, number: int):
        msg = pickle.dumps(messages.PlayerNumberMessage(number))
        self.server.send_to_client(msg, self.player_number)

    def receive_game_state(self, game_state: GameState):
        msg = pickle.dumps(messages.GameStateMessage(game_state))
        self.server.send_to_client(msg, self.player_number)

    def receive_last_action(self, action: PlayerAction):
        msg = pickle.dumps(messages.LastActionMessage(action))
        self.server.send_to_client(msg, self.player_number)

    def receive_points(self, points: List[int]):
        msg = pickle.dumps(messages.PointsMessage(points))
        self.server.send_to_client(msg, self.player_number)

    def do_action(self, game_state: GameState, your_coins: int) -> PlayerAction:
        msg = pickle.dumps(messages.DoActionMessage(game_state, your_coins))
        self.server.send_to_client(msg, self.player_number)
        time.sleep(self.timeout)
        response =  self.server.read_client_data(self.player_number)
        if len(response) > 0:
            action = pickle.loads(response).action
            return action
        else:
            return PlayerAction.FAIL


class SimplePlayerInterface(PlayerInterface):
    def __init__(self, name: str):
        self.name = name

    def name(self) -> str:
        return self.name

    def receive_player_number(self, number: int):
        print('{} - thanks for number: {}.'.format(self.name, number))

    def receive_game_state(self, state: GameState):
        print('{} - thanks for state: {} {} {} {}'.format(self.name, state.card, state.coins,
                                                          state.active_player, state.player_cards))

    def receive_last_action(self, action: PlayerAction):
        print('{} - thanks for action: {}'.format(self.name, action))

    def receive_points(self, points: List[int]):
        print('{} - thanks for points: {}'.format(self.name, points))

    def do_action(self, state: GameState, coins_owned: int) -> PlayerAction:
        print('{} - my turn: with {}'.format(self.name, state.card))
        val = random.randint(1, 10) % 2
        if val:
            action = PlayerAction.PASS
        else:
            action = PlayerAction.KEEP

        print('{} with {} coins will {} card {}'.format(
              self.name, coins_owned, action.name, state.card))

        return action
