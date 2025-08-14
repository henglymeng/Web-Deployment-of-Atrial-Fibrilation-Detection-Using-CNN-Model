# Web-Deployment-of-Atrial-Fibrilation-Detection-Using-CNN-Model
# 🫀 AFIB Detection with 1D CNN + ESP32

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![ESP32](https://img.shields.io/badge/Hardware-ESP32-yellow)

## 📌 Overview
This project detects **Atrial Fibrillation (AFIB)** from ECG data using **RR intervals** processed by a **1D Convolutional Neural Network (CNN)**.  
It integrates with an **ESP32 microcontroller** for real-time LED & buzzer alerts.

## 🚀 Features
- 📊 **High Accuracy:** 98.39% on validation data
- ⚡ Real-time predictions via Flask web app
- 🔔 ESP32 hardware feedback (LEDs + buzzer)
- 🔬 Data from MIT-BIH Atrial Fibrillation Database

## 🛠 Tech Stack
- **Python:** `wfdb`, `numpy`, `scipy`, `matplotlib`, `neurokit2`, `tensorflow`, `flask`, `scikit-learn`
- **Hardware:** ESP32 + Arduino IDE
- **Model:** 1D CNN trained on RR intervals

## 📂 How It Works
1. **Preprocessing:** Filter → Normalize → R-peak detection → RR interval extraction  
2. **Model:** Train CNN to classify AFIB vs Normal rhythm  
3. **Deployment:** Flask server handles predictions and sends results to ESP32  
4. **Feedback:**  
   - 🟢 Green LED = Normal rhythm  
   - 🟡 Yellow LED + buzzer = AFIB detected  

## 📷 Demo
**AFIB Detection:** Yellow LED + buzzer  
**Normal Rhythm:** Green LED

## ⚙️ Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/afib-detection.git
cd afib-detection

# Install dependencies
pip install -r requirements.txt

# Run web app
python app.py
