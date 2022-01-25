import os, time
import socket 
from subprocess import check_output
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import threading

def APS_handler(address, *args):

	print("OSC APS Message Received: " + str(args[0]))

	if args[0] == "who":
		client.send_message("/APS", myAPS_ID)
	#os.system("vlc Videos/Waterfall.mp4")


if __name__ == '__main__':

	#localip = socket.gethostbyname_ex(socket.gethostname())
	localip = str(check_output(['hostname', '-I'], universal_newlines=True).
strip('\n'))
	localip = str(check_output(['hostname', '-I'])).split(' ')[0].replace("b'","")
	print(localip)
	myAPS_ID = socket.gethostname()

	dispatcher = Dispatcher()
	dispatcher.map("/APS", APS_handler)
	dispatcher.set_default_handler(print)

	#server_port_QLAB = 2020
	#server_QLAB = ThreadingOSCUDPServer(("127.0.0.1", server_port_QLAB), dispatcher)
	#server_thread_QLAB = threading.Thread(target=server_QLAB.serve_forever)
	#server_thread_QLAB.start()

	client = SimpleUDPClient("192.168.42.255", 1234)
	client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	server = BlockingOSCUDPServer((localip, 2020), dispatcher)
	server.serve_forever()