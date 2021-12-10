import numpy as np 
import json 

image_to_text  = lambda image: json.dumps(image.tolist())
text_to_image  = lambda text:  np.array(json.loads(text))

if __name__ == '__main__':
    import cv2 

    l = len(image_to_text(cv2.imread('mask.jpg')))
    print(l)
