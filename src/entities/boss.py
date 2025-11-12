import pygame, math, random
from .game_object import GameObject
from src.systems.bullet_pattern import BulletPattern
from src.utils.constants import *

class Boss(GameObject):
  def __init__(self, x, y, image, bullet_image, stage=1):
    super().__init__(x, y)
    self.image = image
    self.bullet_image = bullet_image
    self.stage = stage
    self.radius = 25

    # 스테이지에 따른 능력치
    config = DIFFICULTY_LEVELS.get(stage, DIFFICULTY_LEVELS[1])
    self.max_hp = config["boss_hp"]
    self.hp = self.max_hp
    self.phase = 1          # 공격 페이즈
    self.attack_cooldown = config["cooldown"]
    self.attack_speed = config["attack_speed"]
    
    self.attack_timer = 0
    self.pattern_index = 0
    self.target_x = x
    self.target_y = y
    self.move_timer = 0
    self.pulse = 0
    self.hit_flash = 0                      # 피격 시 깜빡임 효과

  def update(self, dt):
    # 페이즈 체크
    hp_ratio = self.hp / self.max_hp
    if hp_ratio < 0.33 and self.phase < 3:
      self.phase = 3
    elif hp_ratio < 0.66 and self.phase < 2:
      self.phase = 2

    # 이동
    self.move_timer += dt
    if self.move_timer > 3.0:
      self.target_x = random.randint(200, WIDTH - 200)
      self.target_y = random.randint(80, 200)
      self.move_timer = 0

    self.x += (self.target_x - self.x) * dt * 0.5
    self.y += (self.target_y - self.y) * dt * 0.5

    # 공격타이머
    self.attack_timer += dt

    # 이펙트
    self.pulse += dt * 3
    if self.hit_flash > 0:
      self.hit_flash -= dt * 5

  # 새 페이즈 진입
  def enter_phase(self, new_phase):
    self.phase = new_phase
    self.attack_cooldown *= 0.8
    return True


  def take_damage(self, damage):
    self.hp -= damage
    self.hit_flash = 1.0

    if self.hp <= 0:
      self.hp = 0
      self.active = False
      return True
    return False

  def try_attack(self, player):
    if self.attack_timer >= self.attack_cooldown:
      self.attack_timer = 0
      return self.generate_pattern(player)
    return []

  def generate_pattern(self, player):
    patterns = []

    if self.phase == 1:
      patterns = [
        lambda: BulletPattern.create_circle(self.x, self.y, 16, 150, self.bullet_image),
        lambda: BulletPattern.create_aimed_burst(self.x, self.y, player.x, player.y, 5, 200, self.bullet_image)
      ]
    elif self.phase == 2:
      patterns = [
        lambda: BulletPattern.create_circle(self.x, self.y, 24, 120, self.bullet_image, "spiral"),
        lambda: BulletPattern.create_double_circle(self.x, self.y, 12, 150, self.bullet_image),
        lambda: BulletPattern.create_aimed_burst(self.x, self.y, player.x, player.y, 7, 200, self.bullet_image),
        lambda: BulletPattern.create_homing_cluster(self.x, self.y, 6, 100, self.bullet_image, player)
      ]
    else:
      patterns = [
        lambda: BulletPattern.create_circle(self.x, self.y, 32, 100, self.bullet_image, "accel"),
        lambda: BulletPattern.create_spiral_wave(self.x, self.y, 3, 12, 120, self.bullet_image),
        lambda: BulletPattern.create_laser_cross(self.x, self.y),
        lambda: BulletPattern.create_homing_cluster(self.x, self.y, 10, 120, self.bullet_image, player),
        lambda: BulletPattern.create_random_spray(self.x, self.y, 30, 80, 180, self.bullet_image),
      ]

    # 반복 패턴
    self.pattern_index = (self.pattern_index + 1) % len(patterns)
    return patterns[self.pattern_index]()

  # 보스 그리기
  def draw(self, screen):
    if not self.active:
      return

    # 히트 플래시
    flash_color = NEON_PINK if self.hit_flash > 0.5 else NEON_PURPLE

    # 펄스 글로우
    pulse_size = int(60 + math.sin(self.pulse) * 10)
    pulse_alpha = int(100 + math.sin(self.pulse) * 50)

    for i in range(3, 0, -1):
      glow_size = pulse_size + i * 15
      glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
      pygame.draw.circle(glow_surf, (*flash_color, pulse_alpha // (i + 1)), (glow_size, glow_size), glow_size)
      screen.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))
  
    # 이미지
    img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
    screen.blit(self.image, img_rect)

    # HP 바
    self.draw_hp_bar(screen)

    # 페이즈 표시
    font = pygame.font.Font(None, 24)
    phase_text = font.render(f"PHASE {self.phase}", True, NEON_YELLOW)
    screen.blit(phase_text, (self.x - 40, self.y - 100))

  # HP 바 그리기
  def draw_hp_bar(self, screen):
    bar_width = 150
    bar_height = 12
    bar_x = self.x - bar_width // 2
    bar_y = self.y - 80

    # 배경
    pygame.draw.rect(screen, (50, 50, 50), (bar_x - 2, bar_y -2, bar_width + 4, bar_height + 4))

    # HP(그라데이션)
    hp_ratio = max(0, self.hp / self.max_hp)
    current_width = int(bar_width * hp_ratio)
    
    if hp_ratio > 0.5:
      color = NEON_CYAN
    elif hp_ratio > 0.25:
      color = NEON_YELLOW
    else:
      color = NEON_PINK

    if current_width > 0:
      pygame.draw.rect(screen, color, (bar_x, bar_y, current_width, bar_height))

    # 외곽선
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    # HP 숫자
    font = pygame.font.Font(None, 18)
    hp_text = font.render(f"{int(self.hp)}/{int(self.max_hp)}", True, WHITE)
    screen.blit(hp_text, (self.x - hp_text.get_width()//2, bar_y + 15))

    # 페이지 표시
    if self.phase > 1:
      phase_font = pygame.font.Font(None, 24)
      phase_text = phase_font.render(f"PHASE {self.phase}", True, NEON_YELLOW)
      screen.blit(phase_text, (self.x - 40, self.y - 100))


  