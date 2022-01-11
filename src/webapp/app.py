from flask import Flask , request
from flask.json import jsonify
from src.predictor import Mask_Predictor 
import os , cv2
import numpy as np


def home():

  image = request.files['image']
  print(image)
  image = cv2.imdecode(np.fromfile(image , np.uint8) , cv2.IMREAD_ANYCOLOR)
  
  
  pred = mp.get_prediction(image)
  
  
  return jsonify(prediction = pred)



app = Flask(__name__)
mp = Mask_Predictor(path = os.getcwd()+ os.environ['MODEL_DIR'] + os.environ['MODEL_NAME'], size = 224)
app.add_url_rule("/" , view_func = home , methods = ['POST'])
app.run()
