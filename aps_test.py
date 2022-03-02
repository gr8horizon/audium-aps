import os, time
import socket 
from subprocess import check_output
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import threading
# Requires: python-osc

# def APS_handler(address, *args):

# 	print("OSC APS Message Received: " + str(args[0]))

# 	if args[0] == "who":
# 		client.send_message("/APS", myAPS_ID)

# 	elif args[0] == "reboot":
# 		client.send_message("/APS/" + myAPS_ID, "rebooting")
# 		os.system("sudo reboot")
# 	elif args[0] == "version":
# 		client.send_message("")

# 	elif args[0] == "pull":
# 		client.send_message("/APS/" + myAPS_ID, "pulled")
# 		os.system("git -C ~/audium-aps pull")
# 		os.system("sudo systemctl restart aps.service")


def serve():
	server = ThreadingOSCUDPServer(("192.168.42.110", 1234), dispatcher)
	server.serve_forever()

if __name__ == '__main__':

	# localip = socket.gethostbyname(socket.gethostname())

	dispatcher = Dispatcher()
	dispatcher.set_default_handler(print)

	serve()
	print('hi')
	

	client_1 = SimpleUDPClient("192.168.42.101", 2020)
	client_1.send_message("/APS", "who")
	