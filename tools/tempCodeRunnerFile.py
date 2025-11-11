for i in range(5):
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