import copy

class Action:
    def __init__(self):
        self.action_completed = False

    def applyAction(self, board):
        """
        Do stuff then set action_completed to True
        """
        pass

class Movement(Action):
    def __init__(self, d):
        super()
        self.direction = d

    def applyAction(self, board):
        if self.direction == "hard_drop":
            board.doHardDrop()
        else:
            board.traverse(self.direction)
        self.action_completed = True

class Block:
    def __init__(self, rot):
        self.rotation_index = 0
        self.rotations = rot

    def rotate(self):
        """
        Rotate the block counterclockwise
        """
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def getBlock(self):
        return self.rotations[self.rotation_index]

class Board:
    BOARD_X_WIDTH = 10
    BOARD_Y_HEIGHT = 20

    X_SPAWN = 0
    Y_SPAWN = 0

    NULL_BLOCK = 0

    def __init__(self):
        # Create all blocks
        self.initialiseBlocks()

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

    def initialiseBlocks(self):
        self.blocks = {}

        # Create L-block

        shape_L_1 = [[0, 0, 0, 0],
                     [1, 0, 0, 0],
                     [1, 0, 0, 0],
                     [1, 1, 0, 0]]

        shape_L_2 = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 1, 0],
                     [1, 1, 1, 0]]

        shape_L_3 = [[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 0]]

        shape_L_4 = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [1, 1, 1, 0],
                     [1, 0, 0, 0]]

        shapes = [shape_L_1, shape_L_2, shape_L_3, shape_L_4]

        self.blocks['L-block'] = Block(shapes)

        # Create Reverse L-block

        shape_RevL_1 = [[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [1, 1, 0, 0]]

        shape_RevL_2 = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [1, 1, 1, 0],
                        [0, 0, 1, 0]]

        shape_RevL_3 = [[0, 0, 0, 0],
                        [0, 1, 1, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0]]

        shape_RevL_4 = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 1, 0],
                        [1, 1, 1, 0]]

        shapes = [shape_RevL_1, shape_RevL_2, shape_RevL_3, shape_RevL_4]

        self.blocks['RevL-block'] = Block(shapes)

        # Create I-block

        shape_Long_1 = [[1, 0, 0, 0],
                        [1, 0, 0, 0],
                        [1, 0, 0, 0],
                        [1, 0, 0, 0]]

        shape_Long_2 = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0]]

        shapes = [shape_Long_1, shape_Long_2]

        self.blocks['I-block'] = Block(shapes)

        # Create Z-block

        shape_Z_1 = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 1, 0]]

        shape_Z_2 = [[0, 0, 0, 0],
                     [0, 1, 0, 0],
                     [1, 1, 0, 0],
                     [1, 0, 0, 0]]

        shapes = [shape_Z_1, shape_Z_2]

        self.blocks['Z-block'] = Block(shapes)

        # Create Reverse Z-block

        shape_RevZ_1 = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 1, 1, 0],
                        [1, 1, 0, 0]]

        shape_RevZ_2 = [[0, 0, 0, 0],
                        [1, 0, 0, 0],
                        [1, 1, 0, 0],
                        [0, 1, 0, 0]]

        shapes = [shape_RevZ_1, shape_RevZ_2]

        self.blocks['RevZ-block'] = Block(shapes)

        # Create T-block

        shape_T_1 = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [1, 1, 1, 0],
                     [0, 1, 0, 0]]

        shape_T_2 = [[0, 0, 0, 0],
                     [1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [1, 0, 0, 0]]

        shape_T_3 = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 1, 0, 0],
                     [1, 1, 1, 0]]

        shape_T_4 = [[0, 0, 0, 0],
                     [0, 1, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0]]

        shapes = [shape_T_1, shape_T_2, shape_T_3, shape_T_4]

        self.blocks['T-block'] = Block(shapes)

        # Create Square block

        shape_Square = [[0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [1, 1, 0, 0],
                        [1, 1, 0, 0]]

        shapes = [shape_Square]

        self.blocks['S-block'] = Block(shapes)

    def applyAction(self, action):
        action.applyAction(self)

    def getAvailableBlocks(self):
        """
        Returns an array strings with names of available blocks.
        """
        return list(self.blocks.keys())

    def setActiveBlockFromString(self, shape_n):
        """
        Take a string parameter and retrieve the shape from the dictionary containing all the shapes.
        """
        self.active_block = self.blocks[shape_n]

    def setActiveBlock(self, shape):
        """
        Takes the parameter shape of class "Shape" and sets the active block to it.
        """
        self.active_block = shape

    def mergeActiveWithBoard(self):
        """
        Merges the active block with the board. Returns the resulting board.
        """
        return self.addShape(self.active_block_position, self.active_block.getBlock())

    def doHardDrop(self):
        while self.collisionCheck("down") == False:
            self.traverse("down")

    def traverse(self, direction):
        """
        Will traverse the active block iff the direction won't collide. The
        possible directions are: 'left', 'down' and 'right'.
        """
        if not self.collisionCheck(direction):
            self.active_block_position = self.getNewXYCoordinateWithDirection(direction)

    def getNewXYCoordinateWithDirection(self, direction):
        """
        Takes a direction of type string with the possible values 'left',
        'down' and 'right. Returns a tuple with the new x and y coordinate.
        """
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

        return x_new, y_new

    def collisionCheck(self, direction):
        """
        Does a collision check for a given direction with the possible
        values 'left', 'down' and right. Returns True if there is a
        collision otherwise False.
        """
        x_new, y_new = self.getNewXYCoordinateWithDirection(direction)

        if x_new < 0:
            return True
        elif y_new+4 > self.BOARD_Y_HEIGHT:
            return True

        shape = self.active_block.getBlock()
        for xprime in range(4):
            for yprime in range(4):
                if self.board[y_new+yprime][x_new+xprime] > 0:
                    if shape[yprime][xprime] > 0:
                        return True

        return False

    def update(self):
        """
        This method's purpose is to determine whether the active block
        should merge to the static one. Runs for each 'tick'.
        """
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
            self.active_block_position = self.getNewXYCoordinateWithDirection('down')
        print()

    def addShape(self, position, shape):
        """
        Adds a shape onto the board with a given position (which is a tuple of x, y).
        """
        x, y = position

        # Assume the shape size is 4x4
        temp = copy.deepcopy(self.board)

        for xprime in range(4):
            for yprime in range(4):
                temp[y+yprime][x+xprime] = temp[y+yprime][x+xprime] + shape[yprime][xprime]
        return temp

    def printBoard(self, board):
        """
        Prints the board to the terminal.
        """
        for y_row in board:
            temp = ""
            for item in y_row:
                temp += str(item)
            print(temp)
