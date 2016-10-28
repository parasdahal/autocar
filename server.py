import socket,os,struct,time
import cv2
import urllib
import numpy as np
import pygame
import serial
import CNN
from pygame.locals import *
import threading

class Server():

	def __init__(self,url,mode="TRAIN"):
		
		self.port = None
		self.mode = mode
		self.url = url

		if mode == "TRAIN":
			pygame.init()
			self.screen = pygame.display.set_mode((1280, 720))
			clock = pygame.time.Clock()
		if mode == "AUTO":
			self.net = CNN.CNN()
			self.net.load_model('trained_dataset.h5')

		self.training_file = None

	def listen(self):

		print "Mode Training: "+str(self.mode)
		
		try:
			stream=urllib.urlopen(self.url)
			print "Connected to car stream"
		except:
			print "Cant connect to car stream"
			exit(0)
		
		dataset_record=open('training_data/dataset_record.txt','a+')			
		
		bytes=''
		frame  = 1
		while True:
			bytes+=stream.read(1024)
			a = bytes.find('\xff\xd8')	# start of jpeg frame
			b = bytes.find('\xff\xd9')	# end of jpeg frame

			if a!=-1 and b!=-1:
						
				jpg = bytes[a:b+2]
				bytes= bytes[b+2:]
				image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
				
				filename = 'images/'+str(frame)+".jpg"
				
				#display the image on pygame
				pyim = pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"RGB")
				pyim = pygame.transform.scale(pyim, (1280, 720))
				self.screen.blit(pyim,(0,0))
				pygame.display.flip()

				print "Frame recieved"
				
				if self.mode == "TRAIN":

					for event in pygame.event.get():
						if event.type == KEYDOWN:
							key = pygame.key.get_pressed()

							if key[pygame.K_UP] and key[pygame.K_RIGHT]:

								print "Forward Right\n"
								cv2.imwrite('training_data/'+filename,image)
								dataset_record.write("training_data/"+filename+" "+"1\n")

							elif key[pygame.K_UP] and key[pygame.K_LEFT]:
								
								print "Forward Left"
								cv2.imwrite('training_data/'+filename,image)
								dataset_record.write("training_data/"+filename+" "+"2\n")

							elif key[pygame.K_UP]:

								print "Forward"
								cv2.imwrite('training_data/'+filename,image)
								dataset_record.write("training_data/"+filename+" "+"3\n")

							elif key[pygame.K_RIGHT]:

								print "Right"
								cv2.imwrite('training_data/'+filename,image)
								dataset_record.write("training_data/"+filename+" "+"4\n")

							elif key[pygame.K_LEFT]:

								print "Left"
								cv2.imwrite('training_data/'+filename,image)
								dataset_record.write("training_data/"+filename+" "+"5\n")

							elif key[pygame.K_DOWN]:

								print "Backwards"
								cv2.imwrite('training_data/'+filename,image)
								dataset_record.write("training_data/"+filename+" "+"6\n")

							elif key[pygame.K_q]:

								cv2.imwrite('training_data/'+filename,image)
								print 'Training data collection over.'
								exit()

						
					frame +=1

			
				if self.mode == "AUTO":
					image = cv2.resize(image, (32, 32))
					image = [image]
					print self.net.predict(image)

server = Server('http://172.16.3.64:8080',"TRAIN")
server.listen()

			

