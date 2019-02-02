import asyncio
import websockets
import json
import random
import tetrislib
import threading
import logging
import functools

class GameServer:
    PROTOCOL_VERSION = "0.3.1"
    def __init__(self, ws):
        # Create an internal tetrisboard
        self.client_name = ""

        self.game_started = False
        self.game_over = False
        
        self.board = tetrislib.Board()
        self.next_block = None           # this is a string

        self.tick_timer = 1
        self.websocket = ws

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
            self.startGame()
            return self.createJSONResponse("game_started", 1)
        elif a_type == "end_game" and a_val == True:
            self.game_over = True
            return self.createJSONResponse("status", 1)
    
    def generateNextShape(self):
        avail_shapes = self.board.getAvailableShapes()
        next_block_i = random.randint(0, len(avail_shapes)-1)
        self.next_block = avail_blocks[next_block_i]

    def gotoNextTick(self, websocket):
        self.board.update()
        
        board_json = self.createJSONResponse("board",self.board.mergeActiveWithBoard())        
        print(board_json)
        asyncio.ensure_future(websocket.send(board_json))

    def startGame(self):
        # Generate active shape
        avail_shapes = self.board.getAvailableShapes()
        i = random.randint(0, len(avail_shapes)-1)
        self.board.setActiveShapeFromString(avail_shapes[i])


def startServer():
    logging.basicConfig(level=logging.DEBUG)
    connected_ws = set()
    
    def updateNextTick(g, wait, websocket, path):
        loop = asyncio.get_event_loop()
        loop.call_soon(functools.partial(g.gotoNextTick, websocket))
        time = loop.time()
        loop.call_at(time + wait, functools.partial(updateNextTick, g, wait, websocket, path))
    
    async def main(websocket, path):
        connected_ws.add(websocket)
        loop = asyncio.get_event_loop()

        g = GameServer(websocket)
        wait = 1.0
        
        while True:
            msg = await websocket.recv()
            s = json.loads(msg)
            print(s)
            if s["type"] == "start_game" and s["value"] == 1:
                time = loop.time()
                loop.call_at(time + 1.0, functools.partial(updateNextTick, g, wait, websocket, path))
            ans = g.parseAction(s)
            await websocket.send(ans)
            
            
    asyncio.get_event_loop().set_debug(True)
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(main, 'localhost', 7441))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    startServer()
