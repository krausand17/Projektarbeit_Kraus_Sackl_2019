import json
from .tt_logger import ttl


def notify(state, newVal, newVal_name):
	ttl.info("notify: changed {} to {}".format(newVal_name, newVal))
	msg = buildJSON(state)
	state.msgMOCK.append(msg)
	if state.app.serverOn:
		state.msgOUT.append(msg)
	
		

def buildJSON(state):
	raw={
		"power": state.power,
		"speed": state.curr_speed,
		"angle": state.angle,
		"direction": state.direction
	}
	stateJSON=json.dumps(raw)
	return stateJSON		
