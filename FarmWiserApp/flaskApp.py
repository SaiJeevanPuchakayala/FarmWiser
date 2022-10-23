from flask import Flask, jsonify, render_template, request, jsonify
import numpy as np
from utils import *
from flask_caching import Cache


app = Flask(__name__)

app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)


@app.route("/")
def home():
    title = "FarmWiser | Home"
    news = newsExtracter()
    return render_template("index.html", title=title, news=news)


@app.route("/cropRecommender")
def cropRecommender():
    title = "FarmWiser | Crop"
    return render_template("cropRecommender.html", title=title)


@app.route("/weatherFinder")
def weatherFinder():
    title = "FarmWiser | Weather"
    return render_template("weatherFinder.html", title=title)


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
                "cropRecommendResult.html", prediction=crop_reccomended, title=title
            )

        else:

            return render_template(
                "cropRecommendResult.html",
                prediction="Sorry we couldn't process your request currently. Please try again",
                title="Unable to Process",
            )


@app.route("/CropPrice")
@cache.cached(timeout=300, query_string=True)
def CropPriceScreener():
    title = "FarmWiser | Crop Price Screener"
    commodityName = request.args["commodityName"]
    yearValue = request.args["yearValue"]
    monthValue = request.args["monthValue"]
    priceDataTable, table_title = ScrapeCommodityPriceData(
        commodityName, yearValue, monthValue
    )
    return render_template(
        "CommodityPriceTable.html",
        title=title,
        pricesData=priceDataTable,
        table_title=table_title,
    )


if __name__ == "__main__":
    app.run(debug=True)
