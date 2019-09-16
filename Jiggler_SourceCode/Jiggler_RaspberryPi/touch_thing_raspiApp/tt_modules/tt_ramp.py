import RPi.GPIO as GPIO

from time import sleep
from .tt_logger import ttl

GPIO.setmode(GPIO.BOARD)
# speed
GPIO.setup(32, GPIO.OUT)  # pin 26 = pulse, gelb
GPIO.setup(22, GPIO.OUT)  # pin 22 = enable, rot
GPIO.output(22, GPIO.HIGH)
# direction
GPIO.setup(24, GPIO.OUT)  # pin 22 = enable, grün
GPIO.output(24, GPIO.LOW)

pwm=GPIO.PWM(32,1)
pwm.ChangeDutyCycle(50)

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
			pwm.start(1)
		elif curr_speed==0 and demand_speed>1:
			a=2
			n+=round(n*ramp_size)
			pwm.start(1)			
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
		
		pwm.ChangeFrequency(round(y))
		
		ttl.debug(log_msg.format(round(y),i,x))
		sleep(delay)
		x+=inc
	
	if demand_speed==0:
		pwm.stop()
	state.curr_speed=state.demand_speed	
	

# n	-- nr of steps		-- default 10
# a -- freq at step 1	-- default 200	freq must not be 0; 
# b -- freq at step n 	-- default 14000	
def rampExp(x=1,a=200,b=14000,n=10):	
	return a*pow(pow(b/a,1/(n-1)),(x-1))
	
	