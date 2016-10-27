import pygame,time
from pygame.locals import *



pygame.init()
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()
dataset_record=open('training_data/dataset_record.txt','a')
filename = str(time.time())+".jpg"
while  True:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			key = pygame.key.get_pressed()

			if key[pygame.K_UP] and key[pygame.K_RIGHT]:
				print "Forward Right\n"
				dataset_record.write(filename+" "+"FR\n")
			elif key[pygame.K_UP] and key[pygame.K_LEFT]:
				print "Forward Left"
				dataset_record.write(filename+" "+"FL\n")
			elif key[pygame.K_UP]:
				print "Forward"
				dataset_record.write(filename+" "+"F\n")
			elif key[pygame.K_RIGHT]:
				print "Right"
				dataset_record.write(filename+" "+"R\n")
			elif key[pygame.K_LEFT]:
				print "Left"
				dataset_record.write(filename+" "+"L\n")
			elif key[pygame.K_DOWN]:
				print "Backwards"
				dataset_record.write(filename+" "+"B\n")
			elif key[pygame.K_q]:
				print 'Training data collection over.'
				exit()