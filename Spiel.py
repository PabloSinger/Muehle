
import Spielfeld
class Spiel:

  zug  = None
  spielfeld = None



  def __init__(self):
   spielfeld = Spielfeld()

  def new_game(self):
    self.zug = 0
    self.spielfeld.reset()


    


