
# Import required module/s
import socket
from pyfiglet import Figlet
from termcolor import colored, cprint
from colorama import Fore, Back, Style

# NOTE: You are free to use any module(s) required for better representation of the data received from the Server.

# NOTE: DO NOT modify the connectToServer() and the 'if' conditions in main() function.
# 		Although you can make modifications to main() where you wish to call formatRecvdData() function.

def connectToServer(HOST, PORT):
	"""Create a socket connection with the Server and connect to it.

	Parameters
	----------
	HOST : str
		IP address of Host or Server, the Client needs to connect to
	PORT : int
		Port address of Host or Server, the Client needs to connect to

	Returns
	-------
	socket
		Object of socket class for connecting and communication to Server
	"""

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.connect((HOST, PORT))

	return server_socket


def formatRecvdData(data_recvd):
	"""Format the data received from the Server as required for better representation.

	Parameters
	----------
	data_recvd : str
		Data received from the Server about scheduling of Vaccination Appointment
	"""

	##############	ADD YOUR CODE HERE	##############
	
	flag_wel = False
	flag_in = False
	flag_out = False
	
	if(">>>" in data_recvd):
		flag_in = True
	if("<<<" in data_recvd):
		flag_out = True
	if("Welcome" in data_recvd):
		flag_wel = True
	
	if(flag_wel):
		w = data_recvd.split("-")[0]
		s = data_recvd.split("-")[1]
		ii = data_recvd.split("-")[2]
		meta = ii.split("\n")[1]
		opt = ii.split("\n")[2]
		
		f = Figlet(font="standard")
		print(colored(f.renderText(w), "green", attrs=["bold", "reverse"]))
		print(colored(s, "white", attrs=["bold", "reverse"]), end="\n\n")
		print(meta)
		for ele in opt.split(","):
			print(ele.split(":")[0].split("'")[1], " : ", ele.split(":")[1].split("'")[1], end="\n")
		print(">", end=" ")
		flag_in = False
	if(flag_in):
		if(">>> Provide the date" in data_recvd):
			meta = data_recvd.split("\n")[1]
			print(meta)
			print(">", end=" ")
		elif(">>> Select the Dose" in data_recvd or ">>> Select the Age" in data_recvd or ">>> Select the State" in data_recvd or ">>> Select the District" in data_recvd):
			meta = data_recvd.split("\n")[1]
			print(meta)
			opt = data_recvd.split("{")[1]
			for ele in opt.split(","):
				print(ele.split(":")[0].split("'")[1], " : ", ele.split(":")[1].split("'")[1], end="\n")
			print(">", end=" ")
		else:
			print(data_recvd)
	if(flag_out):
		if("selected" in data_recvd or "You are eligible" in data_recvd or "Selected" in data_recvd):
			print(colored(data_recvd, "green", "on_white"), end="\n\n")
		elif("See ya!" in data_recvd):
			print(colored(data_recvd, "cyan"), end="\n\n")
		elif("Invalid" in data_recvd or "You are not eligible" in data_recvd or "no available slots" in data_recvd):
			print(colored(data_recvd, "red", "on_white", attrs=["blink"]), end="\n\n")
		else:
			print(colored(data_recvd, "blue", "on_white"), end="\n\n")
	
	##################################################


if __name__ == '__main__':
	"""Main function, code begins here
	"""

	# Define constants for IP and Port address of the Server to connect to.
	# NOTE: DO NOT modify the values of these two constants
	HOST = '127.0.0.1'
	PORT = 24680

	# Start the connection to the Server
	server_socket = None
	try:
		server_socket = connectToServer(HOST, PORT)
	except ConnectionRefusedError:
		print("*** Start the server first! ***")
	
	# Receive the data sent by the Server and provide inputs when asked for.
	if server_socket != None:
		while True:
			data_recvd = server_socket.recv(1024).decode('utf-8')
			formatRecvdData(data_recvd)

			if '>>>' in data_recvd:
				data_to_send = input()
				server_socket.sendall(data_to_send.encode('utf-8'))
			
			if not data_recvd:
				server_socket.close()
				break
		
		server_socket.close()
