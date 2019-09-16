import json
from .tt_logger import ttl


def notify(state, newVal, newVal_name):
	ttl.info("notify: changed {} to {}".format(newVal_name, newVal))
	if state.app.serverOn:
		state.msgOUT.append(buildJSON(state))
		

def buildJSON(state):
	raw={
		"power": state.power,
		"speed": state.curr_speed,
		"angle": state.angle,
		"direction": state.direction
	}
	stateJSON=json.dumps(raw)
	return stateJSON		
