import pickle
import numpy as np
import gradio as gr

modelsList = ["CR_DecisionTree.pkl", "CR_NaiveBayes.pkl", "CR_RF.pkl", "CR_XB.pkl"]

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


def inputDataProcessor(N, P, K, temperature, humidity, ph, rainfall, model):
    l = [N, P, K, temperature, humidity, ph, rainfall]
    l = np.asarray(l)
    l = np.reshape(l, (1, 7))
    crop_reccomended = cropPredictor(l, model)
    return crop_reccomended


label = gr.outputs.Label()

app = gr.Interface(
    fn=inputDataProcessor,
    inputs=[
        "number",
        "number",
        "number",
        "number",
        "number",
        "number",
        "number",
        gr.inputs.Radio(["Random Forest", "Decision Tree", "Naive Bayes", "XGBoost"]),
    ],
    outputs=label,
    title="Crop Recommendation System",
    description="Recommends optimum crops to be cultivated by farmers based on several parameters and help them make an informed decision before cultivation.",
    description="Recommends optimum crops to be cultivated by farmers based on several parameters and help them make an informed decision before cultivation.",
    description="Recommends optimum crops to be cultivated by farmers based on several parameters and help them make an informed decision before cultivation.",
    theme="darkhuggingface",
    examples=[
        [
            65,
            60,
            22,
            25.36768364,
            72.52054555,
            6.6069840860000015,
            107.9124111,
            "Naive Bayes",
        ],
        [
            38,
            60,
            76,
            18.65054116,
            17.80852431,
            8.868741443,
            77.92798682,
            "Decision Tree",
        ],
        [
            10,
            55,
            23,
            21.18853178,
            19.63438599,
            5.728233081,
            137.1948633,
            "Random Forest",
        ],
    ],
    live=True,
)


app.launch(debug=True, inbrowser=True)
