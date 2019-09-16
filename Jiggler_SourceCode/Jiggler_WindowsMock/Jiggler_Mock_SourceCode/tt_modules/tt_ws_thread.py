import threading
import asyncio
import json
from time import sleep

import websockets

from .tt_consumer import buildJSON
from .tt_queue import*
from .tt_logger import ttl



class appServerThread (threading.Thread):
	def __init__(self, loop, state):
		threading.Thread.__init__(self)	
		self.loop = loop
		self.state = state
	def run(self):
		ttl.info("Starting appServerThread")
		createPiServer(self.loop, self.state)
		ttl.info("Exiting appServerThread")
		
		
def createPiServer(loop, state):
	asyncio.set_event_loop(loop)

	from subprocess import check_output
	#HOST = str(check_output(['hostname', '-I']))[2:-4]
	jsdf = str(check_output(['ipconfig']))
	#print(jsdf)
	HOST = "127.0.0.1"
	PORT = 55555	
		
	async def hello(websocket, path):
		print('client connected')
		ttl.info('client connected to ws: {}'.format(websocket))
		await websocket.send(buildJSON(state))
		go = 1		
		while go:
			msg=""
			try:				
				try:
					msg = await asyncio.wait_for(websocket.recv(), timeout=1)
				except asyncio.TimeoutError:
					pass
			except websockets.ConnectionClosed:
				print("Client disconnected")
				ttl.info("Client disconnected")
				go=0
				break
			else: 				
				if msg:
					queue_msg(state,msg)
				while state.msgOUT:
					msg = state.msgOUT.pop(0)
					await websocket.send(msg)
					ttl.info("sent update to client")
					ttl.debug(msg)
					sleep(0.2)				
		websocket.close()			
			
	
	start_server = websockets.serve(hello, HOST, PORT,process_request=proc_req)
	state.stop = asyncio.Future(loop=loop)
	
	server = loop.run_until_complete(start_server)
	state.app.menu_screen.wsLabel.text=HOST + ':' + str(PORT)
	print('Websocket-Server listening on ' + HOST + ':' + str(PORT))
	ttl.info('Websocket-Server listening on {}:{}'.format(HOST,PORT))
	
	try:		
		loop.run_until_complete(state.stop)
		
	except asyncio.CancelledError:
		ttl.info("Cancelled Future")
		
	finally:
		print("Cleaning up... ")
		ttl.info("shutting down server")
		server.close()
		loop.run_until_complete(server.wait_closed())
		asyncio.gather(*asyncio.Task.all_tasks()).cancel()
		loop.stop()
		loop.close()
		loop=None
		state.stop=None
	print(" ...done.")
	ttl.info("loop stopped and closed")
	state.app.menu_screen.wsLabel.text=""
	
def proc_req(path, request_headers):
	ttl.debug("Request Header: ")
	ttl.debug("path: " + path)
	ttl.debug("request_headers:\n" + str(request_headers) + "\n")
	
#kivy_venv\Scripts\activate	