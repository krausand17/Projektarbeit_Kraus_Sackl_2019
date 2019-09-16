from .tt_setters import*
from .tt_logger import ttl	


def msg_cb(state, msgIN):
	if msgIN:
		if msgIN[0] in funcList:
			func = funcList.get(msgIN[0])
			func(state)
		else:
			ttl.error("unknown command in queue: " + msgIN[0])
		msgIN.pop(0)

funcList={"setDemSpeedInc":setDemSpeedInc,"setDemSpeedDec":setDemSpeedDec,
	"setPower":setPower,"setDir":setDir,"setAngleInc":setAngleInc,
	"setAngleDec":setAngleDec,"setAngleInit":setAngleInit,
	"toStart":toStart}		
		
