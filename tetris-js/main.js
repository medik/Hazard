"use strict";

var comVersion = "0.3";

var game = new Kiwi.Game(null, "Hello World", null, { renderer: Kiwi.RENDERER_CANVAS });
var myState = new Kiwi.State("myState");
var name = "";

var playGrid = new PlayGrid(myState);

var connection = new WebSocket("ws://localhost:7441");
connection.onopen = function (event) {
    window.alert("Connected to server!");
    //connection.send("Client connected!");
};

/*
* Send the desired action to the TetrisSlinger server.
* @param {String} typeStr - The action type.
* @param {String} valueStr - The value.
* @see {@link https://knark.io/tetrisslinger-docs/com.html} for further information.
*/
connection.sendAction = function(typeStr, valueStr) {
    var msgDict = { "version":comVersion, "type":typeStr, "value":valueStr };
    var msg = JSON.stringify(msgDict);
    this.send(msg);
};

/*
* Handler for incoming messages from the TetrisSlinger server. Do not call from this application.
* @param {Event} e
*/
connection.onmessage = function(e){
    console.log("[SERVER MESSAGE] " + e.data);
    var server_message = e.data;
    var message = JSON.parse(server_message);

    if (!message.response_type) {
        return;
    }

    switch(message.response_type) {
        case "board":
            playGrid.setBoard(message.value);
            break;
/*
        case "active_shape":
            playGrid.resetActiveShape(message.value);
            break;
*/
        case "queued_powerup":
            myState.queuedPowerup = new Powerup(this.state, message.value);
            break;

        case "status":
            break;
        default:
            console.error("Error: server message type not recognized: " + message.response_type);
    }
};

/*
* A preload function which is used by Kiwi to initialise resources and
* controls used by the library.
*/

myState.preload = function(){
    /*
     * Initialise image resources
     */
    Kiwi.State.prototype.preload.call(this);
    this.addImage("bg","bg.png");
    this.addImage("fg","fg.png");

    for(let i=0; i<powerupNames.length; i+=1)
    {
        this.addImage(powerupNames[i], "icons/powerup" + powerupNames[i] + ".png");
    }

    /*
     * Controls used by the player
     */

    this.leftKey = Kiwi.Input.Keycodes.LEFT;
    this.rightKey = Kiwi.Input.Keycodes.RIGHT;
    this.upKey = Kiwi.Input.Keycodes.UP;
    this.downKey = Kiwi.Input.Keycodes.DOWN;
    this.spaceKey = Kiwi.Input.Keycodes.SPACEBAR;

    // Reserved for powerups
    this.specialKey = Kiwi.Input.Keycodes.A;
/*
    this.special2Key = Kiwi.Input.Keycodes.TWO;
    this.special3Key = Kiwi.Input.Keycodes.THREE;
    this.special4Key = Kiwi.Input.Keycodes.FOUR;
    this.special5Key = Kiwi.Input.Keycodes.FIVE;
*/
    this.testKey = Kiwi.Input.Keycodes.T;

};

/*
 * This function creates the game by creating the playing grid and
 * starts an instance with the server.
 */

myState.create = function(){
    Kiwi.State.prototype.create.call(this);

    // Attach callback to be executed when a key is pressed.
    this.game.input.keyboard.onKeyDown.add(myState.onPress, this);

    // Create the playing grid
    this.blocksArray = [];
    for (let i=0;i<playGrid.sizeY;i+=1) {
        this.blocksArray[i] = [];
        for (let j=0;j<playGrid.sizeX;j+=1) {
            this.blocksArray[i][j] = new Kiwi.GameObjects.StaticImage(this, this.textures["bg"], 10 + j*24, 10 + i*24);
            this.addChild(this.blocksArray[i][j]);
        }
    }

    // Ask the player's name
    while(!name)
    {
        name = prompt("Please enter your name", "Player");
    }
    this.nameText = new Kiwi.GameObjects.TextField(this, name, 270, 10);
    this.addChild(this.nameText);

    // Send the player details to the server and tell it to start a game
    connection.sendAction("set_name", name);
    connection.sendAction("start_game", true);

    // Create a reference to the player's next powerup and add its sprite
    this.queuedPowerup = new Powerup(this.state, "Shotgun");

    // TODO create powerup sprites in myState.preload instead
    this.powerupSprite = new Kiwi.GameObjects.StaticImage(this, this.textures[this.queuedPowerup.name], 100, 500 );
    this.addChild(this.powerupSprite);

};

/*
 * The update function. Updates the game logic as well as rendering
 * the blocks.
 */

myState.update = function(){
    Kiwi.State.prototype.update.call(this);

    // Update game logic
    //playGrid.update();

    // TODO remove this, end_game should be sent by the server
    /*
    if (playGrid.gameOver) {
        connection.sendAction("end_game", true);
    }
    */

/*
    // TODO don't ask for active shape when you are waiting for one!
    if (playGrid.waitForActiveShape) {
        connection.sendAction("get_active_shape", true);
    }
*/

    // Render the blocks
    for (let i=0;i<playGrid.sizeY;i+=1) {
        for (let j=0;j<playGrid.sizeX;j+=1) {
            if (playGrid.grid[i][j] == 0) {
                this.blocksArray[i][j].atlas = this.textures["bg"];
            }
            else if (playGrid.grid[i][j] != 0) {
                this.blocksArray[i][j].atlas = this.textures["fg"];
            }
        }
    }

    this.powerupSprite.atlas = this.textures[this.queuedPowerup.name];

};

/*
 * The function which binds keys to actions.
 */

myState.onPress = function(keyCode) {
    switch (keyCode) {
        case this.leftKey:
            //playGrid.updateActivePos(-1,0);
            connection.sendAction("move_active_shape", "left");
            break;
        case this.rightKey:
            //playGrid.updateActivePos(1,0);
            connection.sendAction("move_active_shape", "right");
            break;
        case this.upKey:
            connection.sendAction("move_active_shape", "rotate");
            //playGrid.rotateActiveShape();
            break;
        case this.downKey:
            connection.sendAction("move_active_shape", "down");
            break;
        case this.spaceKey:
            connection.sendAction("move_active_shape", "hard_drop");
            break;
        case this.specialKey:
            connection.sendAction("use_queued_powerup", true);
            connection.sendAction("get_queued_powerup", true);
            break;
/*
        case this.special2Key:
            connection.sendAction("special2");
            break;
        case this.special3Key:
            connection.sendAction("special3");
            break;
        case this.special4Key:
            connection.sendAction("special4");
            break;
        case this.special5Key:
            connection.sendAction("special5");
            break;
        case this.testKey:
            connection.sendAction("test");
            break;
*/
    }
};

game.states.addState(myState, true);
