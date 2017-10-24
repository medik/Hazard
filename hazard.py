import copy
VERSION = "0.1"

class Board:
    BOARD_X_WIDTH = 10
    BOARD_Y_HEIGHT = 20

    X_SPAWN = 0
    Y_SPAWN = 0
    
    NULL_BLOCK = 0
    SHAPES = { 'L-block': [ [0, 0, 0, 0],
                            [1, 0, 0, 0],
                            [1, 0, 0, 0],
                            [1, 1, 0, 0]]}
    
    def __init__(self):
        # Build tetris board with origo at top left corner
        # Assume that x and y are the horizontal and vertical respectively
        # Assume that x=10 and y=20
        # Let self.board[y][x] contain the block
        
        self.board = []
        self.active_block = None
        self.active_block_position = (self.X_SPAWN, self.Y_SPAWN)
        
        for y_i in range(self.BOARD_Y_HEIGHT):
            x_arr = []
            for x_i in range(self.BOARD_X_WIDTH):
                x_arr.append(self.NULL_BLOCK)
            self.board.append(x_arr[:])

    def setActiveBlock(self, shape):
        self.active_block = shape

    def mergeActiveWithBoard(self):
        return self.addShape(self.active_block_position, self.active_block)

    def collisionCheck(self, direction):
        x_old, y_old = self.active_block_position

        x_new = 0
        y_new = 0
        
        if direction == 'down':
            x_new = x_old
            y_new = y_old+1
        elif direction == 'left':
            x_new = x_old - 1
            y_new = y_old
        elif direction == 'right':
            x_new = x_old + 1
            y_new = y_old

        if x_new < 0:
            return True
        elif y_new+4 > self.BOARD_Y_HEIGHT:
            return True
        
        shape = self.active_block
        for xprime in range(4):
            for yprime in range(4):
                if self.board[y_new+yprime][x_new+xprime] > 0:
                    if shape[yprime][xprime] > 0:
                        return True
        
        return False

    def update(self):
        self.setActiveBlock(self.SHAPES['L-block'])
        b = self.mergeActiveWithBoard()
        self.printBoard(b)


        x_old, y_old = self.active_block_position

        if self.collisionCheck('down'):
            # Merge this board permanent
            self.board = b
            
            # Reset position
            self.active_block_position = (self.X_SPAWN, self.Y_SPAWN)
        else:
            # increment active block position
            self.active_block_position = (x_old, y_old+1)
        print()

    def addShape(self, position, shape):
        x, y = position
        
        # Assume the shape size is 4x4
        temp = copy.deepcopy(self.board)

        for xprime in range(4):
            for yprime in range(4):
                temp[y+yprime][x+xprime] = shape[yprime][xprime]
        return temp

    def printBoard(self, board):
        for y_row in board:
            temp = ""
            for item in y_row:
                temp += str(item)
            print(temp)
        

def main():
    print("Starting Hazard Game Server " + VERSION +
          ", built by Olof Sjödin and/or members of Qnarch")

    b = Board()
    for i in range(41):
        b.update()
    


if __name__ == "__main__":
    main()
