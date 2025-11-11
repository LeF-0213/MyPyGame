import pygame, math
from .game_object import GameObject
from src.utils.constants import *

class PowerUp(GameObject):
  TYPES = {
    "power": {"color": NEON_CYAN, "symbol": "p"},
    "bomb": {"color": NEON_PINK, "symbol": "B"},
    "hp": {"color": NEON_GREEN, "symbol": "+"}
  }

  def __init__(self, x, y, powerup_type="power"):
    super().__init__(x, y)
    self.type = powerup_type
    self.radius = 15
    self.speed = 100
    self.pulse = 0

  def update(self, dt):
    self.y += self.speed * dt
    self.pulse += dt * 5
    if self.y > HEIGHT + 50:
      self.active = False

  def draw(self, screen):
    config = self.TYPES[self.type]
    color = config["color"]
    pulse_size = 15 + math.sin(self.pulse) * 3

    for i in range(4, 0, -1):
      glow_size = int(pulse_size + i * 5)
      glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
      pygame.draw.circle(glow_surf, (*color, 80 // i), (glow_size, glow_size), glow_size)
      screen.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))

    pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(pulse_size))
    pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), int(pulse_size))

    font = pygame.font.Font(None, 24)
    text = font.render(config["symbol"], True, WHITE)
    screen.blit(text, (self.x - text.get_width()//2, self.y - text.get_height()//2))

  def apply(self, player):
    if self.type == "power":
      player.power_level = min(player.power_level + 1, 3)
      return "POWER UP!"
    elif self.type == "bomb":
      player.bombs += 1
      return "BOMB +1"
    elif self.type == "hp":
      player.hp = min(player.hp + 1, PLAYER_MAX_HP)
      return "HP +1"