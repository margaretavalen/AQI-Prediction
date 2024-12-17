import streamlit as st
import pandas as pd
import pickle


st.set_page_config(
    page_title="Air Pollution Prediction",
    menu_items= {
        "Get Help" : "https://github.com/kedarnathdev/AQIprediction",
        "Report a bug" : "https://github.com/kedarnathdev/AQIprediction/issues",
        "About": None,
       }
)


hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



models = {
    'KNN Model': 'model/KNN_Model.pkl',
    'SVM Model': 'model/SVM_Model.pkl'
}
 

def load_model(filename):
    with open(filename, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

st.header('Air Quality Index Prediction')
st.subheader('Enter the following values:')
PM10 = st.number_input('Particulate Matter 10 (PM10)', min_value=0.0000, max_value=600.0, format="%.3f")
PM25 = st.number_input('Particulate Matter 2.5 (PM2.5)', min_value=0.0000, max_value=500.0, format="%.3f")
SO2 = st.number_input('Sulfur Dioksida (SO2)', min_value=0.0000, max_value=1.0, format="%.3f")
CO = st.number_input('Karbon Monoksida (CO)', min_value=0.0000, max_value=2.0, format="%.3f")
O3 = st.number_input('Konsentrasi Ozon (O3)', min_value=0.0000, max_value=0.6, format="%.3f")
NO2 = st.number_input('Nitrogen Dioksida (NO2)', min_value=0.0000, max_value=50.0, format="%.3f")

selected_model = st.selectbox('Select a model', list(models.keys()))

if st.button('Predict'):
    if not (PM10 and PM25 and SO2 and CO and O3 and NO2):
        st.error('Please fill all the fields.')
    else:
        model_file = models[selected_model]
        model = load_model(model_file)

        input_df = pd.DataFrame({
            'PM10': PM10,
            'PM25': PM25,
            'SO2': SO2,
            'CO': CO,
            'O3': O3,
            'NO2': NO2
        }, index=[0])

        prediction = model.predict(input_df)[0]

        if prediction <= 50:
            color = 'green'
            description = 'Good: Air quality is satisfactory, and air pollution poses little or no risk.'
        elif prediction <= 100:
            color = 'yellow'
            description = 'Moderate: Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.'
        elif prediction <= 150:
            color = 'orange'
            description = 'Unhealthy for Sensitive Groups: Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
        elif prediction <= 200:
            color = 'red'
            description = 'Unhealthy: Some members of the general public may experience health effects members of sensitive groups may experience more serious health effects.'
        elif prediction <= 300:
            color = 'purple'
            description = 'Very Unhealthy: Health alert, The risk of health effects is increased for everyone.'
        else:
            color = 'maroon'
            description = 'Hazardous: Health warning of emergency conditions: everyone is more likely to be affected.'

        
        st.markdown(f'<h1 style="color:{color};">Air Quality Index: {prediction}</h1>', unsafe_allow_html=True)
        st.write(description)