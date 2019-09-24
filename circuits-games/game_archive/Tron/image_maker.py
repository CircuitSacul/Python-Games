from PIL import Image
import numpy as np

w, h = 15, 20

data = np.zeros((h, w, 4), dtype=np.uint8)
data2 = np.zeros((h, w, 4), dtype=np.uint8)

data[:,:] = (0, 0, 0, 0)

data[0:6, 6:9] = (0, 0, 255, 100) #front wheel

data[6, 1:14] = (100, 100, 100, 100) #handle bars
data[7:14, 5:10] = (0, 0, 255, 100) #body
data[13, 7] = (0, 0, 0, 100) #seat
data[9:13, 6:9] = (0, 0, 0, 100) #seat

data[14:20, 6:9] = (0, 0, 255, 100) #back wheel

data2[:,:] = (0, 0, 0, 0)

data2[0:6, 6:9] = (255, 0, 0, 100) #front wheel

data2[6, 1:14] = (100, 100, 100, 100) #handle bars
data2[7:14, 5:10] = (255, 0, 0, 100) #body
data2[13, 7] = (0, 0, 0, 100) #seat
data2[9:13, 6:9] = (0, 0, 0, 100) #seat

data2[14:20, 6:9] = (255, 0, 0, 100) #back wheel

img = Image.fromarray(data, 'RGBA')
img.save('bike1.png')

img = Image.fromarray(data2, 'RGBA')
img.save('bike2.png')
