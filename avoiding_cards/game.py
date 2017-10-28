import random
from typing import List

from avoiding_cards.player import GameState, PlayerAction, PlayerInterface


class CardDeck:
    def __init__(self):
        random.seed()
        deck = list(range(3, 36))
        for i in range(random.randint(3, 9)):
            random.shuffle(deck)
        self._deck = deck[9:21]

    def draw(self) -> int:
        if self.size() > 0:
            return self._deck.pop()
        else:
            return 0

    def size(self) -> int:
        return len(self._deck)


class Player:
    def __init__(self, interface: PlayerInterface, coins: int=1):
        self.interface = interface
        self._coins = coins
        self._cards = []

    def current_coins(self) -> int:
        return self._coins

    def current_cards(self) -> List[int]:
        return self._cards

    def current_points(self):
        # coin points
        total = -self._coins
        # card points
        last_card = 0
        for this_card in self._cards:
            if this_card != last_card + 1:
                total += this_card
            last_card = this_card
        return total

    def add_coins(self, coins: int):
        self._coins += coins

    def remove_coin(self):
        self._coins -= 1

    def add_card(self, card: int):
        self._cards.append(card)
        self._cards.sort()


class GameLoop:
    def __init__(self, players: List[PlayerInterface]):
        self._players = [Player(player) for player in players]
        self._deck = CardDeck()
        self._card = self._deck.draw()
        self._coins = 0
        self._active_player = 0
        self._player_cards = []

    def get_game_state(self):
        self._player_cards = [player.current_cards() for player in self._players]
        return GameState(self._card, self._coins, self._active_player, self._player_cards)

    def get_player_points(self):
        return [player.current_points() for player in self._players]

    def broadcast_player_number(self):
        for number, player in enumerate(self._players):
            player.interface.receive_player_number(number)

    def broadcast_game_state(self):
        for player in self._players:
            player.interface.receive_game_state(self.get_game_state())

    def broadcast_last_action(self, action: PlayerAction):
        for player in self._players:
            player.interface.receive_last_action(action)

    def play_turn(self):
        player = self._players[self._active_player]

        # players must take the card if they don't have any more coins
        if player.current_coins() == 0:
            action = PlayerAction.KEEP
        else:
            action = player.interface.do_action(self.get_game_state(), player.current_coins())

        self.broadcast_last_action(action)

        if action == PlayerAction.KEEP:
            # player gets the card
            player.add_card(self._card)
            self._card = self._deck.draw()
            # player gets all coins on the card
            player.add_coins(self._coins)
            self._coins = 0

        if action == PlayerAction.PASS:
            # player gives a coin
            player.remove_coin()
            self._coins += 1
            # avoiding_cards moves to the next player
            self._active_player = (self._active_player + 1) % len(self._players)

    def start(self):
        # tell players their number in the queue
        self.broadcast_player_number()

        # play while there are cards in the deck
        while self._card:
            # broadcast avoiding_cards state before each turn
            self.broadcast_game_state()
            self.play_turn()

        # broadcast final avoiding_cards state
        self.broadcast_game_state()

        # show points
        print(self.get_player_points())
