from tensorflow.keras import models
import numpy as np 
import cv2 


class Mask_Predictor():
  def __init__(self , path , size):
    self.__model = models.load_model(path)
    self.__size =  size

  def __pimage(self , face_roi):
    final_image = cv2.resize(face_roi, (self.__size, self.__size))
    final_image = np.expand_dims(final_image, axis = 0)
    final_image = final_image/255.0

    return final_image
  
  def get_prediction(self , image):
    image = self.__pimage(image)
    prediction = self.__model.predict(image)
    return 1 if (prediction >= 0.5) else 0

