import socket
import threading

#global var
buf = []
name = ""

#IP and port
bind_ip   = "192.168.176.108"
bind_port = 9020

#Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip,bind_port))
server.listen(5)          
print "[*] Listening on %s : %d" % (bind_ip,bind_port)

# this is our client-handling thread
def handle_client(client_socket):
	client.send("Welcome to Seth's chat room\r\n")

	# print out what the client sends
	while True:
		request = ""
		holdChar = ""
		while True:
			temp = client_socket.recv(1)
			request = request + temp
			if (temp == "\n" and holdChar == "\r"):
				break
			holdChar = temp
		print "[*] Received: %s" % request
		response = handle_request(request)
		# send back a packet
		# if response == "quit":
		# 	client_socket.close()
		client_socket.send(response)
	client_socket.close()

def handle_request(request):
	global buf, name

	request = request.split(" ")
	print request[0]
	if request[0] == "help\r\n":
		return "test: (input words to be returned)\n name: (input a name for your chatname)\n get (to receive what has been inputted)\n push: (words to be inputted into the buffer)\n getrange x x (the Xs are numbers to grab the range of the buffer)\n random text (will return an error message)\n adios (will close the connection)\r\n"
	elif request[0] == "test:":
		tempMessage = ""
		for i in request:
			if i != "test:":
				if tempMessage == "":
					tempMessage = i
				else:
					tempMessage = tempMessage + " " + i
		tempMessage.strip('\r\n')
		return tempMessage + "\r\n"
	elif request[0] == "name:":
		for row in request:
			if row != "name:":
				name = name + " " + row
		name = name.strip()
		return "OK\r\n"
	elif request[0] == "get\r\n":
		message = ""
		for row in buf:
			message = message + row
		if message == "":
			return message + "\r\n"
		return message + "\r\n"
	elif request[0] == "push:":
		if name == "":
			name = "unknown"
		line = name + ":"
		for row in request:
			if row != "push:":
				line = line + " " + row
		line.strip('\r\n')
		buf.append(line)
		return "OK\r\n"
	elif request[0] == "getrange":
		firstNum = int(request[1])
		secNum = int(request[2]) + 1
		combinedMessage = ""
		for row in buf[firstNum:secNum]:
			combinedMessage = combinedMessage + row
		return combinedMessage + "\r\n"
	elif request[0] == "adios":
		buf = ""
		name = ""
		#client_socket.close()
		return "quit"
	elif request == "\r\n":
		return ""
	else:
		return "Error: unrecognized command: SOME UNRECOGNIZED COMMAND\r\n"


while True:
	client,addr = server.accept()
	print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
	# spin up our client thread to handle incoming data
	client_handler = threading.Thread(target=handle_client,args=(client,))
	client_handler.start()

