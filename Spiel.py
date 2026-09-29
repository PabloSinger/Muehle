import Spielfeld
import Gui

class Spiel:
  gui = None
  zug  = None
  cur_player = None
  spielfeld = None
  playing = None



  def __init__(self):
    self.spielfeld = Spielfeld.Spielfeld()
    self.new_game()
    
   #self.gui = Gui.Gui()
   #self.gui.mainloop()

  def gameloop(self):
    print("spiel startet")
    while self.playing:
      print("ja")
      user_in = input(self.cur_player +" ist am zug!")
      if user_in == "quit":
        print("spiel beendet!")
        break


  def new_game(self):
    self.zug = 0
    self.cur_player = "white"
    self.playing = True
    #self.spielfeld.reset()
    self.gameloop()


if __name__ == "__main__":
    spiel = Spiel()
  


