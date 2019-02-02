"""""
tetrislib.py v 0.3

Documentation is found at https://knark.io/tetrisslinger-docs/

Olof Sjödin <me@olofsjodin.se> Copyright (C) 2017-2018

"""""

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
    def __init__(self, d, rep=1):
        super()
        self.direction = d
        self.repeat = rep

    def applyAction(self, board):
        for i in range(self.repeat):
            if self.direction == "hard_drop":
                board.doHardDrop()
            elif self.direction == "rotate":
                board.rotateActive()
            else:
                board.traverse(self.direction)
        self.action_completed = True

class SetShape(Action):
    def __init__(self, s):
        super()
        self.shape = s

    def applyAction(self, board):
        board.setActiveShapeFromString(self.shape)
        self.action_completed = True

class Shape:
    def __init__(self, rot):
        self.rotation_index = 0
        self.rotations = rot

    def rotate(self):
        """
        Rotate the shape counterclockwise
        """
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def getNextRotation(self):
        ret = copy.deepcopy(self)
        ret.rotate()
        return ret
    
    def getNextSize(self):
        temp = self.rotations[(self.rotation_index + 1) % len(self.rotations)]
        y_ret = len(temp)
        x_ret = len(temp[0])

        return x_ret, y_ret

    def getSize(self):
        # Assume that we are measuring the current rotation
        temp = self.rotations[self.rotation_index]
        y_ret = len(temp)
        x_ret = len(temp[0])

        return x_ret, y_ret

    def getShape(self):
        return self.rotations[self.rotation_index]

