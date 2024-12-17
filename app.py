import streamlit as st
import pickle

# Streamlit page configuration
st.set_page_config(
    page_title="Air Pollution Prediction",
    menu_items={
        "Get Help": "https://github.com/kedarnathdev/AQIprediction",
        "Report a bug": "https://github.com/kedarnathdev/AQIprediction/issues",
        "About": "This app predicts Air Quality Index (AQI) levels based on pollutant data using pre-trained models."
    }
)

# Hide the footer
hide_streamlit_style = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Dictionary to store model filenames
models = {
    'KNN Model': 'KNN_Model.pkl',
    'SVM Model': 'SVM_Model.pkl'
}

def load_model(filename):
    """Loads a model from a pickle file."""
    try:
        with open(filename, 'rb') as model_file:
            model = pickle.load(model_file)
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        return None

def predict_pollution(model, pm10, pm25, so2, co, o3, no2):
    """Predicts air pollution level using the provided model and input data."""
    if model is not None:
        try:
            prediction = model.predict([[pm10, pm25, so2, co, o3, no2]])
            return prediction
        except Exception as e:
            st.error(f"Prediction error: {e}")
            return None
    else:
        st.error("Model not loaded.")
        return None

def map_pollution_level(prediction):
    pollution_levels = {
        0: ('Baik', 'Air quality is good and poses little or no risk.', 'green'),
        1: ('Sedang', 'Air quality is acceptable; however, some pollutants may cause a health concern for sensitive individuals.', 'blue'),
        2: ('Tidak Sehat', 'Everyone may begin to experience health effects; sensitive groups may experience more serious effects.', 'yellow'),
        3: ('Sangat Tidak Sehat', 'Health alert: everyone may experience more serious health effects.', 'red')
    }
    return pollution_levels.get(prediction, ("Unknown", "No description available.", "gray"))

def app():
    # Page title
    st.header('Air Quality Index Prediction')
    st.subheader('Enter the following pollutant values:')

    # Input fields for pollutant data
    col1, col2 = st.columns(2)
    with col1:
        pm10 = st.number_input('PM10 (µg/m³)', min_value=0.0)
        pm25 = st.number_input('PM2.5 (µg/m³)', min_value=0.0)
        so2 = st.number_input('SO2 (ppm)', min_value=0.0)
    with col2:
        co = st.number_input('CO (ppm)', min_value=0.0)
        o3 = st.number_input('O3 (ppm)', min_value=0.0)
        no2 = st.number_input('NO2 (ppm)', min_value=0.0,)

    # Model selection
    selected_model_name = st.selectbox('Select a model', list(models.keys()))

    # Load the selected model
    model_filename = models[selected_model_name]
    classifier = load_model(model_filename)

    # Prediction button
    if st.button('Predict'):
        prediction = predict_pollution(classifier, pm10, pm25, so2, co, o3, no2)
        if prediction is not None:
            pollution_level, description, color = map_pollution_level(prediction[0])
            st.markdown(f"<h4 style='color:{color}'>The predicted air quality category is: {pollution_level}</h4>", unsafe_allow_html=True)
            st.info(description)

if __name__ == "__main__":
    app()