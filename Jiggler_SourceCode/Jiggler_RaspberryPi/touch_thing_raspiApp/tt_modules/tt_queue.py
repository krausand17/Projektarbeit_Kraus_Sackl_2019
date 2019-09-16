from .tt_logger import ttl

def queue_msg(state, new_msg):
	if new_msg:
		state.msgIN.append(new_msg)
		ttl.debug("Appended to msgIN:" + new_msg)
			