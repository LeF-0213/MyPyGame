import pygame, math
from src.utils.constants import *

class RankingScreen:
  def __init__(self, screen, ranking_system):
    self.screen = screen
    self.ranking_system = ranking_system
    self.active = True

    self.title_font = pygame.font.Font(None, 72)
    self.header_font = pygame.font.Font(None, 36)
    self.rank_font = pygame.font.Font(None, 28)
    self.small_font = pygame.font.Font(None, 24)

    self.pulse = 0
    self.scroll_offset = 0

  def update(self, dt):
    self.pulse += dt * 2

  def draw(self):
    # 그라데이션 배경
    for y in range(HEIGHT):
      ratio = y / HEIGHT
      r = int(5 + ratio * 15)
      g = int(5 + ratio * 10)
      b = int(20 + ratio * 40)
      pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    # 타이틀
    title_text = self.title_font.render("HALL OF FAME", True, NEON_YELLOW)
    pulse_alpha = int(150 + math.sin(self.pulse) * 50)

    for i in range(3, 0, -1):
      glow_surf = pygame.Surface((title_text.get_width() + i*10, title_text.get_height() + i*10), pygame.SRCALPHA)
      glow_text = self.title_font.render("HALL OF FAME", True, (*NEON_YELLOW, pulse_alpha // i))
      glow_surf.blit(glow_text, (i*5, i*5))
      self.screen.blit(glow_surf, (WIDTH//2 - title_text.get_width()/2 - i*5, 50 - i*5))

    self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))

    # 구분선
    pygame.draw.line(self.screen, NEON_CYAN, (100, 130), (WIDTH - 100, 130), 2)

    # 헤더
    y_offset = 160
    header_texts = ["RANK", "NAME", "SCORE", "STAGE", "CHARACTER", "DATE"]
    header_x_positions = [150, 250, 400, 530, 650, 800]

    for i, (text, x_pos) in enumerate(zip(header_texts, header_x_positions)):
      header = self.header_font.render(text, True, NEON_CYAN)
      self.screen.blit(header, (x_pos, y_offset))

    # 구분선
    pygame.draw.line(self.screen, NEON_PURPLE, (100, y_offset + 40), (WIDTH - 100, y_offset + 40), 1)

    # 랭킹 목록
    rankings = self.ranking_system.get_top_rankings(15)
    y_offset = 220

    if not rankings:
      no_data = self.header_font.render("No records yet!", True, (150, 150, 150))
      self.screen.blit(no_data, (WIDTH//2 - no_data.get_width()//2, HEIGHT//2))
    else:
      for i, entry in enumerate(rankings):
        rank = i + 1

        # 순위별 색상
        if rank == 1:
          color = NEON_YELLOW
          rank_text = "🥇1st"
        elif rank == 2:
          color = (200, 200, 200)
          rank_text = "🥈2nd"
        elif rank == 3:
          color = (205, 127, 50)
          rank_text = "🥉3rd"
        else:
          color = WHITE
          rank_text = f"🏅{rank}th"

        # 배경 (짝수/홀수 구분)
        if i % 2 == 0:
          bg_rect = pygame.Rect(110, y_offset - 5, WIDTH - 220, 35)
          pygame.draw.rect(self.screen, (20, 20, 40, 100), bg_rect, border_radius=5)

        # 순위
        rank_surface = self.rank_font.render(rank_text, True, color)
        self.screen.blit(rank_surface, (155, y_offset))

        # 이름
        name_surface = self.rank_font.render(entry["name"][:15], True, color)
        self.screen.blit(name_surface, (250, y_offset))

        # 점수
        score_surface = self.rank_font.render(f"{entry['score']:,}", True, NEON_PINK)
        self.screen.blit(score_surface, (400, y_offset))

        # 스테이지
        stage_surface = self.rank_font.render(f"Stage {entry['stage']}", True, NEON_GREEN)
        self.screen.blit(stage_surface, (530, y_offset))

        # 캐릭터
        char_surface = self.small_font.render(entry["character"], True, NEON_CYAN)
        self.screen.blit(char_surface, (650, y_offset + 2))

        # 날짜
        date_surface = self.small_font.render(entry["date"], True, (150, 150, 150))
        self.screen.blit(date_surface, (800, y_offset + 2))

        y_offset += 40

    # 하단 안내
    pygame.draw.line(self.screen, NEON_CYAN, (100, HEIGHT - 100), (WIDTH - 100, HEIGHT - 100), 2)

    if int(self.pulse * 2) % 2 == 0:
      back_text = self.header_font.render("PRESS ESC TO RETURN", True, NEON_YELLOW)
      self.screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 60))

  def handle_events(self, event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        self.active = False
        return "back"

    return None