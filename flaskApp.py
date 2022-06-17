from flask import Flask, render_template, request
import requests
import config
import pickle
import numpy as np

def weather_fetch(city_name):
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

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

app = Flask(__name__)

@app.route('/')
def home():
    title = 'FarmWiser'
    return render_template('index.html', title=title)


@app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'FarmWiser - Crop Recommendation'

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # state = request.form.get("stt")
        city = request.form.get("city")

        model = request.form.get("model")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            l = [N,P,K,temperature,humidity,ph,rainfall]
            l = np.asarray(l)
            l = np.reshape(l,(1,7))
            crop_reccomended = cropPredictor(l,model)
            print(crop_reccomended)

            return render_template('result.html', prediction=crop_reccomended, title=title)

        else:

            return render_template('try_again.html', title=title)


if __name__ == '__main__':
    app.run(debug=False)