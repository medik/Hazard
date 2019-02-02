import asyncio
import websockets
import json
import random
import tetrislib
import threading
import logging
import functools

class User:
    PROTOCOL_VERSION = "0.4-dev"
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
            b = self.board.mergeActiveWithBoard()
            return self.createJSONResponse("board", b)
        elif a_type == "get_active_shape":
            active_shape = self.getBoard().active_shape_str
            return self.createJSONResponse("active_shape", active_shape)
        elif a_type == "move_active_shape":
            self.getBoard().traverse(a_val)
            b = self.board.mergeActiveWithBoard()
            return self.createJSONResponse("board", b)
        elif a_type == "get_queued_powerup":
            return self.createJSONResponse("queued_powerup", "Nothing")
        elif a_type == "use_queued_powerup":
            b = self.board.getBoard()
            return self.createJSONResponse("board", b)
        elif a_type == "set_name":
            self.client_name = a_val
            return self.createJSONResponse("status", 1)
        elif a_type == "is_ready" and a_val == True:
            self.is_ready = True
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

    def gotoNextTick(self):
        self.board.update()
        board_json = self.createJSONResponse("board",self.board.mergeActiveWithBoard())        
        #print(board_json)


    def startGame(self):
        # Generate active shape
        avail_shapes = self.board.getAvailableShapes()
        i = random.randint(0, len(avail_shapes)-1)
        self.board.setActiveShapeFromString(avail_shapes[i])

def createResponse(response_t, value):
    ret = {}
    ret["version"] = "0.4-dev"
    ret["response_type"] = response_t
    ret["value"] = value
    return ret

def createJSONResponse(response_t, value):
    return json.dumps(createResponse(response_t, value))


def startLobby():
    print("Starting Lobby server")
    logging.basicConfig(level=logging.DEBUG)
    connected_to_server = {}
    ready_flag = {}

    def sendAll(msg):
        for n, c in connected_to_server.items():
            asyncio.ensure_future(c.websocket.send(msg))

    async def sendAllAsync(msg):
        for n, c in connected_to_server.items():
            await c.websocket.send(msg) 
    
    def isEveryoneReady():
        numReady = 0
        for name, is_ready in ready_flag.items():
            if is_ready:
                numReady += 1
        if numReady < len(connected_to_server):
            return False
        else:
            return True
        
    def addConnectedUser(name, u):
        connected_to_server[name] = u
        ready_flag[name] = False
        sendAll(createJSONResponse("new_player", name))
        print(name + " connected")

    async def main(websocket, path):
        global not_started_yet
        loop = asyncio.get_event_loop()
        u = User(websocket)
        wait = 1.0

        # Get user name
        name = ""
        while name == "":
            msg = await websocket.recv()
            s = json.loads(msg)

            if s["type"] == "my_name_is":
                name = s["value"]
                u.client_name = name

        # Send all connected users
        for conn in connected_to_server:
            asyncio.run_coroutine_threadsafe(websocket.send(createJSONResponse("new_player", conn)), loop)

        # Add connected user
        connected_to_server[name] = u
        ready_flag[name] = False
        print(name + " connected")
        sendAll(createJSONResponse("new_player", name))

        # Lobby state
            
        ready = False
        while not ready:
            msg = await websocket.recv()
            s = json.loads(msg)

            if s["type"] == "is_ready":
                print(name + " is ready")
                ready_flag[name] = True
                ready = True

    asyncio.get_event_loop().set_debug(True)
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(main, 'localhost', 7441))
    asyncio.get_event_loop().run_forever()
    


def startGame():
    tick = 1
    def updateNextTick(g, wait, path):
        global tick
        loop = asyncio.get_event_loop()
        print(loop.time())
        next_boards = {}
        for n, c in connected_to_server.items():
            c.board.update()
            board = c.board.mergeActiveWithBoard()
            #board_json = createJSONResponse("board", board)
            #asyncio.ensure_future(c.websocket.send(board_json))            
            next_boards[n] = board
        print(tick)
        tick += 1

        sendAll(createJSONResponse("connected_boards", next_boards))
        print(loop.time())
        time = loop.time()
        loop.call_at(time + wait, functools.partial(updateNextTick, g, wait, path))

        #loop.call_soon(functools.partial(g.gotoNextTick, g.websocket))
        #time = loop.time()
        #loop.call_at(time + wait, functools.partial(updateNextTick, g, wait, path))

def startServer():
    logging.basicConfig(level=logging.DEBUG)
    connected_to_server = {}
    ready_flag = {}
    
    def sendAll(msg):
        for n, c in connected_to_server.items():
            asyncio.ensure_future(c.websocket.send(msg))

    async def sendAllAsync(msg):
        for n, c in connected_to_server.items():
            await c.websocket.send(msg)    
    
    async def start_game(u, websocket):
        # Wait for everyone
        ready = False
        while not ready:
            ready = isEveryoneReady()
            
        print("Starting game for " + u.client_name)
        u.startGame()
        await websocket.send(createJSONResponse("start_game", True))
        # Start game
        await start_game(u, websocket)

        print("Start tick timer")
        time = loop.time()
        loop.call_at(time + 1.0, functools.partial(updateNextTick, u, wait, path))

        # Game state
        while True:
            msg = await websocket.recv()
            s = json.loads(msg)
            ans = u.parseAction(s)
            await websocket.send(ans)
    
    async def main(websocket, path):
        global not_started_yet
        loop = asyncio.get_event_loop()
        u = User(websocket)
        wait = 1.0

        # Get user name
        name = ""
        while name == "":
            msg = await websocket.recv()
            s = json.loads(msg)

            if s["type"] == "my_name_is":
                name = s["value"]
                u.client_name = name

        # Send all connected users
        for conn in connected_to_server:
            asyncio.run_coroutine_threadsafe(websocket.send(createJSONResponse("new_player", conn)), loop)

        # Add connected user
        connected_to_server[name] = u
        ready_flag[name] = False
        print(name + " connected")
        sendAll(createJSONResponse("new_player", name))

        # Lobby state
            
        ready = False
        while not ready:
            msg = await websocket.recv()
            s = json.loads(msg)

            if s["type"] == "is_ready":
                print(name + " is ready")
                ready_flag[name] = True
                ready = True
                
        # I am ready
        sendAll(createJSONResponse("lobby_user_ready", u.client_name))
        
        asyncio.run_coroutine_threadsafe(start_game(u, websocket), loop)

        while True:
            msg = await websocket.recv()
            s = json.loads(msg)
            ans = u.parseAction(s)
            await websocket.send(ans)
                    
            
    asyncio.get_event_loop().set_debug(True)
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(main, 'localhost', 7441))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    startLobby()
