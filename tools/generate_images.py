from PIL import Image, ImageDraw
import random
import math

# ================ 종이비행기 =================
def create_paper_plane(size=60, style="classic"):
  # 투명 배경 이미지 생성
  img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)

  # 중심 좌표
  center_x = size // 2
  center_y = size // 2

  # === 클래식 종이비행기 ===
  if style == "classic":
    # 메인 몸체(삼각형)
    body_points = [
      (center_x, center_y - 22),         # 앞쪽 끝
      (center_x - 18, center_y + 18),    # 왼쪽 날개 끝
      (center_x, center_y + 10),         # 뒷쪽 중앙
      (center_x + 18, center_y + 18)     # 오른쪽 날개 끝
    ]

    # 그림자(어두운 파란색)
    shadow_points = [(p[0] + 1, p[1] + 1) for p in body_points]
    draw.polygon(shadow_points, fill=(50, 80, 150, 180))

    # 메인 바디(밝은 하늘색)
    draw.polygon(shadow_points, fill=(120, 180, 255, 255))

    # 중앙 접힌 선
    draw.line([
      (center_x, center_y - 22),
      (center_x, center_y + 10)
    ], fill=(80, 130, 200, 255), width=2)

    # 날개 접힌 선
    draw.line([
      (center_x - 18, center_y + 18),
      (center_x, center_y - 10)
    ], fill=(80, 130, 200, 200), width=1)
    draw.line([
      (center_x + 18, center_y + 18),
      (center_x, center_y - 10)
    ], fill=(80, 130, 200, 200), width=1)

    # 외곽선
    draw.polygon(body_points, outline=(60, 100, 180, 255), width=2)

    # 하이라이트(빛 반사)
    highlight_points = [
      (center_x - 3, center_y - 15),
      (center_x - 8, center_y + 5),
      (center_x - 5, center_y + 3),
      (center_x, center_y - 13)
    ]
    draw.polygon(highlight_points, fill=(200, 230, 255, 150))
  # === 모던 종이비행기(각진 디자인) ===
  elif style == "modern":
    body_points = [
      (center_x, center_y - 24),      # 앞쪽
      (center_x - 20, center_y + 16), # 왼쪽 날개
      (center_x - 8, center_y + 16),  # 왼쪽 꼬리
      (center_x, center_y + 8),       # 뒷쪽 중앙
      (center_x + 8, center_y + 16),  # 오른쪽 꼬리
      (center_x + 20, center_y + 16), # 오른쪽 날개
    ]

    # 그라데이션 레이어
    for i in range(3):
      offset_points = [(p[0] + i, p[1] + i) for p in body_points]
      alpha = 100 - i * 20
      draw.polygon(offset_points, fill=(80, 120, 200, alpha))

    # 메인 색상
    draw.polygon(body_points, fill=(100, 160, 255, 255))

    # 디테일 라인
    draw.line([
      (center_x, center_y - 24),
      (center_x, center_y + 8)
    ], fill=(70, 110, 180, 255), width=3)

    # 날개 패턴
    draw.line([
      (center_x - 20, center_y + 16),
      (center_x - 5, center_y - 8)
    ], fill=(150, 200, 255, 200), width=2)
    draw.line([
      (center_x + 20, center_y + 16),
      (center_x + 5, center_y - 8)
    ], fill=(150, 200, 255, 200), width=2)

    # 외곽선
    draw.polygon(body_points, outline=(50, 80, 150, 255), width=2)
  # === 스타일리시 종이비행기(곡선 강조) ===
  elif style == "stylish":
    body_points = [
      (center_x, center_y - 25),
      (center_x - 22, center_y + 15),
      (center_x - 10, center_y + 12),
      (center_x, center_y + 5),
      (center_x + 10, center_y + 12),
      (center_x + 22, center_y + 15)
    ]

    # 그라데이션 배경
    for i in range(5, 0, -1):
      offset_points = [(p[0], p[1] + i) for p in body_points]
      alpha = 50 + i * 10
      draw.polygon(offset_points, fill=(80, 100, 200, alpha))

    # 메인 색상(더 선명한 파란색)
    draw.polygon(body_points, fill=(110, 170, 255, 255))

    # 중앙 스트라이프
    stripe_left = [
      (center_x - 3, center_y - 20),
      (center_x - 6, center_y + 5),
      (center_x - 3, center_y + 5),
      (center_x, center_y - 20)
    ]
    stripe_right = [
      (center_x + 3, center_y - 20),
      (center_x + 6, center_y + 5),
      (center_x + 3, center_y + 5),
      (center_x, center_y - 20)
    ]
    draw.polygon(stripe_left, fill=(70, 120, 220, 255))
    draw.polygon(stripe_right, fill=(70, 120, 220, 255))

    # 윙팁 하이라이트
    draw.ellipse([center_x - 22, center_y + 10, center_x - 16, center_y + 16], fill=(180, 220, 255, 200))
    draw.ellipse([center_x + 16, center_y + 10, center_x + 22, center_y + 16], fill=(180, 220, 255, 200))

    # 외곽선 (더 굵게)
    draw.polygon(body_points, outline=(40, 70, 150, 255), width=3)

    # 앞쪽 하이라이트
    draw.ellipse([center_x - 5, center_y - 22, center_x + 5, center_y - 12], fill=(200, 230, 255, 180))

  return img

