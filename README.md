# 🌍 Air Quality Index (AQI) Prediction Poject

## 📌 Overview  
This project predicts the **Air Quality Index (AQI)** based on input parameters using a pre-trained machine learning model. It utilizes machine learning Support Vector Machine (SVM) and K Nearest Neighbours (KNN) models trained on historical data to provide accurate AQI predictions. It's designed to be user-friendly, allowing users to easily enter air quality parameters and receive instant predictions.

---

## 📂 Project Structure  
```
- `app.py`: The Flask application file.
- `templates/`: Contains HTML templates for rendering pages.
- `model/`: The pre-trained machine learning model used for predictions.
```

---

## 🛠 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/AQI-Prediction
cd AQI_Prediction
```
### 2️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the Flask App  
```bash
python app.py
```

---

## 🎯 Data Source 
Real-time hourly data from various station across Jakarta
Data sourced from official Satu Data Jakarta website: Indeks Standar Pencemaran Udara (ISPU) Tahun 2021 Page
Dataset period: January to December 2021
Data includes various pollutant measurements and AQI calculations  

---

## 🏆 Results  
- **Gradient Boosting Regressor** outperformed other models  
- It achieved the best results in terms of **MSE, MAE, and R² Score**  
- Model exported as `gradient_boosting_model.joblib` for fast inference  

---

## 👨‍💻 Author  
Developed by **Margareta Valencia** 💅	 

---
