# 게임 전역 상수 정의

# 화면 설정
WIDTH = 800
HEIGHT = 600
FPS = 60

# 색상(사이버펑크)
NEON_PINK = (255, 0, 200)
NEON_CYAN = (0, 255, 255)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE = (180, 0, 255)
NEON_GREEN = (0, 255, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (10, 5, 25)

# 플레이어
PLAYER_SPEED = 350
PLAYER_SLOW_SPEED = 140
PLAYER_HITBOX_RADIUS = 3
PLAYER_SHOOT_COOLDOWN = 0.15  # 초당 약 6발
PLAYER_MAX_HP = 3
PLAYER_ITEM_COUNT = 3

# 적/보스
BOSS_ATTACK_COOLDOWN = 2.5
ENEMY_SPAWN_INTERVAL = 3.0

# 탄막
BULLET_RADIUS = 6
PLAYER_BULLET_SPEED = 400
ENEMY_BULLET_SPEED = 150

# 파워업
POWERUP_SPEED = 100
POWERUP_DURATION = 5.0  # 지속 시간(초)

# 난이도
DIFFICULTY_LEVELS = {
  1: {"name": "EASY", "boss_hp": 200, "attack_speed": 3.0, "cooldown": 2.5, "boss_count": 1},
  2: {"name": "NORMAL", "boss_hp": 350, "attack_speed": 2.5, "cooldown": 2, "boss_count": 1},
  3: {"name": "HARD", "boss_hp": 250, "attack_speed": 2.0, "cooldown": 1, "boss_count": 2},
  4: {"name": "INSANE", "boss_hp": 250, "attack_speed": 1.5, "cooldown": 1, "boss_count": 3}
}

# 점수
SCORE_BULLET_HIT = 10
SCORE_BOSS_DEFEAT = 1000
SCORE_POWERUP = 50

# 파일 경로
ASSETS_PATH = "assets/images/"

# 리플레이
MAX_REPLAY_LENGTH = 10000  # 최대 프레임 수