class Board:
    BOARD_X_WIDTH = 10
    BOARD_Y_HEIGHT = 20

    X_SPAWN = 4
    Y_SPAWN = 0

    NULL_BLOCK = 0

    def __init__(self):
        # Create all shapes
        self.initialiseShapes()

        # Build tetris board with origo at top left corner
        # Assume that x and y are the horizontal and vertical respectively
        # Assume that x=10 and y=20
        # Let self.board[y][x] contain the block

        self.board = []
        self.active_shape = None
        self.active_shape_str = ""
        self.active_shape_position = (self.X_SPAWN, self.Y_SPAWN)

        for y_i in range(self.BOARD_Y_HEIGHT):
            x_arr = []
            for x_i in range(self.BOARD_X_WIDTH):
                x_arr.append(self.NULL_BLOCK)
            self.board.append(x_arr[:])

    # Initialisation functions
    def initialiseShapes(self):
        self.shapes = {}

        # Create L-shape

        shape_L_1 = [[1, 0],
                     [1, 0],
                     [1, 1]]

        shape_L_2 = [[0, 0, 1],
                     [1, 1, 1]]

        shape_L_3 = [[1, 1],
                     [0, 1],
                     [0, 1]]

        shape_L_4 = [[1, 1, 1],
                     [1, 0, 0]]

        shapes = [shape_L_1, shape_L_2, shape_L_3, shape_L_4]

        self.shapes['L-shape'] = Shape(shapes)

        # Create Reverse L-shape

        shape_RevL_1 = [[0, 1],
                        [0, 1],
                        [1, 1]]

        shape_RevL_2 = [[1, 1, 1],
                        [0, 0, 1]]

        shape_RevL_3 = [[1, 1],
                        [1, 0],
                        [1, 0]]

        shape_RevL_4 = [[1, 0, 0],
                        [1, 1, 1]]

        shapes = [shape_RevL_1, shape_RevL_2, shape_RevL_3, shape_RevL_4]

        self.shapes['RevL-shape'] = Shape(shapes)

        # Create I-shape

        shape_Long_1 = [[1],
                        [1],
                        [1],
                        [1]]

        shape_Long_2 = [[1, 1, 1, 1]]

        shapes = [shape_Long_1, shape_Long_2]

        self.shapes['I-shape'] = Shape(shapes)

        # Create Z-shape

        shape_Z_1 = [[1, 1, 0],
                     [0, 1, 1]]

        shape_Z_2 = [[0, 1],
                     [1, 1],
                     [1, 0]]

        shapes = [shape_Z_1, shape_Z_2]

        self.shapes['Z-shape'] = Shape(shapes)

        # Create Reverse Z-shape

        shape_RevZ_1 = [[0, 1, 1],
                        [1, 1, 0]]

        shape_RevZ_2 = [[1, 0],
                        [1, 1],
                        [0, 1]]

        shapes = [shape_RevZ_1, shape_RevZ_2]

        self.shapes['RevZ-shape'] = Shape(shapes)

        # Create T-shape

        shape_T_1 = [[1, 1, 1],
                     [0, 1, 0]]

        shape_T_2 = [[1, 0],
                     [1, 1],
                     [1, 0]]

        shape_T_3 = [[0, 1, 0],
                     [1, 1, 1]]

        shape_T_4 = [[0, 1],
                     [1, 1],
                     [0, 1]]

        shapes = [shape_T_1, shape_T_2, shape_T_3, shape_T_4]

        self.shapes['T-shape'] = Shape(shapes)

        # Create Square shape

        shape_Square = [[1, 1],
                        [1, 1]]

        shapes = [shape_Square]

        self.shapes['S-shape'] = Shape(shapes)

    # Get methods
    def getBoard(self):
        ret = copy.deepcopy(self.board)
        return ret
    
    def getAvailableShapes(self):
        """
        Returns an array strings with names of available shapes.
        """
        return list(self.shapes.keys())

    def getNewXYCoordinateWithDirection(self, direction):
        """
        Takes a direction of type string with the possible values 'left',
        'down' and 'right. Returns a tuple with the new x and y coordinate.
        """
        x_old, y_old = self.active_shape_position

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

    def getNumberOfNonZeroesForEachRow(self):
        ret = []

        for y_i in range(self.BOARD_Y_HEIGHT):
            non_zeroes_count = 0
            for x_i in range(self.BOARD_X_WIDTH):
                if self.board[y_i][x_i] > 0:
                    non_zeroes_count += 1
            ret.append(non_zeroes_count)

        return ret

    # Set methods
    def setActiveShapeFromString(self, shape_n):
        """
        Take a string parameter and retrieve the shape from the dictionary containing all the shapes.
        """
        temp = copy.deepcopy(self.shapes[shape_n])
        self.active_shape = temp

    def setActiveShape(self, shape):
        """
        Takes the parameter shape of class "Shape" and sets the active block to it. Do not use this.
        """
        
        temp = copy.deepcopy(self.blocks[shape_n])
        self.active_shape_str = shape_n
        self.active_shape = shape

    def rotateActive(self):
        x_o, y_o = self.active_shape_position
        x_shape_size, y_shape_size = self.active_shape.getSize()

        x_right_marginal = self.BOARD_X_WIDTH - x_o
        y_bottom_marginal = self.BOARD_Y_HEIGHT - y_o

        x_new = x_o
        y_new = y_o

        # If the marginal isn't enough, correct the postion with the difference
        if x_right_marginal < y_shape_size:
            x_new = x_o - (y_shape_size-x_right_marginal)

        if y_bottom_marginal < x_shape_size:
            y_new = y_o - (x_shape_size-y_bottom_marginal)

        # Do not allow rotation if the next rotation will collide with a sticky block
        nextRotShape = self.active_shape.getNextRotation()
        pos = (x_new, y_new)

        if not self.collisionCheckWithShapeAndPos(pos, nextRotShape):
            self.active_shape_position = (x_new, y_new)
            self.active_shape.rotate()

    def traverse(self, direction):
        """
        Will traverse the active shape iff the direction won't collide. The
        possible directions are: 'left', 'down' and 'right'.
        """
        if direction == "hard_drop":
            self.doHardDrop()
            return
        elif direction == "rotate":
            self.rotateActive()
            return
        
        if not self.collisionCheck(direction):
            self.active_shape_position = self.getNewXYCoordinateWithDirection(direction)

    # Helper methods
    def addShape(self, position, shape):
        """
        Adds a shape onto the board with a given position (which is a tuple of x, y).
        """
        x, y = position
        active_x_size, active_y_size = self.active_shape.getSize()

        # Assume the shape size is 4x4
        temp = copy.deepcopy(self.board)

        for xprime in range(active_x_size):
            for yprime in range(active_y_size):
                temp[y+yprime][x+xprime] = temp[y+yprime][x+xprime] + shape[yprime][xprime]
        return temp

    def applyAction(self, action):
        """
        Takes the parameter action and call the applyAction method with reference to this instance.
        """
        action.applyAction(self)

    def collisionCheck(self, direction):
        """
        Does a collision check for a given direction with the possible
        values 'left', 'down' and right. Returns True if there is a
        collision otherwise False.
        """
        x_new, y_new = self.getNewXYCoordinateWithDirection(direction)
        active_x_size, active_y_size = self.active_shape.getSize()

        if x_new < 0:
            return True
        elif x_new + active_x_size > self.BOARD_X_WIDTH:
            return True
        elif y_new + active_y_size > self.BOARD_Y_HEIGHT:
            return True

        shape = self.active_shape.getShape()
        for xprime in range(active_x_size):
            for yprime in range(active_y_size):
                if self.board[y_new+yprime][x_new+xprime] > 0:
                    if shape[yprime][xprime] > 0:
                        return True

        return False

    def collisionCheckWithShapeAndPos(self, position, shape):
        """ Apply a given shape onto the board with a given coordinate, then,
        check whether there is a collision or not. """

        # Let position be a tuple
        x, y = position
        shape_x_width, shape_y_width = shape.getSize()

        shapeArr = shape.getShape()
        for xprime in range(shape_x_width):
            for yprime in range(shape_y_width):
                if self.board[y+yprime][x+xprime] > 0 and shapeArr[yprime][xprime] > 0:
                    return True
        return False

    def doHardDrop(self):
        """
        Makes the active shape go directly to the bottom of the board.
        """
        while self.collisionCheck("down") == False:
            self.traverse("down")
        self.update()

    def fillNullRowsFromTop(self, board, n):
        """
        Adding null blocks from the top of the board.
        """
        temp = []
        for y_i in range(n):
            x_arr = []
            for x_i in range(self.BOARD_X_WIDTH):
                x_arr.append(self.NULL_BLOCK)
            temp.append(x_arr[:])

        temp.extend(board)

        self.board = temp

    def mergeActiveWithBoard(self):
        """
        Merges the active shape with the board. Returns the resulting board.
        """
        return self.addShape(self.active_shape_position, self.active_shape.getShape())

    def printBoard(self, board):
        """
        Prints the board to the terminal.
        """
        for y_row in board:
            temp = ""
            for item in y_row:
                temp += str(item)
            print(temp)

    def removeRows(self, int_arr):
        """
        Takes an array of integers and remove it from the board.
        """
        temp = []
        for yprime in range(self.BOARD_Y_HEIGHT):
            if not yprime in int_arr:
                temp.append(self.board[yprime])

        self.fillNullRowsFromTop(temp, len(int_arr))

    def update(self):
        """
        This method's purpose is to determine whether the active shape
        should merge to the static one. Runs for each 'tick'.
        """
        b = self.mergeActiveWithBoard()


        x_old, y_old = self.active_shape_position

        if self.collisionCheck('down'):
            # Merge this board permanent
            self.board = b

            # Check for tetris and remove them
            non_zeroes = self.getNumberOfNonZeroesForEachRow()
            non_zeroes_y = [ i for i in range(self.BOARD_Y_HEIGHT) if non_zeroes[i] >= self.BOARD_X_WIDTH ]
            if len(non_zeroes_y) > 0:
                self.removeRows(non_zeroes_y)

            # Reset position
            self.active_shape_position = (self.X_SPAWN, self.Y_SPAWN)
        else:
            # increment active shape position
            self.active_shape_position = self.getNewXYCoordinateWithDirection('down')

        # debug
        #self.printBoard(b)
        #print()
