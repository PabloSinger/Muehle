import Spielfeld
import ast
import consol_graphics
import copy

class Spiel:
  gui = None
  zug  = None
  cur_player = None
  spielfeld = None
  playing = None
  spielphase = None
  last_mühle = None
  snapshots = None



  def __init__(self):
    self.spielfeld = Spielfeld.Spielfeld()


  def new_game(self):
    self.zug = 0
    self.spielphase = 0
    self.last_mühle = 0
    self.cur_player = "white"
    self.playing = True
    self.spielfeld.reset()
    self.snapshots = list()
    self.gameloop()



  def gameloop(self):

    print("spiel startet")
    while self.playing:
      self.set_conditions()

      #user input wird ausgewertet
      try:

        self.spielzug()


      except (ValueError, SyntaxError, IndexError) as e:
        print(f"Fehler: Ungültiges Format! Bitte nutze das Format (q,x,y),(q,x,y).")
        print(f"Details: {e}")
      except KeyboardInterrupt:
        print("\nBye!")
        return

  def spielzug(self):

        user_in = self.get_user_input("Gib einen Zug ein!")

        if self.check_move(user_in):
            self.move(user_in)
            consol_graphics.draw(self.spielfeld.felder)

            if self.check_mühle(user_in):
              self.handle_mühle()
              consol_graphics.draw(self.spielfeld.felder)
              self.last_mühle = 0
            else:
              self.last_mühle += 1
            self.zug += 1
            self.take_snapshot()
            if self.check_draw():
               print("draw!")
               self.playing = False
            if self.check_win():
               

               




  def set_conditions(self):
        if self.zug > 17:
          self.spielphase = 1
          if 4 > self.spielfeld.get_piece_count(self.zug%2):
              self.spielphase = 2
        print("spielphase", self.spielphase)
        print("zug:",self.zug)

        if self.zug%2:
              self.cur_player ="black"
        else: self.cur_player = "white"

  def get_user_input(self, message: str):
      
      user_in = input(self.cur_player +": " + message) 

      if user_in = "new": self.playing = False;self.new_game()
         # (q,x,y),(q,x,y)
      return ast.literal_eval(f"[{user_in}]")

  def check_move(self, ergebnis)-> bool:

        if all(map(self.spielfeld.field_exists,ergebnis)):
          if self.spielphase == 0:
            if self.spielfeld.check_move((self.zug%2,-1,-1),ergebnis[0],self.spielphase):
                return True
            else: print("Ungültiges Format!");return False
          else:
            if self.spielfeld.check_move(ergebnis[0],ergebnis[1],self.spielphase):
              return True
            else: print("Ungültiges Format!");return False
        else:
          print("keine gültige eingabe!")
          return False

  def move(self, ergebnis):
      if self.spielphase == 0:
        self.spielfeld.move_piece((self.zug%2,-1,-1),ergebnis[0],self.spielphase)
      else:
          self.spielfeld.move_piece(ergebnis[0],ergebnis[1],self.spielphase)

  def check_mühle(self,user_in)-> bool:
      if self.spielphase:
        return self.spielfeld.check_mühle(user_in[1])
      else:
        return self.spielfeld.check_mühle(user_in[0])

  def handle_mühle(self) -> None:
    gegner = (self.zug + 1) % 2
    while True:
        print("gebe bitte die zu entfernende positition ein")
        try:
            remove_pos = self.get_user_input("Welcher Stein soll entfernt werden?")[0]
            if not self.spielfeld.field_exists(remove_pos):
                print("Feld existiert nicht!")
                continue
        except ValueError:
            print("Fehler: Ungültiges Format! Bitte nutze das Format (q,x,y).")
            continue
        if self.spielfeld.get_field_state(remove_pos) == gegner and self.spielfeld.is_removable(remove_pos):

            self.spielfeld.remove_piece(remove_pos)
            return
  def take_snapshot(self):
     self.snapshots.append(copy.deepcopy(self.spielfeld.felder))

  def check_draw(self) -> bool:
      return self.last_mühle == 50 or self.snapshots.count(self.spielfeld.felder) == 2

  def check_win(self) -> bool:
      return self.spielphase > 17 and (self.spielfeld.get_piece_count(False) < 3 or (self.spielfeld.get_piece_count(True) < 3))


if __name__ == "__main__":
    spiel = Spiel()
    spiel.new_game()
