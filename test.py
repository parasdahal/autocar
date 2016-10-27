import pygame,time
from pygame.locals import *


dataset_record=open('dataset_record.txt','a')
pygame.init()
while True:
	filename = str(time.time())+".jpg"
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
				exit()