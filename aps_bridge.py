import os, time, sys
import socket 
from subprocess import check_output
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import threading
# Requires: python-osc

def APS_handler(address, *args):

	print("OSC APS Message Received: " + str(args[0]))

	if args[0] == "who":
		client.send_message("/APS", myAPS_ID)

	elif args[0] == "reboot":
		client.send_message("/APS/" + myAPS_ID, "rebooting")
		os.system("sudo reboot")
	elif args[0] == "version":
		client.send_message("")

	elif args[0] == "pull":
		client.send_message("/APS/" + myAPS_ID, "pulled")
		os.system("git -C ~/audium-aps pull")
		os.system("sudo systemctl restart aps.service")

def APS_play_handler(address, *args):

	print("OSC APS Play Message Received: " + str(args[0]))
	client.send_message("/APS/play", args[0])

	# os.system("killall vlc")  # FIXME: do we need a wait here? or failure handler?
	# os.system("sleep 1")
	# TODO:
	# if args contains 43, add "--aspect-ratio 43 "
	# if args contains noloop, don't add "--loop "

	#if not os.path.exists('~/Videos/' + args[0]):
		#return

	# try this and hope killall doesn't take too much time, preventing
	vlc_running = os.system('pidof vlc')
	if vlc_running != 256:
		os.system('killall vlc')
		time.sleep(0.1)



	if len(args) > 1:
		if args[1] == 43:
			os.system("vlc -I http --http-password=22 --loop --no-video-title --aspect-ratio 4:3 ~/Videos/" + args[0])
		elif args[1] == "noloop":
			os.system("vlc -I http --http-password=22 --no-video-title ~/Videos/" + args[0])
	else:
		os.system("vlc -I http --http-password=22 --loop --no-video-title ~/Videos/" + args[0])

def APS_kill_handler(address, *args):

	print("OSC APS Kill Message Received. ")
	client.send_message("/APS/kill", myAPS_ID)
	os.system("killall vlc")


if __name__ == '__main__':

	# time.sleep(10) # because some Pi's need time to resolve their Manual IP assignment
	#localip = socket.gethostbyname_ex(socket.gethostname())
	# localip = str(check_output(['hostname', '-I'], universal_newlines=True).strip('\n'))

	localip = str(check_output(['hostname', '-I'])).split(' ')[0].replace("b'","")

	while (localip[-3:-1] != "10"): # want 101:106  # FIXME (find a better way!)
		print(localip + "!!!")
		sys.stdout.flush()
		time.sleep(5)
		localip = str(check_output(['hostname', '-I'])).split(' ')[0].replace("b'","")
		
	print(localip)
	sys.stdout.flush()
	myAPS_ID = socket.gethostname()

	dispatcher = Dispatcher()
	dispatcher.map("/APS", APS_handler)
	dispatcher.map("/APS/play", APS_play_handler)
	dispatcher.map("/APS/kill", APS_kill_handler)
	dispatcher.set_default_handler(print)

	#server_port_QLAB = 2020
	#server_QLAB = ThreadingOSCUDPServer(("127.0.0.1", server_port_QLAB), dispatcher)
	#server_thread_QLAB = threading.Thread(target=server_QLAB.serve_forever)
	#server_thread_QLAB.start()

	client = SimpleUDPClient("192.168.42.255", 1234)
	client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	server = ThreadingOSCUDPServer((localip, 2020), dispatcher)
	server.serve_forever()