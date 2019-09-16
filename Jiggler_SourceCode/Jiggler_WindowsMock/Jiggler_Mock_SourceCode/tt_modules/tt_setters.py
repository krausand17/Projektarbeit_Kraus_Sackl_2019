from time import sleep

from .tt_ramp import*
from .tt_notify import*
from .tt_logger import ttl


def setPower(state):
	if(state.power=="ON"):
		state.last_speed=state.curr_speed
		setAngleNeut(state)
		if state.curr_speed > 0:
			state.demand_speed=0
			ramp(state)
		state.app.main_screen.pwrButton.background_color=(1.0, 1.0, 1.0, 1.0)
		state.power="OFF"		
	else:
		state.power="ON"
		state.app.main_screen.pwrButton.background_color=(0.0, 0.0, 10.0, 1.0)
		if state.last_speed > 0:
			state.demand_speed=state.last_speed
			ramp(state)
	state.app.main_screen.speedLabel.text="Speed: " + str(state.curr_speed)			
	notify(state, state.curr_speed, "curr_speed")	
	notify(state, state.power, "power")	
	
	
def setDir(state):	
	temp=state.curr_speed
	if(state.direction=="LEFT"):
		newDir = "RIGHT"
	else:
		newDir = "LEFT"
	if temp > 0:
		state.demand_speed=0
		ramp(state)
		sleep(0.1)
		print("")		
		state.direction=newDir
		state.demand_speed=temp
		ramp(state)
	else:
		state.direction=newDir
	state.app.main_screen.dirLabel.text="Direction: " + newDir
	notify(state, state.direction, "direction")

def toStart(state):
	setAngleNeut(state)
	state.demand_speed=0
	ramp(state)
	state.app.main_screen.speedLabel.text="Speed: " + str(state.curr_speed)
	notify(state, state.curr_speed, "curr_speed")
	
def setDemSpeedInc(state):
	if state.demand_speed < 10:
		state.demand_speed+=1
		ramp(state)
		state.app.main_screen.speedLabel.text="Speed: " + str(state.curr_speed)
		notify(state, state.curr_speed, "curr_speed")
		
	
def setDemSpeedDec(state):
	if state.demand_speed > 0:
		state.demand_speed-=1
		ramp(state)
		state.app.main_screen.speedLabel.text="Speed: " + str(state.curr_speed)
		notify(state, state.curr_speed, "curr_speed")
		
	
def setAngleInc(state):
	if state.angle < 3:
		state.angle+=1
		sleep(0.2)
		state.app.main_screen.angleLabel.text="Angle: " + str(state.angle)
		notify(state, state.angle, "angle")
		
		
def setAngleDec(state):
	if state.angle > -3:
		state.angle-=1
		sleep(0.2)
		state.app.main_screen.angleLabel.text="Angle: " + str(state.angle)
		notify(state, state.angle, "angle")


def setAngleInit(state):
	endlagenschalter = 0 	# hardcoded for testing
	offsetTest = 2 			# presuming divice lost power/data with angle_Motor at lvl 2 
	print("starting angle INIT...\n")
	ttl.info("starting angle INIT")
	
	while not endlagenschalter:
		state.angle = 0
		setAngleInc(state)
		offsetTest += 1
		if offsetTest == 3:
			endlagenschalter = 1
			
	state.angle=3
	setAngleNeut(state)
	ttl.info("angle INIT complete")
	

def setAngleNeut(state):
	if state.angle < 0:
		setAngleInc(state)
		setAngleNeut(state)
	if state.angle > 0:
		setAngleDec(state)
		setAngleNeut(state)		
