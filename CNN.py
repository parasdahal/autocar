import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
import h5py

class CNN:
	def __init__(self):
		self.trained_model = None

	def build_training_dataset(self,path):
		"""Build hdf5 file from collection of images and labels

		Parameters
		----------
		path: string
			Path to text file with content "path/to/image label"
		"""
		from tflearn.data_utils import build_hdf5_image_dataset as hdf5
		hdf5(path,image_shape=(32,32),mode='file',output_path='training_data/training_dataset.h5',categorical_labels=True, grayscale=False)
	
	def network(self):
		"""Build the training neural network

		Returns
		-------
		network: tensor
			the network tensor
		"""
		network = input_data(shape=[None,32,32,3])
		# 32 convolution filters with size 3 and stride 1
		network = conv_2d(network,32,3,activation='relu')
		# max pooling layer with kernel size of 2
		network = max_pool_2d(network,2)
		# 64 convolution filter with size 3 and stride 1
		network = conv_2d(network,64,3,activation='relu')
		# max pooling layer with kernel size of 2
		network = max_pool_2d(network,2)
		# fully connected neural network with 512 nodes
		network = fully_connected(network,512,activation='relu')
		# fully connected neural network with 6 nodes
		network = fully_connected(network,7,activation='softmax')
		# classifier
		network = regression(network,optimizer='adam',loss='categorical_crossentropy',learning_rate=0.01)

		return network

	def train(self,path,num_iters=1000,save=False):
		"""Train the network with input data
		Parameters
		----------
		path: string
			Path of the .h5 dataset
		"""
		
		f=h5py.File(path,'r')
		X = f['X'][()]
		Y = f['Y'][()]	

		network = self.network()
		# wrapping the network in deep learning model
		model = tflearn.DNN(network,tensorboard_verbose=1)

		# start training
		model.fit(X,Y,n_epoch=num_iters,shuffle=True,show_metric=True,batch_size=100,snapshot_epoch=True,run_id='autocar')

		# save the model in the instance
		self.trained_model = model
		
		if save==True:
			# save the model in a file
			model.save('training_data/trained_model.tf')

	def load_model(self,model_path):
		"""
		Parameters
		----------
		model_path: string
			Path to the saved model file
		"""
		model = tflearn.DNN(self.network())
		model.load(model_path)
		self.trained_model = model

	def predict(self,X):
		"""Make predictions after trained model is loaded
		Parameters
		----------
		X: ndarray()
			Image of size 64x64
		"""
		vector = self.trained_model.predict(X)
		prob = max(vector)
		index = [i for i, j in enumerate(vector) if j == vector]
		direction = ""
		if index == 0:
			direction = "Forward Right"
		elif index == 1:
			direction = "Forward Left"
		elif index == 2:
			direction = "Forward"
		elif index == 3:
			direction = "Right"
		elif index == 4:
			direction = "Left"
		elif index == 5:
			direction = "Backwards"
		print direction
		return vector



