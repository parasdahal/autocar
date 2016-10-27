import numpy as np
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation

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
		hdf5(path,image_shape=(64,64),mode='file',output_path='training_dataset.h5',categorical_labels=True,grayscale=True)
	
	def network(self):
		"""Build the training neural network

		Returns
		-------
		network: tensor
			the network tensor
		"""
		network = tflean.layers.core.input_data(shape=[None,64,64])
		# 32 convolution filters with size 3 and stride 1
		network = conv_2d(network,32,3,1,activation='relu')
		# max pooling layer with kernel size of 2
		network = max_pool_2d(network,2)
		# 64 convolution filter with size 3 and stride 1
		network = conv_2d(network,64,3,1,activation='relu')
		# max pooling layer with kernel size of 2
		network = max_pool_2d(network,2)
		# fully connected neural network with 512 nodes
		network = tflean.layers.core.fully_connected(network,512,activation='relu')
		# fully connected neural network with 256 nodes
		network = tflean.layers.core.fully_connected(network,256,activation='relu')
		# fully connected neural network with 6 nodes
		network = tflearn.layers.core.fully_connected(network,6)
		# classifier
		network = regression(network,optimizer='adam',loss='categorical_crossentropy',learning_rate=0.001)

		return network

	def train(self,path,num_iters=1000):
		"""Train the network with input data
		Parameters
		----------
		path: string
			Path of the .h5 dataset
		"""
		import h5py
		data = h5py.File(path,'w')
		X = data['X']
		Y = data['Y']

		network = self.network()
		# wrapping the network in deep learning model
		model = tflearn.DNN(network,tensorboard_verbose=1,checkpoint_path='model.ckpt')

		# start training
		model.fit(X,Y,n_epoch=num_iters,shuffle=True,show_metric=True,batch_size=100,snapshot_epoch=True,run_id='autocar')

		# save the model in a file
		model.save('trained_model.tf')

	def load_model(self,model_path):
		"""
		Parameters
		----------
		model_path: string
			Path to the saved model file
		"""
		model = tflearn.DNN(self.network)
		model.load('model_path')
		self.trained_model = model

	def predict(self,X):
		"""Make predictions after trained model is loaded
		Parameters
		----------
		X: ndarray()
			Image of size 64x64
		"""
		self.trained_model.predict(X)



