# FarmWiser
## Revolutionize your farming with Farmwiser, the ultimate TinyML based Smart Agriculture solution!

![AI-Farm](/Images/AI-Farm.png)

Farmwiser is a cutting-edge project that combines the power of Machine Learning and Internet of Things (IoT) to provide advanced analytics and insights to farmers. With Farmwiser, farmers can monitor and analyze soil health, crop growth, weather patterns, and pest infestation, among other things.

Using TinyML, the system processes real-time data from sensors and cameras placed in the farm and generates personalized recommendations to optimize the farming process, such as when to irrigate, fertilize, or harvest crops.

Farmwiser's user-friendly interface allows farmers to access data and recommendations from anywhere, at any time, using their mobile devices or computers. By reducing manual labor, improving productivity and minimizing losses, Farmwiser empowers farmers to make data-driven decisions that maximize their profits and ensure sustainable agriculture. Join the smart farming revolution with Farmwiser!

<br>
<br>

## ⭐ Integrated Applications:
## 1. [ChromaticScan](https://chromaticscan.streamlit.app/)
<hr>

**ChromaticScan is a state-of-the-art convolutional neural network (CNN) algorithm that is specifically designed for detecting plant diseases. It utilizes transfer learning by fine-tuning the ResNet 34 model on a large dataset of leaf images to achieve an impressive 99.2% accuracy in detecting various plant diseases. The algorithm is trained to identify specific patterns and features in the leaf images that are indicative of different types of diseases, such as leaf spots, blights, and wilts.**

<br>

## 2. [Soilitix](https://soilitix.streamlit.app/)
<hr>

**Soilitix is a web application designed for monitoring soil health. It allows farmers and gardeners to track important soil metrics such as temperature, moisture, and humidity. The application provides an easy-to-use interface that enables users to visualize and analyze their soil data, helping them make informed decisions about their crops and plants.**

<br>
<br>

## ⭐ Relevance:
- Helps farmer’s to predict the diseases of the crop using Data Science techniques.
- Usage of weather prediction for automated irrigation system.
- Helps farmer’s to know the suitable crop to grow in that season.
- And development of an app or website for making the product accessible for the farmer which include prediction algorithms and few essential forecasting graphs.

<br>
<br>

## ⭐ Scope:
- Integration with more sensors and devices: Currently, Farmwiser is designed to work with a limited set of sensors and devices. In the future, more sensors and devices can be integrated into the system to provide even more data points for analysis. This can include sensors for soil moisture, pH, and nutrient levels, as well as drones and satellites for aerial imaging.

- Enhanced machine learning models: As more data is collected from the farm, the machine learning models used by Farmwiser can be further optimized and refined to provide more accurate predictions and recommendations. This can include developing new models to predict crop yields, identify crop diseases and pests, and optimize irrigation and fertilization schedules.

- Expansion to other regions and crops: Currently, Farmwiser is designed to work with a specific set of crops and regions. In the future, the project can be expanded to cover other crops and regions, both in India and globally. This can help the project reach more farmers and provide them with the tools and knowledge they need to improve their yields and incomes.

<br>
<br>

## ⭐ Flow of the project:
- Data Collection: Sensors and IoT devices are used to collect data from the farm, including soil moisture, temperature, humidity, and other environmental factors. This data is stored in a database for further analysis.
- Data Pre-processing: The collected data is cleaned and pre-processed to remove any noise or irrelevant information. Data normalization and feature scaling techniques are applied to ensure that the data is consistent across all sensors.
- Finding the Key Performance Indicators(KPI’s) from factors influencing agriculture and check
correlation between them.
- Integrate all the required sensors to a controller that senses all the essential values.
- Collecting the real time data of KPI’s using sensors (NPK(Nitrogen, Phosphorus, and
Potassium) values, pH values etc.)
- Model Training: Machine learning models will be trained on the preprocessed data to predict crop to be sown, detect pests, and diseases, and recommend optimal irrigation and fertilization schedules.
- Model Deployment: The trained models will be deployed on the edge devices such as Raspberry Pi or Arduino, to run inference on the collected data.
- Alert and Notification: The system will generate alerts and notifications to the farmers in case of any abnormalities or unusual behavior detected in the farm.
- Data Visualization: The system will also provide a web or mobile application for farmers to visualize the collected data and receive actionable insights and recommendations on crop management.
- Feedback Loop: The system will continuously learn from the feedback and actions taken by the farmers and refine the models to improve their accuracy and effectiveness.

<br>
<br>

## ⭐ Run Locally
Clone the project

```bash
>_ git clone https://github.com/SaiJeevanPuchakayala/FarmWiser.git
```

Change directory to FarmWiserApp

```bash
 >_ cd FarmWiserApp
```

Install dependencies

```bash
 >_ pip install -r requirements.txt 
```

Start the server
```bash
>_ python app.py 
```
<br>
<br>

## ⭐ Tech Stack

![Tech Stack](/Images/30.png)

<br>
<br>

## ⭐ Web App Interface: FarmWiser

![Responsive UI 1](/Images/31.png)

![News Viewer](/Images/newsviewer.jpg)

![Responsive UI 2](/Images/32.png)

![Responsive UI 3](/Images/38.png)

<br>
<br>

## ⭐ Hardware SetUp for Soil Health Monitoring

![Soil Health Monitoring Flow](/Images/35.png)

![Soil Health Monitoring](/Images/36.png)

![Soil Health Monitoring](/Images/37.png)
