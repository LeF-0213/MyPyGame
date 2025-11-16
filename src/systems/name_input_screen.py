import pygame, math
from src.utils.constants import *

class NameInputScreen:
  def __init__(self, screen, score, stage, character_name):
    self.screen = screen
    self.score = score
    self.stage = stage
    self.character_name = character_name
    self.active = True

    # 폰트
    self.title_font = pygame.font.Font(None, 72)
    self.text_font = pygame.font.Font(None, 48)
    self.small_font = pygame.font.Font(None, 24)

    self.name = ""
    self.max_length = 15
    self.cursor_visible = True
    self.cursor_timer = 0
    self.pulse = 0

  def update(self, dt):
    self.pulse += dt * 2
    self.cursor_timer += dt

    if self.cursor_timer > 0.5:
      self.cursor_timer = 0
      self.cursor_visible = not self.cursor_visible

  def draw(self):
    # 반투명 오버레이
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    self.screen.blit(overlay, (0, 0))

    # 타이틀
    title_text = self.title_font.render("NEW HIGH SCORE!", True, NEON_YELLOW)
    pulse_alpha = int(150 + math.sin(self.pulse) * 50)

    for i in range(3, 0, -1):
      glow_surf = pygame.Surface((title_text.get_width() + i*10, title_text.get_height() + i*10), pygame.SRCALPHA)
      glow_text = self.title_font.render("NEW HIGH SCORE!", True, (*NEON_YELLOW, pulse_alpha // i))
      glow_surf.blit(glow_text, (i*5, i*5))
      self.screen.blit(glow_surf, (WIDTH//2 - title_text.get_width()//2 - i*5, 150 - i*5))

    self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 150))

    # 점수 정보
    score_text = self.text_font.render(f"SCORE: {int(self.score):,}", True, NEON_CYAN)
    self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 240))

    stage_text = self.small_font.render(f"Stage {self.stage} | {self.character_name}", True, NEON_PINK)
    self.screen.blit(stage_text, (WIDTH//2 - stage_text.get_width()//2, 290))

    # 이름 입력 안내
    prompt_text = self.text_font.render("Enter Your Name:", True, WHITE)
    self.screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, 360))

    # 입력 박스
    box_width = 500
    box_height = 60
    box_x = WIDTH//2 - box_width//2
    box_y = 420

    # 박스 배경
    pygame.draw.rect(self.screen, (30, 30, 50), (box_x, box_y, box_width, box_height), border_radius=10)
    
    # 박스 테두리 (펄스 효과)
    pulse_size = int(2 + math.sin(self.pulse * 3) * 2)
    pygame.draw.rect(self.screen, NEON_CYAN, (box_x, box_y, box_width, box_height), pulse_size, border_radius=10)

    # 입력된 테스트
    display_name = self.name if self.name else ""
    if self.cursor_visible:
      display_name += "|"

    name_text = self.text_font.render(display_name, True, NEON_YELLOW)
    text_x = box_x + (box_width - name_text.get_width()) // 2
    text_y = box_y + (box_height - name_text.get_height()) // 2
    self.screen.blit(name_text, (text_x, text_y))

    # 글자 수 표시
    count_text = self.small_font.render(f"{len(self.name)}/{self.max_length}", True, (150, 150, 150))
    self.screen.blit(count_text, (box_x + box_width - count_text.get_width() - 10, box_y + box_height + 10))

    # 안내 메시지
    if int(self.pulse * 2) % 2 == 0:
      if self.name:
        info_text = self.small_font.render("Press ENTER to submit | ESC to skip", True, WHITE)
      else:
        info_text = self.small_font.render("Type your name... (ESC to skip)", True, (150, 150, 150))

      self.screen.blit(info_text, (WIDTH//2 - info_text.get_width()//2, HEIGHT - 80))

  def handle_events(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RETURN:
        if not self.name.strip():
          self.name = "Player"
        self.active = False
        return("submit", self.name)

      elif event.key == pygame.K_ESCAPE:
        self.active = False
        return ("skip", "Player")

      elif event.key == pygame.K_BACKSPACE:
        self.name = self.name[:-1]

      elif len(self.name) < self.max_length:
        if event.unicode.isprintable() and event.unicode not in ['|']:
          self.name += event.unicode

    return (None, None)