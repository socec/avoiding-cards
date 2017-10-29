from enum import Enum
from typing import List


class GameState:
    def __init__(self, card: int, coins: int, active_player: int, player_cards: List[List[int]]):
        self.card = card
        self.coins = coins
        self.active_player = active_player
        self.player_cards = player_cards


class PlayerAction(Enum):
    FAIL = 0
    KEEP = 1
    PASS = 2


class PlayerInterface:
    def name(self) -> str:
        return 'UNKNOWN'

    def receive_player_number(self, number: int):
        pass

    def receive_game_state(self, game_state: GameState):
        pass

    def receive_last_action(self, action: PlayerAction):
        pass

    def receive_points(self, points: List[int]):
        pass

    def do_action(self, game_state: GameState, your_coins: int) -> PlayerAction:
        return PlayerAction.FAIL
