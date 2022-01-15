from flask import Flask , request , render_template
from flask.json import jsonify
from src.predictor import Mask_Predictor 
import os , cv2
import numpy as np

def collect():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        name = request.form["name"]
        code = request.form["code"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        print("Submitted : " , name , code , phone , email , address)
        return "Hello"

def predict():

  image = request.data

  image = cv2.imdecode(np.fromstring(image , np.uint8) , cv2.IMREAD_ANYCOLOR)
  
  
  pred = mp.get_prediction(image)
  
  
  return jsonify(prediction = pred)



app = Flask(__name__)
mp = Mask_Predictor(path = os.getcwd()+ os.environ['MODEL_DIR'] + os.environ['MODEL_NAME'], size = 224)
app.add_url_rule("/collect" , view_func = collect , methods = ['GET' , 'POST'])
app.add_url_rule("/predict" , view_func = predict , methods = ['POST'])
app.run(host="0.0.0.0" , port=os.environ["PORT"])
