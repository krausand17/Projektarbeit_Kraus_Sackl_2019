from time import sleep
from .tt_logger import ttl

def ramp(state):
	ttl.info("Ramp started")
	curr_speed = state.curr_speed 
	demand_speed = state.demand_speed
	n=10
	x=2
	delay=0.1
	
	if curr_speed < demand_speed:
		ramp_size=round((demand_speed-curr_speed)/16,1)
		a=rampExp(state.curr_speed)
		b=rampExp(state.demand_speed)
		inc=1
		if curr_speed==0 and demand_speed==1:
			a=2
			b=200
		elif curr_speed==0 and demand_speed>1:
			a=2
			n+=round(n*ramp_size)			
	else:
		ramp_size=round((curr_speed-demand_speed)/16,1)	
		a=rampExp(state.demand_speed)
		b=rampExp(state.curr_speed)
		inc=-1		
		if demand_speed==0 and curr_speed>1:
			n+=round(n*ramp_size)
			a=2
		elif demand_speed==0 and curr_speed==1:
			a=2
			b=200
		x=n-1
		
	log_msg = "ramp to freq {}, i: {}, x: {}"	
	for i in range(0,n-1):		
		y = rampExp(x,a,b,n)
		ttl.debug(log_msg.format(round(y),i,x))
		sleep(delay)
		x+=inc
		
	state.curr_speed=state.demand_speed	
	

# n	-- nr of steps		-- default 10
# a -- freq at step 1	-- default 200	freq must not be 0; 
# b -- freq at step n 	-- default 14000	
def rampExp(x=1,a=200,b=14000,n=10):	
	return a*pow(pow(b/a,1/(n-1)),(x-1))
	
	