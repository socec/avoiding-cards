from avoiding_cards.game import GameLoop
from avoiding_cards.strategies import PlayerInterfaceSimple

the_players = [PlayerInterfaceSimple('111'),
               PlayerInterfaceSimple('222'),
               PlayerInterfaceSimple('333')]
GameLoop(the_players).start()
