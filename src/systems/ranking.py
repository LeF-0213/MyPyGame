import json, os
from datetime import datetime

class RankingSystem:
  def __init__(self, filename="rankings.json"):
    self.filename = filename
    self.rankings = []
    self.load_rankings()

  # 랭킹 데이터 로드
  def load_rankings(self):
    try:
      if os.path.exists(self.filename):
        with open(self.filename, 'r', encoding='utf-8') as f:
          self.rankings = json.load(f)
      else:
        self.rankings = []
    except Exception as e:
      print(f"랭킹 로드 실패: {e}")
      self.rankings = []
  
  # 랭킹 데이터 저장
  def save_rankings(self):
    try:
      with open(self.filename, 'w', encoding='utf-8') as f:
        json.dump(self.rankings, f, ensure_ascii=False, indent=2)
    except Exception as e:
      print(f"랭킹 저장 실패: {e}")
  
  # 새로운 점수 추가
  def add_score(self, player_name, score, stage, character):
    entry = {
      'name': player_name,
      'score': int(score),
      'stage': stage,
      'character': character,
      'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    self.rankings.append(entry)
    # 점수 내림차순 정렬
    self.rankings.sort(key=lambda x: x["score"], reverse=True)
    # 상위 50개만 유지(메모리 절약)
    self.rankings = self.rankings[:50]
    self.save_rankings()

  # 상위 랭킹 가져오기
  def get_top_rankings(self, count=10):
    return self.rankings[:count]

  # Top 10 진입 여부 확인
  def is_high_score(self, score):
    if len(self.rankings) < 10:
      return True
    return score > self.rankigs[9]["score"]

  # 해당 점수의 순위 반환
  def get_rank_position(self, score):
    for i, entry in enumerate(self.rankings):
      if score >= entry["score"]:
        return i + 1
    return len(self.rankings) + 1
