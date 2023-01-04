from flask import Flask, render_template, request
import numpy as np
from flask_caching import Cache
from utils import *


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
                prediction="Sorry we couldn't process your request currently. Please try again later!",
                title="Unable to Process",
            )


@app.route("/CropPriceReport", methods=["GET", "POST"])
@cache.cached(timeout=300, query_string=True)
def CropPriceScreener():

    if request.method == "GET":
        title = "FarmWiser | Crop Price Report Generator"
        return render_template("CommodityPriceReportGenerator.html", title=title)

    if request.method == "POST":
        title = "FarmWiser | Crop Price Viewer"
        commodityName = request.form["commodityName"]
        yearValue = request.form["yearValue"]
        monthValue = request.form["monthValue"]
        priceDataTable, table_title = ScrapeCommodityPriceData(
            commodityName, yearValue, monthValue
        )
        return render_template(
            "CommodityPriceViewer.html",
            title=title,
            pricesData=priceDataTable,
            table_title=table_title,
        )


if __name__ == "__main__":
    app.run(debug=True)
