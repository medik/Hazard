import asyncio
import websockets
import json
import random
import tetrislib

class GameFacade:
    def __init__(self):
        # Create an internal tetrisboard
        self.board = tetrislib.Board()
        self.next_block = None           # this is a string

    def parseJSON(self, json):
        """ parsing json and do useful things with it """

        

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
