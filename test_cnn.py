import CNN
import numpy as np
network = CNN.CNN()
import h5py
import cv2
test = cv2.imread('training_data/test.jpg')
test = cv2.resize(test, (32, 32))
test = [test]

# network.build_training_dataset('training_data/dataset_record.txt')
network.train(path='training_data/training_dataset.h5',num_iters=300,save=True)
# network.load_model('training_data/trained_model.tf')
print network.predict(test)