# ================== 탄막 ====================
# ===== 탄막 이미지(작은 원형 탄환) =====
def create_normal_bullet(size=16):
  img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)
  draw.ellipse([2, 2, 14, 14], fill=(255, 100, 255, 255), outline=(255, 255, 255, 200), width=1)

  return img

# ===== 별 모양 탄막 =====
def create_star_bullet(size=20, color_style="neon"):
  img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)

  cx, cy = size // 2, size // 2

  # === 별 5개 꼭지점 계산 ===
  points = []
  for i in range(10):
    angle = (i * 36 - 90) * math.pi / 180 # 36도씩 회전
    radius = (size // 2 - 2) if i % 2 == 0 else (size // 4)
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    points.append((x, y))

  # === 네온 스타일(핑크) ===
  if color_style == "neon":
    for i in range(3, 0, -1):
      # 글로우 효과
      offset_points = [(x + random.uniform(-i, i), y + random.uniform(-i, i)) for x, y in points]
      draw.polygon(offset_points, fill=(255, 0, 150, 80))

    draw.polygon(points, fill=(255, 0, 200, 255))
    draw.polygon(points, outline=(255, 100, 255, 255), width=2)
  # === 사이버 스타일 (시안) ===
  elif color_style == "cyber":
    for i in range(3, 0, -1):
      offset_points = points
      draw.polygon(offset_points, fill=(0, 150, 255, 100 - i * 20))

    draw.polygon(points, fill=(0, 200, 255, 255))
    draw.polygon(points, outline=(0, 255, 255, 255), width=2)
  # === 전기 스타일(옐로우) ===
  elif color_style == "electric":
    for i in range(3, 0, -1):
      draw.polygon(points, fill=(255, 255, 0, 120 - i * 30))

    draw.polygon(points, fill=(255, 255, 100, 255))
    draw.polygon(points, outline=(255, 255, 200, 255), width=1)

  # 중앙 코어
  draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))

  return img

