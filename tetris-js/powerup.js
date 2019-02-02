"use strict";

/**
 * @file A protoype for powerups.
 * @author Alexander Hjelm <alexander-hjelm@tutanota.com>
 */

var powerupNames = ["Nothing", "AddRow", "Earthquake", "Milkshake", "RemovePow", "Shotgun", "Gravity", "ClearBoard", "SwitchBoard"];

function Powerup(state, name) {
    this.state = state;

    if (!powerupNames.includes(name))
    {
        throw name + " is not an available power-up! (See powerup.js)";
    }

    this.name = name;

}
