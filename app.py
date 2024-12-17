import streamlit as st
import pickle
import os

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
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Model file '{filename}' not found.")
        with open(filename, 'rb') as model_file:
            model = pickle.load(model_file)
        return model
    except FileNotFoundError as e:
        st.error(f"Error loading the model: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error loading the model: {e}")
        return None

def predict_pollution(model, pm10, pm25, so2, co, o3, no2):
    """Predicts air pollution level using the provided model and input data."""
    try:
        prediction = model.predict([[pm10, pm25, so2, co, o3, no2]])
        return prediction
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

def map_pollution_level(prediction):
    pollution_levels = {
        0: ('Baik', 'Tingkat mutu udara yang sangat baik, tidak memberikan efek negatif terhadap manusia, hewan, dan tumbuhan.', 'green'),
        1: ('Sedang', 'Tingkat mutu udara masih dapat diterima pada kesehatan manusia, hewan, dan tumbuhan.', 'blue'),
        2: ('Tidak Sehat', 'Tingkat mutu udara yang bersifat merugikan pada manusia, hewan, dan tumbuhan.', 'yellow'),
        3: ('Sangat Tidak Sehat', 'Tingkat mutu udara yang dapat meningkatkan resiko kesehatan pada sejumlah segmen populasi yang terpapar.', 'red')
    }
    return pollution_levels.get(prediction, ("Tidak Diketahui", "Tidak ada deskripsi yang sesuai.", "gray"))

def app():
    # Page title
    st.header('Air Quality Index Prediction')
    st.subheader('Enter the following pollutant values:')

    # Input fields for pollutant data
    col1, col2 = st.columns(2)
    with col1:
        pm10 = st.number_input('PM10 (µg/m³)', min_value=0.0, format="%.3f")
        pm25 = st.number_input('PM2.5 (µg/m³)', min_value=0.0, format="%.3f")
        so2 = st.number_input('SO2 (ppm)', min_value=0.0, format="%.3f")
    with col2:
        co = st.number_input('CO (ppm)', min_value=0.0, format="%.3f")
        o3 = st.number_input('O3 (ppm)', min_value=0.0, format="%.3f")
        no2 = st.number_input('NO2 (ppm)', min_value=0.0,  format="%.3f")

    st.write(f"Input data: PM10={pm10}, PM2.5={pm25}, SO2={so2}, CO={co}, O3={o3}, NO2={no2}")

    # Model selection
    selected_model_name = st.selectbox('Select a model', list(models.keys()))

    # Load the selected model
    model_filename = models[selected_model_name]
    classifier = load_model(model_filename)

    # Define the prediction function
    def predict_pollution(pm10, pm25, so2,  co, o3, no2):
        if classifier is not None:
            prediction = classifier.predict([[pm10, pm25, so2,  co, o3, no2]])
            return prediction
        else:
            raise ValueError("The classifier model is not loaded.")

    # Prediction button
    if st.button('Predict'):
        prediction = predict_pollution(classifier, pm10, pm25, so2, co, o3, no2)
        if prediction is not None:
            pollution_level, description, color = map_pollution_level(prediction[0])
            st.markdown(f"<h4 style='color:{color}'>The predicted air quality category is: {pollution_level}</h4>", unsafe_allow_html=True)
            st.info(description)

if __name__ == "__main__":
    app()
