from app import Application 
import platform
import os

PATH = {
        "credentials" : {
        "Windows" :"//database//credentials.json" ,  
        "Linux" : "/database/credentials.json"
        } , 

        "certificate" : {
            "Windows" : "//database//certificate.crt" , 
            "Linux" :"/database/certificate.crt" 

        } , 

        "temp" : {

            "Windows" : "//tmp//" , 

            "Linux" :"/tmp/" 
        }

}


if __name__ == '__main__':
    app = Application()

    platform_name = platform.system()
    ROOT = os.getcwd()

    
    
    app.config["CREDENTIALS"] = ROOT + PATH["credentials"][platform_name]
    
    app.config["CERTIFICATE"] = ROOT + PATH["certificate"][platform_name]


    app.config["TEMP"] =   ROOT + PATH["temp"][platform_name]


    app.config["MODEL_URL"] = "https://maskpredictor.herokuapp.com/predict"

    
    app.run()

    
    


