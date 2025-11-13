import random
from sys.utils.constants import *

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
    for _ in rnage(100):
      x = random.randint(0, WIDTH)
      y = random.radint(0, HEIGHT)
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
      self.screen.glit(glow_surf, (WIDTH//2 - title_text.get_width()//2 - i*5, 100 - i*5))
    
    self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
    self.screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, 180))

    # === 게임 설명 ===
    y_offset = 280

    instructions = [
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "🎮 CONTROLS",
      "",
      "  Mouse        - Move",
      "  Space        - Shoot",
      "  Shift        - Slow Mode",
      "  X            - Use Item (Bomb)",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "⚔️  GAME INFO",
      "",
      "  • 4 Stages with increasing difficulty",
      "  • Boss HP bar & 3 Phase system",
      "  • Power-ups: [P] Power  [I] Item  [+] HP",
      "  • Stage 4: Twin Boss Battle!",
      ""
    ]

    for i, line in enumerate(instructions):
      if line.startswith("🎮") or line.startswith("⚔️"):
        color = NEON_YELLOW
        font = self.menu_font
      elif line.startswith("  •"):
        color = NEON_CYAN
        font = self.small_font
      elif line.startswith("  "):
        color = WHITE
        font = self.small_font
      elif line.startswith("━"):
        color = NEON_PURPLE
        font = self.small_font
      else:
        color = (150, 150, 150)
        font = self.small_font

      text = font.render(line, True, color)
      self.screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset + i * 22))

    # === 난이도 선택 ===
    stage_y = HEIGHT - 150

    stage_title = self.menu_font.render("SELECT STAGE", True, NEON_YELLOW)

