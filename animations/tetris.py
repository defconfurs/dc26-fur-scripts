## Tetris
import dcfurs
# import pyb
# import settings
import badge
import random

class tetris:
    def __init__(self):
        self.interval = 20
        self.leftThreshold = -20
        self.rightThreshold = 20
        self.zThreshold = -50
        self.holdingZ = False
        self.holdingLeft = False
        self.holdingRight = False
        self.colMax = 18 # Rotated 90˚ to left
        self.rowMax = 7  # Rotated 90˚ to left
        self.currentPiece = random.randint(0,6)
        self.currentRotation = 0
        self.currentX = 15
        self.currentY = 2
        self.speed = 20
        self.counter = 0
        self.forceDown = False
        # print("Setup")
        self.tetromino = [
            [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
            [0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0],
            [0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,1,0,0,0,1,1,0,0,0,0,0],
            [0,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0]
        ]
        # Create playing field
        self.board = [0] * (self.rowMax+1) * (self.colMax+1)
        for y in range(0, self.rowMax):
            for x in range(0, self.colMax):
                thisInd = (x*self.rowMax) + y
                print("thisInd: " + str(thisInd) + " | x: " + str(x) + "  | y: " + str(y))
                # if y == 0 or y == (self.rowMax - 1) or x == 0:
                #     self.board[thisInd] = 1
                # else:
                #     self.board[(x*self.rowMax + y)] = 0
    def draw(self):
        # print("Draw")
        (self.tx, self.ty, self.tz) = badge.imu.filtered_xyz()
        # print(str(self.tx) + ":" + str(self.ty) + ":" + str(self.tz))
        self.counter += 1
        # if (badge.imu.read(0x3) & 0x80) != 0: # Shake event
        #     print("I'm all shook up")
        if self.tx < self.leftThreshold and not self.holdingLeft:
            self.holdingLeft = True
            fits = self.doesPieceFit(self.currentPiece, self.currentX, self.currentY - 1, self.currentRotation)
            if fits:
                self.currentY -= 1
            print("left[" + str(fits) + "]: " + str(self.currentY))
        else:
            self.holdingLeft = False
        if self.tx > self.rightThreshold and not self.holdingRight:
            self.holdingRight = True
            fits = self.doesPieceFit(self.currentPiece, self.currentX, self.currentY + 1, self.currentRotation)
            if fits:
                self.currentY += 1
            print("right[" + str(fits) + "]: " + str(self.currentY))
        else:
            self.holdingRight = False
        if self.tz < self.zThreshold:
            if not self.holdingZ:
                self.holdingZ = True
                print("back: Rotate")
                self.currentRotation += 1
                if self.currentRotation > 3:
                    self.currentRotation = 0
        else:
            self.holdingZ = False
        if self.counter == self.speed:
            dcfurs.clear()
            self.counter = 0
            self.forceDown = True
        if self.forceDown:
            self.forceDown = False
            if self.doesPieceFit(self.currentPiece, self.currentX - 1, self.currentY, self.currentRotation):
                self.currentX -= 1
            else:
                print("Doesn't fit. lock in place or game over.")
                for y in range(0, 4):
                    for x in range(0, 4):
                        if self.tetromino[self.currentPiece][self.rotate(x, y, self.currentRotation)] == 1:
                            thisInd = (self.currentX + x) * self.rowMax + (self.currentY + y)
                            if thisInd <= len(self.board):
                                self.board[thisInd] = 1
                self.currentX = 15
                self.currentY = 2
                self.currentRotation = 0
                self.currentPiece = random.randint(0,6)
        # Draw things
        dcfurs.clear()

        for y in range(0, self.rowMax):
            for x in range(0, self.colMax):
                thisInd = (x*self.rowMax) + y
                if self.board[thisInd] == 1:
                # if y == 0 or y == (self.rowMax - 1) or x == 0:
                    dcfurs.set_pixel(x, y, 254)

        self.drawPiece(self.currentPiece, self.currentX, self.currentY, self.currentRotation)

            # Rotate all pieces
            # self.currentRotation += 1
            # if self.currentRotation > 3:
            #     self.currentRotation = 0
            #     self.currentPiece += 1
            #     if self.currentPiece > 6:
            #         self.currentPiece = 0
            # self.drawPiece(self.currentPiece, 11, 2, self.currentRotation)
        # if forceDown:

    def doesPieceFit(self, piece, x, y, r):
        for tx in range(0, 4):
            for ty in range(0, 4):
                ind = self.rotate(tx, ty, r)
                # ind = self.rotate(tx, ty, r)
                # fInd = (ty + y) * self.rowMax + (tx + x)
                fInd = (tx + x) * self.rowMax + (ty + y)
                # print("Index: " + str(ind))
                if ty + y >= -1 and ty + y < self.rowMax + 1:
                    if tx + x >= -1 and tx + x < self.colMax + 1:
                        # If the tetromino is within the playing field return false if any of it overlaps with an existing led
                        if ind > len(self.tetromino[piece]):
                            print("OUT OF BOUNDS!!!!")
                            print(str(ind) + " > " + str(len(self.tetromino[piece])))
                            return False
                        if fInd > len(self.board):
                            print("OUT OF BOUNDS!!!!")
                            print(str(fInd) + " > " + str(len(self.board)))
                            return False

                        if self.tetromino[piece][ind - 1] == 1 and self.board[fInd - 1] == 1:
                            print("Piece[" + str(piece) + "][" + str(ind) + "]: " + str(self.tetromino[piece][ind]) + " == 1 and board[" + str(fInd) + "]: " + str(self.board[fInd]) + " == 1")
                            return False
                    else:
                        # print("Piece[" + str(piece) + "][" + str(ind) + "]: " + str(self.tetromino[piece][ind]) + " == 1 and board[" + str(fInd) + "]: " + str(self.board[fInd]) + " == 1")
                        return False
                else:
                    # print("Piece[" + str(piece) + "][" + str(ind) + "]: " + str(self.tetromino[piece][ind]) + " == 1 and board[" + str(fInd) + "]: " + str(self.board[fInd]) + " == 1")
                    return False
        return True

    def rotate(self, x, y, r):
        ind = 0
        if r == 0:
            ind = y * 4 + x
        if r == 1:
            ind = 12 + y - (x * 4)
        if r == 2:
            ind = 15 - (y * 4) - x
        if r == 3:
            ind = 3 - y + (x * 4)
        return ind

    def drawPiece(self, piece, x, y, r):
        on = 100
        for tx in range(0, 4):
            for ty in range(0, 4):
                # print("x: " + str(tx) + "  | y: " + str(ty))
                if self.tetromino[piece][self.rotate(tx, ty, r)] == 1:
                    thisX = int(tx + x)
                    thisY = int(ty + y)
                    dcfurs.set_pixel(thisX, thisY, on)

