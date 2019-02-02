"use strict";

/**
 * @file Here is the definitions of all the possible shapes and a definition of the shape prototype. The rotation is counter-clockwise.
 * @author Alexander Hjelm <alexander-hjelm@tutanota.com>
 */

//Shape definitions
const possibleShapes = {};
const iShape = [];
const tShape = [];
const lShape = [];
const lprimeShape = [];
const zShape = [];
const zprimeShape = [];
const sqaureShape = [];


//An 'I' shape, and all rotations
const iRot1 = [];
iRot1[0] = [0, 0, 0, 0];
iRot1[1] = [1, 1, 1, 1];
iRot1[2] = [0, 0, 0, 0];
iRot1[3] = [0, 0, 0, 0];

const iRot2 = [];
iRot2[0] = [0, 1, 0, 0];
iRot2[1] = [0, 1, 0, 0];
iRot2[2] = [0, 1, 0, 0];
iRot2[3] = [0, 1, 0, 0];

//A 'T' shape, and all rotations
const tRot1 = [];
tRot1[0] = [0, 1, 0];
tRot1[1] = [1, 1, 1];
tRot1[2] = [0, 0, 0];

const tRot2 = [];
tRot2[0] = [0, 1, 0];
tRot2[1] = [0, 1, 1];
tRot2[2] = [0, 1, 0];

const tRot3 = [];
tRot3[0] = [0, 0, 0];
tRot3[1] = [1, 1, 1];
tRot3[2] = [0, 1, 0];

const tRot4 = [];
tRot4[0] = [0, 1, 0];
tRot4[1] = [1, 1, 0];
tRot4[2] = [0, 1, 0];

//An 'L' shape, and all rotations
const lRot1 = [];
lRot1[0] = [0, 0, 1];
lRot1[1] = [1, 1, 1];
lRot1[2] = [0, 0, 0];

const lRot2 = [];
lRot2[0] = [0, 1, 0];
lRot2[1] = [0, 1, 0];
lRot2[2] = [0, 1, 1];

const lRot3 = [];
lRot3[0] = [0, 0, 0];
lRot3[1] = [1, 1, 1];
lRot3[2] = [1, 0, 0];

const lRot4 = [];
lRot4[0] = [1, 1, 0];
lRot4[1] = [0, 1, 0];
lRot4[2] = [0, 1, 0];

//A mirrored 'L' shape, and all rotations
const lprimeRot1 = [];
lprimeRot1[0] = [1, 0, 0];
lprimeRot1[1] = [1, 1, 1];
lprimeRot1[2] = [0, 0, 0];

const lprimeRot2 = [];
lprimeRot2[0] = [0, 1, 1];
lprimeRot2[1] = [0, 1, 0];
lprimeRot2[2] = [0, 1, 0];

const lprimeRot3 = [];
lprimeRot3[0] = [0, 0, 0];
lprimeRot3[1] = [1, 1, 1];
lprimeRot3[2] = [0, 0, 1];

const lprimeRot4 = [];
lprimeRot4[0] = [0, 0, 1];
lprimeRot4[1] = [0, 0, 1];
lprimeRot4[2] = [0, 1, 1];

//A 'Z' shape, and all rotations
const zRot1 = [];
zRot1[0] = [0, 0, 0];
zRot1[1] = [1, 1, 0];
zRot1[2] = [0, 1, 1];

const zRot2 = [];
zRot2[0] = [0, 0, 1];
zRot2[1] = [0, 1, 1];
zRot2[2] = [0, 1, 0];

//A mirrored 'Z' shape, and all rotations
const zprimeRot1 = [];
zprimeRot1[0] = [0, 0, 0];
zprimeRot1[1] = [0, 1, 1];
zprimeRot1[2] = [1, 1, 0];

const zprimeRot2 = [];
zprimeRot2[0] = [1, 0, 0];
zprimeRot2[1] = [1, 1, 0];
zprimeRot2[2] = [0, 1, 0];

//A square shape, and all rotations
const squareRot1 = [];
squareRot1[0] = [0, 1, 1];
squareRot1[1] = [0, 1, 1];
squareRot1[2] = [0, 0, 0];

possibleShapes["I-shape"] = iShape;
possibleShapes["T-shape"] = tShape;
possibleShapes["L-shape"] = lShape;
possibleShapes["RevL-shape"] = lprimeShape;
possibleShapes["Z-shape"] = zShape;
possibleShapes["RevZ-shape"] = zprimeShape;
possibleShapes["S-shape"] = sqaureShape;

iShape[0] = iRot1;
iShape[1] = iRot2;

tShape[0] = tRot1;
tShape[1] = tRot2;
tShape[2] = tRot3;
tShape[3] = tRot4;

lShape[0] = lRot1;
lShape[1] = lRot2;
lShape[2] = lRot3;
lShape[3] = lRot4;

lprimeShape[0] = lprimeRot1;
lprimeShape[1] = lprimeRot2;
lprimeShape[2] = lprimeRot3;
lprimeShape[3] = lprimeRot4;

zShape[0] = zRot1;
zShape[1] = zRot2;

zprimeShape[0] = zprimeRot1;
zprimeShape[1] = zprimeRot2;

sqaureShape[0] = squareRot1;

/*
* Create a shape.
* @param {Kiwi.State} state - The game state variable.
* @param {String} shapeStr - A key representing the shape to be created. Accepted values:
*    "I-shape", "T-shape", "L-shape", "RevL-shape", "Z-shape", "RevZ-shape", "S-shape".
*/
function Shape (state, shapeStr) {
    this.state = state;
    this.shape = possibleShapes[shapeStr];
    this.currentRot = 0;
    this.table = this.shape[0];
}

/**
* Rotate this shape by 90 degrees counter-clockwise.
*/
Shape.prototype.rotate = function () {
    var nextIndex = this.getNextRotIndex();
    this.table = this.shape[nextIndex];
    this.currentRot = nextIndex;
};

/**
* Return the index of the next rotation matrix permutation of this shape.
* @return {int} Index of the next rotation matrix.
*/
Shape.prototype.getNextRotIndex = function () {
    return ( this.currentRot + 1 ) % this.shape.length; //x = (x+1) % {number of rotations}
};
