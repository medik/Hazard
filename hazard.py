import copy
VERSION = "0.1"

class Board:
    BOARD_X_WIDTH = 10
    BOARD_Y_WIDTH = 20
    NULL_BLOCK = 0
    SHAPES = { 'L-block': [ [1, 0, 0, 0],
                            [1, 0, 0, 0],
                            [1, 1, 0, 0],
                            [0, 0, 0, 0]]}
    
    def __init__(self):
        # Build tetris board with origo at top left corner
        # Assume that x and y are the horizontal and vertical respectively
        # Assume that x=10 and y=20
        # Let self.board[x][y] contain the block
        
        self.board = []
        self.active_block = None
        self.active_block_position = (0,0)
        
        for x in range(self.BOARD_X_WIDTH):
            self.board.append([])
            for y in range(self.BOARD_Y_WIDTH):
                self.board[x].append(self.NULL_BLOCK)

    def setActiveBlock(self, shape):
        self.active_block = shape

    def mergeActiveWithBoard(self):
        return self.addShape(self.active_block_position, self.active_block)

    def update(self):
        self.setActiveBlock(self.SHAPES['L-block'])
        b = self.mergeActiveWithBoard()
        self.printBoard(b)
        # increment active block position
        x_old, y_old = self.active_block_position
        self.active_block_position = (x_old+1, y_old)
        print()

    def addShape(self, position, shape):
        x, y = position
        
        # Assume the shape size is 4x4
        temp = copy.deepcopy(self.board)
        
        for xprime in range(4):
            for yprime in range(4):
                temp[x+xprime][y+yprime] = shape[xprime][yprime]
        return temp

    def printBoard(self, board):
        for x_row in board:
            temp = ""
            for y_col in x_row:
                temp += str(y_col)
            print(temp)
        

def main():
    print("Starting Hazard Game Server " + VERSION +
          ", built by Olof Sjödin and/or members of Qnarch")

    b = Board()
    for i in range(3):
        b.update()

if __name__ == "__main__":
    main()
