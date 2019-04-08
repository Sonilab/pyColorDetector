from PIL import Image
import numpy as np
import color


#This demo of color detection

#Reading File
im = np.array(Image.open('test.jpg'))
print( color.run(im) )
print("Finished.")