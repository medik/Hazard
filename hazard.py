VERSION = "0.1"

class Board:
    BOARD_X_WIDTH = 10
    BOARD_Y_WIDTH = 20
    NULL_BLOCK = 0
    SHAPES = { 'L-shape': [ [1, 0, 0, 0],
                            [1, 0, 0, 0],
                            [1, 1, 0, 0],
                            [0, 0, 0, 0]]}
    
    def __init__(self):
        # Build tetris board with origo at top left corner
        # Assume that x and y are the horizontal and vertical respectively
        # Assume that x=10 and y=20
        # Let self.board[x][y] contain the block
        
        self.board = []
        
        for x in range(self.BOARD_X_WIDTH):
            self.board.append([])
            for y in range(self.BOARD_Y_WIDTH):
                self.board[x].append(self.NULL_BLOCK)

    def addShape(self, x, y, shape):
        # Assume the shape size is 4x4
        
        for xprime in range(4):
            for yprime in range(4):
                self.board[x+xprime][y+yprime] = shape[xprime][yprime]
                
            

    def printBoard(self):
        for x_row in self.board:
            temp = ""
            for y_col in x_row:
                temp += str(y_col)
            print(temp)
        

def main():
    print("Starting Hazard Game Server " + VERSION +
          ", built by Olof Sjödin and/or members of Qnarch")

    b = Board()
    b.addShape(0,0, b.SHAPES['L-shape'])
    b.printBoard()

if __name__ == "__main__":
    main()
