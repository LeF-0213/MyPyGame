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

def create_dragon_king(size=200):
    """🐉 드래곤 킹 - Stage 1 (네온 사이버 드래곤)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    
    # === 몸통 (중앙 큰 다이아몬드) ===
    body_size = 50
    body = [
        (cx, cy - body_size),           # 머리 (위)
        (cx + body_size, cy),           # 오른쪽
        (cx, cy + body_size + 20),      # 꼬리 (아래)
        (cx - body_size, cy),           # 왼쪽
    ]
    
    # 그림자
    shadow_body = [(x+3, y+3) for x, y in body]
    draw.polygon(shadow_body, fill=(80, 0, 120, 150))
    
    # 메인 몸통
    draw.polygon(body, fill=(180, 0, 255, 255))  # 보라
    draw.polygon(body, outline=(255, 50, 255, 255), width=4)
    
    # === 날개 (뒤쪽) ===
    # 왼쪽 날개
    left_wing = [
        (cx - 10, cy - 10),
        (cx - 70, cy - 35),
        (cx - 85, cy - 5),
        (cx - 70, cy + 20),
        (cx - 30, cy + 5),
    ]
    draw.polygon(left_wing, fill=(150, 0, 200, 220))
    draw.polygon(left_wing, outline=(255, 0, 255, 255), width=3)
    
    # 오른쪽 날개
    right_wing = [
        (cx + 10, cy - 10),
        (cx + 70, cy - 35),
        (cx + 85, cy - 5),
        (cx + 70, cy + 20),
        (cx + 30, cy + 5),
    ]
    draw.polygon(right_wing, fill=(150, 0, 200, 220))
    draw.polygon(right_wing, outline=(255, 0, 255, 255), width=3)
    
    # === 머리 디테일 ===
    # 뿔 (왼쪽)
    horn_left = [
        (cx - 15, cy - body_size),
        (cx - 25, cy - body_size - 25),
        (cx - 18, cy - body_size - 22)
    ]
    draw.polygon(horn_left, fill=(255, 0, 200, 255))
    
    # 뿔 (오른쪽)
    horn_right = [
        (cx + 15, cy - body_size),
        (cx + 25, cy - body_size - 25),
        (cx + 18, cy - body_size - 22)
    ]
    draw.polygon(horn_right, fill=(255, 0, 200, 255))
    
    # 눈 (빛나는 효과)
    for eye_x in [cx - 18, cx + 18]:
        for r in range(8, 3, -1):
            draw.ellipse([eye_x - r, cy - body_size + 15 - r,eye_x + r, cy - body_size + 15 + r], fill=(0, 255, 255, 255 // (9 - r)))
        draw.ellipse([eye_x - 4, cy - body_size + 11, eye_x + 4, cy - body_size + 19], fill=(0, 255, 255, 255))
    
    # === 에너지 코어 (가슴) ===
    for r in range(15, 8, -1):
        alpha = 200 - (15 - r) * 20
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 255, 200, alpha))
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(0, 255, 255, 255))
    
    # === 몸통 라인 ===
    draw.line([(cx, cy - body_size + 10), (cx, cy + body_size)], fill=(255, 100, 255, 255), width=3)
    
    return img


def create_cyber_beast(size=200):
    """👾 사이버 비스트 - Stage 2 (메카닉 몬스터)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    
    # === 메인 바디 (육각형) ===
    angles = 6
    radius = 55
    body_points = []
    for i in range(angles):
        angle = (i / angles) * 2 * math.pi - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        body_points.append((x, y))
    
    # 그림자
    shadow_points = [(x+3, y+3) for x, y in body_points]
    draw.polygon(shadow_points, fill=(0, 80, 120, 150))
    
    # 메인 바디
    draw.polygon(body_points, fill=(0, 150, 255, 255))  # 시안
    draw.polygon(body_points, outline=(0, 255, 255, 255), width=4)
    
    # === 기계 팔 (4개) ===
    arm_positions = [
        (-60, -20, -80, -35),  # 왼쪽 위
        (-60, 20, -80, 35),    # 왼쪽 아래
        (60, -20, 80, -35),    # 오른쪽 위
        (60, 20, 80, 35),      # 오른쪽 아래
    ]
    
    for x1, y1, x2, y2 in arm_positions:
        # 팔
        draw.line([(cx + x1, cy + y1), (cx + x2, cy + y2)],fill=(0, 200, 255, 255), width=8)
        # 관절
        draw.ellipse([cx + x1 - 6, cy + y1 - 6, cx + x1 + 6, cy + y1 + 6], fill=(255, 0, 200, 255))
        # 끝 부분 (무기)
        draw.ellipse([cx + x2 - 8, cy + y2 - 8, cx + x2 + 8, cy + y2 + 8], fill=(255, 255, 0, 255))
    
    # === 코어 (중앙 육각형) ===
    core_radius = 25
    core_points = []
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = cx + core_radius * math.cos(angle)
        y = cy + core_radius * math.sin(angle)
        core_points.append((x, y))
    
    draw.polygon(core_points, fill=(255, 0, 200, 255))
    draw.polygon(core_points, outline=(255, 255, 255, 255), width=2)
    
    # === 눈 (3개) ===
    for eye_y in [cy - 15, cy, cy + 15]:
        for r in range(6, 2, -1):
            draw.ellipse([cx - r, eye_y - r, cx + r, eye_y + r],
                        fill=(255, 255, 0, 200 - r * 20))
        draw.ellipse([cx - 3, eye_y - 3, cx + 3, eye_y + 3],
                    fill=(255, 255, 255, 255))
    
    # === 기계 디테일 (선) ===
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x1 = cx + 25 * math.cos(angle)
        y1 = cy + 25 * math.sin(angle)
        x2 = cx + 55 * math.cos(angle)
        y2 = cy + 55 * math.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=(0, 255, 255, 255), width=2)
    
    return img


