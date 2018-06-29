import asyncio
import websockets
import json
import random
import tetrislib

class GameServer:
    """ 
    The purpose of the GameServer class is to:
    * Control the Board via commands using JSON-objects
    * Determine the rules of the game
    """
    
    PROTOCOL_VERSION = "0.3.1"
    def __init__(self):
        # Create an internal tetrisboard
        self.client_name = ""

        self.game_started = False
        self.game_over = False
        
        self.board = tetrislib.Board()
        self.next_block = None           # this is a string

    def getBoard(self):
        return self.board

    def createResponse(self, response_t, value):
        ret = {}
        ret["version"] = self.PROTOCOL_VERSION
        ret["response_type"] = response_t
        ret["value"] = value
        return ret

    def createJSONResponse(self, response_t, value):
        return json.dumps(self.createResponse(response_t, value))

    def parseAction(self, action):
        """ Assume a dictionary with an action as specified in com.rst """
        a_type = action["type"]
        a_val = action["value"]
        
        if a_type == "get_board":
            b = self.board.getBoard()
            return self.createJSONResponse("board", b)

        elif a_type == "get_active_shape":
            active_shape = self.getBoard().active_shape_str
            return self.createJSONResponse("active_shape", active_shape)

        elif a_type == "move_active_shape":
            self.getBoard().traverse(a_val)
            return self.createJSONResponse("status", 1)
        
        elif a_type == "get_queued_powerup":
            return self.createJSONResponse("queued_powerup", "Nothing")

        elif a_type == "use_queued_powerup":
            b = self.board.getBoard()
            return self.createJSONResponse("board", b)

        elif a_type == "set_name":
            self.client_name = a_val
            return self.createJSONResponse("status", 1)

        elif a_type == "start_game" and a_val == True:
            self.game_started = True

            rand_shape_str = self.generateRandomShape()
            print("Set shape to " + rand_shape_str)
            self.board.setActiveShapeFromString(rand_shape_str)
            
            return self.createJSONResponse("status", 1)

        elif a_type == "end_game" and a_val == True:
            self.game_over = True
            return self.createJSONResponse("status", 1)

    def generateRandomShape(self):
        """ Returns a string of an available shape"""
        avail_shapes = self.board.getAvailableShapes()
        return avail_shapes[random.randint(0, len(avail_shapes)-1)]
        
    def generateNextShape(self):
        self.next_shape = self.generateRandomShape()

    def update(self):
        self.board.update()
    

def startServer():
    current_games = []

    async def incommingConHandler(websocket, path):
        """ Handles all traffic in a single thread """
        g = GameServer()
        
        async for message in websocket:
            # Assume a JSON
            s = json.loads(message)
            print(s["type"] + ": '" + str(s["value"]) + "'")
            response = g.parseAction(s)
            await websocket.send(response)
            

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(incommingConHandler, 'localhost', 7441))
    
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    startServer()
