from avoiding_cards.player import GameState, PlayerAction
from typing import List


class PlayerNameMessage:
    def __init__(self, name: str):
        self.name = name


class PlayerNumberMessage:
    def __init__(self, number: int):
        self.number = number


class GameStateMessage:
    def __init__(self, game_state: GameState):
        self.game_state = game_state


class LastActionMessage:
    def __init__(self, action: PlayerAction):
        self.action = action


class DoActionMessage:
    def __init__(self, game_state: GameState, your_coins: int):
        self.game_state = game_state
        self.your_coins = your_coins


class ActionResponseMessage:
    def __init__(self, action: PlayerAction):
        self.action = action


class PointsMessage:
    def __init__(self, points: List[int]):
        self.points = points
