import math

class GameObject:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.active = True
  
  def distance_to(self, other):
    return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

  def angle_to(self, other):
    return math.atan2(other.y - self.y, other.x - self.x)