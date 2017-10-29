from avoiding_cards.game import GameLoop
from avoiding_cards.strategies import PlayerInterfaceSimple
from  avoiding_cards import messages


gs = messages.GameState(1, 2, 3, [4])
msg = messages.DoActionMessage(gs, 5)
import pickle
pmsg = pickle.dumps(msg)
print(pmsg)
msg2 = pickle.loads(pmsg)
print(msg.your_coins == msg2.your_coins)


the_players = [PlayerInterfaceSimple('111'),
               PlayerInterfaceSimple('222'),
               PlayerInterfaceSimple('333')]
GameLoop(the_players).start()
