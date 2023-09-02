# import streamlit as st

# year = st.text_input("Car model year", key="year", value = '2014')
# transmission = st.selectbox('Transmission type',['Manual','Automatic'], help="Select the transmission type")
# engine = st.slider('Engine power', 700.0, 2000.0)
# max_power = st.slider('Maximum power', 50.0, 200.0)

# def on_button_click(year, transmission, engine, max_power):
#     st.write(year, transmission, engine, max_power)
    
#     # Create a button with a label and a callback function
# button_clicked = st.button("Click me")
    
#     # Check if the button has been clicked
# if button_clicked:
#     on_button_click(year, transmission, engine, max_power)

import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the pickle model
with open('car_price_prediction.model', 'rb') as model_file:
    model = pickle.load(model_file)


X_train = pd.read_csv("X_train.csv")
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)


def predict_output(year, transmission, engine, max_power):
    input_data = [[float(year), 0 if transmission == 'Automatic' else 1, float(engine), float(max_power)]]
    input_data = scaler.transform(input_data)
    output = model.predict(input_data)
    output = np.exp(output)
    return output

def main():
    st.title("Car Model Predictor")
    
    year = st.text_input("Car model year", key="year", value='2014')
    transmission = st.selectbox('Transmission type', ['Manual', 'Automatic'])
    engine = st.slider('Engine power', min_value=700.0, max_value=2000.0, value=1000.0)
    max_power = st.slider('Maximum power', min_value=50.0, max_value=200.0, value=125.0)

    # Create a button with a label and a callback function
    button_clicked = st.button("Predict")

    # Check if the button has been clicked
    if button_clicked:
        # Use default values if the user didn't input anything
        if not year:
            year = '2014'
        if not transmission:
            transmission = 'Manual'
        if not engine:
            engine = 1463.565853 # mean value of df.engine
        if not max_power:
            max_power = 92.057087 # mean value of df.max_power

        # Call the prediction function
        output = predict_output(year, transmission, engine, max_power)
        output = round(float(output), 2)
        # Display the prediction result
        #st.write("Predicted output:", output)
        st.markdown(f"<h1 style='text-align: center;'>{'Predicted Car Selling Price'}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{output}</h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

