import numpy as np ,cv2
import json 

image_to_text  = lambda image: json.dumps(image.tolist())
text_to_image  = lambda text:  np.array(json.loads(text))

if __name__ == '__main__':
    
    #cv2.imread("D:/Projectlads/Face-Mask-Detection/src/db_stuffs/images/mask/Rounak Banerjee.jpeg")
    #cv2.resize(cv2.imread("D:/Projectlads/Face-Mask-Detection/src/db_stuffs/images/mask/Rounak Banerjee.jpeg"), (224, 224))
    x = image_to_text(cv2.resize(cv2.imread("D:/Projectlads/Face-Mask-Detection/src/db_stuffs/images/withoutMask/Sandip Ghosh.jpeg"), (224, 224))) 
    print(len(x))