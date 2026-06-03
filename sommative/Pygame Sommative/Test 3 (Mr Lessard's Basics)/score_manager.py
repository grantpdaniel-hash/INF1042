class ScoreManager:
    def __init__(self, correct_pts: int, wrong_pts: int):
        self.score        = 0
        self.correct_pts  = correct_pts
        self.wrong_pts    = wrong_pts   # already negative from settings
        self.correct_streak = 0
        self.total_correct  = 0
        self.total_wrong    = 0

    def correct(self):
        self.correct_streak += 1
        self.total_correct  += 1
        bonus = 50 if self.correct_streak >= 3 else 0
        self.score += self.correct_pts + bonus
        return self.correct_pts + bonus

    def wrong(self):
        self.correct_streak = 0
        self.total_wrong   += 1
        self.score          = max(0, self.score + self.wrong_pts)
        return self.wrong_pts

    def reset(self):
        self.__init__(self.correct_pts, self.wrong_pts)