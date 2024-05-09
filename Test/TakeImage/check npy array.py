import numpy as np

depthImage = np.load('C:/Users/skwe9/Desktop/images/ea6a8fe1c15e4a20b77599013551f378 depthData.npy')
print("shape of array", depthImage.shape)
print("size of array", depthImage.size)
maxValue = np.min(depthImage)
print(" min element", maxValue)
print("element at 100,100", depthImage[100][100])
print(" number of non-zeros", len(np.nonzero(depthImage)[0]))
