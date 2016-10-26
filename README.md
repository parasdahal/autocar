# Autocar

An implementation of self driving vehicles by end to end learning using Convolutional Neural Network.

## Android app (Java)

Sends stream of video frames (10/sec) + optional accelerometer data (speed of the car calculated by app) over TCP to Server.

## CNN (TFlearn, Python)

Gets Numpy array from the Server and uses it to train the CNN model. The trained model is saved into a file for making predictions by driver program.

## Server (Python)

### Train mode

Recieves frames and data. Saves only when there is a key press action (FL,FR,F,L,R,B). The image is
converted to grayscale, sliced to get bottom half and flattened to get a single dimensional array. Accelerometer data is added to the array (if present). Numpy array is stored into a file and fed to CNN.

### Auto mode

Uses predict method from CNN to feed image frame array from TCP server and get the output. The output is fed into the serial port to send signals to the car via transmitter.