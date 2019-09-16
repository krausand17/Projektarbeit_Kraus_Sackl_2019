import threading
import asyncio
import json
from time import sleep

import websockets

from .tt_consumer import buildJSON
from .tt_queue import*
from .tt_logger import ttl



class MockServerThread (threading.Thread):
	def __init__(self, loop, state):
		threading.Thread.__init__(self)	
		self.loop = loop
		self.state = state
	def run(self):
		ttl.info("Starting mockThread")
		createMockServer(self.loop, self.state)
		ttl.info("Exiting mockThread")
		
		
def createMockServer(loop, state):
	asyncio.set_event_loop(loop)

	HOST = '127.0.0.1'
	PORT = 44444	
		
	async def hello(websocket, path):
		print('mock connected')
		ttl.info('mock connected to ws: {}'.format(websocket))
		await websocket.send(buildJSON(state))
		go = 1		
		while go:
			msg=""
			try:		
				try:
					msg = await asyncio.wait_for(websocket.recv(), timeout=0.2)
				except asyncio.TimeoutError:
					pass
			except websockets.ConnectionClosed:
				print("mock disconnected")
				ttl.info("mock disconnected")
				go=0
				break	
			else:
				while state.msgMOCK:
					msg = state.msgMOCK.pop(0)
					await websocket.send(msg)
					ttl.info("sent update to mock")
					ttl.debug(msg)
					sleep(0.2)									
		websocket.close()			
			
	
	start_server = websockets.serve(hello, HOST, PORT)
	state.stopMock = asyncio.Future(loop=loop)
	
	server = loop.run_until_complete(start_server)
	print('mock-Server listening on ' + HOST + ':' + str(PORT))
	ttl.info('mock-Server listening on {}:{}'.format(HOST,PORT))
	
	try:		
		loop.run_until_complete(state.stopMock)
		
	except asyncio.CancelledError:
		ttl.info("Cancelled Future of mock loop")
		
	finally:
		ttl.info("shutting down mock-server")
		server.close()
		loop.run_until_complete(server.wait_closed())
		asyncio.gather(*asyncio.Task.all_tasks()).cancel()
		loop.stop()
		loop.close()
		loop=None
		state.stopMock=None
	ttl.info("mock loop stopped and closed")
	state.app.menu_screen.wsLabel.text=""
	

	
	