import requests
import config
import pickle
from bs4 import BeautifulSoup
import cfscrape
import os


scraper = cfscrape.create_scraper()


class News_Scraper:
    def __init__(self, keywords):
        self.markup = requests.get(
            "https://economictimes.indiatimes.com/news/economy/agriculture"
        ).text
        self.keywords = keywords

    def parse(self):
        soup = BeautifulSoup(self.markup, "lxml")
        links = soup.findAll("a", limit=500)
        self.news_links = []
        self.news_linksTexts = []
        for link in links:
            for keyword in self.keywords:
                if keyword in link.text and "?" not in link.text:
                    self.news_links.append(link)
        for link in self.news_links:
            self.news_linksTexts.append(link.text)


def newsExtracter():
    s = News_Scraper(
        [
            "agriculture",
            "farming",
            "demand",
            "prices",
            "government",
            "crop",
            "production",
            "increase",
            "decrease",
            "rainfall",
            "weather",
            "market prices",
        ]
    )

    news_text_list = []
    news_links_list = []
    s.parse()
    for x in s.news_links:
        news_text_list.append(x.text)
        news_links_list.append("https://economictimes.indiatimes.com" + x["href"])
    news = list(zip(news_text_list, news_links_list))
    print(list(set(news)))
    return list(set(news))


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


CR_RF_model_path = "FarmWiserApp/ml_models/CR_RF.pkl"
CR_DecisionTree_model_path = "FarmWiserApp/ml_models/CR_DecisionTree.pkl"
CR_NaiveBayes_model_path = "FarmWiserApp/ml_models/CR_NaiveBayes.pkl"
CR_XB_model_path = "FarmWiserApp/ml_models/CR_XB.pkl"


def cropPredictor(inputData, model):
    if model == "Random Forest":
        model = pickle.load(open(CR_RF_model_path, "rb"))
        pred = model.predict(inputData)
        # print("RF")
        return pred[0]

    elif model == "Decision Tree":
        model = pickle.load(open(CR_DecisionTree_model_path, "rb"))
        pred = model.predict(inputData)
        # print("DT")
        return pred[0]

    elif model == "Naive Bayes":
        model = pickle.load(open(CR_NaiveBayes_model_path, "rb"))
        pred = model.predict(inputData)
        # print("NB")
        return pred[0]

    elif model == "XGBoost":
        model = pickle.load(open(CR_XB_model_path, "rb"))
        xbpred = model.predict(inputData)
        pred = categoricalValues[xbpred[0]]
        # print("XB")
        return pred