def create_thunder_lord(size=200):
    """⚡ 썬더 로드 - Stage 3 (전기 드래곤)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    
    # === 뱀 같은 몸통 (S자 곡선) ===
    segments = 8
    for i in range(segments):
        t = i / segments
        # S자 곡선
        x = cx + 30 * math.sin(t * math.pi * 2)
        y = cy - 60 + t * 120
        radius = 25 - t * 8
        
        # 세그먼트
        draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                    fill=(255, 255, 0, 255))
        draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                    outline=(255, 255, 255, 255), width=2)
        
        # 전기 스파크
        if i % 2 == 0:
            spark_points = [
                (x - radius, y),
                (x - radius - 15, y - 10),
                (x - radius - 5, y),
                (x - radius - 20, y + 10),
                (x - radius, y)
            ]
            draw.polygon(spark_points, fill=(255, 255, 100, 255))
    
    # === 머리 (꼭대기) ===
    head_size = 40
    head = [
        (cx, cy - 80),                    # 뾰족한 머리
        (cx + 25, cy - 60),
        (cx + 20, cy - 40),
        (cx - 20, cy - 40),
        (cx - 25, cy - 60),
    ]
    
    # 그림자
    shadow_head = [(x+2, y+2) for x, y in head]
    draw.polygon(shadow_head, fill=(100, 100, 0, 150))
    
    # 메인 머리
    draw.polygon(head, fill=(255, 255, 0, 255))
    draw.polygon(head, outline=(255, 255, 255, 255), width=3)
    
    # === 뿔 (전기 안테나) ===
    for horn_x in [cx - 20, cx + 20]:
        # 뿔
        horn = [
            (horn_x, cy - 70),
            (horn_x - 5, cy - 95),
            (horn_x + 5, cy - 95),
        ]
        draw.polygon(horn, fill=(255, 200, 0, 255))
        
        # 전기 효과
        for i in range(5):
            offset = i * 5
            draw.line([(horn_x, cy - 70 - offset), 
                      (horn_x + (-1)**i * 8, cy - 75 - offset)],
                     fill=(255, 255, 200, 255), width=2)
    
    # === 눈 (번개 모양) ===
    for eye_x in [cx - 12, cx + 12]:
        # 번개 눈
        lightning = [
            (eye_x, cy - 60),
            (eye_x + 3, cy - 55),
            (eye_x - 1, cy - 55),
            (eye_x + 2, cy - 50),
            (eye_x - 2, cy - 50),
            (eye_x, cy - 45),
        ]
        draw.polygon(lightning, fill=(255, 255, 255, 255))
        
        # 글로우
        for r in range(8, 3, -1):
            draw.ellipse([eye_x - r, cy - 52 - r, eye_x + r, cy - 52 + r],
                        fill=(255, 255, 0, 150 - r * 10))
    
    # === 에너지 코어 (가슴) ===
    for r in range(18, 10, -1):
        alpha = 200 - (18 - r) * 15
        draw.ellipse([cx - r, cy - 50 - r, cx + r, cy - 50 + r],
                    fill=(255, 255, 100, alpha))
    draw.ellipse([cx - 10, cy - 60, cx + 10, cy - 40],
                fill=(255, 255, 255, 255))
    
    return img


def create_twin_demons(size=200):
    """💀 트윈 데몬즈 - Stage 4 (쌍둥이 악마)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    
    # === 쌍둥이 구조 (좌우 대칭) ===
    offset = 35
    
    for side in [-1, 1]:  # -1: 왼쪽, 1: 오른쪽
        base_x = cx + side * offset
        
        # === 몸통 (역삼각형) ===
        body = [
            (base_x, cy - 45),                    # 머리
            (base_x - 25, cy + 30),               # 왼쪽 아래
            (base_x + 25, cy + 30),               # 오른쪽 아래
        ]
        
        # 그림자
        shadow = [(x+2, y+2) for x, y in body]
        draw.polygon(shadow, fill=(80, 0, 0, 150))
        
        # 메인 몸통 (좌우 색 다르게)
        if side == -1:
            body_color = (255, 0, 100, 255)   # 왼쪽: 핑크
            outline_color = (255, 100, 150, 255)
        else:
            body_color = (200, 0, 255, 255)   # 오른쪽: 보라
            outline_color = (255, 100, 255, 255)
        
        draw.polygon(body, fill=body_color)
        draw.polygon(body, outline=outline_color, width=3)
        
        # === 날개 (박쥐 날개) ===
        wing = [
            (base_x, cy - 10),
            (base_x - side * 40, cy - 30),
            (base_x - side * 50, cy - 10),
            (base_x - side * 45, cy + 5),
            (base_x - side * 20, cy + 5),
        ]
        draw.polygon(wing, fill=body_color)
        draw.polygon(wing, outline=outline_color, width=2)
        
        # === 뿔 (악마 뿔) ===
        for horn_side in [-1, 1]:
            horn_x = base_x + horn_side * 15
            horn = [
                (horn_x, cy - 45),
                (horn_x + horn_side * 5, cy - 60),
                (horn_x + horn_side * 12, cy - 58),
                (horn_x + horn_side * 8, cy - 45),
            ]
            draw.polygon(horn, fill=(50, 0, 50, 255))
            draw.line([(horn_x, cy - 45), (horn_x + horn_side * 10, cy - 59)], fill=(255, 0, 0, 255), width=2)
        
        # === 눈 (빛나는 빨간 눈) ===
        eye_x = base_x
        eye_y = cy - 30
        
        for r in range(10, 4, -1):
            alpha = 200 - (10 - r) * 20
            draw.ellipse([eye_x - r, eye_y - r, eye_x + r, eye_y + r],
                        fill=(255, 0, 0, alpha))
        draw.ellipse([eye_x - 5, eye_y - 5, eye_x + 5, eye_y + 5],
                    fill=(255, 50, 50, 255))
        draw.ellipse([eye_x - 2, eye_y - 2, eye_x + 2, eye_y + 2],
                    fill=(255, 255, 255, 255))
        
        # === 이빨 ===
        teeth_y = cy + 30
        for tooth_x in range(-15, 20, 10):
            tooth = [
                (base_x + tooth_x, teeth_y),
                (base_x + tooth_x - 3, teeth_y + 8),
                (base_x + tooth_x + 3, teeth_y + 8),
            ]
            draw.polygon(tooth, fill=(255, 255, 255, 255))
    
    # === 중앙 연결 (에너지) ===
    for i in range(5):
        y_pos = cy - 20 + i * 10
        draw.line([(cx - offset, y_pos), (cx + offset, y_pos)],
                 fill=(255, 0, 200, 150 - i * 20), width=3)
    
    # 중앙 코어
    for r in range(12, 6, -1):
        alpha = 200 - (12 - r) * 20
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                    fill=(255, 0, 150, alpha))
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6],
                fill=(255, 255, 255, 255))
    
    return img

# ===================== 실행 =====================

if __name__ == "__main__":
  print("게임 에셋 생성 start")
  dragon = create_dragon_king(200)
  dragon.save('assets/images/boss_stage1.png')
  # cyber = create_cyber_beast(150)
  # cyber.save('assets/images/boss_stage2.png')
  thunder = create_thunder_lord(200)
  thunder.save('assets/images/boss_stage3.png')
  demons = create_twin_demons(150)
  demons.save('assets/images/boss_stage4.png')


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