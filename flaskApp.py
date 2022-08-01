from flask import Flask, render_template, request
import requests
import config
import pickle
import numpy as np


categoricalValues = {
    20.0: "rice",
    11.0: "maize",
    3.0: "chickpea",
    9.0: "kidneybeans",
    18.0: "pigeonpeas",
    13.0: "mothbeans",
    14.0: "mungbean",
    2.0: "blackgram",
    10.0: "lentil",
    19.0: "pomegranate",
    1.0: "banana",
    12.0: "mango",
    7.0: "grapes",
    21.0: "watermelon",
    15.0: "muskmelon",
    0.0: "apple",
    16.0: "orange",
    17.0: "papaya",
    4.0: "coconut",
    6.0: "cotton",
    8.0: "jute",
    5.0: "coffee",
}


def weather_fetch(city_name):
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url.replace(" ", ""))
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
        model = pickle.load(open("./ml_models/CR_RF.pkl", "rb"))
        pred = model.predict(inputData)
        # print("RF")
        return pred[0]

    elif model == "Decision Tree":
        model = pickle.load(open("./ml_models/CR_DecisionTree.pkl", "rb"))
        pred = model.predict(inputData)
        # print("DT")
        return pred[0]

    elif model == "Naive Bayes":
        model = pickle.load(open("./ml_models/CR_NaiveBayes.pkl", "rb"))
        pred = model.predict(inputData)
        # print("NB")
        return pred[0]

    elif model == "XGBoost":
        model = pickle.load(open("./ml_models/CR_XB.pkl", "rb"))
        xbpred = model.predict(inputData)
        pred = categoricalValues[xbpred[0]]
        # print("XB")
        return pred


app = Flask(__name__)


@app.route("/")
def home():
    title = "FarmWiser"
    return render_template("index.html", title=title)


@app.route("/weather")
def weather():
    title = "FarmWiser"
    return render_template("weather.html", title=title)


@app.route("/cropRecommended", methods=["POST"])
def crop_prediction():
    title = "FarmWiser - Crop Recommendation"

    if request.method == "POST":
        N = int(request.form["nitrogen"])
        P = int(request.form["phosphorous"])
        K = int(request.form["pottasium"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        city = request.form.get("city")

        model = request.form.get("model")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            l = [N, P, K, temperature, humidity, ph, rainfall]
            l = np.asarray(l)
            l = np.reshape(l, (1, 7))
            crop_reccomended = cropPredictor(l, model).capitalize()
            # print(crop_reccomended)

            return render_template(
                "result.html", prediction=crop_reccomended, title=title
            )

        else:

            return render_template(
                "result.html",
                prediction="Sorry we couldn't process your request currently. Please try again",
                title="Unable Process",
            )


if __name__ == "__main__":
    app.run(debug=True)
