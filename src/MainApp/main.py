
from app import Application 


if __name__ == '__main__':
    app = Application()
    
    app.config["USER"] = "nlz47787"
    app.config["PASSWORD"] = "XIho3BxFB7Z4u2Hj"
    app.config["DATABASE"] = "bludb"

    app.config["HOST"] = '8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud'
    app.config["PORT"] = 30120
    
    #app.config["CERTIFICATE"] = "/home/rupam/Face-Mask-Detection/tests/certificate.crt"
    #app.config["TEMP"] = "/home/rupam/Face-Mask-Detection/src/MainApp/tmp/"

    app.config["CERTIFICATE"] = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/tests/certificate.crt"
    app.config["TEMP"] = "C:/Users/hp/Desktop/ProjectLads/Face-Mask-Detection/src/MainApp/tmp/"
    
    app.config["MODEL_URL"] = "https://maskpredictor.herokuapp.com/predict"
    app.run()



