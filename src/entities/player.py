import pygame, math, random
from .game_object import GameObject
from src.utils.constants import *
from .bullet import PlayerBullet

class Player(GameObject):
  def __init__(self, x, y, image, bullet_image):
    super().__init__(x, y)
    self.image = image
    self.radius = 3           # 층돌 처리용 반지름
    self.hp = PLAYER_MAX_HP
    self.bombs = PLAYER_BOMB_COUNT
    self.shoot_cooldown = 0   # 연속 발사 제한용 타이머
    self.invincible = False   # 무적 상태 여부
    self.invincible_timer = 0
    self.power_level = 1      # 공격력
    self.slow_mode = False
    self.bullet_image = bullet_image

  def update(self, dt, particles):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    self.slow_mode = keys[pygame.K_LSHIFT]

    speed = PLAYER_SPEED * (0.4 if self.slow_mode else 1.0)

    dx = mouse_x - self.x
    dy = mouse_y - self.y
    dist = math.sqrt(dx**2 + dy**2)

    if dist > 5:
      move_dist = min(speed * dt, dist)
      self.x += (dx / dist) * move_dist
      self.y += (dy / dist) * move_dist

    self.x = max(20, min(WIDTH - 20, self.x))
    self.y = max(20, min(HEIGHT - 20, self.y))

    if self.shoot_cooldown > 0:
      self.shoot_cooldown -= dt

    if self.invincible:
      self.invincible_timer -= dt
      if self.invincible_timer <= 0:
        self.invincible = False

  def shoot(self):
    if self.shoot_cooldown <= 0:
      self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
      bullets = []
      if self.power_level == 1:
        bullets.append(PlayerBullet(self.x, self.y, self.bullet_image))
      elif self.power_level == 2:
        bullets.append(PlayerBullet(self.x - 8, self.y, self.bullet_image))
        bullets.append(PlayerBullet(self.x + 8, self.y, self.bullet_image))
      else:
        bullets.append(PlayerBullet(self.x, self.y, self.bullet_image))
        bullets.append(PlayerBullet(self.x - 12, self.y, self.bullet_image, -0.2))
      return bullets
    return []

  def use_bomb(self):
    if self.bombs > 0:
      self.bombs -= 1
      self.invincible = True
      self.invincible_timer = 1.0
      return True
    return False

  def take_damage(self):
    if self.invincible:
      return False
    self.hp -= 1
    self.invincible = True
    self.invincible_timer = 2.0
    return True
  
  def draw(self, screen):
    # 무적 상태일 때 깜박임
    if self.invincible and int(self.invincible_timer * 10) % 2 == 0:
      return

    for i in range(3, 0, -1):
      glow_size = 20 + i * 8
      glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
      pygame.draw.circle(glow_surf, (*NEON_CYAN, 30 * i), (glow_size, glow_size), glow_size)
      screen.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))

    img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
    screen.blit(self.image, img_rect)

    if self.slow_mode:
      pygame.draw.circle(screen, NEON_PINK, (int(self.x), int(self.y)), self.radius, 2)

  def is_alive(self):
    return self.hp > 0