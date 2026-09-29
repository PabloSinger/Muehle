import Spielfeld
import ast

class Spiel:
  gui = None
  zug  = None
  cur_player = None
  spielfeld = None
  playing = None
  spielphase = None



  def __init__(self):
    self.spielfeld = Spielfeld.Spielfeld()
    self.new_game()
    
  def new_game(self):
    self.zug = 0
    self.cur_player = "white"
    self.playing = True
    self.spielfeld.reset()
    self.gameloop()


  def gameloop(self):

    print("spiel startet")
    while self.playing:
      self.set_conditions
     
      #user input wird ausgewertet
      try:
        user_in = input(self.cur_player +" ist am zug!")    # (q,x,y),(q,x,y)
        ergebnis = ast.literal_eval(f"[{user_in}]")
        if user_in == "quit":
              print("spiel beendet!")
              break

        if all(map(self.spielfeld.field_exists(ergebnis))):
          if self.spielphase == 0:
            if self.spielfeld.check_move((self.zug%2,-1,-1),ergebnis[0],0):
              self.spielfeld.move((-1,-1,-1),ergebnis[0])
          else:
            if self.spielfeld.check_move(ergebnis[0],ergebnis[1],self.spielphase):
              self.spielfeld.move(ergebnis[0],ergebnis[1])
        else:
          print("keine gültige eingabe!")
          continue
      except (ValueError, SyntaxError) as e:
        print(f"Fehler: Ungültiges Format! Bitte nutze das Format (q,x,y),(q,x,y).")
        print(f"Details: {e}")
    
      zug += 1

      


  def set_conditions(self):

           if self.zug > 17: self.spielphase = 1
           if 4 > self.spielfeld.get_piece_count(self.zug%2): self.spielphase = 2

          
           if self.zug%2:
              self.cur_player ="black"
           else: self.cur_player = "white"
     




if __name__ == "__main__":
    spiel = Spiel()
  


