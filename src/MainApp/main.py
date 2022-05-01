import PySimpleGUI as pygui 



from app import Application

import os 
import platform
import sys 



separator = {"Windows" : "\\" , "Linux" : "/"}

if __name__ == '__main__':

    #change the path according to derectory
    
    app.config["CERTIFICATE"] = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/tests/certificate.crt"
    app.config["TEMP"] = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/MainApp/tmp/"
    
    
    
    
  
    platform_name = platform.system()
    
    root = os.getcwd()

    credentials = [root , "database" , "credentials.json"]
    certificate = [root , "database" , "certificate.crt"]
    temp = [root , "tmp"]

    app = Application()

    
    app.config["CREDENTIALS"] = separator[platform_name].join(credentials)
    
    app.config["CERTIFICATE"] = separator[platform_name].join(certificate)


    app.config["TEMP"] =   separator[platform_name].join(temp) + separator[platform_name]

    app.config["MODEL_URL"] = "https://maskpredictor.herokuapp.com/predict"
    
    
    app.run(sys.argv)
