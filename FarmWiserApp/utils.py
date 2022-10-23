import requests
import config
import pickle
from bs4 import BeautifulSoup
import cfscrape
import os
from selenium import webdriver
import time
import os
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


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


CR_RF_model_path = "CR_RF.pkl"
CR_DecisionTree_model_path = "CR_DecisionTree.pkl"
CR_NaiveBayes_model_path = "CR_NaiveBayes.pkl"
CR_XB_model_path = "CR_XB.pkl"


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


def ScrapeCommodityPriceData(commodityName, yearData, monthData):
    # Selenium Driver Configurations
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(
    #     executable_path=r"chromedriver.exe", options=chrome_options
    # )
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver = webdriver.Chrome(
    #     executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options
    # )

    # Extracting HTML response
    driver.get("https://agmarknet.gov.in/PriceTrends/SA_Pri_Month.aspx")

    commoditySelec_dropdown = driver.find_element("id", "cphBody_Commodity_list")
    commoditySelection = Select(commoditySelec_dropdown)
    commoditySelection.select_by_visible_text(commodityName)

    time.sleep(5)

    yearSelec_dropdown = driver.find_element("id", "cphBody_Year_list")
    yearSelection = Select(yearSelec_dropdown)
    yearSelection.select_by_visible_text(yearData)

    time.sleep(5)

    monthSelec_dropdown = driver.find_element("id", "cphBody_Month_list")
    monthSelection = Select(monthSelec_dropdown)
    monthSelection.select_by_visible_text(monthData)

    submitData = driver.find_element("id", "cphBody_But_Submit")
    submitData.click()

    time.sleep(5)

    html_pageSource = driver.page_source

    time.sleep(5)

    priceDataTable = []
    table_df_soup = BeautifulSoup(html_pageSource, "lxml")
    table_title = table_df_soup.select("#cphBody_Label3")[0].text.strip()
    table_rows = table_df_soup.select("#cphBody_DataGrid_PriMon")[0].select("tbody tr")
    for td in table_rows:
        State = td.select("td")[0].text.strip()
        currentMonthValue = td.select("td")[1].text.strip()
        previousMonthValue = td.select("td")[2].text.strip()
        currentMonthLastYearValue = td.select("td")[3].text.strip()
        changePercentMonth = td.select("td")[4].text.strip()
        changePercentYear = td.select("td")[5].text.strip()

        table_state_item = {
            "State": State,
            "currentMonthValue": currentMonthValue,
            "previousMonthValue": previousMonthValue,
            "currentMonthLastYearValue": currentMonthLastYearValue,
            "changePercentMonth": changePercentMonth,
            "changePercentYear": changePercentYear,
        }
        priceDataTable.append(table_state_item)

    driver.close()
    return priceDataTable, table_title


if __name__ == "__main__":
    commodityName = "Banana"
    yearData = "2022"
    monthData = "September"
    print(ScrapeCommodityPriceData(commodityName, yearData, monthData))
