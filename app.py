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
    """Maps prediction to pollution level category."""
    pollution_levels = {
        0: ('Baik', 'Tingkat mutu udara yang sangat baik, tidak memberikan efek negatif terhadap manusia, hewan, dan tumbuhan.'),
        1: ('Sedang', 'Tingkat mutu udara masih dapat diterima pada kesehatan manusia, hewan, dan tumbuhan.'),
        2: ('Tidak Sehat', 'Tingkat mutu udara yang bersifat merugikan pada manusia, hewan, dan tumbuhan.'),
        3: ('Sangat Tidak Sehat', 'Tingkat mutu udara yang dapat meningkatkan resiko kesehatan pada sejumlah segmen populasi yang terpapar.')
    }
    return pollution_levels.get(prediction, ("Unknown", "No description available."))

def app():
    """Main Streamlit app function."""
    # Page title
    st.header('Air Quality Index Prediction')
    st.subheader('Enter the following pollutant values:')

    # Input fields for pollutant data
    col1, col2 = st.columns(2)
    with col1:
        so2 = st.number_input('SO2 (ppm)', min_value=0.0, max_value=1.0, format="%.3f")
        no2 = st.number_input('NO2 (ppm)', min_value=0.0, max_value=50.0, format="%.3f")
        o3 = st.number_input('O3 (ppm)', min_value=0.0, max_value=0.6, format="%.3f")
    with col2:
        co = st.number_input('CO (ppm)', min_value=0.0, max_value=2.0, format="%.3f")
        pm10 = st.number_input('PM10 (µg/m³)', min_value=0.0, max_value=600.0, format="%.3f")
        pm25 = st.number_input('PM2.5 (µg/m³)', min_value=0.0, max_value=500.0, format="%.3f")

    # Model selection
    selected_model_name = st.selectbox('Select a model', list(models.keys()))

    # Load the selected model
    model_filename = models[selected_model_name]
    classifier = load_model(model_filename)

    # Prediction button
    if st.button('Predict'):
        prediction = predict_pollution(classifier, pm10, pm25, so2, co, o3, no2)
        if prediction is not None:
            pollution_level, description = map_pollution_level(prediction[0])
            st.success(f'The predicted air quality category is: {pollution_level}')
            st.info(description)

if __name__ == "__main__":
    app()