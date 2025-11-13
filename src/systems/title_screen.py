import random, pygame, math
from src.utils.constants import *

class TitleScreen:
  def __init__(self, screen):
    self.screen = screen
    self.active = True
    self.selected_stage = 1

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
      self.screen.blit(glow_surf, (WIDTH//2 - title_text.get_width()//2 - i*5, 30 - i*5))
    
    self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))
    self.screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, 90))

    # === 게임 설명 ===
    y_offset = 140

    instructions = [
      "CONTROLS",
      "========================================",
      "  Mouse -------- Move           ",
      "  Space -------- Shoot          ",
      "  Shift -------- Slow Mode      ",
      "  X -------- Use Item (Bomb)  ",
      "",
      "GAME INFO",
      "========================================",
      "  • 4 Stages with increasing difficulty   ",
      "  • Boss HP bar & 3 Phase system          ",
      "  • Power-ups: [P] Power  [I] Item  [+] HP",
      "  • Stage 4: Twin Boss Battle!            ",
    ]

    for i, line in enumerate(instructions):
      if line.startswith("C") or line.startswith("G"):
        color = NEON_YELLOW
        font = self.menu_font
      elif line.startswith("  •"):
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
    stage_y = HEIGHT - 150

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
  
      # === 시작 안내 (깜빡임) ===
      if int(self.pulse * 2) % 2 == 0:
        start_text = self.subtitle_font.render("PRESS SPACE TO START", True, NEON_YELLOW)

        self.screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT - 60))

      # 마우스 클릭 안내
      mouse_text = self.small_font.render("or click stage button", True, (150, 150, 150))

      self.screen.blit(mouse_text, (WIDTH//2 - mouse_text.get_width()//2, HEIGHT - 30))

  def handle_events(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        self.active = False
        return("start", self.selected_stage)
      elif event.key == pygame.K_LEFT:
        self.selected_stage = max(1, self.selected_stage - 1)
      elif event.key == pygame.K_RIGHT:
        self.selected_stage = min(4, self.selected_stage + 1)
      elif event.key == pygame.K_ESCAPE:
        return ("quit", None)

    # 마우스 클릭
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = event.pos
      button_y = HEIGHT - 100
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

    return (None, None)
    
