import random, pygame, math
from src.utils.constants import *

class TitleScreen:
  def __init__(self, screen):
    self.screen = screen
    self.active = True
    self.selected_stage = 1
    self.selected_player = 0

    # 폰트
    self.title_font = pygame.font.Font(None, 96)
    self.subtitle_font = pygame.font.Font(None, 48)
    self.menu_font = pygame.font.Font(None, 36)
    self.small_font = pygame.font.Font(None, 24)

    # 애니메이션
    self.pulse = 0
    self.star_positions = []

    # 배경 별 생성
    for _ in range(100):
      x = random.randint(0, WIDTH)
      y = random.randint(0, HEIGHT)
      speed = random.uniform(10, 50)
      size = random.randint(1, 3)
      self.star_positions.append([x, y, speed, size])

    # 플레이어 이미지 로드
    self.player_images = []
    self.player_names = ["Black_Dragon", "White_Dragon"]

    for i in range(1, 3):
      img = pygame.image.load(f'assets/images/player{i}.png').convert_alpha()
      self.player_images.append(img)   

  def update(self, dt):
    self.pulse += dt * 2

    # 배경 별 이동
    for star in self.star_positions:
      star[1] += star[2] * dt
      if star[1] > HEIGHT:
        star[1] = 0
        star[0] = random.randint(0, WIDTH)

  def draw(self):
    for y in range(HEIGHT):
      ratio = y / HEIGHT
      r = int(5 + ratio * 15)
      g = int(5 + ratio * 10)
      b = int(20 + ratio * 40)
      pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    for star in self.star_positions:
      x, y, speed, size = star
      alpha = int(100 + 155 * (speed / 50))
      pygame.draw.circle(self.screen, (alpha, alpha, alpha), (int(x), int(y)), size)

    # === 타이틀 ===
    title_text = self.title_font.render("CYBER SHOOTING", True, NEON_CYAN)
    subtitle_text = self.subtitle_font.render("BULLET HELL", True, NEON_PINK)

    # 타이틀 글로우 효과
    pulse_alpha = int(150 + math.sin(self.pulse) * 50)
    for i in range(5, 0, -1):
      glow_surf = pygame.Surface((title_text.get_width() + i*10, title_text.get_height() + i*10), pygame.SRCALPHA)
      glow_text = self.title_font.render("CYBER SHOOTING", True, (*NEON_CYAN, pulse_alpha // (i*1)))
      glow_surf.blit(glow_text, (i*5, i*5))
      self.screen.blit(glow_surf, (WIDTH//2 - title_text.get_width()//2 - i*5, 50 - i*5))
    
    self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
    self.screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, 110))

    # === 플레이어 선택 ===
    player_y = 370

    player_title = self.menu_font.render("SELECT PLAYER", True, NEON_YELLOW)
    self.screen.blit(player_title, (WIDTH//2 - player_title.get_width()//2, player_y))

    # 플레이어 아이콘 표시
    icon_y = player_y + 50
    icon_size = 50
    icon_spacing = 150
    start_x = WIDTH//2 - (len(self.player_images) * icon_spacing - icon_spacing + icon_size) // 2

    for i, img in enumerate(self.player_images):
      icon_x = start_x + i * icon_spacing

      # 선택된 플레이어 강조
      if i == self.selected_player:
        if i == 0:
          color = NEON_CYAN
        else:
          color = NEON_PINK
        outline_width = 4
        pulse_size = int(5 + math.sin(self.pulse * 2) * 3)

        # 펄스 효과
        glow_rect = pygame.Rect(icon_x - pulse_size, icon_y - pulse_size, icon_size + pulse_size*2, icon_size + pulse_size*2)
        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*color, 100), (0, 0, glow_rect.width, glow_rect.height), border_radius=10)
        self.screen.blit(glow_surf, glow_rect)
      else:
        color = NEON_PURPLE
        outline_width = 2
      
      # 아이콘 배경
      icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
      pygame.draw.rect(self.screen, (30, 30, 50), icon_rect, border_radius=8)
      pygame.draw.rect(self.screen, color, icon_rect, outline_width, border_radius=8)

      # 플레이어 이미지
      scaled_img = pygame.transform.scale(img, (icon_size - 10, icon_size - 10))
      img_rect = scaled_img.get_rect(center=icon_rect.center)
      self.screen.blit(scaled_img, img_rect)

      # 플레이어 이름
      name_text = self.small_font.render(self.player_names[i], True, color)
      self.screen.blit(name_text, (icon_x + icon_size//2 - name_text.get_width()//2, icon_y + icon_size + 5))

    # === 게임 설명 ===
    y_offset = 160

    instructions = [
      "CONTROLS",
      "========================================",
      "  Mouse -------- Move           ",
      "  Space -------- Shoot          ",
      "  Shift -------- Slow Mode      ",
      "  X -------- Use Item (Bomb)  ",
      "GAME INFO",
      "========================================",
      "Power-ups: [P] Power  [I] Item  [+] HP",
    ]

    for i, line in enumerate(instructions):
      if line.startswith("C") or line.startswith("G"):
        color = NEON_YELLOW
        font = self.menu_font
      elif line.startswith("P"):
        color = NEON_CYAN
        font = self.small_font
      elif line.startswith("  "):
        color = WHITE
        font = self.small_font
      elif line.startswith("="):
        color = NEON_PURPLE
        font = self.small_font
      else:
        color = (150, 150, 150)
        font = self.small_font

      text = font.render(line, True, color)
      self.screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset + i * 22))

    # === 스테이지 선택 ===
    stage_y = HEIGHT - 280

    stage_title = self.menu_font.render("SELECT STAGE", True, NEON_YELLOW)
    self.screen.blit(stage_title, (WIDTH//2 - stage_title.get_width()//2, stage_y))

    # 스테이지 버튼
    button_y = stage_y + 40
    button_width = 120
    button_spacing = 140
    start_x = WIDTH//2 - (4 * button_spacing - button_spacing + button_width) // 2

    for stage in range(1, 5):
      button_x = start_x + (stage - 1) * button_spacing

      # 선택된 스테이지 강조
      if stage == self.selected_stage:
        color = NEON_CYAN
        ouline_width = 4
        pulse_size = int(5 + math.sin(self.pulse * 2) * 3)

        # 펄스 효과
        glow_rect = pygame.Rect(button_x - pulse_size, button_y - pulse_size, button_width + pulse_size*2, 40 + pulse_size*2)
        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*NEON_CYAN, 100), (0, 0, glow_rect.width, glow_rect.height), border_radius=10)
        pygame.draw.rect(glow_surf, NEON_CYAN, (0, 0, glow_rect.width, glow_rect.height), width=4, border_radius=10)
        self.screen.blit(glow_surf, glow_rect)
      else:
        color = NEON_PURPLE
        outline_width = 2

        # 버튼
        button_rect = pygame.Rect(button_x, button_y, button_width, 50)
        pygame.draw.rect(self.screen, (30, 30, 50), button_rect, border_radius=8)
        pygame.draw.rect(self.screen, color, button_rect, outline_width, border_radius=8)

      # 텍스트
      stage_text = self.menu_font.render(f"Stage {stage}", True, color)
      diff_text = self.small_font.render(
        DIFFICULTY_LEVELS[stage]["name"], True, color
      )

      self.screen.blit(stage_text, (button_x + button_width//2 - stage_text.get_width()//2, button_y + 5))
      self.screen.blit(diff_text, (button_x + button_width//2 - diff_text.get_width()//2, button_y + 30))

      # === 조작법 안내 ===
      controls_y = button_y + 80
      controls = [
        "Controls: Up Down (Player)  | Left Right (Stage) | Space (Start) | ESC (Quit)"
      ]

      for i, line in enumerate(controls):
        text = self.small_font.render(line, True, NEON_GREEN)
        self.screen.blit(text, (WIDTH//2 - text.get_width()//2, controls_y + i * 25))

  
      # === 시작 안내 (깜빡임) ===
      if int(self.pulse * 2) % 2 == 0:
        start_text = self.subtitle_font.render("PRESS SPACE TO START", True, NEON_YELLOW)

        self.screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT - 130))

      # 마우스 클릭 안내
      mouse_text = self.small_font.render("or click stage button", True, NEON_GREEN)

      self.screen.blit(mouse_text, (WIDTH//2 - mouse_text.get_width()//2, HEIGHT - 80))

  def handle_events(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        self.active = False
        return("start", self.selected_stage, self.selected_player)
      elif event.key == pygame.K_LEFT:
        self.selected_stage = max(1, self.selected_stage - 1)
      elif event.key == pygame.K_RIGHT:
        self.selected_stage = min(4, self.selected_stage + 1)
      elif event.key == pygame.K_UP:
        self.selected_player = (self.selected_player - 1) % len(self.player_images)
      elif event.key == pygame.K_DOWN:
        self.selected_player = (self.selected_player + 1) % len(self.player_images)
      elif event.key == pygame.K_ESCAPE:
        return ("quit", None, None)

    # 마우스 클릭
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = event.pos

      # 플레이어 아이콘 클릭 체크
      player_y = 60
      icon_y = player_y + 50
      icon_size = 60
      icon_spacing = 150
      start_x = WIDTH//2 - (len(self.player_images) * icon_spacing - icon_spacing + icon_size) // 2

      for i in range(len(self.player_images)):
        icon_x = start_x + i * icon_spacing
        icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)

        if icon_rect.collidepoint(mouse_x, mouse_y):
          self.selected_player = i
          return (None, None, None)

      # 스테이지 버튼 클릭 체크
      stage_y = icon_y + 120
      button_y = stage_y - 100
      button_width = 120
      button_spacing = 140
      start_x = WIDTH//2 - (4 * button_spacing - button_spacing + button_width) // 2

      for stage in range(1, 5):
        button_x = start_x + (stage - 1) * button_spacing
        button_rect = pygame.Rect(button_x, button_y, button_width, 40)

        if button_rect.collidepoint(mouse_x, mouse_y):
          self.selected_stage = stage
          self.active = False
          return ("start", self.selected_stage)

    return (None, None, None)

  def get_selected_player_image(self):
    return self.player_images[self.selected_player]
    
