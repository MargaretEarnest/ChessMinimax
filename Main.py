import math

from graphics import *
from Board import Board
from ChessPiece import ChessPiece

def pieceHere(p, list):
    return p in list and list[p] is not None

def main():
    win = GraphWin("Board", 400, 400)
    playerTurn = True
    lightColor = True
    x = 0
    y = 0
    for i in range(1, 65):
        s = Rectangle(Point(x, y), Point(x + 50, y + 50))
        s.draw(win)
        if lightColor:
            s.setFill('#ffc266')
        else:
            s.setFill('#996633')
        lightColor = not lightColor
        if i % 8 == 0 and i != 0:
            x = 0
            y += 50
            lightColor = not lightColor
        else:
            x += 50

    names = ["R1", "K1", "B1", "K", "Q", "B2", "Kn2", "R2", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
    whiteList = {}
    blackList = {}
    x = 1
    y = 1
    for n in range(0, 16):
        p = ChessPiece(names[n], "white")
        p.moveTo(win, x * 50 - 25, y * 50 - 25)
        whiteList[(x * 50 - 25, y * 50 - 25)] = p
        p = ChessPiece(names[n], "black")
        p.moveTo(win, x * 50 - 25, (9 - y) * 50 - 25)
        blackList[x * 50 - 25, (9 - y) * 50 - 25] = p
        if (n + 1) % 8 == 0 and n != 0:
            x = 1
            y += 1
        else:
            x += 1
    b = Board(whiteList, blackList, 0)
    previous = None
    # b = whiteList.get((25, 75)).remove(b)
    print(str(b.whiteList.get((175, 25)).findAvailable(b)))
    print(str(b.whiteList.get((175, 25)).name))
    while b.returnWinner() is None:
        if playerTurn:
            mouse = win.getMouse()
            current = (50 * math.floor(float(mouse.x) / 50) + 25, 50 * math.floor(float(mouse.y) / 50) + 25)
            if previous is None and pieceHere(current, b.whiteList):
                b.whiteList.get(current).boxToggle(win)
                previous = current
            elif current is not None and current == previous:
                b.whiteList.get(current).boxToggle(win)
            elif pieceHere(current, b.whiteList) and pieceHere(previous, b.whiteList):
                b.whiteList.get(current).boxToggle(win)
                b.whiteList.get(previous).boxToggle(win)
                previous = current
            elif pieceHere(previous, b.whiteList) and not pieceHere(current, b.whiteList) and b.whiteList.get(previous).validMove(b, current):
                print(str(current[0]) + " " + str(current[1]))
                b.whiteList.get(previous).moveTo(win, current[0], current[1])
                temp = b.whiteList.get(previous)
                b.whiteList[current] = temp
                b.whiteList[previous] = None
                if pieceHere(current, b.blackList) is not None:
                    b.blackList[current] = None
                previous = None
                print(b.whiteList)
                playerTurn = False
            # print(str(b.whiteList.get((175, 25)).findAvailable(b)))
            # print(str(b.whiteList.get((175, 25)).name))
        else:
            print("AI time")
            # whoops can't move into enemy? I'm dumb I think, assess at not 2 am
            # king is broken question mark
            #pawn, queen, bishop, knight, and rook seem fine
            # time.sleep(5)
            # break
            playerTurn = not playerTurn
    win.close()


main()
