import pygame, math, random
from .game_object import GameObject
from src.utils.constants import *

class Bullet(GameObject):
  def __init__(self, x, y, speed, angle, image=None):
    super().__init__(x, y)
    self.speed = speed
    self.angle = angle
    self.image = image
    self.radius = 6

  def update(self, dt):
    self.x += math.cos(self.angle) * self.speed * dt
    self.y += math.sin(self.angle) * self.speed * dt

    if (self.x < -50 or self.x > WIDTH + 50 or self.y < -50 or self.y > HEIGHT + 50):
      self.active = False

  def draw(self, screen):
    if self.image:
      img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
      screen.blit(self.image, img_rect)
    else:  
      pygame.draw.circle(screen, NEON_CYAN, (int(self.x), int(self.y)), 4)
      pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 2)

class SpiralBullet(Bullet):
  def __init__(self, x, y, speed, angle, image=None, spiral_speed=2):
    super().__init__(x, y, speed, angle, image)
    self.spiral_speed = spiral_speed

  def update(self, dt):
    self.angle += self.spiral_speed * dt
    super().update(dt)

class AcceleratingBullet(Bullet):
  def __init__(self, x, y, speed, angle, image=None, accel=50):
    super().__init__(x, y, speed, angle, image)
    self.accel = accel

  def update(self, dt):
    self.speed += self.accel * dt
    super().update(dt)

class HomingBullet(Bullet):
  def __init__(self, x, y, speed, angle, image=None, turn_speed=2.0):
    super().__init__(x, y, speed, angle, image)
    self.turn_speed = turn_speed
    self.target = None

  # 생성 시점에서 target을 정하면 유연성이 떨어짐
  def set_target(self, target):
    self.target = target

  def update(self, dt):
    if self.target:
      dx = self.target.x - self.x
      dy = self.target.y = self.y
      target_angle = math.atan2(dy, dx)
      diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
      self.angle += max(-self.turn_speed*dt, min(self.turn_speed*dt, diff))
    super().update(dt)

class LaserBullet(GameObject):
  def __init__(self, x, y, angle, length=400, duration=1.5):
    super().__init__(x, y)
    self.angle = angle
    self.length = length
    self.duration = duration
    self.active = True

  def update(self, dt):
    self.duration -= dt
    if self.duration <= 0:
      self.active = False

  def draw(self, screen):
    end_x = self.x + math.cos(self.angle) * self.length
    end_y = self.y + math.sin(self.angle) * self.length
    pygame.draw.line(screen, NEON_PURPLE, (self.x, self.y), (end_x, end_y))

class PlayerBullet(GameObject):
  def __init__(self, x, y, angle_offset=0, image=None):
    super().__init__(x, y)
    self.angle = -math.pi/2 + angle_offset
    self.speed = 400
    self.image = image
    self.radius = 6
    self.damage = 10
    self.active = True

  def update(self, dt):
    self.x += math.cos(self.angle) * self.speed * dt
    self.y += math.sin(self.angle) * self.speed * dt

    if self.y < -20:
      self.active = False

  def draw(self, screen):
    for i in range(2, 0, -1):
      glow_size = 8 + i * 4
      glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
      pygame.draw.circle(glow_surf, (*NEON_PINK, 100), (glow_size, glow_size), glow_size)
      screen.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))

    if self.image:
      img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
      screen.blit(self.image, img_rect)
    else:
      pygame.draw.circle(screen, NEON_PINK, (int(self.x), int(self.y)), 6)


