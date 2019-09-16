import logging
import sys
import os


current_dir = os.getcwd() + "/tt_logs"
log_file_name = "tt_log.txt"

os.environ['KCFG_KIVY_LOG_LEVEL'] = "error"
argv=sys.argv

loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
slvl = "error"
lvl = logging.ERROR

	
if "debug" in argv:
	slvl = "debug"
	lvl = logging.DEBUG
	
elif "info" in argv:
	slvl = "info"
	lvl = logging.INFO
	
elif "warn" in argv:
	slvl = "warning"
	lvl = logging.WARNING
	
	
for l in loggers:
	l.setLevel(lvl)


fh = None
sh = logging.StreamHandler()
sh_format = logging.Formatter('[%(levelname)s] - %(name)s - %(message)s')
sh.setFormatter(sh_format)
sh.setLevel(lvl)

def fh_check(lgr):
	if fh:
		lgr.addHandler(fh)
		

if "-f" in argv:
	fh = logging.FileHandler(current_dir+"/"+log_file_name)
	fh_format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
	fh.setFormatter(fh_format)
	fh.setLevel(lvl)
	
	if "-k" in argv:
		os.environ['KCFG_KIVY_LOG_DIR'] = current_dir
		os.environ['KCFG_KIVY_LOG_NAME'] = "kv_" + log_file_name
		if os.path.exists(current_dir + "/kv_" + log_file_name):
			os.remove(current_dir + "/kv_" + log_file_name)	
	
if "-k" in argv:
	os.environ['KCFG_KIVY_LOG_LEVEL'] = slvl
	
if "-w" in argv:
	wslogger = logging.getLogger('websockets')
	wslogger.setLevel(lvl)
	wslogger.addHandler(logging.StreamHandler())
	#fh_check(wslogger)
	

ttl = logging.getLogger('working_touch_thing')
ttl.setLevel(lvl)
ttl.addHandler(sh)
fh_check(ttl)


# # Output Test	
# ttl.error('error')		
# ttl.warning('warning')		
# ttl.info('info')		
# ttl.debug('debug')		


