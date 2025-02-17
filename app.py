from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import requests
import joblib
import json
import pandas as pd
import math
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

def load_model(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

model_knn = joblib.load('model/knn_model.pkl')
model_svm = joblib.load('model/svm_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    return render_template('predict.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        # Ambil data input dari formulir
        PM10 = float(request.form.get('PM10', 0))
        PM2_5 = float(request.form.get('PM2.5', 0))
        NO2 = float(request.form.get('NO2', 0))
        CO = float(request.form.get('CO', 0))
        SO2 = float(request.form.get('SO2', 0))
        O3 = float(request.form.get('O3', 0))
        model_choice = request.form.get('model_choice', '').lower()

        # Data array untuk prediksi
        data = np.array([[PM2_5, PM10, NO2, CO, SO2, O3]])

        # Pilih model berdasarkan input pengguna
        if model_choice == 'knn' and model_knn:
            prediction = model_knn.predict(data)[0]
        elif model_choice == 'svm' and model_svm:
            prediction = model_svm.predict(data)[0]
        else:
            return "Invalid model or model not loaded", 400

        # Map hasil prediksi ke tingkat mutu udara
        air_quality = {
            0: ('Baik', 'Tingkat mutu udara yang sangat baik, tidak memberikan efek negatif terhadap manusia, hewan, dan tumbuhan.', 'green'),
            1: ('Sedang', 'Tingkat mutu udara masih dapat diterima pada kesehatan manusia, hewan, dan tumbuhan.', 'blue'),
            2: ('Tidak Sehat', 'Tingkat mutu udara yang bersifat merugikan pada manusia, hewan, dan tumbuhan.', 'yellow'),
            3: ('Sangat Tidak Sehat', 'Tingkat mutu udara yang dapat meningkatkan resiko kesehatan pada sejumlah segmen populasi yang terpapar.', 'red')
        }

        if prediction in air_quality:
            result_description = air_quality[prediction]
        else:
            result_description = ('Unknown', 'Tidak ada deskripsi untuk hasil ini.', 'gray')

        # Render hasil prediksi
        return render_template("result.html", 
                               prediction=result_description[0],
                               description=result_description[1],
                               color=result_description[2])
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/data')
def data():
    try:
        # Read the Excel file using pandas
        EXCEL_FILE_PATH = 'dataset/ispu_jakarta.csv'  # Make sure this path is correct
        df = pd.read_csv(EXCEL_FILE_PATH)
        data = df.to_dict(orient='records')
        return render_template('data.html', data=data)
    except Exception as e:
        logger.error(f"Error in documentation route: {str(e)}")
        return f"An error occurred: {str(e)}"

@app.route('/visualization', methods=['GET'])
def visual():
   try:
       # Read the Excel file using pandas 
       EXCEL_FILE_PATH = 'dataset/ispu_jakarta.csv'  # Pastikan path ini benar
       df = pd.read_csv(EXCEL_FILE_PATH)
       stations = df['stasiun'].unique().tolist()
       stations.sort()
       pollutants = ['pm10', 'pm25', 'so2', 'co', 'o3', 'no2']
       return render_template('visualization.html', stations=stations, pollutants=pollutants)
   except Exception as e:
       print(f"Error: {str(e)}")
       return f"An error occurred: {str(e)}"

@app.route('/visualization', methods=['POST'])
def visualization():
    try:
        EXCEL_FILE_PATH = 'dataset/ispu_jakarta.csv'  # Pastikan path ini benar
        df = pd.read_csv(EXCEL_FILE_PATH)
        stations = df['stasiun'].unique().tolist()
        pollutants = ['pm10', 'pm25', 'so2', 'co', 'o3', 'no2']

        # Get the selected station and pollutant from the form
        stasiun_filter = request.form.get('stasiun', stations[0])
        pollutant_filter = request.form.get('pollutant', 'pm10')

        # Filter data based on the selected station
        df_filtered = df[df['stasiun'] == stasiun_filter]

        # Generate the plot for AQI or the selected pollutant
        if pollutant_filter == "AQI":
            fig = px.line(df_filtered, x="tanggal", y="AQI", title=f"Time Series of AQI in {stasiun_filter}")
        else:
            fig = px.line(df_filtered, x="tanggal", y=pollutant_filter, title=f"Time Series of {pollutant_filter} in {stasiun_filter}")
        
        fig_hist = px.histogram(df_filtered, x=pollutant_filter, nbins=50, title=f"Distribution of {pollutant_filter} Levels")
        
        category_counts = df_filtered['categori'].value_counts().reset_index()
        category_counts.columns = ['categori', 'Count']
        fig_bar = px.bar(category_counts, x='categori', y='Count', title=f"AQI Category Distribution")

        # Convert figures to HTML
        graph_1 = pio.to_html(fig, full_html=False)
        graph_2 = pio.to_html(fig_hist, full_html=False)
        graph_3 = pio.to_html(fig_bar, full_html=False)
        
        return render_template('visualization.html', 
                               stations=stations, 
                               pollutants=pollutants, 
                               graph_1=graph_1, 
                               graph_2=graph_2, 
                               graph_3=graph_3,
                               stasiun_filter=stasiun_filter, 
                               pollutant_filter=pollutant_filter)
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"An error occurred: {str(e)}"

    # df = load_data('dataset/ispu_jakarta.csv')

    # # Ambil data dari form
    # stasiun_filter = request.form.get('stasiun')
    # pollutant_filter = request.form.get('pollutant')

    # # Filter data berdasarkan stasiun
    # df_filtered = df[df['stasiun'] == stasiun_filter]

    # # Generate grafik time-series
    # if pollutant_filter == "AQI":
    #     fig = px.line(df_filtered, x="tanggal", y="AQI", title=f"Time Series of AQI in {stasiun_filter}")
    # else:
    #     fig = px.line(df_filtered, x="tanggal", y=pollutant_filter, title=f"Time Series of {pollutant_filter} in {stasiun_filter}")
    # graph_time_series = pio.to_html(fig, full_html=False)

    # # Generate distribusi polutan
    # fig_hist = px.histogram(df_filtered, x=pollutant_filter, nbins=50, title=f"Distribution of {pollutant_filter} Levels")
    # graph_histogram = pio.to_html(fig_hist, full_html=False)

    # # Generate distribusi kategori AQI
    # category_counts = df_filtered['categori'].value_counts().reset_index()
    # category_counts.columns = ['categori', 'Count']
    # fig_bar = px.bar(category_counts, x='categori', y='Count', title=f"AQI Category Distribution")
    # graph_bar = pio.to_html(fig_bar, full_html=False)

    # # Mengirimkan hasil visualisasi dalam format JSON
    # return jsonify({
    #     'graph_time_series': graph_time_series,
    #     'graph_histogram': graph_histogram,
    #     'graph_bar': graph_bar
    # })

#     df = load_data('dataset/ispu_jakarta.csv')
    
#     station = request.form.get('station')
#     pollutant = request.form.get('pollutant')
    
#     df_filtered = df[df['stasiun'] == station]
    
#     time_series = create_time_series(df_filtered, pollutant, station)
#     histogram = create_histogram(df_filtered, pollutant, station)
#     category_dist = create_category_distribution(df_filtered, station)
    
#     return jsonify({
#         'time_series': time_series,
#         'histogram': histogram,
#         'category_distribution': category_dist
#     })

@app.route('/author')
def author():
    return render_template("author.html")

if __name__ == '__main__':
    app.run(debug=True)
