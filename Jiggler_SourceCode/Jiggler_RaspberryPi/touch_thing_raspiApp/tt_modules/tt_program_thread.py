import threading
import json
from time import sleep

from .tt_logger import ttl
from .tt_queue import*


class Tt_ProgramThread (threading.Thread):
	def __init__(self, state, pName = "def_prog"):
		threading.Thread.__init__(self)
		self.event = threading.Event()
		self.state = state
		self.pName = pName
	def run(self):
		ttl.info("Starting ProgThread")
		runProgram(self.state, self.pName, self.event)
		ttl.info("Exiting ProgThread")
		
def runProgram(state, pName, event):
	progJSON = None
	path = "./tt_progs/" + pName + ".json"
	try:		
		progFile = open(path, "r")
		progJSON = json.load(progFile)
	except IOError:
		ttl.error("couldn't open program file '{}'".format(path))
	
	if progJSON:
	
		queue_msg(state, "toStart")
		
		tl = 0
		params = progJSON["params"]
		for i in range(1, len(params), 2):
			tl += params[i]
		state.app.main_screen.runningLabel.text="Running: "+progJSON["name"]+", "+str(tl)
		state.app.menu_screen.prNameLabel.text="Name: "+progJSON["name"]
		state.app.menu_screen.prDurLabel.text="Duration: "+str(tl)
		print("p_name: ", progJSON["name"])
		print("p_diff: ", progJSON["difficultyLevel"])
		print("p_totL: ", tl, "sec")
		ttl.info("Selected Program: {}".format(progJSON["name"]))
		
		sleep(2) #to give everything time to set to neutral
		
		for i in range(0, len(params)-1, 2):
			if not event.is_set():
				queue_msg(state, params[i])
				ttl.debug("appended cmd: {}".format(params[i]))
				for i in range(0, params[i+1]):
					if not event.is_set():
						sleep(1)
						tl -= 1
						state.app.main_screen.runningLabel.text="Running: "+progJSON["name"]+", "+str(tl)
					else:
						break
				# sleep(params[i+1])
				# tl -= params[i+1]
				# state.app.main_screen.runningLabel.text="Running: "+progJSON["name"]+", "+str(tl)
			else:
				print("Aborted by User")
				ttl.info("Aborted by User")
				break
				
		queue_msg(state, "toStart")
		state.app.main_screen.runningLabel.text=""
		state.app.menu_screen.prNameLabel.text=""
		state.app.menu_screen.prDurLabel.text=""
		print("Program ended")
		ttl.info("Program ended")

