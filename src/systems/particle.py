import pygame, math, random
from src.utils.constants import *

class Particle:
  def __init__(self, x, y, particle_type="explosion"):
    self.x = x
    self.y = y
    self.type = particle_type
    self.age = 0
    self.active = True

    if particle_type == "explosion":
      self.lifetime = random.uniform(0.4, 0.8)
      angle = random.uniform(0, 2 * math.pi)
      speed = random.uniform(50, 200)
      self.vx = math.cos(angle) * speed
      self.vy = math.sin(angle) * speed
      self.size = random.randint(6, 12)
      self.color = random.choice([NEON_PINK, NEON_CYAN, NEON_YELLOW])
    else: # trail
      self.lifetime = random.uniform(0,2, 0.4)
      self.vx = random.uniform(-30, 30)
      self.vy = random.uniform(-30, 30)
      self.size = random.randint(3, 6)
      self.color = NEON_CYAN

  def update(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt
    self.age += dt
    self.vx *= 0.98
    self.vy *= 0.98
    return self.age < self.lifetime
  
  def draw(self, screen):
    life_ratio = self.age / self.lifetime
    alpha = int(255 * (1 - life_ratio))
    size = max(1, int(self.size * (1 - life_ratio * 0.5)))

    for i in range(2, 0, -1):
      glow_size = size + i * 2
      glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
      pygame.draw.circle(glow_surf, (*self.color, alpha // (i + 1)), (glow_size, glow_size), glow_size)
      screen.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)), special_flags=pygame.BLEND_ADD)

class ParticleSystem:
  def __init__(self):
    self.particles = []

  def emit(self, x, y, particle_type, count):
    for _ in range(count):
      self.particles.append(Particle(x, y, particle_type))

  def update(self, dt):
    self.particles = [p for p in self.particles if p.update(dt)]

  def draw(self, screen):
    for p in self.particles:
      p.draw(screen)