import pygame, math, random
from .entities import *
from .systems import *
from .utils.constants import *

class Game:
  def __init__(self, difficulty=1):
    pygame.init()
    pygame.font.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎮 고전 슈팅 게임")
    self.clock = pygame.time.Clock()
    self.running = True
    self.difficulty = difficulty

    self.score = 0
    self.game_over = False
    self.victory = False

    # 이미지 로드
    try:
      self.player_img = pygame.image.load('assets/images/player.png').convert_alpha()
      self.boss_img = pygame.image.load('assets/images/boss.png').convert_alpha()
      self.bullet_img = pygame.image.load('assets/images/bullet_cyan.png').convert_alpha()
      self.boss_bullet_img = pygame.image.load('assets/images/bullet.png').convert_alpha()
      self.enemy_bullet_img = pygame.image.load('assets/images/bullet_normal.png').convert_alpha()
      self.bg_img = pygame.image.load('assets/images/background.png').convert()
    except:
      self.player_img = self.create_default_image(40, NEON_CYAN)
      self.boss_img = self.create_default_image(120, NEON_PURPLE)
      self.bullet_img = self.create_default_image(16, NEON_PINK)
      self.bg_img = pygame.Surface((WIDTH, HEIGHT))
      self.bg_img.fill(DARK_BG)

    self.player = Player(WIDTH // 2, HEIGHT - 100, self.player_img, self.bullet_img)
    self.boss = Boss(WIDTH // 2, 150, self.boss_img, self.boss_bullet_img, difficulty)
    self.player_bullets = []
    self.enemy_bullets = []
    self.powerups = []
    self.particles = ParticleSystem()

    self.powerup_timer = 0
    self.message = ""
    self.message_timer = 0

    self.font = pygame.font.Font(None, 36)
    self.small_font = pygame.font.Font(None, 24)


  def create_default_image(self, size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (size//2, size//2), size//2)
    return surf

  def check_collision(self, obj1, obj2):
    return obj1.distance_to(obj2) < (obj1.radius + obj2.radius)

  def show_message(self, text):
    self.message = text
    self.message_timer = 2.0

  def update(self, dt):
    if self.game_over or self.victory:
      return

    if self.player.slow_mode:
      dt *= 0.3

    self.score += dt * 10

    # 플레이어
    self.player.update(dt, self.particles)

    # 보스
    self.boss.update(dt)
    new_bullets = self.boss.try_attack(self.player)
    self.enemy_bullets.extend(new_bullets)

    # 플레이어 탄막
    for bullet in self.player_bullets[:]:
      bullet.update(dt)
      if not bullet.active:
        self.player_bullets.remove(bullet)
      elif self.check_collision(bullet, self.boss):
        defeated = self.boss.take_damage(bullet.damage)
        bullet.active = False
        self.score += 10
        self.particles.emit(bullet.x, bullet.y, "explosion", 5)

        if defeated:
          self.victory = True
          self.particles.emit(self.boss.x, self.boss.y, "explosion", 100)

    # 적 탄막
    for bullet in self.enemy_bullets[:]:
      bullet.update(dt)
      if not bullet.active:
        self.enemy_bullets.remove(bullet)
      elif self.check_collision(bullet, self.player):
        if self.player.take_damage():
          bullet.active = False
          self.particles.emit(self.player.x, self.player.y, "explosion", 20)
          if not self.player.is_alive():
            self.game_over = True

    # 파워업
    self.powerup_timer += dt
    if self.powerup_timer > 10.0:
      self.powerup_timer = 0
      powerup_type = random.choice(["power", "bomb", "hp"])
      self.powerups.append(PowerUp(random.randint(50, WIDTH - 50), -30, powerup_type))

    for powerup in self.powerups[:]:
      powerup.update(dt)
      if not powerup.active:
        self.powerups.remove(powerup)
      elif self.check_collision(powerup, self.player):
        message = powerup.apply(self.player)
        self.show_message(message)
        powerup.active = False
        self.score += 50

    # 파티클
    self.particles.update(dt)

    # 메시지
    if self.message_timer > 0:
      self.message_timer -= dt

  def draw(self):
    self.screen.blit(self.bg_img, (0, 0))

    self.boss.draw(self.screen)
    
    for bullet in self.enemy_bullets:
      bullet.draw(self.screen)

    for bullet in self.player_bullets:
      bullet.draw(self.screen)

    for powerup in self.powerups:
      powerup.draw(self.screen)

    self.particles.draw(self.screen)
    self.player.draw(self.screen)

    # UI
    score_text = self.font.render(f"SCORE: {int(self.score)}", True, NEON_CYAN)
    self.screen.blit(score_text, (10, 10))

    hp_text = self.small_font.render(f"HP: {int(self.player.hp)}", True, NEON_GREEN)
    self.screen.blit(hp_text, (10, 50))

    bomb_text = self.small_font.render(f"BOMB: {self.player.bombs}", True, NEON_PINK)
    self.screen.blit(bomb_text, (10, 75))

    power_text = self.small_font.render(f"POWER: {self.player.power_level}", True, NEON_YELLOW)
    self.screen.blit(power_text, (10, 100))

    if self.player.slow_mode:
      slow_text = self.small_font.render("♦︎ slow_mode ♦︎", True, NEON_YELLOW)
      self.screen.blit(slow_text, (WIDTH - 120, 10))

    # 메시지
    if self.message_timer > 0:
      msg_text = self.font.render(self.message, True, NEON_YELLOW)
      self.screen.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, HEIGHT - 100))

    # 게임 오버/승리
    if self.game_over or self.victory:
      overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
      overlay.fill((0, 0, 0, 180))
      self.screen.blit(overlay, (0, 0))

      if self.victory:
        title = self.font.render("★ VICTORY ★", True, NEON_YELLOW)
      else:
        title = self.font.render("GAME OVER", True, NEON_PINK)

      score = self.font.render(f"Final Score: {int(self.score)}", True, NEON_CYAN)
      restart = self.small_font.render("Press R to Restart | ESC to Quit", True, WHITE)

      self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
      self.screen.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2 - 20))
      self.screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 40))

    pygame.display.flip()

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.running = False
        elif event.key == pygame.K_r and (self.game_over or self.victory):
          self.__init__(self.difficulty)
        elif event.key == pygame.K_SPACE:
          bullets = self.player.shoot()
          self.player_bullets.extend(bullets)
        elif event.key == pygame.K_x:
          if self.player.use_bomb():
            self.enemy_bullets.clear()
            self.particles.emit(self.player.x, self.player.y, "explosion", 50)

  def run(self):
    while self.running:
      dt = self.clock.tick(FPS) / 1000.0
      self.handle_events()
      self.update(dt)
      self.draw()

    pygame.quit()