# =================== 배경 ===================
# 사이버 펑크 배경
def create_cyberpunk_background(width=800, height=600):
  img = Image.new('RGB', (width, height), (10, 5, 25))
  draw = ImageDraw.Draw(img)

  # === 그라데이션 하늘 ===
  for y in range(height):
    ratio = y / height
    r = int(10 + ratio * 30)
    g = int(5 + ratio * 15)
    b = int(25 + ratio * 50)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

  # === 원거리 빌딩 ===
  for i in range(20):
    x = random.randint(0, width)
    building_width = random.randint(30, 80)
    building_height = random.randint(150, 300)

    # 빌딩 그림자
    draw.rectangle([x, height - building_height, x + building_width, height], fill=(20, 10, 40))

    # 창문(네온 불빛)
    for floor in range(building_height // 15):
      for window in range(building_width // 10):
        wx = x + 5 + window * 10
        wy = height - building_height + 10 + floor * 15

        # 랜덤하게 불 켜진 창문
        if random.random() > 0.6:
          color = random.choice([
            (255, 0, 150),  # 핑크
            (0, 255, 255),  # 시안
            (255, 255, 0),  # 노랑
            (100, 255, 100) # 그린
          ])
          draw.rectangle([wx, wy, wx + 3, wy + 8], fill=color)
    
  # === 근거리 빌딩(더 밝고 디테일) ===
  # for i in range(5):
  #   x = random.randint(0, width - 100)
  #   building_width = random.randint(60, 120)
  #   building_height = random.randint(300, 450)

  #   # 메인 빌딩
  #   draw.rectangle([x, height - building_height, x + building_height, height], fill=(40, 20, 60))

  #   # 네온 외곽선
  #   neon_color = random.choice([
  #     (255, 0, 200),
  #     (0, 255, 255),
  #     (255, 100, 255)
  #   ])
  #   draw.rectangle([x, height - building_height, x + building_width, height], outline=neon_color, width=2)

  #   # 빌딩 창문들
  #   for floor in range(building_height // 12):
  #     for window in range(building_width // 8):
  #       wx = x + 4 + window * 8
  #       wy = height - building_height + 5 + floor * 12

  #       if random.random() > 0.4:
  #         window_color = random.choice([
  #           (255, 0, 150),
  #           (0, 200, 255),
  #           (255, 200, 0),
  #           (100, 255, 150)
  #         ])
  #         draw.rectangle([wx, wy, wx + 4, wy + 8], fill=window_color)
        
  # === 네온 광고판 ===
  # for i in range(8):
  #   x = random.randint(50, width - 150)
  #   y = random.randint(100, height - 200)
  #   ad_width = random.randint(80, 150)
  #   ad_height = random.randint(40, 80)

  #   # 글로우 효과
  #   for glow in range(5, 0, -1):
  #     draw.rectangle([x - glow, y - glow, x + ad_width + glow, y + ad_height + glow], fill=(255, 0, 200, 30))

  #   # 광고판
  #   ad_color = random.choice([
  #     (255, 0, 150),
  #     (0, 255, 255),
  #     (255, 255, 0)
  #   ])
  #   draw.rectangle([x, y, x + ad_width, y + ad_height], fill=ad_color)

  #   # 가로 라인
  #   for line in range(3):
  #     ly = y + (ad_height // 4) * (line + 1)
  #     draw.line([(x + 5, ly), (x + ad_width - 5, ly)], fill=(0, 0, 0), width=2)

  # === 날아다니는 차량 ===
  for i in range(12):
    x = random.randint(0, width)
    y = random.randint(50, height - 100)

    # 차량 본체
    draw.ellipse([x, y, x + 15, y + 6], fill=(100, 200, 255, 200))

    # 헤드라이트
    light_color = random.choice([(255, 0, 200), (0, 255, 255)])
    for j in range(3):
      draw.point((x - j, y + 3), fill=light_color)

  return img
  # === 레이저 빔 (하늘에서) ===
  # for _ in range(5):
  #   x = random.randint(0, width)
  #   draw.line([(x, 0), (x + random.randint(-50, 50), 200)], fill=(255, 0, 200, 100), width=2)

  

# =============== 파티클 - 불꽃 ==================
def create_fire_particle(size=16):
  img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)

  cx, cy = size // 2, size // 2

  # 외곽 불꽃(주황)
  for r in range(size//2, size//4, -1):
    alpha = int(200 * (size//2 - r) / (size//4))
    draw.ellipse([cx - r, cy - r, cx + r, cy+ r], fill=(255, 100, 0, alpha))

  # 중간 불꽃(노랑)
  for r in range(size//3, size//6, -1):
    alpha = int(255 * (size//3 -r) / (size//6))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 200, 0, alpha))

  # 중앙(흰색 - 가장 뜨거운 부분)
  draw.ellipse([cx - size//6, cy - size//6, cx + size//6, cy + size//6], fill=(255, 255, 200, 255))

  return img

# ================ 파티클 - 연기 ===============
def create_smoke_particle(size=24):
  img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)
    
  cx, cy = size // 2, size // 2

  # 불규칙한 연기 모양
  for i in range(5):
    offset_x = random.randint(-size//4, size//4)
    offset_y = random.randint(-size//4, size//4)
    r = random.randint(size//6, size//3)

    alpha = random.randint(30, 80)
    gray = random.randint(100, 180)

    draw.ellipse([cx + offset_x - r, cy + offset_y -r, cx + offset_x + r, cy + offset_y + r], fill=(gray, gray, gray, alpha))

    return img

# ================= 파티클 - 빛 =================
def create_light_particle(size=20, color_style="white"):
  img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)

  cx, cy = size//2, size//2

  if color_style == "white":
    colors = [(255, 255, 255), (255, 255, 200), (200, 200, 255)]
  elif color_style == "neon_pink":
      colors = [(255, 0, 200), (255, 100, 255), (200, 0, 150)]
  elif color_style == "neon_cyan":
      colors = [(0, 255, 255), (100, 255, 255), (0, 200, 200)]
  else:
      colors = [(255, 255, 0), (255, 255, 100), (255, 200, 0)]

  # 외부 글로우
  for r in range(size//2, 0, -1):
    alpha = int(150 * (size//2 - r) / (size//2))
    color_idx = min(int((size//2 - r) / (size//6)), 2)
    color = colors[color_idx]
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, alpha))

  # 밝은 중심
  draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255, 255))

  return img

# ================== 드래곤 보스 (네온 사이버펑크) ==============
def create_dragon_boss(size=150):
  img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)

  cx, cy = size//2, size//2

  # === 날개(뒤쪽) ====
  # 왼쪽 날개
  left_wing = [
    (cx - 10, cy - 5),
    (cx - 55, cy - 30),
    (cx - 70, cy - 10),
    (cx - 60, cy + 10),
    (cx - 40, cy + 5),
    (cx - 20, cy + 10)
  ]
  # 그라데이션 효과
  for i in range(3, 0, -1):
    offset_wing = [(x - i, y - i) for x, y in left_wing]
    draw.polygon(offset_wing, fill=(100, 0, 150, 100 + i * 30))
  draw.polygon(left_wing, fill=(150, 0, 255, 220))
  draw.polygon(left_wing, outline=(255, 0, 255, 255), width=2)

  # 오른쪽 날개
  right_wing = [
      (cx + 10, cy - 5),
      (cx + 55, cy - 30),
      (cx + 70, cy - 10),
      (cx + 60, cy + 10),
      (cx + 40, cy + 5),
      (cx + 20, cy + 10)
  ]
  for i in range(3, 0, -1):
      offset_wing = [(x + i, y - i) for x, y in right_wing]
      draw.polygon(offset_wing, fill=(100, 0, 150, 100 + i * 30))
  draw.polygon(right_wing, fill=(150, 0, 255, 220))
  draw.polygon(right_wing, outline=(255, 0, 255, 255), width=2)

  # === 몸통 ====
  body = [
      (cx, cy - 25),  # 머리
      (cx + 15, cy),
      (cx + 12, cy + 20),
      (cx + 8, cy + 40),  # 꼬리
      (cx - 8, cy + 40),
      (cx - 12, cy + 20),
      (cx - 15, cy)
  ]
  # 그림자
  shadow_body = [(x + 2, y + 2) for x, y in body]
  draw.polygon(shadow_body, fill=(50, 0, 100, 150))
  # 메인 몸통
  draw.polygon(body, fill=(180, 0, 255, 255))
  draw.polygon(body, outline=(255, 100, 255, 255), width=3)

  # === 머리 디테일 ===
  # 눈 (빛나는 효과)
  # 왼쪽 눈
  for r in range(8, 4, -1):
    alpha = int(255 * (9 - r) / 4)
    draw.ellipse([cx - 12 - r//2, cy - 18 - r//2, cx - 12 + r//2, cy - 18 + r//2], 
    fill=(0, 255, 255, alpha))
  draw.ellipse([cx - 14, cy - 20, cx - 10, cy - 16], fill=(0, 255, 255, 255))

  # 오른쪽 눈
  for r in range(8, 4, -1):
    alpha = int(255 * (9 - r) / 4)
    draw.ellipse([cx + 12 - r//2, cy - 18 - r//2, cx + 12 + r//2, cy - 18 + r//2], 
    fill=(0, 255, 255, alpha))
  draw.ellipse([cx + 10, cy - 20, cx + 14, cy - 16], fill=(0, 255, 255, 255))

  # 뿔
  # 왼쪽 뿔
  horn_left = [(cx - 8, cy - 25), (cx - 15, cy - 40), (cx - 12, cy - 38)]
  draw.polygon(horn_left, fill=(255, 0, 200, 255))
  draw.line([(cx - 8, cy - 25), (cx - 15, cy - 40)], fill=(255, 100, 255, 255), width=2)
  # 오른쪽 뿔
  horn_right = [(cx + 8, cy - 25), (cx + 15, cy - 40), (cx + 12, cy - 38)]
  draw.polygon(horn_right, fill=(255, 0, 200, 255))
  draw.line([(cx + 8, cy - 25), (cx + 15, cy - 40)], fill=(255, 100, 255, 255), width=2)

  # === 네온 라인 디테일 ===
  # 몸통 중앙선
  draw.line([(cx, cy - 20), (cx, cy + 35)], fill=(0, 255, 255, 255), width=2)
    
  # 날개 에너지 라인
  draw.line([(cx - 20, cy + 5), (cx - 50, cy - 15)], fill=(255, 0, 255, 200), width=2)
  draw.line([(cx + 20, cy + 5), (cx + 50, cy - 15)], fill=(255, 0, 255, 200), width=2)
  
  # === 코어 (가슴 부분 빛나는 구슬) ===
  for r in range(12, 6, -1):
      alpha = int(200 * (13 - r) / 6)
      draw.ellipse([cx - r//2, cy + 5 - r//2, cx + r//2, cy + 5 + r//2], fill=(0, 255, 200, alpha))
  draw.ellipse([cx - 6, cy - 1, cx + 6, cy + 11], fill=(0, 255, 255, 255))
  
  return img

# ===================== 실행 =====================

if __name__ == "__main__":
  print("게임 에셋 생성 start")
  # bullet = create_normal_bullet(16)
  # bullet.save('bullet_normal.png')

"""
  bg = create_cyberpunk_background(800, 600)
  bg.save('background.png')

  # === 드래곤 ===
  dragon = create_dragon_boss(150)
  dragon.save('boss.png')

  # === 탄막 ====
  star_neon = create_star_bullet(20, "neon")
  star_neon.save('bullet.png')

  star_cyber = create_star_bullet(20, "cyber")
  star_cyber.save('bullet_cyan.png')

  star_electric = create_star_bullet(20, "electric")
  star_electric.save('bullet_yellow.png')

  # === 파티클 ===
  # 불꽃
  fire_small = create_fire_particle(12)
  fire_small.save('particle_fire_small.png')

  fire_medium = create_fire_particle(16)
  fire_medium.save('particle_fire_medium.png')

  fire_large = create_fire_particle(24)
  fire_large.save('particle_fire_large.png')

  # 연기
  for i in range(3):
    smoke = create_smoke_particle(24)
    smoke.save(f'particle_smoke_{i+1}.png')

  # 빛
  light_white = create_light_particle(20, "white")
  light_white.save('particle_light_white.png')

  light_pink = create_light_particle(20, "neon_pink")
  light_pink.save('particle_light_pink.png')
  
  light_cyan = create_light_particle(20, "neon_cyan")
  light_cyan.save('particle_light_cyan.png')
  
  light_yellow = create_light_particle(20, "yellow")
  light_yellow.save('particle_light_yellow.png')

  # === 종이 비행기 === 
  classic = create_paper_plane(60, "classic")
  classic.save("player.png")

  modern = create_paper_plane(60, "modern")
  modern.save("player_modern.png")

  stylish = create_paper_plane(60, "stylish")
  stylish.save("player_stylish.png")

  classic_large = create_paper_plane(120, "classic")
  classic_large.save("player_large.png")
"""