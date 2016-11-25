import socket

target_host = "localhost"
target_port = 9020
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host,target_port))
response = client.recv(4096)

while True:
	print response
	message = raw_input("-> ")
	if message == "adios":
		client.close()
	client.send(message + "\r\n")
	# receive some data 
	response = client.recv(4096)