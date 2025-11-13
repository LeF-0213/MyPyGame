import pygame, math, random
from .entities import *
from .systems import *
from .utils.constants import *

class Game:
  def __init__(self, difficulty=1, start_stage=1):
    pygame.init()
    pygame.font.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎮 고전 슈팅 게임")
    self.clock = pygame.time.Clock()
    self.running = True
    self.difficulty = difficulty

    # 스테이지 시스템
    self.current_stage = start_stage
    self.max_stage = 4

    self.score = 0
    self.game_over = False
    self.victory = False
    self.stage_clear = False

    # 이미지 로드
    try:
      self.player_img = pygame.image.load('assets/images/player.png').convert_alpha()
      self.boss1_img = pygame.image.load('assets/images/boss.png').convert_alpha()
      self.boss2_img = pygame.image.load('assets/images/boss_stage2.png').convert_alpha()
      self.boss3_img = pygame.image.load('assets/images/boss_stage3.png').convert_alpha()
      self.boss4_img = pygame.image.load('assets/images/boss_stage4.png').convert_alpha()
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
    # self.boss = Boss(WIDTH // 2, 150, self.boss_img, self.boss_bullet_img, difficulty)
    self.bosses = []
    self.create_stage_bosses(self.current_stage)
    self.player_bullets = []
    self.enemy_bullets = []
    self.powerups = []
    self.particles = ParticleSystem()

    self.powerup_timer = 0
    self.message = ""
    self.message_timer = 0

    self.font = pygame.font.Font(None, 36)
    self.small_font = pygame.font.Font(None, 24)
    self.large_font = pygame.font.Font(None, 72)


  def create_default_image(self, size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (size//2, size//2), size//2)
    return surf

  # 스테이지에 맞는 보스 생성
  def create_stage_bosses(self, stage):
    self.bosses.clear()
    config = DIFFICULTY_LEVELS.get(stage, DIFFICULTY_LEVELS[1])
    boss_count = config["boss_count"]

    if boss_count == 1:
      if stage == 1:
        boss = Boss(WIDTH // 2, 150, self.boss1_img, self.boss_bullet_img, stage)
      else:
        boss = Boss(WIDTH // 2, 150, self.boss2_img, self.boss_bullet_img, stage)
      self.bosses.append(boss)

    elif boss_count == 2:
      boss1 = Boss(WIDTH // 3, 150, self.boss3_img, self.boss_bullet_img, stage)
      boss2 = Boss(WIDTH * 2 // 3, 150, self.boss4_img, self.boss_bullet_img, stage)

      # 서로 다른 패턴 타이밍 (교차 공격)
      boss2.attack_timer = config["cooldown"] / 2 # 절반씩 차이

      self.bosses.append(boss1)
      self.bosses.append(boss2)

    elif boss_count == 3:
      boss1 = Boss(WIDTH // 4, 150, self.boss2_img, self.boss_bullet_img, stage)
      boss2 = Boss(WIDTH * 2 // 4, 150, self.boss4_img, self.boss_bullet_img, stage)
      boss3 = Boss(WIDTH * 3 // 4, 150, self.boss3_img, self.boss_bullet_img, stage)

      boss2.attack_timer = config["cooldown"] * 2 / 3
      boss3.attack_timer = config["cooldown"] * 3 / 4

      self.bosses.append(boss1)
      self.bosses.append(boss2)
      self.bosses.append(boss3)
    
  # 다음 스테이지
  def next_stage(self):
    if self.current_stage < self.max_stage:
      self.current_stage += 1
      self.stage_clear = False
      self.enemy_bullets.clear()
      self.create_stage_bosses(self.current_stage)

      # 스테이지 보너스
      self.score += 1000 * self.current_stage
    else:
      # 전체 게임 클리어!
      self.victory = True

  # 충돌 감지
  def check_collision(self, obj1, obj2):
    if not hasattr(obj1, 'radius') or not hasattr(obj2, 'radius'):
      return False

    distance = math.sqrt((obj2.x - obj1.x)**2 + (obj2.y - obj1.y)**2)
    return distance < (obj1.radius + obj2.radius)

  def show_message(self, text):
    self.message = text
    self.message_timer = 2.0

  def update(self, dt):
    if self.game_over or self.victory:
      return

    if self.stage_clear:
      return

    if self.player.slow_mode:
      dt *= 0.3

    self.score += dt * 10

    # 플레이어
    self.player.update(dt, self.particles)

    # 모든 보스 업데이트
    all_bosses_defeated = True
    for boss in self.bosses:
      if boss.active:
        all_bosses_defeated = False
        boss.update(dt)
        new_bullets = boss.try_attack(self.player)
        self.enemy_bullets.extend(new_bullets)

        # 적 탄막
        for bullet in self.enemy_bullets[:]:
          bullet.update(dt)
          if not bullet.active:
            self.enemy_bullets.remove(bullet)
          if isinstance(bullet, LaserBullet):
            if bullet.check_collision_with_point(self.player.x, self.player.y, self.player.radius):
              if self.player.take_damage():
                self.particles.emit(self.player.x, self.player.y, "explosion", 20)
                if not self.player.is_alive():
                  self.game_over = True                      
          else: 
            if self.check_collision(bullet, self.player):
              if self.player.take_damage():
                bullet.active = False
                self.particles.emit(self.player.x, self.player.y, "explosion", 20)
                if not self.player.is_alive():
                  self.game_over = True

    # 모든 보스 격파 체크
    if all_bosses_defeated and len(self.bosses) > 0:
      self.stage_clear = True
      self.score += 5000

    # 플레이어 탄막
    for bullet in self.player_bullets[:]:
      bullet.update(dt)
      if not bullet.active:
        self.player_bullets.remove(bullet)
        continue

      for boss in self.bosses:
        if boss.active and self.check_collision(bullet, boss):
          defeated = boss.take_damage(bullet.damage)
          bullet.active = False
          self.score += 10
          self.particles.emit(bullet.x, bullet.y, "explosion", 5)

          if defeated:
            self.particles.emit(boss.x, boss.y, "explosion", 100)

    # 파워업
    self.powerup_timer += dt
    if self.powerup_timer > 10.0:
      self.powerup_timer = 0
      powerup_type = random.choice(["power", "item", "hp"])
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

    for boss in self.bosses:
      if boss.active:
        boss.draw(self.screen)
    
    for bullet in self.enemy_bullets:
      bullet.draw(self.screen)

    for bullet in self.player_bullets:
      bullet.draw(self.screen)

    for powerup in self.powerups:
      powerup.draw(self.screen)

    self.particles.draw(self.screen)
    self.player.draw(self.screen)

    # UI
    stage_config = DIFFICULTY_LEVELS[self.current_stage]
    stage_name = stage_config['name']

    stage_text = self.font.render(
      f"STAGE {self.current_stage}: {stage_name}", True, NEON_YELLOW
    )
    self.screen.blit(stage_text, (WIDTH//2 - stage_text.get_width()//2, 10))

    score_text = self.font.render(f"SCORE: {int(self.score)}", True, NEON_CYAN)
    self.screen.blit(score_text, (10, 10))

    hp_text = self.small_font.render(f"HP: {int(self.player.hp)}", True, NEON_GREEN)
    self.screen.blit(hp_text, (10, 50))

    item_text = self.small_font.render(f"ITEM: {self.player.items}", True, NEON_PINK)
    self.screen.blit(item_text, (10, 75))

    power_text = self.small_font.render(f"POWER: {self.player.power_level}", True, NEON_YELLOW)
    self.screen.blit(power_text, (10, 100))

    # 남은 보스 수
    active_bosses = sum(1 for boss in self.bosses if boss.active)
    if active_bosses > 0:
      boss_text = self.small_font.render(f"LEFT BOSS: {active_bosses}/{len(self.bosses)}", True, NEON_PINK)
      self.screen.blit(boss_text, (WIDTH - 200, 50))

    # 스테이지 클리어 화면
    if self.stage_clear:
      overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
      overlay.fill((0, 0, 0, 180))
      self.screen.blit(overlay, (0, 0))

      clear_text = self.large_font.render("STAGE CLEAR!", True, NEON_YELLOW)
      self.screen.blit(clear_text, (WIDTH//2 - clear_text.get_width()//2, HEIGHT//2 - 100))

      if self.current_stage < self.max_stage:
        next_text = self.font.render(
          f"Press SPACE for Stage {self.current_stage + 1}", True, WHITE
        )
        self.screen.blit(next_text, (WIDTH//2 - next_text.get_width()//2, HEIGHT//2 + 20))
      else:
        victory_text = self.font.render("ALL STAGES COMPLETE!", True, NEON_GREEN)
        self.screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 + 20))

    if self.player.slow_mode:
      slow_text = self.small_font.render("♦︎ slow_mode ♦︎", True, NEON_YELLOW)
      self.screen.blit(slow_text, (WIDTH - 120, 10))

    # 메시지
    if self.message_timer > 0:
      msg_text = self.font.render(self.message, True, NEON_YELLOW)
      self.screen.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, HEIGHT - 100))

    # 게임 오버/승리
    if self.game_over:
      overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
      overlay.fill((0, 0, 0, 180))
      self.screen.blit(overlay, (0, 0))

      go_text = self.large_font.render("GAME OVER", True, NEON_PINK)
      self.screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 60))
      
      score_text = self.font.render(f"Final Score: {int(self.score)}", True, NEON_CYAN)
      self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
      
      restart = self.small_font.render("Press R to Restart | ESC to Quit", True, WHITE)
      self.screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 80))

    if self.victory:
      overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
      overlay.fill((0, 0, 0, 200))
      self.screen.blit(overlay, (0, 0))
      
      victory_text = self.large_font.render("VICTORY!", True, NEON_GREEN)
      self.screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - 100))
      
      final_score = self.font.render(f"Final Score: {int(self.score)}", True, NEON_YELLOW)
      self.screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2))
      
      congrats = self.small_font.render("You defeated all bosses!", True, WHITE)
      self.screen.blit(congrats, (WIDTH//2 - congrats.get_width()//2, HEIGHT//2 + 60))

    pygame.display.flip()

  def handle_events(self):
    action = None
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.running = False
        elif event.key == pygame.K_r and self.game_over:
          self.running = False
          # Game(self.difficulty, 1).run()
          return "restart"
        elif event.key == pygame.K_SPACE:
          if self.stage_clear:
            self.next_stage()
          else: 
            bullets = self.player.shoot()
            self.player_bullets.extend(bullets)
        elif event.key == pygame.K_x:
          if self.player.use_item():
            self.enemy_bullets.clear()
            self.particles.emit(self.player.x, self.player.y, "explosion", 50)

      return action

  def run(self):
    while self.running:
      dt = self.clock.tick(FPS) / 1000.0
      action = self.handle_events()

      if action == "restart":
        return "restart"

      self.update(dt)
      self.draw()

    return None

  def run_game_with_title(self):
    pygame.init()

    running = True
    while running:
      screen = pygame.display.set_mode((WIDTH, HEIGHT))
      pygame.display.set_caption("🎮 고전 슈팅 게임 - Title")
      clock = pygame.time.Clock()

      title = TitleScreen(screen)
      title_running = True
      selected_stage = 1

      while title_running and title.active:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
            title_running = False

          action, stage = title.handle_events(event)
          if action == "start":
            selected_stage = stage
            title_running = False
          elif action == "quit":
            running = False
            title_running = False

        title.update(dt)
        title.draw()
        pygame.display.flip()

      if not running:
        break

      print(f"\n🎮 Starting Stage {selected_stage}...")
      print(f"Difficulty: {DIFFICULTY_LEVELS[selected_stage]['name']}\n")
      
      game = Game(difficulty=1, start_stage=selected_stage)
      result = game.run()
      
      # 재시작하지 않으면 타이틀로
      if result != "restart":
        print("\n🎮 Returning to title screen...")

    pygame.quit()

