import socket,os,struct,time
import cv2
import numpy as np
import pygame
from pygame.locals import *
import threading

class Server():
	def __init__(self,port,mode="TRAIN"):
		self.port = port
		self.mode = mode

		if mode == "TRAIN":
			pygame.init()
			self.screen = pygame.display.set_mode((800, 600))
			clock = pygame.time.Clock()

		self.training_file = None
		self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.socket.bind(("",port))
		print "Server started at port %d " % port

	def listen(self):

		#import CNN
		#neuralnet = CNN.CNN()
		#neuralnet.load_model('path')

		print "Mode Training: "+str(self.mode)
		
			
		while self.mode =="TRAIN":
			
			self.socket.listen(5)
			
			client_socket,address= self.socket.accept()

			print "Connected to car"

			if self.mode == "TRAIN":
				
				# filename is current timestamp
				filename = 'training_data/images/'+str(time.time())+".jpg"

				self.training_file = filename

				with open(filename, 'wb') as image:
					while True:
						data =client_socket.recv(4096)
						if not data:break
						image.write(data)

				print "Frame recieved"

				
				dataset_record=open('training_data/dataset_record.txt','a')
				
				for event in pygame.event.get():
					if event.type == KEYDOWN:
						key = pygame.key.get_pressed()

						if key[pygame.K_UP] and key[pygame.K_RIGHT]:
							print "Forward Right\n"
							dataset_record.write(filename+" "+"1\n")
						elif key[pygame.K_UP] and key[pygame.K_LEFT]:
							print "Forward Left"
							dataset_record.write(filename+" "+"2\n")
						elif key[pygame.K_UP]:
							print "Forward"
							dataset_record.write(filename+" "+"3\n")
						elif key[pygame.K_RIGHT]:
							print "Right"
							dataset_record.write(filename+" "+"4\n")
						elif key[pygame.K_LEFT]:
							print "Left"
							dataset_record.write(filename+" "+"5\n")
						elif key[pygame.K_DOWN]:
							print "Backwards"
							dataset_record.write(filename+" "+"6\n")
						elif key[pygame.K_q]:
							print 'Training data collection over.'
							exit()

			# enter into the auto mode
			if self.mode == "AUTO":
				# apply image transformations and make it suitable
				processed = self.image_preprocess(data)
				print neuralnet.predict(processed)
				self.show_recieved_image(data)

	def image_preprocess(self,image):
		# encode the image as grayscale
		gray = cv2.imdecode(np.fromstring(image, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
		# resize the image to fit the input nodes of the neural network
		gray = cv2.resize(image, (62, 62))
		return gray

	def show_recieved_image(self,data):
		image = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
		cv2.imshow('Recieved image', image)

server = Server(8000,"TRAIN")
server.listen()



			

