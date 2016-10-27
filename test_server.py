import socket
import os
import time


images = []
for im in os.listdir('image'):
	images.append(im)

for image in images:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	address =('localhost',6666)
	sock.connect(address)
	with open('image/'+image, 'rb') as file_to_send:
		for data in file_to_send:
			sock.sendall(data)
	print "image sent"
	sock.close()
	print "Sleeping.."
	time.sleep(0.3)