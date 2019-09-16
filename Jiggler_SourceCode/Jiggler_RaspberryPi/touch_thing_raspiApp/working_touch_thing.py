#!/usr/bin/python3

import sys
import os
os.environ['KIVY_GL_BACKEND'] = 'gl'
os.environ['DISPLAY'] = ':0.0'
KCFG_KIVY_LOG_ENABLE = '1'
import signal
from time import sleep
import threading
import asyncio

from tt_modules.tt_logger import*

from RPi.GPIO import cleanup
import kivy
kivy.require('1.11.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from kivy.properties import OptionProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty

from tt_modules.tt_consumer import msg_cb
from tt_modules.tt_queue import*
from tt_modules.tt_ws_thread import*
from tt_modules.tt_program_thread import*


class MainScreen(Screen):
    pwrButton = ObjectProperty(None)

class MenuScreen(Screen):
    pass

class DeviceState(EventDispatcher):
	power = OptionProperty("OFF", options=["OFF", "ON"])
	curr_speed = NumericProperty(0)
	demand_speed = NumericProperty(0)
	last_speed=0
	direction = OptionProperty("LEFT", options=["LEFT", "RIGHT"])
	angle = NumericProperty(0)
	msgIN = ListProperty()
	msgOUT = []
	stop=None
	app=None	
	
class TouchThingApp(App):

	new_loop = ""
	pwsThread = None
	progThread = None
	progChoice = ""
	serverOn = False
	state = DeviceState()
	state.bind(msgIN=msg_cb)
	
	def build(self):
		self.root = root = ScreenManager()
		self.main_screen = MainScreen(name='main_screen')
		self.menu_screen = MenuScreen(name='menu_screen')
		root.add_widget(self.main_screen)
		root.add_widget(self.menu_screen)
		self.state.app=self
		return self.root		

	def button_on_off(app):		
		queue_msg(app.state,"setPower")

	def quit(app):
		app.stop_prog()
		if app.state.stop:
			app.new_loop.call_soon_threadsafe(app.nope, app.state.stop.cancel())
		if app.pwsThread:
			app.pwsThread.join()
		if app.state.power=="ON":
			queue_msg(app.state,"setPower")
		cleanup()
		print("\nBye\n")
		sys.exit()

	def faster(app):
		if app.state.power=="ON":
			queue_msg(app.state,"setDemSpeedInc")

	def slower(app):
		if app.state.power=="ON":
			queue_msg(app.state,"setDemSpeedDec")

	def changeDir(app):
		queue_msg(app.state,"setDir")		
			
	def angleInc(app):
		if app.state.power=="ON":
			queue_msg(app.state,"setAngleInc")
		
	def angleDec(app):
		if app.state.power=="ON":
			queue_msg(app.state,"setAngleDec")
		
	def select_prog(app, selection):		
		app.progChoice = selection
		app.menu_screen.selPrLabel.text="Selected: " + selection
		print("prog selected:", selection)
	
	def run_prog(app):
		if app.state.power == "ON":
			if app.progThread:
				if app.progThread.is_alive():
					pass
				else:
					app.progThread = Tt_ProgramThread(app.state, app.progChoice)						
					app.progThread.start()
			else:
				app.progThread = Tt_ProgramThread(app.state, app.progChoice)						
				app.progThread.start()
		
	def stop_prog(app):
		if app.progThread:
			app.progThread.event.set()
			app.progThread.join()
			app.progThread = None
			
		
	def connectExt(app):
		if not app.new_loop:
			app.new_loop = asyncio.new_event_loop()
		if not app.serverOn:
			pwsThread = appServerThread(app.new_loop, app.state)
			ttl.debug("connectExt() ordering pwsThread")
			pwsThread.start()
			app.serverOn=True
		else:						
			if app.state.stop:
				try:
					app.new_loop.call_soon_threadsafe(app.nope, app.state.stop.cancel())					
				except RuntimeError:
					pass				
				finally:
					app.new_loop.stop()
					app.serverOn=False
					app.new_loop = None
	
	# callback after canceling future
	def nope(a, b):
		pass
	
	def on_start(self, **kwargs):				
		queue_msg(self.state,"setAngleInit")
		print("\n...Ready\n")		
		
		
if __name__=='__main__':
	TouchThingApp().run()
	