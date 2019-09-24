from PIL import Image
import numpy as np

w, h = 40, 60

data = np.zeros((h, w, 4), dtype=np.uint8)

data[:,:] = (0, 0, 0, 0)



img = Image.fromarray(data, 'RGBA')
img.save('bike1.png')

