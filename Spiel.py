import Spielfeld
import Gui

class Spiel:
  gui = None
  zug  = 0
  zugphase = None
  spielfeld = None
  playing = None
  spielphase = None
  last_mühle = None
  snapshots = None
  player = None
  start,destination = None,None


  def __init__(self):
    self.player = {False: "white",True: "gray"}
    self.spielfeld = Spielfeld.Spielfeld()
    self.gui = Gui.Gui(self)


  def new_game(self):
    self.zug = 0
    self.zugphase = 1
    self.spielphase = 0
    self.last_mühle = 0
   
    self.playing = True
    self.spielfeld.reset()
    self.snapshots = list()
    self.gameloop()
    self.set_conditions()


  def gameloop(self):

    while self.playing:

        self.gui.check_user_in()
        self.gui.draw()

    self.gui.quit()

  def user_klicked(self,pos):

      print("zugphase",self.zugphase)
      print("spielphase",self.spielphase)

      match self.zugphase:
        case 0: 
           if self.check_start(pos):
            self.mark_start(pos)
            self.zugphase = 1
          
        case 1:

          if pos == self.start:
                self.mark_start(pos,False)
                self.zugphase = 0
          else:
            if self.spielphase:
              if self.check_move((self.start,pos)):
                   self.spielzug(pos)
            else:
                if self.check_move((pos,)):
                     self.spielzug(pos)
            
        case 2:
            self.handle_mühle(pos)
            

  def mark_start(self,pos,rev = True):
      if rev:
       self.start = pos
       self.gui.mark(pos,True)
      else:
        
        self.gui.mark(pos,False)
  def check_start(self,pos):
          return self.spielfeld.get_field_state(pos) == self.zug%2


  def spielzug(self,pos):

    if self.spielphase:
      self.move((self.start,pos))
    else:
      self.move((pos,))

    if self.check_mühle(pos):
            
            self.zugphase = 2
            self.last_mühle = 0
            return
    else:
        
          self.next_zug()

  def set_conditions(self):

    self.zugphase = 1
    if self.zug > 17:
      self.zugphase = 0
      self.spielphase = 1
     
      if 4 > self.spielfeld.get_piece_count(self.zug%2):
          self.spielphase = 2
         
          
  def check_move(self, movement)-> bool:
        
        if all(map(self.spielfeld.field_exists,movement)):

          if self.spielphase:
             if self.spielfeld.check_move(movement[0],movement[1],self.spielphase):
                  return True
          else:
              if self.spielfeld.check_move((self.zug%2,-1,-1),movement[0],self.spielphase):
                           return True
        else:
          
          return False

  def move(self, movement):
      
      if self.spielphase:
        self.spielfeld.move_piece(movement[0],movement[1],self.spielphase)
      else:
          self.spielfeld.move_piece((self.zug%2,-1,-1),movement[0],self.spielphase)
      self.mark_start(self.start,False)

  def check_mühle(self,pos)-> bool:
   
        return self.spielfeld.check_mühle(pos)
   

  def handle_mühle(self,remove_pos) -> None:
    gegner = (self.zug + 1) % 2
         
    if not self.spielfeld.field_exists(remove_pos):
                print("Feld existiert nicht!");return
    if self.spielfeld.get_field_state(remove_pos) == gegner and self.spielfeld.is_removable(remove_pos):
            self.spielfeld.remove_piece(remove_pos);
            
            self.next_zug()
            return

  def next_zug(self):
        
        self.take_snapshot()
  
        if self.check_draw():
          print("draw")
          self.playing = False;return
        
        elif self.check_win() is not None:
          print(self.player[self.check_win()],"has won")
          self.playing = False;return
  
        self.zug += 1
        self.last_mühle += 1
        self.set_conditions()
      
  

  def take_snapshot(self):
     
     self.snapshots.append(self.deep_tuple(self.spielfeld.felder))

  def deep_tuple(self,iterable):
    
        return tuple(self.deep_tuple(item) if isinstance(item, list) else item for item in iterable)

      
  def check_draw(self) -> bool:
     
      return self.last_mühle == 50 or self.snapshots.count(self.snapshots[len(self.snapshots)-1]) == 3

  def check_win(self) -> bool|None:
    if self.zug > 17:
      if self.spielfeld.get_piece_count(False) < 3:
           return True
      elif self.spielfeld.get_piece_count(True) < 3:
            return False
    return None


  def quit_game(self):
     self.playing= False
     

  def get_spielfeld(self) -> Spielfeld:
     return self.spielfeld

if __name__ == "__main__":
    spiel = Spiel()
    spiel.new_game()

