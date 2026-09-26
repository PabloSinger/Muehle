

class Stein:

  pos = None
  farbe = None

  def __init__(self, farbe, position = (-1,-1,-1)):
    self.pos = position
    self.farbe = farbe


  def moveTo(self, newPos):
    self.pos = newPos



