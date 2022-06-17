import pickle
import numpy as np
import gradio as gr
import requests
import config

modelsList = ["CR_DecisionTree.pkl","CR_NaiveBayes.pkl","CR_RF.pkl","CR_XB.pkl"]

def cropPredictor(inputData, model):
    if model == "Random Forest":
        model = pickle.load(open("CR_RF.pkl", 'rb'))
        pred = model.predict(inputData)
        print("RF")
        return pred[0]

    elif model == "Decision Tree":
        model = pickle.load(open("CR_DecisionTree.pkl", 'rb'))
        pred = model.predict(inputData)
        print("DT")
        return pred[0]

    elif model == "Naive Bayes":
        model = pickle.load(open("CR_NaiveBayes.pkl", 'rb'))
        pred = model.predict(inputData)
        print("NB")
        return pred[0]


def weather_fetch(city_name):
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/3.0/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None


def inputDataProcessor(N,P,K,temperature,humidity,ph,rainfall,model):
    l = [N,P,K,temperature,humidity,ph,rainfall]
    l = np.asarray(l)
    l = np.reshape(l,(1,7))
    crop_reccomended = cropPredictor(l,model)
    return crop_reccomended




label = gr.outputs.Label()

app = gr.Interface(fn=inputDataProcessor, 
inputs=["number","number","number","number","number","number","number",gr.inputs.Radio(["Random Forest", "Decision Tree", "Naive Bayes"])],  
outputs=label ,
                    title="Crop Recommendation System", 

                    description="Recommends optimum crops to be cultivated by farmers based on several parameters and help them make an informed decision before cultivation.", 
description="Recommends optimum crops to be cultivated by farmers based on several parameters and help them make an informed decision before cultivation.", 
                    description="Recommends optimum crops to be cultivated by farmers based on several parameters and help them make an informed decision before cultivation.", 

                    theme = 'darkhuggingface',

                examples=[
                            [65,60,22,25.36768364,72.52054555,6.6069840860000015,107.9124111,"Naive Bayes"],
                            [38,60,76,18.65054116,17.80852431,8.868741443,77.92798682,"Decision Tree"],
                            [10,55,23,21.18853178,19.63438599,5.728233081,137.1948633,"Random Forest"]
                        ],

                    live=True
                )


app.launch(debug=True,inbrowser =True)