"use strict";

/**
 * @file Here is the definition of the PlayGrid prototype. The PlayGrid is the game for the
 *     tetris game and contains the active shape and all static squares, as well as methods to
 *     manipulate these.
 * @author Alexander Hjelm <alexander-hjelm@tutanota.com>
 */

/*
* Create a PlayGrid with only empty squares.
* @param {Kiwi.State} state - The game state variable.
*/
function PlayGrid (state){
    this.state = state;

    this.sizeX = 10;
    this.sizeY = 20;

    this.activePosX = 3;
    this.activePosY = 0;

    this.grid = [];

    this.gameOver = false;
    this.waitForActiveShape = true;

    this.time = new Date().getTime();

    for (let i=0;i<this.sizeY;i+=1) {
        this.grid[i] = [];
        for (let j=0;j<this.sizeX;j+=1) {
            this.grid[i][j] = 0;
        }
    }

    //this.activeShape = new Shape(this.state, "I-shape");
    //this.fillOutActiveShape(1);
}

/*
* Main update function. This function is called on every frame.
*//*
PlayGrid.prototype.update = function() {
    if(this.activeShape && new Date().getTime() > this.time + 300) {

        for (let i=0;i<this.activeShape.table.length;i+=1) {
            for (let j=0;j<this.activeShape.table[i].length;j+=1) {
                if(this.activeShape.table[i][j] == 1) {
                    let x = this.activePosX + i;
                    let y = this.activePosY + j;
                    if (y >= this.sizeY - 1 || this.grid[x][y+1] == 2) {
                        this.fillOutActiveShape(2); // 2 is reserved for fallen blocks for now

                        //row clear check
                        for (let k=0;k<this.sizeY;k+=1) {
                            for (let l=0;l<this.sizeX;l+=1) {
                                if (this.grid[l][k] != 2) {
                                    break;
                                }

                                if (l == 9) {
                                    console.log("row clear");
                                    for (let m=k;m>0;m--) {
                                        for (let n=0;n<this.sizeX;n+=1) {
                                            this.grid[n][m] = this.grid[n][m-1]
                                        }
                                    }
                                    connection.sendAction("get_queued_powerup", true);
                                }
                            }
                        }

                        //fail check
                        for (let k=0;k<this.grid.length;k+=1) {
                            if (this.grid[k][0] == 2) {
                                console.log("GAME OVER");
                                this.gameOver = true;
                            }
                        }
                        //this.resetActiveShape(Math.floor(Math.random() * (6 - 0 + 1)) + 0);
			//this.resetActiveShape("S-shape");
                        this.waitForActiveShape = true;
                    }
                }
            }
        }

        this.updateActivePos(0, 1);
        this.time = new Date().getTime();
    }
}
*/
/*
* Copy a board to this PlayGrid.
* @param {int[][]} currentBoard - A 2D array where the element are integer representations of
*     individual squares. The elements are required to be any of the following: 0 = Empty square,
*     2 = Filled Square.
*/
PlayGrid.prototype.setBoard = function(currentBoard) {

    for (let i=0;i<this.sizeY;i+=1) {
        this.grid[i] = [];
        for (let j=0;j<this.sizeX;j+=1) {
            this.grid[i][j] = currentBoard[i][j];
        }
    }

    /*
    for (let i=0;i<this.sizeX;i+=1) {
        this.grid[i] = [];
        for (let j=0;j<this.sizeY;j+=1) {
            this.grid[i][j] = currentBoard[i*10 + j];
        }
    }
    */
    //this.fillOutActiveShape(1);
}

/*
* Set the active shape of this PlayGrid and reset it's position to the top center.
* @param {String} shapeStr - A key representing the shape to be created. Accepted values:
*    "I-shape", "T-shape", "L-shape", "RevL-shape", "Z-shape", "RevZ-shape", "S-shape".
*//*
PlayGrid.prototype.resetActiveShape = function(shapeStr) {
    this.activeShape = new Shape(this.state, shapeStr);
    this.activePosX = 3;
    this.activePosY = 0;
    this.waitForActiveShape = false;
}
*/
/*
* Set the (relative) position of active shape. Collision check is done internally,
*     and the position will not be updated if it would have triggered a collision.
* @param {int} deltaX - The x-coordinate of the movement vector.
* @param {int} deltaY - The y-coordinate of the movement vector.
*//*
PlayGrid.prototype.updateActivePos = function(deltaX, deltaY) {
    //Collision check
    if (this.checkCollision(deltaX, deltaY, this.activeShape.table)) { return; }

    this.fillOutActiveShape(0);
    this.activePosX = this.activePosX + deltaX;
    this.activePosY = this.activePosY + deltaY;
    this.fillOutActiveShape(1);
}
*/
/*
* Rotate the active shape by 90 degrees counter-clockwise
*//*
PlayGrid.prototype.rotateActiveShape = function() {

    //Collision check
    let nextTable = this.activeShape.shape[this.activeShape.getNextRotIndex()];
    if (this.checkCollision(0, 0, nextTable)) { return; }

    this.fillOutActiveShape(0);
    this.activeShape.rotate();
    this.fillOutActiveShape(1);
}
*/
/*
* Set the (relative) position of active shape. Collision check is done internally,
*     and the position will not be updated if it would have triggered a collision.
* @param {int} deltaX - The x-coordinate of the movement vector.
* @param {int} deltaY - The y-coordinate of the movement vector.
*//*
PlayGrid.prototype.fillOutActiveShape  = function(int) {
    for (let i=0;i<this.activeShape.table.length;i+=1) {
        for (let j=0;j<this.activeShape.table[i].length;j+=1) {
            if(this.activeShape.table[i][j] == 1) {
                var x = this.activePosX + i;
                var y = this.activePosY + j;
                this.grid[x][y] = int;
            }
        }
    }
}
*/
/*
* Check if the desired transformation of the active shape would imply a collision
*     with the horisontal walls or any static squares.
* @param {int} deltaX - The x-coordinate of the movement vector.
* @param {int} deltaY - The y-coordinate of the movement vector.
* @param {int[][]} nextTable - The next rotation matrix of the active shape. If
*     the active shape is not rotating, simply pass the current rotation matrix
*     of the active shape.
* @return {bool} If true, the desired transformation will trigger a collision.
*//*
PlayGrid.prototype.checkCollision = function(deltaX, deltaY, nextTable) {
    for (let i=0;i<nextTable.length;i+=1) {
        for (let j=0;j<nextTable[i].length;j+=1) {
            if(nextTable[i][j] == 1) {
                let x = this.activePosX + deltaX + i;
                let y = this.activePosY + deltaY + j;

                if (x < 0) { return true; }
                if (x >= this.sizeX) { return true; }
                if (this.grid[x][y] == 2) {return true; }
            }
        }
    }

    return false;
}
*/
/*
* Get the integer value stored in a point on the Board.
* @param {int} i - The x-coordinate.
* @param {int} j - The y-coordinate.
* @return {int} The integer value stored at the position (x=i,y=j) in the Board. Guaranteed to
*     be one of the following: 0 = Empty square, 2 = Filled Square.
*/
PlayGrid.prototype.getBlockValueAt = function(i, j) {
    var output = this.grid[i][j];
    return output;
}
