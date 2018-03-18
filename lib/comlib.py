import asyncio
import websockets
import json
import random
import tetrislib

class GameServer:
    PROTOCOL_VERSION = "0.3"
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
            return self.createJSONResponse("active_shape", self.get)
        elif a_type == "set_name":
            return self.createJSONResponse("get_set_name_response", "set_name")
        elif a_type == "start_game" and a_val == True:
            self.game_started = True
            print("The game has been started")
    
    def generateNextBlock(self):
        avail_blocks = self.board.getAvailableBlocks()
        next_block_i = random.randint(0, len(avail_blocks)-1)
        self.next_block = avail_blocks[next_block_i]
    
    

def startServer():
    async def echo(websocket, path):
        async for message in websocket:
            print(message)

    asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 7441))
    asyncio.get_event_loop().run_forever()
