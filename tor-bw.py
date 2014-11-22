#!/usr/bin/python
#------------------------------------------
#
#    A script to register a Tor relay's
#	 bandwidth data to disk
#
# Author : Luiz Kill
# Date   : 21/11/2014
#
# http://lzkill.com
#
#------------------------------------------

import os
import sys
import time
import functools
from stem.control import EventType, Controller, Signal
		  

TOR_CONTROL_PORT = 9051
TOR_ADDRESS = "127.0.0.1"
TOR_CONTROLLER_PASSWD = ""
TOR_RECONNECT_DELAY = 5.0

# The Tor controller object
tor_controller = None

is_tor_alive = False

# Location of the Tor bw files
LOCATION="/usr/share/tor/statistics/"

file_rx = None
file_tx = None

rx = 0
tx = 0


def main():
	global tor_controller
	global is_tor_alive
	global file_rx
	global file_tx

	try:
	
		file_rx = open(LOCATION + "rx", "wb")
		file_tx = open(LOCATION + "tx", "wb")
		
		while True:
			if tor_controller == None:
				try:
					tor_controller = Controller.from_port(address=TOR_ADDRESS, port=TOR_CONTROL_PORT)
				except Exception as exc:
					print(time.ctime(),exc)

			elif tor_controller.is_authenticated() == False:
				try:
					tor_controller.authenticate(password=TOR_CONTROLLER_PASSWD)
				except Exception as exc:
					print(time.ctime(),exc)
				else:
					tor_bind()
					
			is_tor_alive = (tor_controller != None and tor_controller.is_authenticated())
			time.sleep(TOR_RECONNECT_DELAY)

	except KeyboardInterrupt:
		print(time.ctime(), 'Script stopped by the user')
		pass

	except Exception as exc:
		print(time.ctime(),exc)

	finally:
		tor_disconnect()
		file_rx.close()
		file_tx.close()

			
def tor_disconnect():
	global is_tor_alive
	global tor_controller

	if tor_controller:
		try:    
			tor_unbind()
			tor_controller.close()
			
		except Exception as exc:
			print(time.ctime(),exc)
			pass

		is_tor_alive = False
		tor_controller = None


def tor_bind():
	global tor_controller
	global tor_bw_event_handler
	if tor_controller:
		tor_bw_event_handler = functools.partial(handle_bandwidth_event)
		tor_controller.add_event_listener(tor_bw_event_handler, EventType.BW)


def tor_unbind():
	global tor_controller
	global tor_bw_event_handler
	if tor_controller:
		tor_controller.remove_event_listener(tor_bw_event_handler)


def handle_bandwidth_event(event):
	global file_rx
	global file_tx
	global rx
	global tx

	rx += event.read
	tx += event.written
	
	file_rx.seek(0)
	file_rx.write(str(rx))
	file_rx.truncate()
	
	file_tx.seek(0)
	file_tx.write(str(tx))
	file_tx.truncate()
	

if __name__ == '__main__':
	main()
	
