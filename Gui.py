import pygame
import pygame_gui
import os

class Gui:

  mouse_down = False
  marked_pos = None
  bg_color = (255,255,200)
  fg_color = "black"
  radius = 15
  thickness = 2
  delta_time = 0
  
  
  def __init__(self,spiel):

    
    self.field_x = 50
    self.field_y = 50
    self.field_size = 700
   
   
    self.window_width = 600
    self.window_height = 600

    self.center_x = self.field_x + self.field_size//2
    self.center_y = self.field_x + self.field_size//2

    self.spiel = spiel

    pygame.init()
    self.window = pygame.display.set_mode((self.window_width, self.window_height),pygame.RESIZABLE)

    self.init_ui()
    self.reshape()

    
    self.clock = pygame.time.Clock()

  def init_ui(self):
      
      self.text_font = pygame.font.SysFont("Arial",20)
      self.text_surface = self.text_font.render("Zug:",self.spiel.zug,True,"red")
      self.text_rect = self.text_surface.get_rect(bottomleft = (self.field_size,self.field_y))

          
      current_dir = os.path.dirname(os.path.abspath(__file__))
      theme_path = os.path.join(current_dir, "gui_themes.json")

      self.ui_manager = pygame_gui.UIManager((self.window_width, self.window_height),theme_path)
     

      self.new_game_button = pygame_gui.elements.UIButton(
      relative_rect=pygame.Rect(

          (self.field_x,self.field_y/8), (self.field_size/7,self.field_y/8*6)
      ),  
        text="new game!",
        manager=self.ui_manager,
        object_id= "#spezial_design")

      

  def check_user_in(self):
    
    for event in pygame.event.get():

      
      
      match event.type:
        case pygame.QUIT:
          print("quit game")
          self.spiel.quit_game()

        case pygame.MOUSEBUTTONDOWN:
          if self.get_field_pos(event.pos):
            
             self.spiel.user_klicked(self.get_field_pos(event.pos))

          self.mouse_down = True
        
        case pygame.MOUSEBUTTONUP:

          if self.is_in_field(event.pos ):
            if self.get_field_pos(event.pos) != self.marked_pos:
               
               self.marked_pos = None
          self.mouse_down = False
        case pygame.VIDEORESIZE:
          self.window_width,self.window_height = event.w, event.h
          self.reshape()

      self.ui_manager.process_events(event)
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == self.new_game_button:
            self.spiel.new_game()

  def reshape(self):

    self.field_size = min(self.window_width,self.window_height)//10*9
    self.field_x = (self.window_width-self.field_size)//2
    self.field_y = (self.window_height-self.field_size)//2
    
    self.center_x = self.field_x + self.field_size//2
    self.center_y = self.field_y + self.field_size//2
    self.thickness = self.field_size//200
    self.radius = self.thickness*5
  
    self.text_rect = self.text_surface.get_rect(bottomleft = (self.field_size*0.9,self.field_y))
    self.ui_manager.set_window_resolution((self.window_width,self.window_height))
    self.new_game_button.set_position((self.field_x,self.field_y/8)) 
    self.new_game_button.set_dimensions((self.field_size/6,self.field_y/8*6))


  def is_in_field(self, mouse_pos: tuple[int,int]) -> bool:
      rel_x = mouse_pos[0] - self.center_x
      rel_y = mouse_pos[1] - self.center_y

      return abs(rel_x) <= self.field_size/2 and 0 <=  abs(rel_y) <= self.field_size/2
   
  def get_field_pos(self,mouse_pos: tuple[int,int])-> tuple[int,int,int]:
      for feld,pos in self.spiel.get_spielfeld():
        if pygame.math.Vector2(mouse_pos).distance_to(self.get_coord(pos)) <= self.radius*3:
          return pos
      return False
      
  def get_coord(self,pos: tuple[int,int,int])-> tuple[int,int ]:

    x = self.center_x + self.field_size/7*(3-pos[0])*(pos[1]-1)
    y = self.center_y - self.field_size/7*(3-pos[0])*(pos[2]-1)
    return x,y

  def draw(self,delta_time):

      self.draw_gui()
      self.draw_field() 
      pygame.display.update()
      self.ui_manager.update(delta_time)

  def draw_gui(self):
    self.text_surface = self.text_font.render("Zug: "+str(self.spiel.zug),self.fg_color,True)
    self.window.fill("gray")
    self.window.blit(self.text_surface, self.text_rect)
    self.ui_manager.draw_ui(self.window)
    

    
  def draw_field(self):

      pygame.draw.rect(
            self.window,
            self.bg_color,
            (self.field_x,self.field_y,self.field_size,self.field_size))
          
      pygame.draw.rect(
          self.window,
          self.fg_color,
          (self.field_x,self.field_y,self.field_size,self.field_size),
          self.thickness)
      
      for i in range(2):
        pygame.draw.line(
          self.window,
          self.fg_color,
          self.get_coord((0,i%2,(i+1)%2)),
          self.get_coord((2,i%2,(i+1)%2)),
          self.thickness)
        pygame.draw.line(
                self.window,
                self.fg_color,
                self.get_coord((0,(i*4+1)%3,(i*2+2)%3)),
                self.get_coord((2,(i*4+1)%3,(i*2+2)%3)),
                self.thickness)
  
    
      
      for i in range(3):
        pygame.draw.rect(
          self.window,
          self.fg_color,
          (*self.get_coord((i,0,2)),self.field_size//7*(6-i*2),self.field_size//7*(6-i*2)),
          self.thickness)
  
      for feld,pos in self.spiel.get_spielfeld():
        
        pygame.draw.circle(
          self.window,
          self.fg_color,
          (self.get_coord(pos)),
          self.radius)
        
        if feld is not None:
          pygame.draw.circle(
            self.window,
            self.spiel.player[feld],
            (self.get_coord(pos)),
            self.radius)
            
    
  def quit(self):
    pygame.quit()

  def mark(self,pos,rev = True):
    if rev:
      self.marked_pos = pos
    else:
       self.marked_pos = None
       
