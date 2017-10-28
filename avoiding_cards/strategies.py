import random
from avoiding_cards.player import GameState, PlayerAction, PlayerInterface


class PlayerInterfaceSimple(PlayerInterface):
    def __init__(self, name: str):
        self.name = name

    def receive_player_number(self, number: int):
        print('{} - thanks for number: {}.'.format(self.name, number))

    def receive_game_state(self, state: GameState):
        print('{} - thanks for state: {} {} {} {}'.format(self.name, state.card, state.coins,
                                                          state.active_player, state.player_cards))

    def receive_last_action(self, action: PlayerAction):
        print('{} - thanks for action: {}.'.format(self.name, action))

    def do_action(self, state: GameState, coins_owned: int) -> PlayerAction:
        val = random.randint(1, 10) % 2
        if val:
            action = PlayerAction.PASS
        else:
            action = PlayerAction.KEEP

        print('{} with {} coins will {} card {}'.format(
              self.name, coins_owned, action.name, state.card))

        return action
