import socket,os,struct,time
import cv2
import pygame
from pygame.locals import *

class Server():
	def __init__(self,port,mode="AUTO"):
		self.port = port
		self.mode = mode
		self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(),port))
		print "Server started at port %d " % port

	def listen(self):

		#import CNN
		#neuralnet = CNN.CNN()
		# neuralnet.load_model('path')


		# listen to one client at max
		self.socket.listen(5)
		client_socket,address = self.socket.accept()
		print "Connected to client "+address
		
		# open the dataset_record file to store image path and label
		if self.mode == "TRAIN":
			train = True
			pygame.init()
			dataset_record=open('dataset_record.txt','a')
	
		while train:

			# recieve the image from the tcp socket
			buffer =''
			data=''
			while len(buf)<4:
				data = client_socket.recv(4-len(buf))
			size = struct.unpack('!i',buf)
			print "Recieving image of %s bytes" % size
			while True:
				data = client.recv(1024)
				if not data:
					break

			# enter into the TRAIN mode
			if self.mode == "TRAIN":
				# filename is current timestamp
				filename = str(time.time())+".jpg"
				# save the image
				image = open('images/'+filename,'wb')
				image.write(data)
				image.close()
				# get pressed key asynchronously and write image path
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						key = pygame.key.get_pressed()

						if key[pygame.K_UP] and key[pygame.K_RIGHT]:
							print "Forward Right\n"
							row = 'images/'+filename+" "+"FR\n"
							dataset_record.write(row)
						elif key[pygame.K_UP] and key[pygame.K_LEFT]:
							print "Forward Left"
							row ='images/'+filename+" "+"FL\n"
							dataset_record.write(row)
						elif key[pygame.K_UP]:
							print "Forward"
							row ='images/'+filename+" "+"F\n"
							dataset_record.write(row)
						elif key[pygame.K_RIGHT]:
							print "Right"
							row ='images/'+filename+" "+"R\n"
							dataset_record.write(row)
						elif key[pygame.K_LEFT]:
							print "Left"
							row = 'images/'+filename+" "+"L\n"
							dataset_record.write(row)
						elif key[pygame.K_DOWN]:
							print "Backwards"
							row = 'images/'+filename+" "+"B\n"
							dataset_record.write(row)
						elif key[pygame.K_q]:
							print 'Training data collection over.'
							train=False
							break
			# enter into the auto mode
			if self.mode == "AUTO":
				# apply image transformations and make it suitable
				processed = self.image_preprocess(data)
				print neuralnet.predict(processed)
				self.show_recieved_image(data)

	def image_preprocess(self,image):
		gray = cv2.imdecode(np.fromstring(image, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
		gray = cv2.resize(image, (62, 62))
		return gray

	def show_recieved_image(self,data):
		image = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
		cv2.imshow('Recieved image', image)

server = Server(80,"TRAIN")
server.listen()



			

