from src.game import Game

if __name__ == "__main__":
  print("🎮 고전 슈팅 게임")
  print("=" * 60)
  print("\n조작법:")
  print("  - 마우스: 이동")
  print("  - 스페이스: 공격")
  print("  - Shift: 슬로우 모션")
  print("  - X: 폭탄 (적 탄막 전부 제거)")
  print("  - R: 재시작")
  print("  - ESC: 종료")
  print("\n난이도 선택:")
  print("  1: EASY")
  print("  2: NORMAL")
  print("  3: HARD")

  # difficulty = input("\n난이도를 선택하세요 (1-3): ")

  # try:
  #   difficulty = int(difficulty)
  #   if difficulty not in [1, 2, 3]:
  #       difficulty = 1
  # except:
  #   difficulty = 1

  game = Game()
  game.run()