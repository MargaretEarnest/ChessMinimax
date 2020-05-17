from graphics import *


class Board:
    whiteList = []
    blackList = []
    score = 0

    def __init__(self, whiteList, blackList, score):
        self.whiteList = whiteList
        self.blackList = blackList
        self.score = score

    def returnWinner(self):
        return None