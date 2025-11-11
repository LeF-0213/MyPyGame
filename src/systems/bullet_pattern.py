import math, random
from src.entities.bullet import *

class BulletPattern:

  # 원형 패턴
  @staticmethod
  def create_circle(x, y, count, speed, image, pattern_type="normal"):
    bullets = []
    angle_step = (2 * math.pi) / count

    for i in range(count):
      angle = i * angle_step

      if pattern_type == "spiral":
        bullet = SpiralBullet(x, y, speed, angle, image)
      elif pattern_type == "accel":
        bullet = AcceleratingBullet(x, y, speed, angle, image)
      else:
        bullet = Bullet(x, y, speed, angle, image)

      bullets.append(bullet)

    return bullets

  # 이중 원형 패턴
  @staticmethod
  def create_double_circle(x, y, count, speed, image):
    bullets = []
    angle_step = (2 * math.pi) / count

    for i in range(count):
      angle = i * angle_step
      bullets.append(Bullet(x, y, speed, angle, image))
      bullets.append(Bullet(x, y, speed * 0.7, angle + angle_step/2, image))

    return bullets

  # 겨냥 부채꼴 패턴
  @staticmethod
  def create_aimed_burst(x, y, target_x, target_y, count, speed, image):
    bullets = []
    base_angle = math.atan2(target_y - y, target_x - x)
    spread = math.pi / 6

    for i in range(count):
      if count == 1:
        angle = base_angle
      else:
        angle = base_angle - spread/2 + (spread * i / (count - 1))
      bullets.append(Bullet(x, y, speed, angle, image))

    return bullets
  
  # 다중 나선 패턴
  @staticmethod
  def create_spiral_wave(x, y, wave_count, bullets_per_wave, speed, image):
    bullets = []
    for wave in range(wave_count):
      angle_offset = (wave / wave_count) * (2 * math.pi)

      for i in range(bullets_per_wave):
        angle = (i / bullets_per_wave) * (2 * math.pi) + angle_offset
        bullets.append(SpiralBullet(x, y, speed, angle, image, spiral_speed = 2))

    return bullets

  # 랜덤 분사 패턴
  @staticmethod
  def create_random_spray(x, y, count, min_speed, max_speed, image):
    bullets = []
    for _ in range(count):
      angle = random.uniform(0, 2 * math.pi)
      speed = random.uniform(min_speed, max_speed)
      bullets.append(Bullet(x, y, speed, angle, image))

    return bullets

  @staticmethod
  def create_homing_cluster(x, y, count, speed, image, target):
    bullets = []
    angle_step = (2 * math.pi) / count

    for i in range(count):
      angle = i * angle_step
      bullet = HomingBullet(x, y, speed, angle, image, turn_speed = 2.0)
      bullet.set_target(target)
      bullets.append(bullet)

    return bullets

  # 십자 레이저 패턴
  @staticmethod
  def create_laser_cross(x, y):
    lasers = []
    for angle in [0, math.pi/2, math.pi, math.pi * 3/2]:
      lasers.append(LaserBullet(x, y, angle, length=600, duration=1.5))

    return lasers

  # x자 레이저 패턴
  @staticmethod
  def create_laser_x(x, y):
    lasers = []

    for angle in [math.pi/4, math.pi*3/4, math.pi*5/4, math.pi*7/4]:
      lasers.append(LaserBullet(x, y, angle, length=600, duration=1.5))

    return lasers
    
  # 회전 레이저 패턴 
  @staticmethod
  def create_laser_spin(x, y, count=8):
    lasers = []
    angle_step = (2 * math.pi) / count

    for i in range(count):
      angle = i * angle_step
      lasers.append(LaserBullet(x, y, angle, length=500, duration=2.0))

    return lasers