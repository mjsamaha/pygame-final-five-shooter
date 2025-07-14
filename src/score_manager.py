
class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0

    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self):
        self.score = 0
