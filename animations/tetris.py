## Tetris
import dcfurs
# import pyb
# import settings
import badge
import random

class tetris:
    def __init__(self):
        self.interval = 20
        self.leftThreshold = -15
        self.rightThreshold = 15
        self.zThreshold = -80
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
        self.gameOver = False
        self.goCounter = 0

        self.displayConsole = False
        self.debugDisplay = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        self.debugDefault = self.debugDisplay
        self.debugDisplayText = ""
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
    def draw(self):
        if self.gameOver == True:
            print ("GAME OVER!!!")
            self.goCounter = self.goCounter + 1
            if self.goCounter >= 100:
                dcfurs.clear()
                self.goCounter = 0
                self.gameOver = False
                self.debugDisplay = self.debugDefault
                self.board = [0] * (self.rowMax+1) * (self.colMax+1)
                # Pick new piece
                self.currentX = 15
                self.currentY = 2
                self.currentRotation = 0
                self.currentPiece = random.randint(0,6)

        else:
            (self.tx, self.ty, self.tz) = badge.imu.filtered_xyz()
            # print(str(self.tx) + ":" + str(self.ty) + ":" + str(self.tz))
            self.counter += 1
            # if (badge.imu.read(0x3) & 0x80) != 0: # Shake event
            #     print("I'm all shook up")
            if self.tx < self.leftThreshold:
                if not self.holdingLeft:
                    self.holdingLeft = True
                    fits = self.doesPieceFit(self.currentPiece, self.currentX, self.currentY - 1, self.currentRotation)
                    if fits:
                        self.currentY -= 1
                    print("left[" + str(fits) + "]: " + str(self.currentY))
            else:
                self.holdingLeft = False
            if self.tx > self.rightThreshold:
                if not self.holdingRight:
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
                    print("Doesn't fit. lock in place.")
                    for y in range(0, 4):
                        for x in range(0, 4):
                            if self.tetromino[self.currentPiece][self.rotate(x, y, self.currentRotation)] == 1:
                                thisInd = (self.currentX + x) * self.rowMax + (self.currentY + y)
                                if thisInd <= len(self.board):
                                    self.board[thisInd] = 1

                    # Detect Lines
                    print("Detect Lines...")
                    for py in range(0, 4):
                        if self.currentY + py < self.colMax - 1:
                            bLine = True
                            for px in range(1, self.rowMax - 1):
                                print("(self.board[(" + str(self.currentY + py) + ") * " + str(self.rowMax) + " + " + str(px) + "] => self.board[" + str((self.currentY + py) * self.rowMax + px) + "] => " + str(self.board[(self.currentY + py) * self.rowMax + px]))
                                if (self.board[(self.currentY + py) * self.rowMax + px]) == 0:
                                    bLine = False
                                    break
                            if bLine == True:
                                print("LINE DETECTED: " + str(self.currentY + py))
                                for px in range(1, self.rowMax - 1):
                                    self.board[(self.currentY + py) * self.rowMax + px] = 0

                    # Pick new piece
                    self.currentX = 15
                    self.currentY = 2
                    self.currentRotation = 0
                    self.currentPiece = random.randint(0,6)

                    # Game over
                    if self.doesPieceFit(self.currentPiece, self.currentX, self.currentY, self.currentRotation):
                        print("continue.")
                    else:
                        self.gameOver = True

            # Draw things
            dcfurs.clear()
            if self.counter == 0 and self.displayConsole == True:
                print("\x1B\x5B2J", end="")
                print("\x1B\x5BH", end="")
                self.debugDisplay = self.debugDefault
            for x in range(0, self.colMax):
                for y in range(0, self.rowMax):
                    thisInd = (x*self.rowMax) + y
                    if self.board[thisInd] == 1:
                        dcfurs.set_pixel(x, y, 254)

            if self.counter == 0 and self.displayConsole == True:
                for x in range(0, self.colMax):
                    for y in range(0, self.rowMax):
                        thisInd = (x*self.rowMax) + y
                        if self.board[thisInd] == 1:
                            self.debugDisplay[x][y] = 1
                        else:
                            self.debugDisplay[x][y] = 0
            self.drawPiece(self.currentPiece, self.currentX, self.currentY, self.currentRotation)

            if self.counter == 0 and self.displayConsole == True:
                self.debugDisplayText = ""
                for x in reversed(range(0, self.colMax)):
                    self.debugDisplayText = self.debugDisplayText + "\n"
                    for y in range(0, self.rowMax):
                        if self.debugDisplay[x][y] == 1:
                            self.debugDisplayText = self.debugDisplayText + " *"
                        else:
                            self.debugDisplayText = self.debugDisplayText + " -"
                print(self.debugDisplayText)


    def doesPieceFit(self, piece, x, y, r):
        # print("piece: " + str(piece) + " | x: " + str(x) + " | y: " + str(y) + " | r: " + str(r))
        for tx in range(0, 4):
            for ty in range(0, 4):
                ind = self.rotate(tx, ty, r)
                # ind = self.rotate(tx, ty, r)
                # fInd = (ty + y) * self.rowMax + (tx + x)
                fInd = (tx + x) * self.rowMax + (ty + y)
                # print("Index: " + str(ind))
                if (ty + y) >= -1 and (ty + y) < (self.rowMax + 1):
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
                        # Piece collision detection
                        if self.tetromino[piece][ind] == 1 and self.board[fInd] == 1:
                            print("OUT OF BOUNDS: Existing Tetromino")
                            return False
                    # Vertical bounds
                    else:
                        print("OUT OF BOUNDS: Vertical")
                        return False
                # Horizontal bounds
                else:
                    print("OUT OF BOUNDS: Horizontal")
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
                    if self.displayConsole == True:
                        if thisX >= 0 and thisX <= self.rowMax:
                            if thisY >= 0 and thisY <= self.colMax:
                                self.debugDisplay[thisX][thisY] = 1
                    dcfurs.set_pixel(thisX, thisY, on)

