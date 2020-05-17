from graphics import *
from Board import Board


class ChessPiece:
    name = ""
    x = 0
    y = 0
    c = None
    t = None
    b = None
    boxed = False
    col = ""

    def __init__(self, name, color):
        self.name = name
        self.col = color

    def moveTo(self, win, nx, ny):
        self.x = nx
        self.y = ny
        if self.boxed:
            self.boxToggle(win)
        if self.c is not None and self.t is not None:
            self.c.undraw()
            self.t.undraw()
        self.c = Circle(Point(self.x, self.y), 20)
        self.t = Text(Point(self.x, self.y), self.name)
        if self.col == "white":
            self.t.setFill('black')
        else:
            self.t.setFill('white')
        self.c.setFill(self.col)
        self.c.draw(win)
        self.t.draw(win)

    def remove(self, b: Board):
        temp = b
        self.t.undraw()
        self.c.undraw()
        if (self.x, self.y) in b.whiteList:
            temp.whiteList[(self.x, self.y)] = None
        if (self.x, self.y) in b.blackList:
            temp.blackList[(self.x, self.y)] = None
        return temp

    def findBishop(self, occupied):
        available = []
        for r in range(1, 5):
            for n in range(1, 9):
                x = self.x + (1 if r // 2 == 1 else -1) * n * 50
                y = self.y + (1 if r % 2 == 1 else -1) * n * 50
                if occupied.get((x, y)) is None and x > 0 and y > 0 and x < 400 and y < 400:
                    available.append((x, y))
                else:
                    break
        return available

    def findRook(self, occupied):
        available = []
        for r in range(1,5):
            for n in range(1, 9):
                x = self.x + (0 if r < 3 else r*2 - 7) * n * 50
                y = self.y + (0 if r > 2 else r*2 - 3) * n * 50
                if occupied.get((x, y)) is None and x > 0 and y > 0 and x < 400 and y < 400:
                    available.append((x, y))
                else:
                    break
        return available

    def findPawn(self, occupied, b: Board):
        available = []
        if occupied.get((self.x, self.y + 50)) is None and (self.x, self.y) in b.whiteList and self.y + 50 < 400:
            available.append((self.x, self.y + 50))
            if self.y == 75:
                available.append((self.x, self.y + 100))
        elif occupied.get((self.x, self.y - 50)) is None and (self.x, self.y) in b.blackList and self.y - 50 > 0:
            available.append((self.x, self.y - 50))
            if self.y == 325:
                available.append((self.x, self.y - 100))
        return available

    def findKnight(self, occupied):
        available = []
        path = [1, 2, 2, 1]
        for n in range(0, 8):
            x = self.x + 50 * (1 if n < 4 else -1) * path[n % 4]
            y = self.y + 50 * (1 if n // 2 % 2 != 0 else -1) * path[(n + 2) % 4]
            if occupied.get((x, y)) is None and x > 0 and y > 0 and x < 400 and y < 400:
                available.append((x, y))
        return available

    def findKing(self, occupied):
        available = []
        for n in range(0, 9):
            x = self.x + (n // 3 - 1) * 50
            y = self.y + (n % 3 - 1) * 50
            if occupied.get((x, y)) is None and x > 0 and y > 0 and x < 400 and y < 400:
                available.append((x, y))
        return available

    def findAvailable(self, b: Board):
        available = []
        occupied = dict(b.whiteList)
        occupied.update(b.blackList)
        if self.name[0] == "P":
            available.extend(self.findPawn(occupied, b))
        elif self.name[0] == "R":
            available.extend(self.findRook(occupied))
        elif self.name[0] == "K" and len(self.name) > 1:
            available.extend(self.findKnight(occupied))
        elif self.name[0] == "B":
            available.extend(self.findBishop(occupied))
        elif self.name[0] == "K":
            available.extend(self.findKing(occupied))
        elif self.name[0] == "Q":
            available.extend(self.findRook(occupied))
            available.extend(self.findBishop(occupied))
        return available

    def validMove(self, b: Board, t):
        return t in self.findAvailable(b)

    def boxToggle(self, win):
        if not self.boxed:
            self.b = Rectangle(Point(self.x - 25, self.y - 25), Point(self.x + 25, self.y + 25))
            self.b.setWidth(8)
            self.b.setOutline("yellow")
            self.b.draw(win)
            self.boxed = True
        else:
            self.b.undraw()
            self.boxed = False
